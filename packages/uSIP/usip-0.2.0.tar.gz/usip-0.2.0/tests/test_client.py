#!/usr/bin/env python3
"""
Tests for the main SIP client
"""

import unittest
import time
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the sip_client module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sip_client import SIPClient, SIPAccount, CallState, RegistrationState


class TestSIPClient(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.account = SIPAccount(
            username="test_user",
            password="test_pass",
            domain="test.com",
            port=5060
        )
        
        # Mock audio to avoid pyaudio dependency in tests
        with patch('sip_client.audio.manager.pyaudio') as mock_pyaudio:
            mock_pyaudio.PyAudio.return_value = Mock()
            self.client = SIPClient(self.account)
    
    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self, 'client'):
            self.client.stop()
    
    def test_client_initialization(self):
        """Test client initialization"""
        self.assertEqual(self.client.account.username, "test_user")
        self.assertEqual(self.client.account.domain, "test.com")
        self.assertEqual(self.client.registration_state, RegistrationState.UNREGISTERED)
        self.assertEqual(len(self.client.calls), 0)
    
    def test_client_start_stop(self):
        """Test client start/stop lifecycle"""
        # Mock the SIP protocol
        self.client.sip_protocol.start = Mock(return_value=True)
        self.client.sip_protocol.stop = Mock()
        
        # Test start
        result = self.client.start()
        self.assertTrue(result)
        self.client.sip_protocol.start.assert_called_once()
        
        # Test stop
        self.client.stop()
        self.client.sip_protocol.stop.assert_called_once()
    
    def test_registration_callbacks(self):
        """Test registration state callbacks"""
        callback_called = False
        received_state = None
        
        def on_reg_state(state):
            nonlocal callback_called, received_state
            callback_called = True
            received_state = state
        
        self.client.on_registration_state = on_reg_state
        
        # Trigger state change
        self.client._set_registration_state(RegistrationState.REGISTERED)
        
        self.assertTrue(callback_called)
        self.assertEqual(received_state, RegistrationState.REGISTERED)
    
    def test_call_callbacks(self):
        """Test call state callbacks"""
        from sip_client.models.call import CallInfo
        
        callback_called = False
        received_call = None
        
        def on_call_state(call_info):
            nonlocal callback_called, received_call
            callback_called = True
            received_call = call_info
        
        self.client.on_call_state = on_call_state
        
        # Create test call
        call_info = CallInfo(
            call_id="test_call",
            local_uri="sip:test@test.com",
            remote_uri="sip:target@test.com",
            state=CallState.CALLING,
            direction="outgoing"
        )
        
        # Trigger state change
        self.client._set_call_state(call_info, CallState.CONNECTED)
        
        self.assertTrue(callback_called)
        self.assertEqual(received_call, call_info)
        self.assertEqual(call_info.state, CallState.CONNECTED)
    
    def test_make_call_not_registered(self):
        """Test making call when not registered"""
        self.client.registration_state = RegistrationState.UNREGISTERED
        
        result = self.client.make_call("1234567890")
        self.assertIsNone(result)
    
    def test_make_call_registered(self):
        """Test making call when registered"""
        self.client.registration_state = RegistrationState.REGISTERED
        
        # Mock SIP protocol
        self.client.sip_protocol.send_invite = Mock(return_value="test_call_id")
        
        # Mock audio manager
        mock_device = Mock()
        mock_device.index = 0
        self.client.audio_manager.get_default_input_device = Mock(return_value=mock_device)
        self.client.audio_manager.get_default_output_device = Mock(return_value=mock_device)
        
        result = self.client.make_call("1234567890")
        
        self.assertEqual(result, "test_call_id")
        self.assertIn("test_call_id", self.client.calls)
        self.assertEqual(self.client.calls["test_call_id"].state, CallState.CALLING)
    
    def test_hangup_call(self):
        """Test hanging up a call"""
        from sip_client.models.call import CallInfo
        
        # Create test call
        call_info = CallInfo(
            call_id="test_call",
            local_uri="sip:test@test.com",
            remote_uri="sip:target@test.com",
            state=CallState.CONNECTED,
            direction="outgoing"
        )
        self.client.calls["test_call"] = call_info
        
        # Mock SIP protocol
        self.client.sip_protocol.send_bye = Mock(return_value=True)
        
        # Mock audio manager
        self.client.audio_manager.stop_audio_stream = Mock()
        
        result = self.client.hangup("test_call")
        
        self.assertTrue(result)
        self.client.sip_protocol.send_bye.assert_called_once_with(call_info)
        self.client.audio_manager.stop_audio_stream.assert_called_once()
        self.assertNotIn("test_call", self.client.calls)
    
    def test_hangup_nonexistent_call(self):
        """Test hanging up a non-existent call"""
        result = self.client.hangup("nonexistent_call")
        self.assertFalse(result)
    
    def test_get_calls(self):
        """Test getting active calls"""
        from sip_client.models.call import CallInfo
        
        # Add test calls
        call1 = CallInfo(
            call_id="call1",
            local_uri="sip:test@test.com",
            remote_uri="sip:target1@test.com",
            state=CallState.CONNECTED,
            direction="outgoing"
        )
        call2 = CallInfo(
            call_id="call2",
            local_uri="sip:test@test.com",
            remote_uri="sip:target2@test.com",
            state=CallState.RINGING,
            direction="incoming"
        )
        
        self.client.calls["call1"] = call1
        self.client.calls["call2"] = call2
        
        calls = self.client.get_calls()
        
        self.assertEqual(len(calls), 2)
        self.assertIn(call1, calls)
        self.assertIn(call2, calls)
    
    def test_get_call(self):
        """Test getting specific call"""
        from sip_client.models.call import CallInfo
        
        call_info = CallInfo(
            call_id="test_call",
            local_uri="sip:test@test.com",
            remote_uri="sip:target@test.com",
            state=CallState.CONNECTED,
            direction="outgoing"
        )
        self.client.calls["test_call"] = call_info
        
        result = self.client.get_call("test_call")
        self.assertEqual(result, call_info)
        
        result = self.client.get_call("nonexistent")
        self.assertIsNone(result)
    
    def test_audio_device_switching(self):
        """Test switching audio devices"""
        from sip_client.models.call import CallInfo
        
        # Create connected call
        call_info = CallInfo(
            call_id="test_call",
            local_uri="sip:test@test.com",
            remote_uri="sip:target@test.com",
            state=CallState.CONNECTED,
            direction="outgoing"
        )
        self.client.calls["test_call"] = call_info
        
        # Mock audio manager
        self.client.audio_manager.switch_input_device = Mock(return_value=True)
        self.client.audio_manager.switch_output_device = Mock(return_value=True)
        
        result = self.client.switch_audio_device("test_call", input_device=1, output_device=2)
        
        self.assertTrue(result)
        self.client.audio_manager.switch_input_device.assert_called_once_with(1)
        self.client.audio_manager.switch_output_device.assert_called_once_with(2)
        self.assertEqual(call_info.input_device, 1)
        self.assertEqual(call_info.output_device, 2)
    
    def test_audio_device_switching_not_connected(self):
        """Test switching audio devices on non-connected call"""
        from sip_client.models.call import CallInfo
        
        call_info = CallInfo(
            call_id="test_call",
            local_uri="sip:test@test.com",
            remote_uri="sip:target@test.com",
            state=CallState.RINGING,
            direction="outgoing"
        )
        self.client.calls["test_call"] = call_info
        
        result = self.client.switch_audio_device("test_call", input_device=1)
        self.assertFalse(result)


class TestSIPClientWithEnvironment(unittest.TestCase):
    
    @patch.dict(os.environ, {
        'SIP_USERNAME': 'env_user',
        'SIP_PASSWORD': 'env_pass',
        'SIP_DOMAIN': 'env_domain.com',
        'SIP_PORT': '5061'
    })
    def test_client_from_environment(self):
        """Test client creation from environment variables"""
        with patch('sip_client.audio.manager.pyaudio') as mock_pyaudio:
            mock_pyaudio.PyAudio.return_value = Mock()
            client = SIPClient()
            
            self.assertEqual(client.account.username, 'env_user')
            self.assertEqual(client.account.password, 'env_pass')
            self.assertEqual(client.account.domain, 'env_domain.com')
            self.assertEqual(client.account.port, 5061)
            
            client.stop()


if __name__ == '__main__':
    unittest.main() 