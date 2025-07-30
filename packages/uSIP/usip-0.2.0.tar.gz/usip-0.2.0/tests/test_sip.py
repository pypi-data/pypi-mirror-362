#!/usr/bin/env python3
"""
Tests for SIP protocol components
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the sip_client module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sip_client.sip.messages import SIPMessageBuilder, SIPMessageParser
from sip_client.sip.authentication import SIPAuthenticator
from sip_client.sip.protocol import SIPProtocol
from sip_client.models.account import SIPAccount
from sip_client.models.call import CallInfo
from sip_client.models.enums import CallState


class TestSIPMessageBuilder(unittest.TestCase):
    
    def test_create_message(self):
        """Test creating basic SIP message"""
        headers = {
            'From': 'test@example.com',
            'To': 'target@example.com',
            'Call-ID': 'test-call-id'
        }
        
        message = SIPMessageBuilder.create_message('INVITE', 'sip:target@example.com', headers, 'body')
        
        self.assertIn('INVITE sip:target@example.com SIP/2.0', message)
        self.assertIn('From: test@example.com', message)
        self.assertIn('To: target@example.com', message)
        self.assertIn('Call-ID: test-call-id', message)
        self.assertIn('Content-Length: 4', message)
        self.assertIn('body', message)
    
    def test_create_register_headers(self):
        """Test creating REGISTER headers"""
        headers = SIPMessageBuilder.create_register_headers(
            'testuser', 'example.com', 5060, 'tag123', 'branch456', 'call789', 1
        )
        
        self.assertIn('testuser', headers['From'])
        self.assertIn('example.com', headers['To'])
        self.assertIn('tag123', headers['From'])
        self.assertIn('branch456', headers['Via'])
        self.assertIn('call789', headers['Call-ID'])
        self.assertIn('1 REGISTER', headers['CSeq'])
        self.assertEqual(headers['Expires'], '3600')
    
    def test_create_invite_headers(self):
        """Test creating INVITE headers"""
        headers = SIPMessageBuilder.create_invite_headers(
            'testuser', 'example.com', 5060, 'sip:target@example.com',
            'tag123', 'branch456', 'call789', 1
        )
        
        self.assertIn('testuser', headers['From'])
        self.assertIn('sip:target@example.com', headers['To'])
        self.assertIn('tag123', headers['From'])
        self.assertIn('branch456', headers['Via'])
        self.assertIn('call789', headers['Call-ID'])
        self.assertIn('1 INVITE', headers['CSeq'])
        self.assertEqual(headers['Content-Type'], 'application/sdp')
    
    def test_create_sdp_body(self):
        """Test creating SDP body"""
        sdp = SIPMessageBuilder.create_sdp_body('testuser', 10000)
        
        self.assertIn('v=0', sdp)
        self.assertIn('o=testuser', sdp)
        self.assertIn('m=audio 10000', sdp)
        self.assertIn('a=rtpmap:0 PCMU/8000', sdp)
        self.assertIn('a=sendrecv', sdp)


class TestSIPMessageParser(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_message = """INVITE sip:target@example.com SIP/2.0\r
Via: SIP/2.0/UDP host:5060;branch=z9hG4bK123\r
From: <sip:user@example.com>;tag=abc123\r
To: <sip:target@example.com>\r
Call-ID: test-call-id\r
CSeq: 1 INVITE\r
Contact: <sip:user@host:5060>\r
Content-Type: application/sdp\r
Content-Length: 100\r
\r
v=0\r
o=user 123 123 IN IP4 192.168.1.1\r
s=Test Session\r
c=IN IP4 192.168.1.1\r
t=0 0\r
m=audio 10000 RTP/AVP 0\r
a=rtpmap:0 PCMU/8000"""
    
    def test_parse_headers(self):
        """Test parsing SIP headers"""
        headers = SIPMessageParser.parse_headers(self.sample_message)
        
        self.assertEqual(headers['Call-ID'], 'test-call-id')
        self.assertEqual(headers['CSeq'], '1 INVITE')
        self.assertIn('sip:user@example.com', headers['From'])
        self.assertIn('sip:target@example.com', headers['To'])
    
    def test_extract_tag(self):
        """Test extracting tag from header"""
        from_header = '<sip:user@example.com>;tag=abc123'
        tag = SIPMessageParser.extract_tag(from_header)
        self.assertEqual(tag, 'abc123')
        
        # Test header without tag
        no_tag_header = '<sip:user@example.com>'
        tag = SIPMessageParser.extract_tag(no_tag_header)
        self.assertIsNone(tag)
    
    def test_extract_contact_uri(self):
        """Test extracting contact URI"""
        contact_header = '<sip:user@host:5060>'
        uri = SIPMessageParser.extract_contact_uri(contact_header)
        self.assertEqual(uri, 'sip:user@host:5060')
        
        # Test simple format
        simple_header = 'Contact: sip:user@host:5060;expires=3600'
        uri = SIPMessageParser.extract_contact_uri(simple_header)
        self.assertEqual(uri, 'sip:user@host:5060')
    
    def test_extract_call_id(self):
        """Test extracting call ID"""
        call_id = SIPMessageParser.extract_call_id(self.sample_message)
        self.assertEqual(call_id, 'test-call-id')
    
    def test_extract_cseq(self):
        """Test extracting CSeq"""
        cseq = SIPMessageParser.extract_cseq(self.sample_message)
        self.assertEqual(cseq, (1, 'INVITE'))
    
    def test_extract_uris(self):
        """Test extracting From and To URIs"""
        from_uri = SIPMessageParser.extract_from_uri(self.sample_message)
        to_uri = SIPMessageParser.extract_to_uri(self.sample_message)
        
        self.assertEqual(from_uri, 'sip:user@example.com')
        self.assertEqual(to_uri, 'sip:target@example.com')
    
    def test_get_method(self):
        """Test getting method from request"""
        method = SIPMessageParser.get_method(self.sample_message)
        self.assertEqual(method, 'INVITE')
        
        # Test response
        response = "SIP/2.0 200 OK\r\nVia: SIP/2.0/UDP host:5060\r\n"
        method = SIPMessageParser.get_method(response)
        self.assertIsNone(method)
    
    def test_get_response_code(self):
        """Test getting response code"""
        request_code = SIPMessageParser.get_response_code(self.sample_message)
        self.assertIsNone(request_code)
        
        response = "SIP/2.0 200 OK\r\nVia: SIP/2.0/UDP host:5060\r\n"
        response_code = SIPMessageParser.get_response_code(response)
        self.assertEqual(response_code, 200)
    
    def test_extract_sdp_body(self):
        """Test extracting SDP body"""
        sdp_body = SIPMessageParser.extract_sdp_body(self.sample_message)
        self.assertIn('v=0', sdp_body)
        self.assertIn('m=audio 10000', sdp_body)
    
    def test_parse_sdp_rtp_port(self):
        """Test parsing RTP port from SDP"""
        sdp_body = "v=0\no=user 123 123 IN IP4 192.168.1.1\ns=Test\nc=IN IP4 192.168.1.1\nt=0 0\nm=audio 12345 RTP/AVP 0\na=rtpmap:0 PCMU/8000"
        port = SIPMessageParser.parse_sdp_rtp_port(sdp_body)
        self.assertEqual(port, 12345)


class TestSIPAuthenticator(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.account = SIPAccount(
            username='testuser',
            password='testpass',
            domain='example.com',
            port=5060
        )
        self.authenticator = SIPAuthenticator(self.account)
    
    def test_parse_auth_challenge(self):
        """Test parsing authentication challenge"""
        response = """SIP/2.0 401 Unauthorized\r
Via: SIP/2.0/UDP host:5060;branch=z9hG4bK123\r
From: <sip:user@example.com>;tag=abc123\r
To: <sip:user@example.com>;tag=def456\r
Call-ID: test-call-id\r
CSeq: 1 REGISTER\r
WWW-Authenticate: Digest realm="example.com", nonce="abc123def456", algorithm=MD5\r
Content-Length: 0\r
\r
"""
        
        challenge = self.authenticator.parse_auth_challenge(response)
        
        self.assertIsNotNone(challenge)
        self.assertEqual(challenge['realm'], 'example.com')
        self.assertEqual(challenge['nonce'], 'abc123def456')
        self.assertEqual(challenge['algorithm'], 'MD5')
    
    def test_parse_auth_challenge_proxy(self):
        """Test parsing proxy authentication challenge"""
        response = """SIP/2.0 407 Proxy Authentication Required\r
Via: SIP/2.0/UDP host:5060;branch=z9hG4bK123\r
From: <sip:user@example.com>;tag=abc123\r
To: <sip:user@example.com>;tag=def456\r
Call-ID: test-call-id\r
CSeq: 1 REGISTER\r
Proxy-Authenticate: Digest realm="proxy.example.com", nonce="xyz789"\r
Content-Length: 0\r
\r
"""
        
        challenge = self.authenticator.parse_auth_challenge(response)
        
        self.assertIsNotNone(challenge)
        self.assertEqual(challenge['realm'], 'proxy.example.com')
        self.assertEqual(challenge['nonce'], 'xyz789')
    
    def test_create_auth_response(self):
        """Test creating authentication response"""
        challenge = {
            'realm': 'example.com',
            'nonce': 'abc123def456'
        }
        
        auth_header = self.authenticator.create_auth_response(challenge, 'REGISTER', 'sip:example.com')
        
        self.assertIn('Digest', auth_header)
        self.assertIn('username="testuser"', auth_header)
        self.assertIn('realm="example.com"', auth_header)
        self.assertIn('nonce="abc123def456"', auth_header)
        self.assertIn('uri="sip:example.com"', auth_header)
        self.assertIn('response=', auth_header)
    
    def test_is_auth_required(self):
        """Test checking if authentication is required"""
        auth_response = "SIP/2.0 401 Unauthorized\r\n"
        proxy_auth_response = "SIP/2.0 407 Proxy Authentication Required\r\n"
        ok_response = "SIP/2.0 200 OK\r\n"
        
        self.assertTrue(self.authenticator.is_auth_required(auth_response))
        self.assertTrue(self.authenticator.is_auth_required(proxy_auth_response))
        self.assertFalse(self.authenticator.is_auth_required(ok_response))


class TestSIPProtocol(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.account = SIPAccount(
            username='testuser',
            password='testpass',
            domain='example.com',
            port=5060
        )
        self.protocol = SIPProtocol(self.account)
    
    def tearDown(self):
        """Clean up after tests"""
        self.protocol.stop()
    
    @patch('sip_client.sip.protocol.socket')
    def test_protocol_start_stop(self, mock_socket):
        """Test protocol start/stop"""
        mock_socket_instance = Mock()
        mock_socket.socket.return_value = mock_socket_instance
        
        result = self.protocol.start()
        self.assertTrue(result)
        self.assertIsNotNone(self.protocol.socket)
        self.assertTrue(self.protocol.listening)
        
        self.protocol.stop()
        self.assertFalse(self.protocol.listening)
        mock_socket_instance.close.assert_called_once()
    
    @patch('sip_client.sip.protocol.socket')
    def test_send_message(self, mock_socket):
        """Test sending SIP message"""
        mock_socket_instance = Mock()
        mock_socket.socket.return_value = mock_socket_instance
        
        self.protocol.start()
        
        result = self.protocol.send_message("TEST MESSAGE")
        self.assertTrue(result)
        mock_socket_instance.sendto.assert_called_once_with(
            b"TEST MESSAGE", 
            (self.account.domain, self.account.port)
        )
    
    @patch('sip_client.sip.protocol.socket')
    def test_send_register(self, mock_socket):
        """Test sending REGISTER"""
        mock_socket_instance = Mock()
        mock_socket.socket.return_value = mock_socket_instance
        
        self.protocol.start()
        
        result = self.protocol.send_register()
        self.assertTrue(result)
        
        # Verify message was sent
        mock_socket_instance.sendto.assert_called_once()
        sent_message = mock_socket_instance.sendto.call_args[0][0].decode()
        self.assertIn('REGISTER', sent_message)
        self.assertIn('testuser', sent_message)
        self.assertIn('example.com', sent_message)
    
    @patch('sip_client.sip.protocol.socket')
    def test_send_invite(self, mock_socket):
        """Test sending INVITE"""
        mock_socket_instance = Mock()
        mock_socket.socket.return_value = mock_socket_instance
        
        self.protocol.start()
        
        call_id = self.protocol.send_invite('sip:target@example.com')
        self.assertIsNotNone(call_id)
        
        # Verify message was sent
        mock_socket_instance.sendto.assert_called_once()
        sent_message = mock_socket_instance.sendto.call_args[0][0].decode()
        self.assertIn('INVITE', sent_message)
        self.assertIn('sip:target@example.com', sent_message)
        self.assertIn('application/sdp', sent_message)
    
    @patch('sip_client.sip.protocol.socket')
    def test_send_ack(self, mock_socket):
        """Test sending ACK"""
        mock_socket_instance = Mock()
        mock_socket.socket.return_value = mock_socket_instance
        
        self.protocol.start()
        
        call_info = CallInfo(
            call_id='test-call',
            local_uri='sip:user@example.com',
            remote_uri='sip:target@example.com',
            state=CallState.CONNECTED,
            direction='outgoing',
            local_tag='tag123',
            remote_tag='tag456',
            cseq=1
        )
        
        result = self.protocol.send_ack(call_info)
        self.assertTrue(result)
        
        # Verify message was sent
        mock_socket_instance.sendto.assert_called_once()
        sent_message = mock_socket_instance.sendto.call_args[0][0].decode()
        self.assertIn('ACK', sent_message)
        self.assertIn('test-call', sent_message)
    
    @patch('sip_client.sip.protocol.socket')
    def test_send_bye(self, mock_socket):
        """Test sending BYE"""
        mock_socket_instance = Mock()
        mock_socket.socket.return_value = mock_socket_instance
        
        self.protocol.start()
        
        call_info = CallInfo(
            call_id='test-call',
            local_uri='sip:user@example.com',
            remote_uri='sip:target@example.com',
            state=CallState.CONNECTED,
            direction='outgoing',
            local_tag='tag123',
            remote_tag='tag456',
            cseq=1
        )
        
        result = self.protocol.send_bye(call_info)
        self.assertTrue(result)
        
        # Verify message was sent
        mock_socket_instance.sendto.assert_called_once()
        sent_message = mock_socket_instance.sendto.call_args[0][0].decode()
        self.assertIn('BYE', sent_message)
        self.assertIn('test-call', sent_message)
        self.assertEqual(call_info.cseq, 2)  # CSeq should be incremented
    
    def test_extract_sip_info(self):
        """Test extracting SIP information"""
        message = """INVITE sip:target@example.com SIP/2.0\r
Via: SIP/2.0/UDP host:5060;branch=z9hG4bK123\r
From: <sip:user@example.com>;tag=abc123\r
To: <sip:target@example.com>\r
Call-ID: test-call-id\r
CSeq: 1 INVITE\r
Contact: <sip:user@host:5060>\r
Content-Length: 0\r
\r
"""
        
        info = self.protocol.extract_sip_info(message)
        
        self.assertEqual(info['call_id'], 'test-call-id')
        self.assertEqual(info['from_uri'], 'sip:user@example.com')
        self.assertEqual(info['to_uri'], 'sip:target@example.com')
        self.assertEqual(info['from_tag'], 'abc123')
        self.assertEqual(info['contact_uri'], 'sip:user@host:5060')
        self.assertEqual(info['cseq'], (1, 'INVITE'))
        self.assertEqual(info['method'], 'INVITE')
    
    def test_callback_system(self):
        """Test callback system"""
        message_received = False
        response_received = False
        request_received = False
        
        def on_message(msg, addr):
            nonlocal message_received
            message_received = True
        
        def on_response(msg, code):
            nonlocal response_received
            response_received = True
        
        def on_request(msg, method):
            nonlocal request_received
            request_received = True
        
        self.protocol.on_message_received = on_message
        self.protocol.on_response_received = on_response
        self.protocol.on_request_received = on_request
        
        # Test response handling
        response = "SIP/2.0 200 OK\r\nVia: SIP/2.0/UDP host:5060\r\n"
        self.protocol._handle_incoming_message(response, ('127.0.0.1', 5060))
        
        self.assertTrue(message_received)
        self.assertTrue(response_received)
        self.assertFalse(request_received)
        
        # Reset flags
        message_received = False
        response_received = False
        
        # Test request handling
        request = "INVITE sip:target@example.com SIP/2.0\r\nVia: SIP/2.0/UDP host:5060\r\n"
        self.protocol._handle_incoming_message(request, ('127.0.0.1', 5060))
        
        self.assertTrue(message_received)
        self.assertFalse(response_received)
        self.assertTrue(request_received)


if __name__ == '__main__':
    unittest.main() 