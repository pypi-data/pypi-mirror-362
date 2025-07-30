#!/usr/bin/env python3
"""
PERFORMANCE BENCHMARK TESTS
===========================
Specialized performance testing for A2A API system with detailed
metrics collection and performance regression detection.
"""

import asyncio
import time
import statistics
import httpx
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)

class PerformanceBenchmarkSuite:
    """Performance benchmark testing suite"""
    
    def __init__(self):
        self.lobby_url = "http://localhost:8080"
        self.bridge_url = "http://localhost:8090"
        self.benchmarks = {}
        
        # Performance targets (in milliseconds)
        self.targets = {
            "discovery_response": 50,      # A2A discovery should be < 50ms
            "status_response": 30,         # Status endpoint should be < 30ms
            "registration_response": 100,  # Agent registration should be < 100ms
            "delegation_response": 200,    # Task delegation should be < 200ms
            "concurrent_load": 500,        # Concurrent requests should complete < 500ms
        }
    
    async def benchmark_a2a_discovery_performance(self):
        """Benchmark A2A discovery endpoint performance"""
        test_name = "a2a_discovery_performance"
        logger.info(f"📊 Benchmark: {test_name}")
        
        iterations = 100
        response_times = []
        successful_requests = 0
        
        async with httpx.AsyncClient() as client:
            for i in range(iterations):
                start_time = time.time()
                try:
                    response = await client.get(f"{self.bridge_url}/.well-known/agent.json")
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000  # Convert to ms
                    response_times.append(response_time)
                    
                    if response.status_code == 200:
                        successful_requests += 1
                        
                except Exception as e:
                    logger.error(f"Request {i} failed: {e}")
                    response_times.append(float('inf'))
        
        # Calculate statistics
        valid_times = [t for t in response_times if t != float('inf')]
        
        if valid_times:
            avg_time = statistics.mean(valid_times)
            median_time = statistics.median(valid_times)
            p95_time = sorted(valid_times)[int(0.95 * len(valid_times))]
            min_time = min(valid_times)
            max_time = max(valid_times)
            std_dev = statistics.stdev(valid_times) if len(valid_times) > 1 else 0
            
            self.benchmarks[test_name] = {
                "iterations": iterations,
                "successful_requests": successful_requests,
                "success_rate": (successful_requests / iterations) * 100,
                "avg_response_time_ms": avg_time,
                "median_response_time_ms": median_time,
                "p95_response_time_ms": p95_time,
                "min_response_time_ms": min_time,
                "max_response_time_ms": max_time,
                "std_dev_ms": std_dev,
                "target_met": avg_time < self.targets["discovery_response"],
                "target_ms": self.targets["discovery_response"]
            }
            
            logger.info(f"   ⏱️ Avg: {avg_time:.1f}ms, P95: {p95_time:.1f}ms")
            logger.info(f"   🎯 Target: {self.targets['discovery_response']}ms ({'✅ MET' if avg_time < self.targets['discovery_response'] else '❌ MISSED'})")
    
    async def benchmark_concurrent_request_handling(self):
        """Benchmark concurrent request handling capacity"""
        test_name = "concurrent_request_handling"
        logger.info(f"📊 Benchmark: {test_name}")
        
        concurrent_levels = [10, 25, 50, 100, 200]
        results_by_level = {}
        
        for level in concurrent_levels:
            logger.info(f"   Testing {level} concurrent requests...")
            
            start_time = time.time()
            response_times = []
            successful_requests = 0
            
            async with httpx.AsyncClient(limits=httpx.Limits(max_connections=level*2)) as client:
                # Create concurrent tasks
                tasks = []
                for i in range(level):
                    # Alternate between different endpoints
                    if i % 3 == 0:
                        url = f"{self.bridge_url}/.well-known/agent.json"
                    elif i % 3 == 1:
                        url = f"{self.bridge_url}/api/a2a/status"
                    else:
                        url = f"{self.bridge_url}/api/a2a/discover"
                    
                    task = self._timed_request(client, url)
                    tasks.append(task)
                
                # Execute all requests concurrently
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, tuple):
                        response_time, success = result
                        response_times.append(response_time)
                        if success:
                            successful_requests += 1
                    else:
                        response_times.append(float('inf'))
            
            end_time = time.time()
            total_time = (end_time - start_time) * 1000  # Convert to ms
            
            valid_times = [t for t in response_times if t != float('inf')]
            
            if valid_times:
                avg_time = statistics.mean(valid_times)
                p95_time = sorted(valid_times)[int(0.95 * len(valid_times))]
                
                results_by_level[level] = {
                    "concurrent_requests": level,
                    "total_time_ms": total_time,
                    "successful_requests": successful_requests,
                    "success_rate": (successful_requests / level) * 100,
                    "avg_response_time_ms": avg_time,
                    "p95_response_time_ms": p95_time,
                    "requests_per_second": level / (total_time / 1000),
                    "target_met": total_time < self.targets["concurrent_load"]
                }
                
                logger.info(f"     ✅ {level} requests: {avg_time:.1f}ms avg, {successful_requests}/{level} success")
        
        self.benchmarks[test_name] = results_by_level
    
    async def benchmark_task_delegation_performance(self):
        """Benchmark task delegation performance"""
        test_name = "task_delegation_performance"
        logger.info(f"📊 Benchmark: {test_name}")
        
        # First register test agents
        async with httpx.AsyncClient() as client:
            for i in range(5):
                agent_data = {
                    "agent_id": f"perf_test_agent_{i}",
                    "name": f"Performance Test Agent {i}",
                    "agent_type": "performance_test",
                    "capabilities": ["data_processing", "analysis", "computation"]
                }
                await client.post(f"{self.lobby_url}/api/agents/register", json=agent_data)
        
        # Now benchmark delegations
        iterations = 50
        response_times = []
        successful_delegations = 0
        
        async with httpx.AsyncClient() as client:
            for i in range(iterations):
                task_data = {
                    "title": f"Performance Test Task {i}",
                    "description": f"Benchmark delegation task {i}",
                    "required_capabilities": ["data_processing"],
                    "input": {"test_data": f"benchmark_{i}"},
                    "sender_id": "benchmark_client"
                }
                
                start_time = time.time()
                try:
                    response = await client.post(f"{self.bridge_url}/api/a2a/delegate", json=task_data)
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000
                    response_times.append(response_time)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success"):
                            successful_delegations += 1
                            
                except Exception as e:
                    logger.error(f"Delegation {i} failed: {e}")
                    response_times.append(float('inf'))
        
        # Calculate statistics
        valid_times = [t for t in response_times if t != float('inf')]
        
        if valid_times:
            avg_time = statistics.mean(valid_times)
            median_time = statistics.median(valid_times)
            p95_time = sorted(valid_times)[int(0.95 * len(valid_times))]
            
            self.benchmarks[test_name] = {
                "iterations": iterations,
                "successful_delegations": successful_delegations,
                "success_rate": (successful_delegations / iterations) * 100,
                "avg_response_time_ms": avg_time,
                "median_response_time_ms": median_time,
                "p95_response_time_ms": p95_time,
                "target_met": avg_time < self.targets["delegation_response"],
                "target_ms": self.targets["delegation_response"]
            }
            
            logger.info(f"   ⏱️ Avg: {avg_time:.1f}ms, Success: {successful_delegations}/{iterations}")
    
    async def benchmark_sustained_load(self):
        """Benchmark sustained load handling"""
        test_name = "sustained_load"
        logger.info(f"📊 Benchmark: {test_name}")
        
        duration_seconds = 30
        requests_per_second = 10
        total_requests = duration_seconds * requests_per_second
        
        logger.info(f"   Running sustained load: {requests_per_second} req/s for {duration_seconds}s")
        
        successful_requests = 0
        failed_requests = 0
        response_times = []
        
        async with httpx.AsyncClient() as client:
            start_time = time.time()
            
            for i in range(total_requests):
                request_start = time.time()
                
                try:
                    # Mix of different request types
                    if i % 4 == 0:
                        response = await client.get(f"{self.bridge_url}/api/a2a/status")
                    elif i % 4 == 1:
                        response = await client.get(f"{self.bridge_url}/.well-known/agent.json")
                    elif i % 4 == 2:
                        response = await client.get(f"{self.bridge_url}/api/a2a/discover")
                    else:
                        response = await client.get(f"{self.bridge_url}/api/health")
                    
                    request_end = time.time()
                    response_time = (request_end - request_start) * 1000
                    response_times.append(response_time)
                    
                    if response.status_code == 200:
                        successful_requests += 1
                    else:
                        failed_requests += 1
                        
                except Exception:
                    failed_requests += 1
                    response_times.append(float('inf'))
                
                # Rate limiting to maintain requests_per_second
                elapsed = time.time() - start_time
                expected_requests = elapsed * requests_per_second
                if i + 1 > expected_requests:
                    await asyncio.sleep((i + 1) / requests_per_second - elapsed)
        
        end_time = time.time()
        actual_duration = end_time - start_time
        actual_rps = total_requests / actual_duration
        
        valid_times = [t for t in response_times if t != float('inf')]
        
        if valid_times:
            avg_time = statistics.mean(valid_times)
            p95_time = sorted(valid_times)[int(0.95 * len(valid_times))]
            
            self.benchmarks[test_name] = {
                "duration_seconds": actual_duration,
                "target_rps": requests_per_second,
                "actual_rps": actual_rps,
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "success_rate": (successful_requests / total_requests) * 100,
                "avg_response_time_ms": avg_time,
                "p95_response_time_ms": p95_time,
                "system_stable": failed_requests < (total_requests * 0.05)  # Less than 5% failures
            }
            
            logger.info(f"   📊 {actual_rps:.1f} req/s, {(successful_requests/total_requests)*100:.1f}% success")
    
    async def _timed_request(self, client: httpx.AsyncClient, url: str):
        """Helper method to time a single request"""
        start_time = time.time()
        try:
            response = await client.get(url)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return response_time, response.status_code == 200
        except Exception:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            return response_time, False
    
    async def run_performance_benchmarks(self):
        """Run all performance benchmarks"""
        logger.info("🚀 Starting Performance Benchmark Suite...")
        
        start_time = time.time()
        
        # Wait for system to be ready
        await asyncio.sleep(2)
        
        # Run benchmarks
        await self.benchmark_a2a_discovery_performance()
        await self.benchmark_concurrent_request_handling()
        await self.benchmark_task_delegation_performance()
        await self.benchmark_sustained_load()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Generate performance report
        self.generate_performance_report(total_time)
        
        # Save results
        self.save_benchmark_results()
    
    def generate_performance_report(self, total_time: float):
        """Generate comprehensive performance report"""
        logger.info("\n" + "="*80)
        logger.info("⚡ PERFORMANCE BENCHMARK RESULTS")
        logger.info("="*80)
        
        # Individual benchmark results
        for test_name, results in self.benchmarks.items():
            logger.info(f"\n📊 {test_name.upper().replace('_', ' ')}")
            
            if test_name == "concurrent_request_handling":
                for level, data in results.items():
                    target_met = "✅" if data["target_met"] else "❌"
                    logger.info(f"   {level:3d} concurrent: {data['avg_response_time_ms']:6.1f}ms avg, "
                              f"{data['success_rate']:5.1f}% success {target_met}")
            else:
                if "avg_response_time_ms" in results:
                    target_met = "✅" if results.get("target_met", False) else "❌"
                    logger.info(f"   Average: {results['avg_response_time_ms']:6.1f}ms {target_met}")
                    
                if "p95_response_time_ms" in results:
                    logger.info(f"   P95:     {results['p95_response_time_ms']:6.1f}ms")
                    
                if "success_rate" in results:
                    logger.info(f"   Success: {results['success_rate']:6.1f}%")
                    
                if "target_ms" in results:
                    logger.info(f"   Target:  {results['target_ms']:6.1f}ms")
        
        # Overall performance assessment
        logger.info(f"\n🎯 PERFORMANCE ASSESSMENT:")
        
        # Count targets met
        targets_met = 0
        total_targets = 0
        
        for test_name, results in self.benchmarks.items():
            if test_name == "concurrent_request_handling":
                for level_data in results.values():
                    total_targets += 1
                    if level_data.get("target_met", False):
                        targets_met += 1
            else:
                if "target_met" in results:
                    total_targets += 1
                    if results["target_met"]:
                        targets_met += 1
        
        performance_score = (targets_met / total_targets) * 100 if total_targets > 0 else 0
        
        logger.info(f"   📈 Performance Score: {performance_score:.1f}% ({targets_met}/{total_targets} targets met)")
        logger.info(f"   ⏱️ Benchmark Duration: {total_time:.1f}s")
        
        # Performance grade
        if performance_score >= 90:
            logger.info("   🏆 Grade: EXCELLENT - System exceeds performance expectations")
        elif performance_score >= 75:
            logger.info("   ✅ Grade: GOOD - System meets most performance targets")
        elif performance_score >= 60:
            logger.info("   ⚠️ Grade: ACCEPTABLE - System has performance issues")
        else:
            logger.info("   ❌ Grade: POOR - System requires performance optimization")
        
        logger.info("="*80)
    
    def save_benchmark_results(self):
        """Save benchmark results to file"""
        try:
            results_file = Path("performance_benchmark_results.json")
            with open(results_file, 'w') as f:
                json.dump(self.benchmarks, f, indent=2, default=str)
            logger.info(f"💾 Benchmark results saved to: {results_file}")
        except Exception as e:
            logger.error(f"Failed to save benchmark results: {e}")

async def main():
    """Main benchmark execution"""
    benchmark_suite = PerformanceBenchmarkSuite()
    
    logger.info("⚡ A2A API Performance Benchmark Suite")
    logger.info("   Target: Production-grade performance validation")
    logger.info("   Coverage: Response times, concurrency, sustained load\n")
    
    await benchmark_suite.run_performance_benchmarks()

if __name__ == "__main__":
    asyncio.run(main()) 