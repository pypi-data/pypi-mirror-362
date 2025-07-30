"""
Main SIP Client - Orchestrates all components to provide a clean API
"""

import os
import time
import threading
import logging
from typing import Optional, Dict, List, Callable

from .models.account import SIPAccount
from .models.call import CallInfo
from .models.enums import CallState, RegistrationState
from .audio.manager import AudioManager
from .audio.devices import AudioDevice
from .sip.protocol import SIPProtocol
from .sip.messages import SIPMessageParser
from .utils.helpers import generate_call_id, generate_tag

logger = logging.getLogger(__name__)


class SIPClient:
    """Main SIP client with voice support"""
    
    def __init__(self, account: Optional[SIPAccount] = None):
        """Initialize SIP client
        
        Args:
            account: SIP account configuration. If None, will try to load from environment.
        """
        if account is None:
            account = SIPAccount(
                username=os.getenv('SIP_USERNAME', ''),
                password=os.getenv('SIP_PASSWORD', ''),
                domain=os.getenv('SIP_DOMAIN', ''),
                port=int(os.getenv('SIP_PORT', 5060))
            )
        
        self.account = account
        self.sip_protocol = SIPProtocol(account)
        self.audio_manager = AudioManager()
        
        # State
        self.registration_state = RegistrationState.UNREGISTERED
        self.calls: Dict[str, CallInfo] = {}
        self.rtp_port = 10000
        
        # Keep-alive timer
        self.keepalive_timer = None
        self.keepalive_interval = 30  # seconds
        
        # Callbacks
        self.on_registration_state: Optional[Callable[[RegistrationState], None]] = None
        self.on_incoming_call: Optional[Callable[[CallInfo], None]] = None
        self.on_call_state: Optional[Callable[[CallInfo], None]] = None
        self.on_call_media: Optional[Callable[[CallInfo], None]] = None
        self.on_message: Optional[Callable[[str, str], None]] = None
        
        # Set up SIP protocol callbacks
        self._setup_sip_callbacks()
    
    def _setup_sip_callbacks(self):
        """Set up SIP protocol callbacks"""
        self.sip_protocol.on_response_received = self._handle_sip_response
        self.sip_protocol.on_request_received = self._handle_sip_request
        self.sip_protocol.on_message_received = self._handle_sip_message
    
    def start(self) -> bool:
        """Start the SIP client"""
        try:
            if not self.sip_protocol.start():
                return False
            
            logger.info("SIP client started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start SIP client: {e}")
            return False
    
    def stop(self):
        """Stop the SIP client"""
        # End all active calls
        for call_id in list(self.calls.keys()):
            self.hangup(call_id)
        
        # Unregister
        if self.registration_state == RegistrationState.REGISTERED:
            self.unregister()
        
        # Stop keep-alive timer
        if self.keepalive_timer:
            self.keepalive_timer.cancel()
        
        # Stop components
        self.sip_protocol.stop()
        self.audio_manager.cleanup()
        
        logger.info("SIP client stopped")
    
    def register(self) -> bool:
        """Register with SIP server"""
        if self.registration_state == RegistrationState.REGISTERING:
            return False
        
        try:
            self._set_registration_state(RegistrationState.REGISTERING)
            
            # Send REGISTER request
            success = self.sip_protocol.send_register()
            
            if success:
                logger.info("REGISTER sent, waiting for response")
                return True
            else:
                self._set_registration_state(RegistrationState.FAILED)
                return False
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            self._set_registration_state(RegistrationState.FAILED)
            return False
    
    def unregister(self) -> bool:
        """Unregister from SIP server"""
        try:
            if self.keepalive_timer:
                self.keepalive_timer.cancel()
            
            # Send REGISTER with Expires: 0
            success = self.sip_protocol.send_register(expires=0)
            
            if success:
                self._set_registration_state(RegistrationState.UNREGISTERED)
            
            return success
            
        except Exception as e:
            logger.error(f"Unregistration error: {e}")
            return False
    
    def make_call(self, target_uri: str, input_device: Optional[int] = None, 
                  output_device: Optional[int] = None) -> Optional[str]:
        """Make an outgoing call"""
        if self.registration_state != RegistrationState.REGISTERED:
            logger.error("Not registered")
            return None
        
        try:
            # Normalize target URI
            if not target_uri.startswith('sip:'):
                if not target_uri.startswith('+'):
                    target_uri = f"+1{target_uri}"  # Assuming US numbers
                target_uri = f"sip:{target_uri}@{self.account.domain}"
            
            # Get audio devices
            if input_device is None:
                device = self.audio_manager.get_default_input_device()
                input_device = device.index if device else 0
            
            if output_device is None:
                device = self.audio_manager.get_default_output_device()
                output_device = device.index if device else 0
            
            # Send INVITE
            call_id = self.sip_protocol.send_invite(target_uri, self.rtp_port)
            
            if call_id:
                # Create call info
                call_info = CallInfo(
                    call_id=call_id,
                    local_uri=self.account.uri,
                    remote_uri=target_uri,
                    state=CallState.CALLING,
                    direction="outgoing",
                    start_time=time.time(),
                    local_tag=generate_tag(),
                    input_device=input_device,
                    output_device=output_device
                )
                
                self.calls[call_id] = call_info
                self._set_call_state(call_info, CallState.CALLING)
                
                logger.info(f"Call initiated: {call_id}")
                return call_id
            
            return None
            
        except Exception as e:
            logger.error(f"Call error: {e}")
            return None
    
    def answer_call(self, call_id: str, input_device: Optional[int] = None, 
                   output_device: Optional[int] = None) -> bool:
        """Answer an incoming call"""
        if call_id not in self.calls:
            return False
        
        call_info = self.calls[call_id]
        if call_info.state != CallState.RINGING:
            return False
        
        try:
            # Get audio devices
            if input_device is None:
                device = self.audio_manager.get_default_input_device()
                input_device = device.index if device else 0
            
            if output_device is None:
                device = self.audio_manager.get_default_output_device()
                output_device = device.index if device else 0
            
            call_info.input_device = input_device
            call_info.output_device = output_device
            
            # Send 200 OK response (would need to store original INVITE)
            # For now, just update state
            call_info.answer_time = time.time()
            self._set_call_state(call_info, CallState.CONNECTED)
            
            # Start audio
            self.audio_manager.start_audio_stream(input_device, output_device, self.rtp_port)
            
            logger.info(f"Call {call_id} answered")
            return True
            
        except Exception as e:
            logger.error(f"Error answering call: {e}")
            return False
    
    def hangup(self, call_id: str) -> bool:
        """Hang up a call"""
        if call_id not in self.calls:
            return False
        
        call_info = self.calls[call_id]
        
        try:
            # Send BYE if call is connected
            if call_info.state == CallState.CONNECTED:
                self.sip_protocol.send_bye(call_info)
            
            # Stop audio
            self.audio_manager.stop_audio_stream()
            
            call_info.end_time = time.time()
            self._set_call_state(call_info, CallState.DISCONNECTED)
            
            # Clean up call
            del self.calls[call_id]
            
            logger.info(f"Call {call_id} ended")
            return True
            
        except Exception as e:
            logger.error(f"Hangup error: {e}")
            return False
    
    def get_calls(self) -> List[CallInfo]:
        """Get list of active calls"""
        return list(self.calls.values())
    
    def get_call(self, call_id: str) -> Optional[CallInfo]:
        """Get call information"""
        return self.calls.get(call_id)
    
    def get_audio_devices(self) -> List[AudioDevice]:
        """Get list of available audio devices"""
        return self.audio_manager.get_audio_devices()
    
    def switch_audio_device(self, call_id: str, input_device: Optional[int] = None, 
                           output_device: Optional[int] = None) -> bool:
        """Switch audio devices during active call"""
        if call_id not in self.calls:
            return False
        
        call_info = self.calls[call_id]
        if call_info.state != CallState.CONNECTED:
            return False
        
        success = True
        
        if input_device is not None:
            success &= self.audio_manager.switch_input_device(input_device)
            if success:
                call_info.input_device = input_device
        
        if output_device is not None:
            success &= self.audio_manager.switch_output_device(output_device)
            if success:
                call_info.output_device = output_device
        
        return success
    
    def _handle_sip_response(self, message: str, response_code: int):
        """Handle SIP response"""
        logger.debug(f"SIP response {response_code}: {message}")
        
        # Handle registration responses
        if "REGISTER" in message:
            if response_code == 200:
                self._set_registration_state(RegistrationState.REGISTERED)
                self._start_keepalive()
            elif response_code in [401, 407]:
                # Handle authentication challenge
                success = self.sip_protocol.handle_auth_challenge(message, "REGISTER", f"sip:{self.account.domain}")
                if not success:
                    self._set_registration_state(RegistrationState.FAILED)
            else:
                self._set_registration_state(RegistrationState.FAILED)
        
        # Handle INVITE responses
        elif "INVITE" in message:
            call_id = SIPMessageParser.extract_call_id(message)
            if call_id and call_id in self.calls:
                call_info = self.calls[call_id]
                
                if response_code == 200:
                    # Call answered
                    sip_info = self.sip_protocol.extract_sip_info(message)
                    call_info.remote_tag = sip_info.get('to_tag')
                    call_info.contact_uri = sip_info.get('contact_uri')
                    
                    # Send ACK
                    self.sip_protocol.send_ack(call_info)
                    
                    # Start audio
                    if call_info.input_device is not None and call_info.output_device is not None:
                        self.audio_manager.start_audio_stream(
                            call_info.input_device, 
                            call_info.output_device, 
                            self.rtp_port
                        )
                    
                    call_info.answer_time = time.time()
                    self._set_call_state(call_info, CallState.CONNECTED)
                    
                elif response_code == 180:
                    self._set_call_state(call_info, CallState.RINGING)
                elif response_code == 183:
                    # Session progress
                    pass
                elif response_code == 486:
                    self._set_call_state(call_info, CallState.BUSY)
                    del self.calls[call_id]
                elif response_code in [401, 407]:
                    # Handle authentication challenge
                    success = self.sip_protocol.handle_auth_challenge(message, "INVITE", call_info.remote_uri)
                    if not success:
                        self._set_call_state(call_info, CallState.FAILED)
                        del self.calls[call_id]
                else:
                    self._set_call_state(call_info, CallState.FAILED)
                    del self.calls[call_id]
    
    def _handle_sip_request(self, message: str, method: str):
        """Handle SIP request"""
        logger.debug(f"SIP request {method}: {message}")
        
        if method == "INVITE":
            self._handle_incoming_invite(message)
        elif method == "BYE":
            self._handle_incoming_bye(message)
        elif method == "ACK":
            # ACK received, call is fully established
            pass
    
    def _handle_incoming_invite(self, message: str):
        """Handle incoming INVITE request"""
        sip_info = self.sip_protocol.extract_sip_info(message)
        call_id = sip_info.get('call_id')
        
        if call_id:
            # Create call info
            call_info = CallInfo(
                call_id=call_id,
                local_uri=self.account.uri,
                remote_uri=sip_info.get('from_uri', ''),
                state=CallState.RINGING,
                direction="incoming",
                start_time=time.time(),
                local_tag=generate_tag(),
                remote_tag=sip_info.get('from_tag')
            )
            
            self.calls[call_id] = call_info
            
            # Send 100 Trying
            self.sip_protocol.send_response(100, "Trying", message)
            
            # Send 180 Ringing
            self.sip_protocol.send_response(180, "Ringing", message)
            
            self._set_call_state(call_info, CallState.RINGING)
            
            # Notify callback
            if self.on_incoming_call:
                self.on_incoming_call(call_info)
    
    def _handle_incoming_bye(self, message: str):
        """Handle incoming BYE request"""
        call_id = SIPMessageParser.extract_call_id(message)
        
        if call_id and call_id in self.calls:
            call_info = self.calls[call_id]
            
            # Send 200 OK
            self.sip_protocol.send_response(200, "OK", message)
            
            # Stop audio
            self.audio_manager.stop_audio_stream()
            
            call_info.end_time = time.time()
            self._set_call_state(call_info, CallState.DISCONNECTED)
            
            # Clean up
            del self.calls[call_id]
    
    def _handle_sip_message(self, message: str, addr):
        """Handle any SIP message"""
        if self.on_message:
            self.on_message(message, str(addr))
    
    def _set_registration_state(self, state: RegistrationState):
        """Set registration state and notify callback"""
        self.registration_state = state
        logger.info(f"Registration state: {state.value}")
        if self.on_registration_state:
            self.on_registration_state(state)
    
    def _set_call_state(self, call_info: CallInfo, state: CallState):
        """Set call state and notify callback"""
        call_info.state = state
        logger.info(f"Call {call_info.call_id} state: {state.value}")
        if self.on_call_state:
            self.on_call_state(call_info)
    
    def _start_keepalive(self):
        """Start registration keepalive timer"""
        def keepalive():
            if self.registration_state == RegistrationState.REGISTERED:
                self.register()  # Re-register
                self.keepalive_timer = threading.Timer(self.keepalive_interval, keepalive)
                self.keepalive_timer.start()
        
        self.keepalive_timer = threading.Timer(self.keepalive_interval, keepalive)
        self.keepalive_timer.start() 