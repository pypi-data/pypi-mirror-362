#!/usr/bin/env python3
"""
Comprehensive tests for SIP registration and calling functionality
This test suite helps diagnose registration timeouts and calling issues
"""

import unittest
import time
import socket
import threading
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the src directory to the path so we can import the sip_client module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sip_client import SIPClient, SIPAccount, CallState, RegistrationState
from sip_client.sip.protocol import SIPProtocol
from sip_client.sip.messages import SIPMessageBuilder, SIPMessageParser
from sip_client.sip.authentication import SIPAuthenticator


class TestRegistrationAndCalling(unittest.TestCase):
    """Comprehensive tests for registration and calling"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Get credentials from environment variables
        username = os.getenv('SIP_USERNAME')
        password = os.getenv('SIP_PASSWORD')
        domain = os.getenv('SIP_DOMAIN')
        port = int(os.getenv('SIP_PORT', '5060'))
        
        # Check if all required environment variables are set
        if not all([username, password, domain]):
            self.skipTest("Required environment variables not set. Please set SIP_USERNAME, SIP_PASSWORD, and SIP_DOMAIN in your .env file")
        
        self.account = SIPAccount(
            username=username,
            password=password,
            domain=domain,
            port=port
        )
        
        # Mock audio to avoid pyaudio dependency in tests
        with patch('sip_client.audio.manager.pyaudio') as mock_pyaudio:
            mock_pyaudio.PyAudio.return_value = Mock()
            self.client = SIPClient(self.account)
    
    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self, 'client'):
            self.client.stop()
    
    def test_network_connectivity(self):
        """Test basic network connectivity to SIP server"""
        print(f"\n=== Testing Network Connectivity ===")
        print(f"Testing connection to {self.account.domain}:{self.account.port}")
        
        try:
            # Test UDP socket connectivity
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            
            # Send a simple test message
            test_message = "TEST MESSAGE"
            sock.sendto(test_message.encode(), (self.account.domain, self.account.port))
            
            # Try to receive (might timeout, that's OK)
            try:
                data, addr = sock.recvfrom(1024)
                print(f"✓ Received response from {addr}: {data.decode()}")
            except socket.timeout:
                print("⚠ No response received (timeout) - this is expected for test message")
            
            sock.close()
            print("✓ Network connectivity test passed")
            
        except Exception as e:
            print(f"✗ Network connectivity test failed: {e}")
            self.fail(f"Network connectivity issue: {e}")
    
    def test_sip_message_formation(self):
        """Test SIP message formation"""
        print(f"\n=== Testing SIP Message Formation ===")
        
        # Test REGISTER message creation
        headers = SIPMessageBuilder.create_register_headers(
            self.account.username, self.account.domain, self.account.port,
            "test_tag", "test_branch", "test_call_id", 1, 3600
        )
        
        register_message = SIPMessageBuilder.create_message('REGISTER', f"sip:{self.account.domain}", headers)
        
        print("Generated REGISTER message:")
        print(register_message)
        
        # Verify message structure
        self.assertIn("REGISTER", register_message)
        self.assertIn(f"sip:{self.account.domain}", register_message)
        self.assertIn("SIP/2.0", register_message)
        self.assertIn(f"From: <sip:{self.account.username}@{self.account.domain}>", register_message)
        self.assertIn(f"To: <sip:{self.account.username}@{self.account.domain}>", register_message)
        self.assertIn("Content-Length:", register_message)
        
        print("✓ SIP message formation test passed")
    
    def test_authentication_parsing(self):
        """Test SIP authentication parsing"""
        print(f"\n=== Testing Authentication Parsing ===")
        
        # Mock 401 response
        auth_challenge = f'''SIP/2.0 401 Unauthorized\r
Via: SIP/2.0/UDP 192.168.1.100:5060;branch=z9hG4bK-test\r
From: <sip:{self.account.username}@{self.account.domain}>;tag=test_tag\r
To: <sip:{self.account.username}@{self.account.domain}>;tag=server_tag\r
Call-ID: test_call_id\r
CSeq: 1 REGISTER\r
WWW-Authenticate: Digest realm="{self.account.domain}", nonce="abc123", algorithm=MD5\r
Content-Length: 0\r
\r
'''
        
        authenticator = SIPAuthenticator(self.account)
        challenge = authenticator.parse_auth_challenge(auth_challenge)
        
        print(f"Parsed challenge: {challenge}")
        
        self.assertIsNotNone(challenge)
        self.assertIn('realm', challenge)
        self.assertIn('nonce', challenge)
        self.assertEqual(challenge['realm'], self.account.domain)
        self.assertEqual(challenge['nonce'], 'abc123')
        
        print("✓ Authentication parsing test passed")
    
    def test_registration_with_mock_server(self):
        """Test registration with mock SIP server"""
        print(f"\n=== Testing Registration with Mock Server ===")
        
        # Mock the SIP protocol to simulate server responses
        mock_responses = []
        
        def mock_send_message(message, address=None):
            print(f"Mock server received: {message}")
            mock_responses.append(message)
            
            # Simulate server response after a delay
            def send_response():
                time.sleep(0.1)  # Small delay to simulate network
                if "REGISTER" in message:
                    # Send 200 OK response
                    response = f'''SIP/2.0 200 OK\r
Via: SIP/2.0/UDP 192.168.1.100:5060;branch=z9hG4bK-test\r
From: <sip:{self.account.username}@{self.account.domain}>;tag=test_tag\r
To: <sip:{self.account.username}@{self.account.domain}>;tag=server_tag\r
Call-ID: test_call_id\r
CSeq: 1 REGISTER\r
Content-Length: 0\r
\r
'''
                    # Simulate incoming response
                    if self.client.sip_protocol.on_response_received:
                        self.client.sip_protocol.on_response_received(response, 200)
            
            threading.Thread(target=send_response, daemon=True).start()
            return True
        
        # Set up callback to track registration state
        registration_states = []
        
        def on_registration_state(state):
            registration_states.append(state)
            print(f"Registration state changed to: {state.value}")
        
        self.client.on_registration_state = on_registration_state
        
        # Mock the send_message method
        self.client.sip_protocol.send_message = mock_send_message
        
        # Start client and register
        self.assertTrue(self.client.start())
        self.assertTrue(self.client.register())
        
        # Wait for registration to complete
        time.sleep(0.5)
        
        # Check results
        self.assertGreater(len(mock_responses), 0)
        self.assertIn("REGISTER", mock_responses[0])
        
        # Should have received state changes
        self.assertIn(RegistrationState.REGISTERING, registration_states)
        self.assertIn(RegistrationState.REGISTERED, registration_states)
        
        print("✓ Registration with mock server test passed")
    
    def test_registration_with_auth_challenge(self):
        """Test registration with authentication challenge"""
        print(f"\n=== Testing Registration with Authentication Challenge ===")
        
        response_count = 0
        
        def mock_send_message(message, address=None):
            nonlocal response_count
            response_count += 1
            print(f"Mock server received message #{response_count}: {message}")
            
            def send_response():
                time.sleep(0.1)
                if response_count == 1 and "REGISTER" in message:
                    # Send 401 Unauthorized
                    response = f'''SIP/2.0 401 Unauthorized\r
Via: SIP/2.0/UDP 192.168.1.100:5060;branch=z9hG4bK-test\r
From: <sip:{self.account.username}@{self.account.domain}>;tag=test_tag\r
To: <sip:{self.account.username}@{self.account.domain}>;tag=server_tag\r
Call-ID: test_call_id\r
CSeq: 1 REGISTER\r
WWW-Authenticate: Digest realm="{self.account.domain}", nonce="abc123", algorithm=MD5\r
Content-Length: 0\r
\r
'''
                    if self.client.sip_protocol.on_response_received:
                        self.client.sip_protocol.on_response_received(response, 401)
                
                elif response_count == 2 and "REGISTER" in message and "Authorization:" in message:
                    # Send 200 OK for authenticated request
                    response = f'''SIP/2.0 200 OK\r
Via: SIP/2.0/UDP 192.168.1.100:5060;branch=z9hG4bK-test\r
From: <sip:{self.account.username}@{self.account.domain}>;tag=test_tag\r
To: <sip:{self.account.username}@{self.account.domain}>;tag=server_tag\r
Call-ID: test_call_id\r
CSeq: 2 REGISTER\r
Content-Length: 0\r
\r
'''
                    if self.client.sip_protocol.on_response_received:
                        self.client.sip_protocol.on_response_received(response, 200)
            
            threading.Thread(target=send_response, daemon=True).start()
            return True
        
        # Set up callback to track registration state
        registration_states = []
        
        def on_registration_state(state):
            registration_states.append(state)
            print(f"Registration state changed to: {state.value}")
        
        self.client.on_registration_state = on_registration_state
        
        # Mock the send_message method
        self.client.sip_protocol.send_message = mock_send_message
        
        # Start client and register
        self.assertTrue(self.client.start())
        self.assertTrue(self.client.register())
        
        # Wait for registration to complete
        time.sleep(1.0)
        
        # Should have sent 2 messages (initial + authenticated)
        self.assertEqual(response_count, 2)
        
        # Should have received state changes
        self.assertIn(RegistrationState.REGISTERING, registration_states)
        self.assertIn(RegistrationState.REGISTERED, registration_states)
        
        print("✓ Registration with auth challenge test passed")
    
    def test_registration_timeout_scenario(self):
        """Test registration timeout scenario"""
        print(f"\n=== Testing Registration Timeout Scenario ===")
        
        def mock_send_message(message, address=None):
            print(f"Mock server received: {message}")
            # Don't send any response - simulate timeout
            return True
        
        # Set up callback to track registration state
        registration_states = []
        
        def on_registration_state(state):
            registration_states.append(state)
            print(f"Registration state changed to: {state.value}")
        
        self.client.on_registration_state = on_registration_state
        
        # Mock the send_message method
        self.client.sip_protocol.send_message = mock_send_message
        
        # Start client and register
        self.assertTrue(self.client.start())
        self.assertTrue(self.client.register())
        
        # Wait for a bit
        time.sleep(1.0)
        
        # Should still be in REGISTERING state (no response received)
        self.assertIn(RegistrationState.REGISTERING, registration_states)
        self.assertEqual(self.client.registration_state, RegistrationState.REGISTERING)
        
        print("✓ Registration timeout scenario test passed")
    
    def test_call_initiation_not_registered(self):
        """Test call initiation when not registered"""
        print(f"\n=== Testing Call Initiation When Not Registered ===")
        
        # Start client but don't register
        self.assertTrue(self.client.start())
        
        # Try to make a call
        call_id = self.client.make_call("4402313295")
        
        # Should fail because not registered
        self.assertIsNone(call_id)
        
        print("✓ Call initiation when not registered test passed")
    
    def test_call_initiation_registered(self):
        """Test call initiation when registered"""
        print(f"\n=== Testing Call Initiation When Registered ===")
        
        # Mock successful registration
        self.client.registration_state = RegistrationState.REGISTERED
        
        # Mock INVITE sending
        def mock_send_invite(target_uri, rtp_port=10000):
            print(f"Mock INVITE sent to {target_uri}")
            return "test_call_id"
        
        self.client.sip_protocol.send_invite = mock_send_invite
        
        # Start client
        self.assertTrue(self.client.start())
        
        # Try to make a call
        call_id = self.client.make_call("4402313295")
        
        # Should succeed
        self.assertIsNotNone(call_id)
        self.assertEqual(call_id, "test_call_id")
        
        # Should have call in client's call list
        self.assertIn(call_id, self.client.calls)
        
        print("✓ Call initiation when registered test passed")
    
    def test_real_registration_with_timeout(self):
        """Test real registration with timeout handling"""
        print(f"\n=== Testing Real Registration with Timeout ===")
        
        # Set up callback to track registration state
        registration_states = []
        start_time = time.time()
        
        def on_registration_state(state):
            elapsed = time.time() - start_time
            registration_states.append((state, elapsed))
            print(f"Registration state changed to: {state.value} (after {elapsed:.2f}s)")
        
        self.client.on_registration_state = on_registration_state
        
        # Start client and register
        self.assertTrue(self.client.start())
        self.assertTrue(self.client.register())
        
        # Wait for registration to complete or timeout
        timeout = 10  # seconds
        elapsed = 0
        while elapsed < timeout and self.client.registration_state == RegistrationState.REGISTERING:
            time.sleep(0.1)
            elapsed = time.time() - start_time
        
        print(f"Registration completed after {elapsed:.2f}s")
        print(f"Final registration state: {self.client.registration_state.value}")
        
        # Print all state changes
        for state, timestamp in registration_states:
            print(f"  {timestamp:.2f}s: {state.value}")
        
        # This test documents the actual behavior rather than asserting success
        if self.client.registration_state != RegistrationState.REGISTERED:
            print("⚠ Registration did not complete successfully")
            print("This indicates a real issue with the SIP server or network")
        else:
            print("✓ Registration completed successfully")
    
    def test_sip_message_parsing(self):
        """Test SIP message parsing"""
        print(f"\n=== Testing SIP Message Parsing ===")
        
        # Test response parsing
        response = f'''SIP/2.0 200 OK\r
Via: SIP/2.0/UDP 192.168.1.100:5060;branch=z9hG4bK-test\r
From: <sip:{self.account.username}@{self.account.domain}>;tag=test_tag\r
To: <sip:{self.account.username}@{self.account.domain}>;tag=server_tag\r
Call-ID: test_call_id\r
CSeq: 1 REGISTER\r
Content-Length: 0\r
\r
'''
        
        # Parse response code
        response_code = SIPMessageParser.get_response_code(response)
        self.assertEqual(response_code, 200)
        
        # Parse headers
        headers = SIPMessageParser.parse_headers(response)
        self.assertEqual(headers['Call-ID'], 'test_call_id')
        self.assertEqual(headers['CSeq'], '1 REGISTER')
        
        # Parse CSeq
        cseq = SIPMessageParser.extract_cseq(response)
        self.assertEqual(cseq, (1, 'REGISTER'))
        
        print("✓ SIP message parsing test passed")


class TestNetworkDiagnostics(unittest.TestCase):
    """Network diagnostic tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        load_dotenv()
        self.domain = os.getenv('SIP_DOMAIN', 'newyork1.voip.ms')
        self.port = int(os.getenv('SIP_PORT', '5060'))
    
    def test_dns_resolution(self):
        """Test DNS resolution for SIP server"""
        print(f"\n=== Testing DNS Resolution ===")
        
        try:
            import socket
            ip_address = socket.gethostbyname(self.domain)
            print(f"✓ DNS resolution successful: {self.domain} -> {ip_address}")
        except Exception as e:
            print(f"✗ DNS resolution failed: {e}")
            self.fail(f"DNS resolution issue: {e}")
    
    def test_port_connectivity(self):
        """Test port connectivity to SIP server"""
        print(f"\n=== Testing Port Connectivity ===")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            
            # For UDP, we can't really test connection, but we can test if the socket can be created
            # and if we can send data without immediate errors
            sock.sendto(b"test", (self.domain, self.port))
            
            print(f"✓ Port connectivity test passed for {self.domain}:{self.port}")
            sock.close()
            
        except Exception as e:
            print(f"✗ Port connectivity test failed: {e}")
            self.fail(f"Port connectivity issue: {e}")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2) 