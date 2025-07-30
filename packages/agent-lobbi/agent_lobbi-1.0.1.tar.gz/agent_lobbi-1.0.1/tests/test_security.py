#!/usr/bin/env python3
"""
Comprehensive Security Test Suite for Agent Lobbi
Tests authentication, rate limiting, input validation, audit logging, and encryption
"""

import unittest
import asyncio
import time
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone, timedelta

# Import security modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.security import (
    SecurityManager, SecurityConfig, SecurityLevel, RateLimiter,
    InputValidator, AuthenticationManager, SecurityAuditLogger,
    SecurityAuditEvent
)

class TestSecurityConfig(unittest.TestCase):
    """Test SecurityConfig class"""
    
    def test_default_config(self):
        """Test default security configuration"""
        config = SecurityConfig()
        
        # Authentication defaults
        self.assertTrue(config.require_auth)
        self.assertEqual(config.jwt_algorithm, "HS256")
        self.assertEqual(config.jwt_expiry_hours, 24)
        self.assertEqual(config.api_key_length, 32)
        
        # Rate limiting defaults
        self.assertTrue(config.rate_limit_enabled)
        self.assertEqual(config.global_rate_limit, 1000)
        self.assertEqual(config.per_agent_rate_limit, 100)
        self.assertEqual(config.burst_allowance, 50)
        
        # Security features enabled
        self.assertTrue(config.cors_enabled)
        self.assertTrue(config.audit_enabled)
        
        # Security headers present
        self.assertIn("X-Content-Type-Options", config.security_headers)
        self.assertIn("X-Frame-Options", config.security_headers)
        self.assertIn("Strict-Transport-Security", config.security_headers)

class TestRateLimiter(unittest.TestCase):
    """Test RateLimiter class"""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization"""
        limiter = RateLimiter(rate_limit=100, burst_capacity=50)
        
        self.assertEqual(limiter.rate_limit, 100)
        self.assertEqual(limiter.burst_capacity, 50)
        self.assertIsInstance(limiter.buckets, dict)
    
    def test_rate_limiting_basic(self):
        """Test basic rate limiting functionality"""
        limiter = RateLimiter(rate_limit=60, burst_capacity=10)  # 1 per second
        
        # First 10 requests should be allowed (burst capacity)
        for i in range(10):
            self.assertTrue(limiter.is_allowed("test_user"))
        
        # 11th request should be denied
        self.assertFalse(limiter.is_allowed("test_user"))
    
    def test_multiple_users(self):
        """Test rate limiting for multiple users"""
        limiter = RateLimiter(rate_limit=60, burst_capacity=1)
        
        # Each user should have their own bucket
        self.assertTrue(limiter.is_allowed("user1"))
        self.assertTrue(limiter.is_allowed("user2"))
        
        # Both users should now be limited
        self.assertFalse(limiter.is_allowed("user1"))
        self.assertFalse(limiter.is_allowed("user2"))
    
    def test_wait_time_calculation(self):
        """Test wait time calculation"""
        limiter = RateLimiter(rate_limit=60, burst_capacity=1)
        
        # Use up token
        limiter.is_allowed("test_user")
        
        # Should need to wait approximately 1 second
        wait_time = limiter.get_wait_time("test_user")
        self.assertGreater(wait_time, 0.9)
        self.assertLess(wait_time, 1.1)

class TestInputValidator(unittest.TestCase):
    """Test InputValidator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = SecurityConfig()
        self.validator = InputValidator(self.config)
    
    def test_valid_message(self):
        """Test validation of valid message"""
        message = {
            "sender_id": "agent_001",
            "receiver_id": "agent_002",
            "message_type": "REQUEST",
            "payload": {"data": "test"}
        }
        
        valid, error = self.validator.validate_message(message)
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_missing_required_fields(self):
        """Test validation fails for missing required fields"""
        message = {"sender_id": "agent_001"}
        
        valid, error = self.validator.validate_message(message)
        self.assertFalse(valid)
        self.assertIn("receiver_id", error)
    
    def test_invalid_sender_id_format(self):
        """Test validation fails for invalid sender_id format"""
        message = {
            "sender_id": "agent@001",  # Invalid character
            "receiver_id": "agent_002",
            "message_type": "REQUEST"
        }
        
        valid, error = self.validator.validate_message(message)
        self.assertFalse(valid)
        self.assertIn("sender_id format", error)
    
    def test_invalid_message_type(self):
        """Test validation fails for invalid message type"""
        message = {
            "sender_id": "agent_001",
            "receiver_id": "agent_002",
            "message_type": "INVALID_TYPE"
        }
        
        valid, error = self.validator.validate_message(message)
        self.assertFalse(valid)
        self.assertIn("Invalid message_type", error)
    
    def test_string_sanitization(self):
        """Test string sanitization"""
        dangerous_text = "Hello&World"
        sanitized = self.validator.sanitize_string(dangerous_text)
        
        self.assertNotIn("&", sanitized)
        self.assertEqual(sanitized, "HelloWorld")

class TestAuthenticationManager(unittest.TestCase):
    """Test AuthenticationManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = SecurityConfig()
        self.auth_manager = AuthenticationManager(self.config)
    
    def test_api_key_generation(self):
        """Test API key generation"""
        api_key = self.auth_manager.generate_api_key("agent_001", ["read", "write"])
        
        self.assertIsInstance(api_key, str)
        self.assertGreaterEqual(len(api_key), self.config.api_key_length)
        self.assertIn(api_key, self.auth_manager.api_keys)
        
        key_data = self.auth_manager.api_keys[api_key]
        self.assertEqual(key_data["agent_id"], "agent_001")
        self.assertEqual(key_data["permissions"], ["read", "write"])
        self.assertTrue(key_data["active"])
    
    def test_api_key_validation_success(self):
        """Test successful API key validation"""
        api_key = self.auth_manager.generate_api_key("agent_001")
        
        valid, error, data = self.auth_manager.validate_api_key(api_key, "127.0.0.1")
        
        self.assertTrue(valid)
        self.assertIsNone(error)
        self.assertIsNotNone(data)
        self.assertEqual(data["agent_id"], "agent_001")
    
    def test_api_key_validation_failure(self):
        """Test API key validation failure"""
        invalid_key = "invalid_key_123"
        
        valid, error, data = self.auth_manager.validate_api_key(invalid_key, "127.0.0.1")
        
        self.assertFalse(valid)
        self.assertEqual(error, "Invalid API key")
        self.assertIsNone(data)
    
    def test_failed_attempt_tracking(self):
        """Test failed authentication attempt tracking"""
        ip_address = "192.168.1.100"
        
        # Make 5 failed attempts
        for i in range(5):
            self.auth_manager.validate_api_key("invalid_key", ip_address)
        
        # IP should now be blocked
        self.assertTrue(self.auth_manager._is_ip_blocked(ip_address))

class TestSecurityAuditLogger(unittest.TestCase):
    """Test SecurityAuditLogger class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        self.config = SecurityConfig(audit_log_file=self.temp_file.name)
        self.audit_logger = SecurityAuditLogger(self.config)
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.audit_logger.close()
        os.unlink(self.temp_file.name)
    
    def test_audit_event_logging(self):
        """Test audit event logging"""
        event = SecurityAuditEvent(
            event_type="LOGIN_ATTEMPT",
            user_id="agent_001",
            ip_address="127.0.0.1",
            details={"success": True},
            risk_level=SecurityLevel.LOW
        )
        
        self.audit_logger.log_event(event)
        
        # Check event was added to memory
        self.assertEqual(len(self.audit_logger.audit_events), 1)
        
        # Check event was written to file
        with open(self.temp_file.name, 'r') as f:
            log_content = f.read()
            self.assertIn("LOGIN_ATTEMPT", log_content)
            self.assertIn("agent_001", log_content)

class TestSecurityManager(unittest.TestCase):
    """Test SecurityManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = SecurityConfig(require_auth=False)  # Disable auth for testing
        self.security_manager = SecurityManager(self.config)
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.security_manager.cleanup()
    
    def test_rate_limit_checking(self):
        """Test rate limit checking"""
        # Should be allowed initially
        allowed, wait_time = self.security_manager.check_rate_limit("test_user")
        self.assertTrue(allowed)
        self.assertEqual(wait_time, 0.0)
    
    def test_message_validation_and_sanitization(self):
        """Test message validation and sanitization"""
        message = {
            "sender_id": "agent_001",
            "receiver_id": "agent_002",
            "message_type": "REQUEST",
            "payload": "Safe content"
        }
        
        valid, error, sanitized = self.security_manager.validate_and_sanitize_message(message)
        
        self.assertTrue(valid)
        self.assertIsNone(error)
        self.assertIn("Safe content", sanitized["payload"])
    
    def test_cors_headers(self):
        """Test CORS headers generation"""
        headers = self.security_manager.get_cors_headers("https://example.com")
        
        self.assertIn("Access-Control-Allow-Origin", headers)
        self.assertIn("Access-Control-Allow-Methods", headers)
        self.assertIn("Access-Control-Allow-Headers", headers)
    
    def test_security_headers(self):
        """Test security headers generation"""
        headers = self.security_manager.get_security_headers()
        
        self.assertIn("X-Content-Type-Options", headers)
        self.assertIn("X-Frame-Options", headers)
        self.assertIn("Strict-Transport-Security", headers)
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(headers["X-Frame-Options"], "DENY")
    
    def test_security_status(self):
        """Test security status reporting"""
        status = self.security_manager.get_security_status()
        
        self.assertIn("config", status)
        self.assertIn("stats", status)
        
        # Check config section
        self.assertEqual(status["config"]["auth_required"], False)
        self.assertEqual(status["config"]["rate_limiting_enabled"], True)
        
        # Check stats section
        self.assertIn("blocked_ips", status["stats"])
        self.assertIn("active_api_keys", status["stats"])

if __name__ == '__main__':
    # Run all security tests
    unittest.main(verbosity=2) 