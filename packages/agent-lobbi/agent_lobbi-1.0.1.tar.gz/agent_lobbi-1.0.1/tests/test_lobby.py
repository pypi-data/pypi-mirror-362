#!/usr/bin/env python3
"""
Comprehensive Lobby Test Suite for Agent Lobbi
Tests core lobby functionality, message routing, agent management, and workflows
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestLobbyBasic(unittest.TestCase):
    """Basic tests for lobby functionality"""
    
    def test_imports(self):
        """Test that all required modules can be imported"""
        try:
            from src.core import lobby
            from src.core import message
            from src.core import database
            from src.core import security
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import required modules: {e}")
    
    def test_lobby_config_creation(self):
        """Test lobby configuration creation"""
        try:
            from src.core.config import LobbyConfig
            config = LobbyConfig()
            self.assertIsNotNone(config)
            self.assertEqual(config.http_port, 8080)
        except Exception as e:
            self.fail(f"Failed to create lobby config: {e}")
    
    def test_message_creation(self):
        """Test message creation"""
        try:
            from src.core.message import Message, MessageType
            
            message = Message(
                sender_id="test_sender",
                receiver_id="test_receiver",
                message_type=MessageType.REQUEST,
                payload={"test": "data"}
            )
            
            self.assertEqual(message.sender_id, "test_sender")
            self.assertEqual(message.receiver_id, "test_receiver")
            self.assertEqual(message.message_type, MessageType.REQUEST)
            self.assertEqual(message.payload["test"], "data")
            
        except Exception as e:
            self.fail(f"Failed to create message: {e}")
    
    def test_security_manager_creation(self):
        """Test security manager creation"""
        try:
            from src.core.security import SecurityManager, SecurityConfig
            
            config = SecurityConfig()
            security_manager = SecurityManager(config)
            
            self.assertIsNotNone(security_manager)
            
            # Test basic functionality
            status = security_manager.get_security_status()
            self.assertIn("config", status)
            self.assertIn("stats", status)
            
        except Exception as e:
            self.fail(f"Failed to create security manager: {e}")

if __name__ == '__main__':
    # Run basic tests first
    unittest.main(verbosity=2) 