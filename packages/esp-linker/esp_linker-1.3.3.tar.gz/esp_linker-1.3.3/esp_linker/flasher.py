"""
ESP-Linker Firmware Flasher
(c) 2025 SK Raihan / SKR Electronics Lab

Firmware flashing functionality using esptool.py for ESP8266 boards.
Includes bundled firmware and automatic port detection.
"""

import os
import sys
import time
import subprocess
import serial.tools.list_ports
from typing import List, Optional, Dict, Any, Callable
from pathlib import Path
import pkg_resources
import threading
import re

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

from .exceptions import FlashError, DeviceNotFoundError


class ProgressTracker:
    """Enhanced progress tracking with visual progress bars"""

    def __init__(self, use_progress_bar: bool = True):
        self.use_progress_bar = use_progress_bar and TQDM_AVAILABLE
        self.current_progress = None

    def start_operation(self, description: str, total: Optional[int] = None):
        """Start a new operation with progress tracking"""
        if self.use_progress_bar and total:
            self.current_progress = tqdm(
                total=total,
                desc=description,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
            )
        else:
            print(f"[~] {description}...")

    def update_progress(self, amount: int = 1, message: Optional[str] = None):
        """Update progress"""
        if self.current_progress:
            self.current_progress.update(amount)
            if message:
                self.current_progress.set_description(message)
        elif message:
            print(f"   {message}")

    def finish_operation(self, success_message: str):
        """Finish current operation"""
        if self.current_progress:
            self.current_progress.close()
            self.current_progress = None
        print(f"[+] {success_message}")

    def reset_progress(self):
        """Reset current progress bar"""
        if self.current_progress:
            self.current_progress.n = 0
            self.current_progress.refresh()

    def simple_message(self, message: str):
        """Display a simple message"""
        print(message)


class ESP8266Flasher:
    """ESP8266 firmware flasher using esptool.py"""
    
    # Default flash parameters
    DEFAULT_BAUD_RATE = 460800
    DEFAULT_FLASH_SIZE = "4MB"
    DEFAULT_FLASH_MODE = "dio"
    DEFAULT_FLASH_FREQ = "40m"
    FLASH_ADDRESS = "0x00000"
    
    def __init__(self):
        """Initialize the flasher"""
        self.firmware_path = self._get_firmware_path()
        self.esptool_path = self._get_esptool_path()
    
    def _get_firmware_path(self) -> str:
        """Get the path to the bundled firmware"""
        try:
            # Try to get firmware from package resources
            firmware_path = pkg_resources.resource_filename('esp_linker', 'firmware/esp-linker-firmware.bin')
            if os.path.exists(firmware_path):
                return firmware_path
        except:
            pass
        
        # Fallback: look in the same directory as this module
        current_dir = Path(__file__).parent
        firmware_path = current_dir / "firmware" / "esp-linker-firmware.bin"
        
        if firmware_path.exists():
            return str(firmware_path)
        
        raise FlashError("ESP-Linker firmware not found. Please reinstall the library.")
    
    def _get_esptool_path(self) -> str:
        """Get the path to esptool.py"""
        try:
            # Try to find esptool in the current Python environment
            import esptool
            return esptool.__file__
        except ImportError:
            raise FlashError("esptool not found. Please install it with: pip install esptool")
    
    def detect_esp8266_ports(self) -> List[Dict[str, str]]:
        """
        Detect ESP8266 boards connected via USB.
        
        Returns:
            List of dictionaries with port information
        """
        esp_ports = []
        ports = list(serial.tools.list_ports.comports())
        
        # Common ESP8266 USB-to-Serial chip identifiers
        esp_identifiers = [
            'CH340',    # NodeMCU v3, Wemos D1 Mini
            'CP210',    # NodeMCU v2, ESP32 DevKit
            'FT232',    # Some ESP8266 boards
            'USB-SERIAL CH340',
            'USB2.0-Serial',
            'Silicon Labs CP210x',
            'FTDI'
        ]
        
        for port in ports:
            port_info = {
                'port': port.device,
                'description': port.description,
                'hwid': port.hwid,
                'manufacturer': getattr(port, 'manufacturer', 'Unknown'),
                'likely_esp': False
            }
            
            # Check if this looks like an ESP8266 board
            description_upper = port.description.upper()
            hwid_upper = port.hwid.upper()
            
            for identifier in esp_identifiers:
                if identifier.upper() in description_upper or identifier.upper() in hwid_upper:
                    port_info['likely_esp'] = True
                    break
            
            esp_ports.append(port_info)
        
        # Sort by likelihood of being ESP8266
        esp_ports.sort(key=lambda x: x['likely_esp'], reverse=True)
        return esp_ports
    
    def auto_detect_port(self) -> str:
        """
        Automatically detect ESP8266 port.
        
        Returns:
            Port name (e.g., 'COM3', '/dev/ttyUSB0')
            
        Raises:
            DeviceNotFoundError: If no ESP8266 found
        """
        ports = self.detect_esp8266_ports()
        
        if not ports:
            raise DeviceNotFoundError("No serial ports found")
        
        # Look for likely ESP8266 ports first
        for port in ports:
            if port['likely_esp']:
                return port['port']
        
        # If no likely ESP8266 found, suggest the first port
        raise DeviceNotFoundError(
            f"No ESP8266 detected. Available ports: {[p['port'] for p in ports]}. "
            f"Please specify port manually."
        )
    
    def flash_firmware(self,
                      port: Optional[str] = None,
                      baud_rate: int = DEFAULT_BAUD_RATE,
                      erase_flash: bool = True,
                      verify: bool = True,
                      progress_callback: Optional[callable] = None,
                      use_progress_bar: bool = True) -> bool:
        """
        Flash ESP-Linker firmware to ESP8266.

        Args:
            port: Serial port (auto-detected if None)
            baud_rate: Flash baud rate (default: 460800)
            erase_flash: Whether to erase flash before flashing
            verify: Whether to verify flash after writing
            progress_callback: Callback function for progress updates
            use_progress_bar: Whether to use visual progress bars

        Returns:
            True if successful

        Raises:
            FlashError: If flashing fails
            DeviceNotFoundError: If ESP8266 not found
        """
        try:
            # Initialize progress tracker
            progress = ProgressTracker(use_progress_bar)

            # Auto-detect port if not specified
            if port is None:
                progress.simple_message("[?] Auto-detecting ESP8266...")
                port = self.auto_detect_port()
                progress.simple_message(f"[^] Found ESP8266 on port: {port}")

            # Verify firmware exists
            if not os.path.exists(self.firmware_path):
                raise FlashError(f"Firmware not found: {self.firmware_path}")

            firmware_size = os.path.getsize(self.firmware_path)
            progress.simple_message(f"[+] Firmware size: {firmware_size:,} bytes ({firmware_size/1024:.1f} KB)")
            
            # Try different baud rates if flashing fails
            baud_rates = [baud_rate, 115200, 230400, 921600] if baud_rate != 115200 else [115200, 230400, 460800]

            # Build base esptool command
            base_cmd = [
                sys.executable, "-m", "esptool",
                "--port", port,
                "--chip", "esp8266"
            ]
            
            # Try flashing with different baud rates if needed
            flash_success = False
            last_error = None

            for baud_idx, current_baud in enumerate(baud_rates):
                try:
                    if baud_idx > 0:
                        print(f"[!] Trying lower baud rate: {current_baud}")
                        time.sleep(2)

                    cmd = base_cmd + ["--baud", str(current_baud)]

                    if erase_flash:
                        progress.start_operation("[~] Erasing flash", total=100)

                        erase_cmd = cmd + ["erase_flash"]

                        # Try erase with retry logic
                        max_retries = 2
                        erase_success = False
                        for attempt in range(max_retries):
                            try:
                                if attempt > 0:
                                    print(f"[!] Erase retry {attempt + 1}/{max_retries}")
                                    time.sleep(2)

                                # Run erase with progress simulation
                                process = subprocess.Popen(erase_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                                # Simulate progress for erase (takes about 10-15 seconds)
                                for i in range(100):
                                    if process.poll() is not None:  # Process finished
                                        break
                                    progress.update_progress(1)
                                    time.sleep(0.1)

                                stdout, stderr = process.communicate()

                                if process.returncode == 0:
                                    progress.finish_operation("Flash erased successfully")
                                    erase_success = True
                                    break
                                else:
                                    if attempt == max_retries - 1:
                                        print(f"[!] Erase failed: {stderr.strip()}")
                                        raise Exception(f"Erase failed: {stderr.strip()}")

                            except Exception as e:
                                if attempt == max_retries - 1:
                                    raise e
                                continue

                        if not erase_success:
                            continue  # Try next baud rate

            # Flash firmware
            progress.start_operation("[>] Flashing firmware", total=firmware_size)

            flash_cmd = cmd + [
                "write_flash",
                "--flash_size", self.DEFAULT_FLASH_SIZE,
                "--flash_mode", self.DEFAULT_FLASH_MODE,
                "--flash_freq", self.DEFAULT_FLASH_FREQ,
                self.FLASH_ADDRESS,
                self.firmware_path
            ]

            try:
                # Execute flash command
                result = subprocess.run(flash_cmd, capture_output=True, text=True, timeout=120)

                if result.returncode == 0:
                    # Simulate progress completion
                    progress.update_progress(firmware_size)
                    progress.finish_operation("Firmware flashed successfully!")
                else:
                    progress.current_progress = None
                    raise FlashError(f"Firmware flash failed: {result.stderr.strip()}")

            except subprocess.TimeoutExpired:
                progress.current_progress = None
                raise FlashError("Firmware flash timed out after 120 seconds")
            except Exception as e:
                progress.current_progress = None
                raise FlashError(f"Firmware flash failed: {str(e)}")

            # Wait for ESP8266 to restart with countdown
            progress.simple_message("[.] Waiting for ESP8266 to restart...")
            if use_progress_bar and TQDM_AVAILABLE:
                for i in tqdm(range(30), desc="[~] Restarting", unit="0.1s"):
                    time.sleep(0.1)
            else:
                time.sleep(3)

            progress.simple_message("[*] ESP-Linker firmware installation complete!")
            
            return True
            
        except subprocess.CalledProcessError as e:
            raise FlashError(f"esptool execution failed: {e}")
        except Exception as e:
            raise FlashError(f"Unexpected error during flashing: {e}")
    
    def get_chip_info(self, port: Optional[str] = None) -> Dict[str, Any]:
        """
        Get ESP8266 chip information.
        
        Args:
            port: Serial port (auto-detected if None)
            
        Returns:
            Dictionary with chip information
        """
        try:
            if port is None:
                port = self.auto_detect_port()
            
            cmd = [
                sys.executable, "-m", "esptool",
                "--port", port,
                "--baud", str(self.DEFAULT_BAUD_RATE),
                "chip_id"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise FlashError(f"Failed to get chip info: {result.stderr}")
            
            # Parse output for chip information
            output = result.stdout
            chip_info = {
                'port': port,
                'chip_type': 'ESP8266',
                'raw_output': output
            }
            
            # Extract specific information from output
            lines = output.split('\n')
            for line in lines:
                if 'Chip ID:' in line:
                    chip_info['chip_id'] = line.split(':')[1].strip()
                elif 'MAC:' in line:
                    chip_info['mac_address'] = line.split(':')[1].strip()
                elif 'Flash size:' in line:
                    chip_info['flash_size'] = line.split(':')[1].strip()
            
            return chip_info
            
        except Exception as e:
            raise FlashError(f"Failed to get chip info: {e}")
    
    def get_firmware_info(self) -> Dict[str, Any]:
        """
        Get information about the bundled firmware.
        
        Returns:
            Dictionary with firmware information
        """
        if not os.path.exists(self.firmware_path):
            raise FlashError("Firmware not found")
        
        stat = os.stat(self.firmware_path)
        
        return {
            'path': self.firmware_path,
            'size': stat.st_size,
            'size_kb': round(stat.st_size / 1024, 1),
            'modified': time.ctime(stat.st_mtime),
            'version': '1.3.3',
            'name': 'ESP-Linker',
            'description': 'ESP-Linker firmware with WiFi configuration and GPIO control'
        }


# Convenience functions
def flash_esp8266(port: Optional[str] = None, 
                  baud_rate: int = ESP8266Flasher.DEFAULT_BAUD_RATE,
                  erase_flash: bool = True,
                  progress_callback: Optional[callable] = None) -> bool:
    """
    Convenience function to flash ESP-Linker firmware.
    
    Args:
        port: Serial port (auto-detected if None)
        baud_rate: Flash baud rate
        erase_flash: Whether to erase flash first
        progress_callback: Progress callback function
        
    Returns:
        True if successful
    """
    flasher = ESP8266Flasher()
    return flasher.flash_firmware(port, baud_rate, erase_flash, True, progress_callback)


def detect_esp8266() -> List[Dict[str, str]]:
    """
    Detect connected ESP8266 boards.
    
    Returns:
        List of port information dictionaries
    """
    flasher = ESP8266Flasher()
    return flasher.detect_esp8266_ports()


def get_chip_info(port: Optional[str] = None) -> Dict[str, Any]:
    """
    Get ESP8266 chip information.
    
    Args:
        port: Serial port (auto-detected if None)
        
    Returns:
        Chip information dictionary
    """
    flasher = ESP8266Flasher()
    return flasher.get_chip_info(port)
