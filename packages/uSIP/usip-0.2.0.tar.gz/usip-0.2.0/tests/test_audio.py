#!/usr/bin/env python3
"""
Tests for audio components
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the sip_client module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sip_client.audio.devices import AudioDevice, AudioDeviceManager
from sip_client.audio.manager import AudioManager


class TestAudioDevice(unittest.TestCase):
    
    def test_audio_device_creation(self):
        """Test audio device creation"""
        device = AudioDevice(
            index=0,
            name="Test Device",
            max_input_channels=2,
            max_output_channels=2,
            default_sample_rate=44100.0
        )
        
        self.assertEqual(device.index, 0)
        self.assertEqual(device.name, "Test Device")
        self.assertEqual(device.max_input_channels, 2)
        self.assertEqual(device.max_output_channels, 2)
        self.assertEqual(device.default_sample_rate, 44100.0)
    
    def test_audio_device_properties(self):
        """Test audio device properties"""
        # Input-only device
        input_device = AudioDevice(
            index=0,
            name="Microphone",
            max_input_channels=1,
            max_output_channels=0,
            default_sample_rate=44100.0
        )
        
        self.assertTrue(input_device.is_input)
        self.assertFalse(input_device.is_output)
        
        # Output-only device
        output_device = AudioDevice(
            index=1,
            name="Speaker",
            max_input_channels=0,
            max_output_channels=2,
            default_sample_rate=44100.0
        )
        
        self.assertFalse(output_device.is_input)
        self.assertTrue(output_device.is_output)
        
        # Input/output device
        duplex_device = AudioDevice(
            index=2,
            name="Headset",
            max_input_channels=1,
            max_output_channels=2,
            default_sample_rate=44100.0
        )
        
        self.assertTrue(duplex_device.is_input)
        self.assertTrue(duplex_device.is_output)
    
    def test_audio_device_string_representation(self):
        """Test audio device string representation"""
        device = AudioDevice(
            index=0,
            name="Test Device",
            max_input_channels=1,
            max_output_channels=2,
            default_sample_rate=44100.0
        )
        
        str_repr = str(device)
        self.assertIn("Test Device", str_repr)
        self.assertIn("INPUT", str_repr)
        self.assertIn("OUTPUT", str_repr)


class TestAudioDeviceManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_pyaudio = Mock()
        self.mock_audio_instance = Mock()
        self.mock_pyaudio.PyAudio.return_value = self.mock_audio_instance
    
    @patch('sip_client.audio.devices.pyaudio')
    def test_device_manager_initialization(self, mock_pyaudio):
        """Test device manager initialization"""
        mock_pyaudio.PyAudio.return_value = Mock()
        
        manager = AudioDeviceManager()
        
        self.assertIsNotNone(manager.audio)
        mock_pyaudio.PyAudio.assert_called_once()
    
    @patch('sip_client.audio.devices.pyaudio')
    def test_device_manager_no_pyaudio(self, mock_pyaudio):
        """Test device manager when pyaudio is not available"""
        mock_pyaudio.PyAudio.side_effect = ImportError("pyaudio not available")
        
        with self.assertRaises(ImportError):
            AudioDeviceManager()
    
    @patch('sip_client.audio.devices.pyaudio')
    def test_get_devices(self, mock_pyaudio):
        """Test getting audio devices"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        # Mock device info
        mock_audio.get_device_count.return_value = 2
        mock_audio.get_device_info_by_index.side_effect = [
            {
                'index': 0,
                'name': 'Microphone',
                'maxInputChannels': 1,
                'maxOutputChannels': 0,
                'defaultSampleRate': 44100.0
            },
            {
                'index': 1,
                'name': 'Speaker',
                'maxInputChannels': 0,
                'maxOutputChannels': 2,
                'defaultSampleRate': 44100.0
            }
        ]
        
        manager = AudioDeviceManager()
        devices = manager.get_devices()
        
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0].name, 'Microphone')
        self.assertEqual(devices[1].name, 'Speaker')
        self.assertTrue(devices[0].is_input)
        self.assertTrue(devices[1].is_output)
    
    @patch('sip_client.audio.devices.pyaudio')
    def test_get_default_devices(self, mock_pyaudio):
        """Test getting default audio devices"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        # Mock default device info
        mock_audio.get_default_input_device_info.return_value = {
            'index': 0,
            'name': 'Default Microphone',
            'maxInputChannels': 1,
            'maxOutputChannels': 0,
            'defaultSampleRate': 44100.0
        }
        
        mock_audio.get_default_output_device_info.return_value = {
            'index': 1,
            'name': 'Default Speaker',
            'maxInputChannels': 0,
            'maxOutputChannels': 2,
            'defaultSampleRate': 44100.0
        }
        
        manager = AudioDeviceManager()
        
        input_device = manager.get_default_input_device()
        output_device = manager.get_default_output_device()
        
        self.assertIsNotNone(input_device)
        self.assertIsNotNone(output_device)
        self.assertEqual(input_device.name, 'Default Microphone')
        self.assertEqual(output_device.name, 'Default Speaker')
    
    @patch('sip_client.audio.devices.pyaudio')
    def test_validate_device(self, mock_pyaudio):
        """Test device validation"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        # Mock device info
        mock_audio.get_device_info_by_index.return_value = {
            'maxInputChannels': 1,
            'maxOutputChannels': 2
        }
        
        manager = AudioDeviceManager()
        
        # Test input validation
        self.assertTrue(manager.validate_device(0, for_input=True))
        
        # Test output validation
        self.assertTrue(manager.validate_device(0, for_input=False))
        
        # Test invalid device
        mock_audio.get_device_info_by_index.side_effect = Exception("Invalid device")
        self.assertFalse(manager.validate_device(999, for_input=True))


class TestAudioManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_pyaudio = Mock()
        self.mock_audio_instance = Mock()
        self.mock_pyaudio.PyAudio.return_value = self.mock_audio_instance
    
    @patch('sip_client.audio.manager.pyaudio')
    def test_audio_manager_initialization(self, mock_pyaudio):
        """Test audio manager initialization"""
        mock_pyaudio.PyAudio.return_value = Mock()
        
        manager = AudioManager()
        
        self.assertIsNotNone(manager.device_manager)
        self.assertFalse(manager.is_streaming)
        self.assertIsNone(manager.input_stream)
        self.assertIsNone(manager.output_stream)
        self.assertEqual(manager.sample_rate, 8000)
        self.assertEqual(manager.channels, 1)
    
    @patch('sip_client.audio.manager.pyaudio', None)
    def test_audio_manager_no_pyaudio(self):
        """Test audio manager when pyaudio is not available"""
        with self.assertRaises(ImportError):
            AudioManager()
    
    @patch('sip_client.audio.manager.pyaudio')
    def test_get_audio_devices(self, mock_pyaudio):
        """Test getting audio devices through manager"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        manager = AudioManager()
        manager.device_manager.get_devices = Mock(return_value=[])
        
        devices = manager.get_audio_devices()
        
        manager.device_manager.get_devices.assert_called_once()
    
    @patch('sip_client.audio.manager.pyaudio')
    @patch('sip_client.audio.manager.socket')
    def test_start_audio_stream(self, mock_socket, mock_pyaudio):
        """Test starting audio stream"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        # Mock socket
        mock_socket_instance = Mock()
        mock_socket.socket.return_value = mock_socket_instance
        
        # Mock streams
        mock_input_stream = Mock()
        mock_output_stream = Mock()
        mock_audio.open.side_effect = [mock_input_stream, mock_output_stream]
        
        manager = AudioManager()
        
        # Mock device validation
        manager.device_manager.validate_device = Mock(return_value=True)
        
        # Start stream
        manager.start_audio_stream(0, 1, 10000)
        
        # Verify socket creation
        mock_socket.socket.assert_called_once()
        mock_socket_instance.bind.assert_called_once_with(('0.0.0.0', 10000))
        
        # Verify audio streams
        self.assertEqual(mock_audio.open.call_count, 2)
        self.assertTrue(manager.is_streaming)
        self.assertIsNotNone(manager.audio_thread)
    
    @patch('sip_client.audio.manager.pyaudio')
    def test_start_audio_stream_invalid_device(self, mock_pyaudio):
        """Test starting audio stream with invalid device"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        manager = AudioManager()
        
        # Mock device validation to fail
        manager.device_manager.validate_device = Mock(return_value=False)
        
        # Start stream should fail
        with self.assertRaises(ValueError):
            manager.start_audio_stream(0, 1, 10000)
    
    @patch('sip_client.audio.manager.pyaudio')
    def test_stop_audio_stream(self, mock_pyaudio):
        """Test stopping audio stream"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        manager = AudioManager()
        
        # Mock streams
        mock_input_stream = Mock()
        mock_output_stream = Mock()
        mock_rtp_socket = Mock()
        
        manager.input_stream = mock_input_stream
        manager.output_stream = mock_output_stream
        manager.rtp_socket = mock_rtp_socket
        manager.is_streaming = True
        
        # Stop stream
        manager.stop_audio_stream()
        
        # Verify cleanup
        mock_input_stream.stop_stream.assert_called_once()
        mock_input_stream.close.assert_called_once()
        mock_output_stream.stop_stream.assert_called_once()
        mock_output_stream.close.assert_called_once()
        mock_rtp_socket.close.assert_called_once()
        self.assertFalse(manager.is_streaming)
    
    @patch('sip_client.audio.manager.pyaudio')
    def test_switch_devices(self, mock_pyaudio):
        """Test switching audio devices"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        manager = AudioManager()
        
        # Mock device validation
        manager.device_manager.validate_device = Mock(return_value=True)
        
        # Mock existing streams
        mock_old_input = Mock()
        mock_old_output = Mock()
        mock_new_input = Mock()
        mock_new_output = Mock()
        
        manager.input_stream = mock_old_input
        manager.output_stream = mock_old_output
        
        # Mock new stream creation
        mock_audio.open.side_effect = [mock_new_input, mock_new_output]
        
        # Switch input device
        result = manager.switch_input_device(2)
        self.assertTrue(result)
        mock_old_input.stop_stream.assert_called_once()
        mock_old_input.close.assert_called_once()
        self.assertEqual(manager.current_input_device, 2)
        
        # Reset mock
        mock_audio.open.reset_mock()
        mock_audio.open.return_value = mock_new_output
        
        # Switch output device
        result = manager.switch_output_device(3)
        self.assertTrue(result)
        mock_old_output.stop_stream.assert_called_once()
        mock_old_output.close.assert_called_once()
        self.assertEqual(manager.current_output_device, 3)
    
    @patch('sip_client.audio.manager.pyaudio')
    def test_cleanup(self, mock_pyaudio):
        """Test cleanup"""
        mock_audio = Mock()
        mock_pyaudio.PyAudio.return_value = mock_audio
        
        manager = AudioManager()
        manager.stop_audio_stream = Mock()
        
        # Mock device manager
        mock_device_manager = Mock()
        manager.device_manager = mock_device_manager
        
        # Cleanup
        manager.cleanup()
        
        # Verify cleanup calls
        manager.stop_audio_stream.assert_called_once()
        mock_device_manager.cleanup.assert_called_once()


if __name__ == '__main__':
    unittest.main() 