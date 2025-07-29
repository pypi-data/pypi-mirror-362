# ESP-Linker: Professional IoT Development Platform

**Transform your ESP8266 into a powerful wireless IoT device with just one line of Python code!**

[![PyPI version](https://img.shields.io/pypi/v/esp-linker?style=for-the-badge&logo=pypi&logoColor=white&color=blue)](https://pypi.org/project/esp-linker)
[![Python versions](https://img.shields.io/pypi/pyversions/esp-linker?style=for-the-badge&logo=python&logoColor=white&color=green)](https://pypi.org/project/esp-linker/)
[![Downloads](https://img.shields.io/pypi/dm/esp-linker?style=for-the-badge&logo=download&logoColor=white&color=orange)](https://pepy.tech/project/esp-linker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[![GitHub stars](https://img.shields.io/github/stars/skr-electronics-lab/esp-linker?style=social)](https://github.com/skr-electronics-lab/esp-linker)
[![YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?style=social&logo=youtube)](https://www.youtube.com/@skr_electronics_lab)
[![Instagram](https://img.shields.io/badge/Instagram-Follow-purple?style=social&logo=instagram)](https://www.instagram.com/skr_electronics_lab)

---

## 🚀 Why ESP-Linker is the Best Choice for IoT Development

**Stop struggling with complex ESP8266 programming!** ESP-Linker is the most user-friendly, professional-grade IoT development platform that transforms your ESP8266 into a powerful wireless device controllable with simple Python commands.

### ❌ Problems with Traditional ESP8266 Development
- **Complex Setup**: Requires Arduino IDE, multiple libraries, and complex C++ code
- **Wired Programming**: Need USB cables and serial connections for every change
- **Limited Functionality**: Basic GPIO control requires writing custom firmware
- **No Remote Access**: Can't control devices from anywhere on your network
- **Steep Learning Curve**: Beginners struggle with low-level programming

### ✅ The ESP-Linker Solution
- **🎯 One-Line Installation**: `pip install esp-linker` - that's it!
- **📡 Wireless Control**: Control GPIO pins over WiFi from anywhere
- **🔧 PyFirmata-Style API**: Familiar Arduino-like commands in Python
- **💾 Built-in Firmware**: 371KB complete firmware included - no Arduino IDE needed
- **🛠️ Professional Tools**: CLI commands, web dashboard, auto-discovery
- **🌐 Cross-Platform**: Works on Windows, Linux, macOS
- **👨‍💻 Beginner-Friendly**: Start coding in minutes, not hours

---

## ⭐ What Makes ESP-Linker Special?

### 🎯 Instant Results - No Complex Setup
```python
# This is ALL you need to control an LED wirelessly!
from esp_linker import connect_auto
board = connect_auto()
board.write(2, 1)  # LED ON - Auto-sets pin mode!
board.write(2, 0)  # LED OFF
```

### 🏢 Complete Professional IoT Platform
- **🔥 Built-in Firmware**: Flash once, use forever (v1.3.0)
- **🔍 Auto-Discovery**: Finds your ESP8266 automatically using mDNS
- **🌐 Web Dashboard**: Modern control panel accessible from any browser
- **⚡ CLI Tools**: 8 professional command-line tools
- **📱 Mobile-Friendly**: Responsive web interface works on phones
- **🔒 Production Ready**: Used in commercial IoT projects worldwide

### 🚀 Advanced Features (v1.3.0)
- **🤖 Auto-Mode Setting**: Pins automatically configured - no manual setup needed
- **🔄 Smart AP Management**: AP mode auto-disables when WiFi connects
- **📊 Real-Time Monitoring**: Live device status and GPIO states
- **🌍 Multi-Device Support**: Control unlimited ESP8266 boards
- **⚡ Ultra-Lightweight Web UI**: Optimized for ESP8266 performance
- **🛡️ Error Recovery**: Auto-retry with exponential backoff

---

## 📋 Complete Step-by-Step Installation Guide

### 🔧 Prerequisites
- **Python 3.7+** installed on your computer
- **ESP8266 board** (NodeMCU, Wemos D1 Mini, or any ESP8266-based board)
- **USB cable** for initial firmware flashing
- **WiFi network** for wireless control

### 📦 Step 1: Install ESP-Linker

```bash
# Install ESP-Linker (includes all dependencies and firmware)
pip install esp-linker

# Verify installation
esp-linker --version
```

**What gets installed:**
- ESP-Linker Python library
- 371KB ESP8266 firmware (v1.3.0)
- esptool for firmware flashing
- zeroconf for auto-discovery
- All required dependencies

### ⚡ Step 2: Flash ESP8266 Firmware

Connect your ESP8266 via USB and flash the firmware:

```bash
# Auto-detect and flash (recommended)
esp-linker flash

# Manual port specification if auto-detect fails
esp-linker flash --port COM3        # Windows
esp-linker flash --port /dev/ttyUSB0 # Linux
esp-linker flash --port /dev/cu.usbserial # macOS

# Custom baud rate (if needed)
esp-linker flash --baud 115200

# Check firmware info
esp-linker flash --firmware-info
```

**What happens during flashing:**
- Auto-detects your ESP8266 board
- Flashes 371KB complete firmware
- Shows progress bars
- Verifies installation
- Sets up mDNS service

### 📡 Step 3: Configure WiFi

```bash
# Interactive WiFi setup wizard (recommended)
esp-linker setup-wifi

# Quick setup with known credentials
esp-linker setup-wifi --ssid "YourWiFi" --password "YourPassword"

# Setup via specific serial port
esp-linker setup-wifi --port COM3
```

**WiFi setup process:**
1. Scans for available networks
2. Shows signal strength for each network
3. Prompts for WiFi password
4. Saves credentials to ESP8266 EEPROM
5. Tests connection
6. Auto-disables AP mode when connected

### 🎯 Step 4: Discover and Connect

```bash
# Find all ESP-Linker devices on your network
esp-linker discover

# Test a specific device
esp-linker test 192.168.1.100
```

### 🚀 Step 5: Start Programming!

```python
from esp_linker import connect_auto

# Method 1: Auto-discovery (easiest)
board = connect_auto()

# Method 2: Manual IP (if you know the IP)
# board = ESPBoard("192.168.1.100")

# Control an LED (auto-sets OUTPUT mode)
board.write(2, 1)    # LED ON
board.write(2, 0)    # LED OFF

# Control PWM (auto-sets PWM mode)
board.pwm(4, 512)    # 50% duty cycle

# Control servo (auto-sets SERVO mode)
board.servo(5, 90)   # 90 degrees

# Read analog input
value = board.read('A0')  # Read analog pin A0
print(f"Analog value: {value}")

# Always close connection
board.close()
```

---

## 🛠️ Complete CLI Commands Reference

ESP-Linker provides 8 professional CLI commands for complete ESP8266 management:

### 1. 🔍 Device Detection
```bash
# Auto-detect connected ESP8266 boards
esp-linker detect

# Example output:
# [+] ESP8266 Found: COM3
#     Description: Silicon Labs CP210x USB to UART Bridge
#     Manufacturer: Silicon Labs
#     VID:PID: 10C4:EA60
```

### 2. ⚡ Firmware Flashing
```bash
# Auto-flash with progress bars (recommended)
esp-linker flash

# Manual port specification
esp-linker flash --port COM3

# Custom baud rate
esp-linker flash --baud 921600

# Show firmware information
esp-linker flash --firmware-info

# Example output:
# [+] Flashing ESP-Linker firmware v1.3.0...
# [████████████████████████████████] 100% (371KB/371KB)
# [+] Firmware flashed successfully!
# [+] Device will restart automatically
```

### 3. 📡 WiFi Configuration
```bash
# Interactive WiFi setup wizard (recommended)
esp-linker setup-wifi

# Quick setup with credentials
esp-linker setup-wifi --ssid "MyWiFi" --password "MyPassword"

# Setup via specific port
esp-linker setup-wifi --port COM3

# Example interactive session:
# [?] Select WiFi network:
# 1. MyHomeWiFi (-45 dBm) [WPA2]
# 2. NeighborWiFi (-67 dBm) [WPA2]
# 3. PublicWiFi (-78 dBm) [Open]
# Enter choice (1-3): 1
# [?] Enter password for 'MyHomeWiFi': ********
# [+] WiFi configured successfully!
# [+] Device IP: 192.168.1.100
```

### 4. 🌐 Device Discovery
```bash
# Find all ESP-Linker devices on network
esp-linker discover

# Set custom timeout
esp-linker discover --timeout 15

# Example output:
# [+] Scanning network for ESP-Linker devices...
# [+] Found 2 ESP-Linker device(s):
# 1. ESP-Linker v1.3.0 at 192.168.1.100 (Living Room)
# 2. ESP-Linker v1.3.0 at 192.168.1.101 (Bedroom)
```

### 5. 🧪 Device Testing
```bash
# Comprehensive device testing
esp-linker test 192.168.1.100

# Test with custom timeout
esp-linker test --ip 192.168.1.100 --timeout 10

# Example test output:
# [+] Testing ESP-Linker device at 192.168.1.100...
# [✓] Device status: OK
# [✓] GPIO pin 2 test: PASS
# [✓] PWM functionality: PASS
# [✓] Servo control: PASS
# [✓] Analog reading: PASS (value: 512)
# [+] All tests passed!
```

### 6. 📋 Device Management
```bash
# List saved devices
esp-linker devices list

# Add a device with friendly name
esp-linker devices add --name "Living Room" --ip 192.168.1.100

# Remove a device
esp-linker devices remove "Living Room"

# Show device details
esp-linker devices info "Living Room"

# Example device list:
# Saved ESP-Linker Devices:
# 1. Living Room (192.168.1.100) - Online
# 2. Bedroom (192.168.1.101) - Offline
# 3. Workshop (192.168.1.102) - Online
```

### 7. 🌐 Web Dashboard
```bash
# Launch web dashboard
esp-linker dashboard

# Custom port
esp-linker dashboard --port 8080

# Custom host (for remote access)
esp-linker dashboard --host 0.0.0.0 --port 5000

# Example output:
# [+] Starting ESP-Linker Dashboard...
# [+] Dashboard running at: http://localhost:5000
# [+] Press Ctrl+C to stop
```

### 8. 📶 WiFi Management
```bash
# Enable AP mode (for configuration)
esp-linker wifi enable-ap --ip 192.168.1.100

# Disable AP mode
esp-linker wifi disable-ap --ip 192.168.1.100

# Check WiFi status
esp-linker wifi status --ip 192.168.1.100

# Example WiFi status:
# WiFi Status for 192.168.1.100:
# - Station Mode: Connected to 'MyHomeWiFi'
# - Station IP: 192.168.1.100
# - Signal Strength: -42 dBm (Excellent)
# - AP Mode: Disabled (auto-disabled when STA connected)
```

---

## 🎓 Complete Programming Tutorial for Beginners

### 🔌 Hardware Setup Guide

**✅ Supported ESP8266 Boards:**
- NodeMCU v1.0 (ESP-12E)
- Wemos D1 Mini
- ESP8266 Development Board
- Adafruit Feather HUZZAH ESP8266
- SparkFun ESP8266 Thing
- Any ESP8266-based board with USB programming

**🔧 Basic Wiring Examples:**
```
ESP8266 Pin  |  Arduino Pin  |  Component
-------------|---------------|------------------
GPIO2 (D4)   |  Digital 2    |  LED + 220Ω Resistor
GPIO4 (D2)   |  Digital 4    |  PWM Device (Motor, LED)
GPIO5 (D1)   |  Digital 5    |  Servo Motor Signal
GPIO12 (D6)  |  Digital 12   |  Button (INPUT_PULLUP)
GPIO13 (D7)  |  Digital 13   |  Relay Module
GPIO14 (D5)  |  Digital 14   |  Sensor Digital Output
A0           |  Analog A0    |  Potentiometer, LDR, etc.
GND          |  GND          |  Common Ground
3V3          |  3.3V         |  Power Supply (3.3V)
VIN          |  5V           |  External 5V Power
```

**⚠️ Important Notes:**
- ESP8266 pins are 3.3V - don't connect 5V directly!
- GPIO2 has built-in LED (inverted: LOW=ON, HIGH=OFF)
- A0 pin reads 0-1024 (0-1V range with voltage divider)
- Use voltage dividers for 5V sensors

### 💻 Software Installation Guide

#### 1. Install Python 3.7+ (if not installed)
```bash
# Check if Python is installed
python --version

# If not installed, download from:
# https://python.org/downloads/
# ✅ Make sure to check "Add Python to PATH" during installation
```

#### 2. Install ESP-Linker
```bash
# Install ESP-Linker (includes all dependencies)
pip install esp-linker

# Verify installation
esp-linker --version
esp-linker --help

# Check installed version in Python
python -c "import esp_linker; print(f'ESP-Linker v{esp_linker.__version__}')"
```

#### 3. Install USB Drivers (if needed)
- **CP210x Driver**: For NodeMCU, Wemos D1 Mini
- **CH340 Driver**: For some ESP8266 clones
- **FTDI Driver**: For FTDI-based ESP8266 boards

Download from manufacturer websites or Windows Update.

### Firmware Flashing Guide

#### 1. Connect Your ESP8266
- Connect ESP8266 to computer via USB cable
- Install drivers if needed (usually CP210x or CH340)

#### 2. Auto-Flash (Recommended)
```bash
# Auto-detect and flash
esp-linker flash

# Manual port specification
esp-linker flash --port COM3        # Windows
esp-linker flash --port /dev/ttyUSB0 # Linux
esp-linker flash --port /dev/cu.usbserial # macOS
```

#### 3. Verify Firmware
```bash
# Check firmware info
esp-linker flash --firmware-info

# Detect ESP8266 boards
esp-linker detect
```

### WiFi Configuration Guide

#### 1. Interactive Setup (Recommended)
```bash
esp-linker setup-wifi
```

Follow the prompts:
1. Select your ESP8266 port
2. Choose WiFi network from scan results
3. Enter WiFi password
4. Test connection

#### 2. Manual Configuration
```bash
# Configure specific network
esp-linker setup-wifi --ssid "YourWiFi" --password "YourPassword"
```

#### 3. Verify Connection
```bash
# Discover devices on network
esp-linker discover
```

---

## 👨‍💻 Complete Programming Guide for Beginners

### 🎯 Connection Methods

#### Method 1: Auto-Discovery (Recommended for Beginners)
```python
from esp_linker import connect_auto

# Automatically finds and connects to your ESP8266
board = connect_auto()
print("✅ Connected to ESP8266!")

# Your code here...

board.close()
```

#### Method 2: Manual IP Connection
```python
from esp_linker import ESPBoard

# Connect using specific IP address
board = ESPBoard("192.168.1.100")  # Replace with your ESP8266's IP
print("✅ Connected to ESP8266!")

# Your code here...

board.close()
```

#### Method 3: Context Manager (Auto-Close)
```python
from esp_linker import ESPBoard

# Automatically closes connection when done
with ESPBoard("192.168.1.100") as board:
    board.write(2, 1)  # LED ON
    # Connection automatically closed when exiting 'with' block
```

### 💡 Basic GPIO Control

#### Digital Output (LED Control)
```python
from esp_linker import connect_auto

board = connect_auto()

# Method 1: Using integers (Arduino style)
board.write(2, 1)    # LED ON (GPIO2)
board.write(2, 0)    # LED OFF

# Method 2: Using boolean values (more readable)
board.write(2, True)   # LED ON
board.write(2, False)  # LED OFF

# Method 3: Multiple LEDs
board.write(2, 1)   # LED 1 ON
board.write(4, 1)   # LED 2 ON
board.write(5, 1)   # LED 3 ON

board.close()
```

#### Digital Input (Button/Switch Reading)
```python
# Read a button connected to GPIO12 (with pull-up resistor)
button_state = board.read(12)

if button_state == 1:
    print("✅ Button pressed!")
    board.write(2, 1)  # Turn on LED when button pressed
else:
    print("❌ Button not pressed")
    board.write(2, 0)  # Turn off LED when button released

# Continuous button monitoring
import time
while True:
    if board.read(12) == 1:  # Button pressed
        board.write(2, 1)    # LED ON
        print("Button pressed - LED ON")
    else:
        board.write(2, 0)    # LED OFF
    time.sleep(0.1)  # Check every 100ms
```

#### Analog Input (Sensor Reading)
```python
# Read analog sensor connected to A0 (0-1024 range)
sensor_value = board.read('A0')

# Convert to voltage (ESP8266 A0 pin: 0-1V range)
voltage = sensor_value * 1.0 / 1024
print(f"Sensor value: {sensor_value}, Voltage: {voltage:.3f}V")

# Convert to percentage
percentage = sensor_value * 100 / 1024
print(f"Sensor reading: {percentage:.1f}%")

# Example: Light sensor (LDR)
light_value = board.read('A0')
if light_value < 300:
    print("🌙 It's dark - turning on lights")
    board.write(2, 1)  # Turn on LED
else:
    print("☀️ It's bright - turning off lights")
    board.write(2, 0)  # Turn off LED
```

### ⚡ PWM Control (Analog Output)

PWM (Pulse Width Modulation) lets you control the "analog" output by rapidly switching between ON and OFF.

#### LED Brightness Control
```python
from esp_linker import connect_auto
import time

board = connect_auto()

# Control LED brightness (0-1023 range)
print("💡 LED Brightness Control Demo")

board.pwm(4, 0)      # 0% brightness (OFF)
print("LED: 0% brightness")
time.sleep(1)

board.pwm(4, 256)    # 25% brightness
print("LED: 25% brightness")
time.sleep(1)

board.pwm(4, 512)    # 50% brightness
print("LED: 50% brightness")
time.sleep(1)

board.pwm(4, 768)    # 75% brightness
print("LED: 75% brightness")
time.sleep(1)

board.pwm(4, 1023)   # 100% brightness (full ON)
print("LED: 100% brightness")

# Smooth fade effect
print("🌟 Smooth fade effect...")
for brightness in range(0, 1024, 10):
    board.pwm(4, brightness)
    time.sleep(0.05)

board.close()
```

#### DC Motor Speed Control
```python
# Control DC motor speed using PWM
print("🚗 Motor Speed Control Demo")

board.pwm(5, 0)      # Motor stopped
print("Motor: Stopped")
time.sleep(2)

board.pwm(5, 300)    # Slow speed (~30%)
print("Motor: Slow speed")
time.sleep(2)

board.pwm(5, 600)    # Medium speed (~60%)
print("Motor: Medium speed")
time.sleep(2)

board.pwm(5, 1023)   # Full speed (100%)
print("Motor: Full speed")
time.sleep(2)

board.pwm(5, 0)      # Stop motor
print("Motor: Stopped")
```

#### Fan Speed Control with Temperature
```python
# Automatic fan control based on temperature sensor
def auto_fan_control():
    while True:
        # Read temperature from analog sensor (e.g., LM35)
        temp_reading = board.read('A0')
        # Convert to temperature (adjust formula for your sensor)
        temperature = temp_reading * 100 / 1024  # Example conversion

        print(f"🌡️ Temperature: {temperature:.1f}°C")

        if temperature > 30:
            board.pwm(4, 1023)  # Fan full speed
            print("🌪️ Fan: Full speed")
        elif temperature > 25:
            board.pwm(4, 512)   # Fan half speed
            print("💨 Fan: Half speed")
        elif temperature > 20:
            board.pwm(4, 256)   # Fan low speed
            print("🍃 Fan: Low speed")
        else:
            board.pwm(4, 0)     # Fan off
            print("⭕ Fan: Off")

        time.sleep(5)  # Check every 5 seconds

# auto_fan_control()  # Uncomment to run
```

### 🎛️ Servo Motor Control

Servo motors can be positioned precisely from 0° to 180°.

#### Basic Servo Control
```python
from esp_linker import connect_auto
import time

board = connect_auto()

print("🎯 Servo Control Demo")

# Control servo position (0-180 degrees)
board.servo(5, 0)     # Minimum position (0°)
print("Servo: 0° (minimum)")
time.sleep(1)

board.servo(5, 90)    # Center position (90°)
print("Servo: 90° (center)")
time.sleep(1)

board.servo(5, 180)   # Maximum position (180°)
print("Servo: 180° (maximum)")
time.sleep(1)

board.close()
```

#### Servo Sweep Animation
```python
import time

print("🔄 Servo Sweep Demo")

# Sweep servo from 0° to 180°
print("Sweeping 0° → 180°...")
for angle in range(0, 181, 10):
    board.servo(5, angle)
    print(f"Servo: {angle}°")
    time.sleep(0.2)

# Sweep servo from 180° to 0°
print("Sweeping 180° → 0°...")
for angle in range(180, -1, -10):
    board.servo(5, angle)
    print(f"Servo: {angle}°")
    time.sleep(0.2)

print("✅ Sweep complete!")
```

#### Interactive Servo Control
```python
# Control servo with user input
def interactive_servo():
    print("🎮 Interactive Servo Control")
    print("Enter angles (0-180) or 'q' to quit:")

    while True:
        user_input = input("Enter angle: ").strip()

        if user_input.lower() == 'q':
            break

        try:
            angle = int(user_input)
            if 0 <= angle <= 180:
                board.servo(5, angle)
                print(f"✅ Servo moved to {angle}°")
            else:
                print("❌ Angle must be between 0 and 180")
        except ValueError:
            print("❌ Please enter a valid number")

    print("👋 Goodbye!")

# interactive_servo()  # Uncomment to run
```

---

## 🏗️ Real-World Project Examples

### 🏠 Project 1: Smart Home Lighting System
```python
"""
Smart Home Lighting with ESP-Linker
- Automatic lighting based on time and light sensor
- Manual override with button
- Remote control via Python
"""
import time
import datetime
from esp_linker import connect_auto

class SmartLighting:
    def __init__(self):
        self.board = connect_auto()
        self.living_room_light = 2  # GPIO2
        self.bedroom_light = 4      # GPIO4
        self.light_sensor = 'A0'    # Light sensor
        self.manual_button = 12     # Manual override button
        self.auto_mode = True

        print("🏠 Smart Home Lighting System Started")

    def read_light_level(self):
        """Read ambient light level (0-100%)"""
        reading = self.board.read(self.light_sensor)
        light_percentage = reading * 100 / 1024
        return light_percentage

    def control_lights(self):
        """Main lighting control logic"""
        if not self.auto_mode:
            return

        light_level = self.read_light_level()
        current_hour = datetime.datetime.now().hour

        if light_level < 30 or 18 <= current_hour <= 23:
            # Evening: Bright lights
            self.board.pwm(self.living_room_light, 800)
            self.board.pwm(self.bedroom_light, 600)
            print(f"🌆 Evening mode - Lights ON")
        elif current_hour >= 23 or current_hour <= 6:
            # Night: Dim lights
            self.board.pwm(self.living_room_light, 200)
            self.board.pwm(self.bedroom_light, 100)
            print(f"🌙 Night mode - Dim lights")
        else:
            # Day: Lights off
            self.board.pwm(self.living_room_light, 0)
            self.board.pwm(self.bedroom_light, 0)
            print(f"☀️ Day mode - Lights OFF")

    def run(self):
        """Main loop"""
        try:
            while True:
                self.control_lights()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n👋 Smart Lighting stopped")
            self.board.close()

# Usage
smart_lights = SmartLighting()
smart_lights.run()
```

### 🌱 Project 2: Smart Garden System
```python
"""
Smart Garden with ESP-Linker
- Monitors soil moisture
- Automatic watering
- Status indicators
"""
import time
from esp_linker import connect_auto

class SmartGarden:
    def __init__(self):
        self.board = connect_auto()
        self.water_pump = 2         # Water pump relay
        self.soil_sensor = 'A0'     # Soil moisture sensor
        self.status_led = 4         # Status LED
        self.dry_threshold = 300    # Moisture threshold

        print("🌱 Smart Garden System Started")

    def read_soil_moisture(self):
        """Read soil moisture level"""
        reading = self.board.read(self.soil_sensor)
        moisture_percent = (1024 - reading) * 100 / 1024
        return reading, moisture_percent

    def water_plants(self, duration=10):
        """Water plants for specified duration"""
        print(f"💧 Watering for {duration} seconds...")
        self.board.write(self.water_pump, 1)

        # Blink LED while watering
        for i in range(duration):
            self.board.write(self.status_led, 1)
            time.sleep(0.5)
            self.board.write(self.status_led, 0)
            time.sleep(0.5)

        self.board.write(self.water_pump, 0)
        print("✅ Watering completed")

    def monitor_garden(self):
        """Main monitoring function"""
        moisture_raw, moisture_percent = self.read_soil_moisture()
        print(f"🌱 Soil moisture: {moisture_percent:.1f}%")

        if moisture_raw < self.dry_threshold:
            print("🚨 Soil is dry - watering needed!")
            self.water_plants()
        else:
            print("✅ Soil moisture OK")
            self.board.write(self.status_led, 1)  # Solid LED = OK

    def run(self):
        """Main loop"""
        try:
            while True:
                self.monitor_garden()
                time.sleep(3600)  # Check every hour
        except KeyboardInterrupt:
            print("\n👋 Smart Garden stopped")
            self.board.close()

# Usage
garden = SmartGarden()
garden.run()
```

### 🔒 Project 3: Security System
```python
"""
Simple Security System with ESP-Linker
- Motion detection
- Alarm system
- Remote monitoring
"""
import time
from esp_linker import connect_auto

class SecuritySystem:
    def __init__(self):
        self.board = connect_auto()
        self.motion_sensor = 12     # PIR motion sensor
        self.alarm_led = 2          # Alarm LED
        self.buzzer = 4             # Alarm buzzer
        self.status_led = 5         # System status LED
        self.armed = False

        print("🔒 Security System Started")

    def arm_system(self):
        """Arm the security system"""
        self.armed = True
        self.board.write(self.status_led, 1)
        print("🛡️ Security system ARMED")

    def disarm_system(self):
        """Disarm the security system"""
        self.armed = False
        self.board.write(self.status_led, 0)
        self.board.write(self.alarm_led, 0)
        self.board.write(self.buzzer, 0)
        print("🔓 Security system DISARMED")

    def trigger_alarm(self):
        """Trigger security alarm"""
        print("🚨 MOTION DETECTED! ALARM TRIGGERED!")

        # Sound alarm for 30 seconds
        for _ in range(60):  # 30 seconds (0.5s intervals)
            self.board.write(self.alarm_led, 1)
            self.board.write(self.buzzer, 1)
            time.sleep(0.25)
            self.board.write(self.alarm_led, 0)
            self.board.write(self.buzzer, 0)
            time.sleep(0.25)

    def monitor(self):
        """Main monitoring loop"""
        print("👁️ Monitoring for motion...")

        try:
            while True:
                if self.armed:
                    motion = self.board.read(self.motion_sensor)

                    if motion == 1:  # Motion detected
                        self.trigger_alarm()
                        self.disarm_system()  # Auto-disarm after alarm

                        # Wait for manual re-arming
                        input("Press Enter to re-arm system...")
                        self.arm_system()

                time.sleep(0.5)  # Check every 500ms

        except KeyboardInterrupt:
            print("\n👋 Security system stopped")
            self.disarm_system()
            self.board.close()

# Usage
security = SecuritySystem()
security.arm_system()
security.monitor()
```

---

### 🎓 Advanced Programming Examples

#### Blinking LED Pattern
```python
import time

def blink_pattern(pin, pattern, delay=0.5):
    """
    Blink LED in a specific pattern
    pattern: list of 1s and 0s (1=ON, 0=OFF)
    """
    for state in pattern:
        board.write(pin, state)
        time.sleep(delay)

# SOS pattern in Morse code
sos_pattern = [1,0,1,0,1,0,0,1,1,1,0,1,1,1,0,1,1,1,0,0,1,0,1,0,1]
blink_pattern(2, sos_pattern, 0.2)
```

#### Temperature-Controlled Fan
```python
def auto_fan_control():
    """
    Automatically control fan based on temperature
    """
    while True:
        # Read temperature sensor (assuming LM35)
        temp_reading = board.read('A0')
        temperature = (temp_reading * 3.3 / 1024) * 100  # Convert to Celsius
        
        if temperature > 30:
            board.pwm(4, 1023)  # Fan full speed
        elif temperature > 25:
            board.pwm(4, 512)   # Fan half speed
        else:
            board.pwm(4, 0)     # Fan off
        
        print(f"Temperature: {temperature:.1f}°C")
        time.sleep(2)

auto_fan_control()
```

#### Smart Home Light Controller
```python
import datetime

def smart_lighting():
    """
    Automatic lighting based on time of day
    """
    current_hour = datetime.datetime.now().hour
    
    if 6 <= current_hour <= 8:      # Morning
        board.pwm(2, 300)            # Dim light
    elif 18 <= current_hour <= 22:  # Evening
        board.pwm(2, 800)            # Bright light
    elif 22 <= current_hour or current_hour <= 6:  # Night
        board.pwm(2, 100)            # Very dim
    else:                            # Day
        board.pwm(2, 0)              # Off

smart_lighting()
```

---

## Complete CLI Commands Reference

ESP-Linker provides 8 professional CLI commands for complete ESP8266 management:

### 1. Device Detection
```bash
# Auto-detect ESP8266 boards
esp-linker detect

# Example output:
# [+] ESP8266 Found: COM3
#     Description: Silicon Labs CP210x USB to UART Bridge
#     Manufacturer: Silicon Labs
```

### 2. Firmware Flashing
```bash
# Auto-flash with progress bars
esp-linker flash

# Specify port manually
esp-linker flash --port COM3

# Use different baud rate
esp-linker flash --baud 115200

# Show firmware information
esp-linker flash --firmware-info
```

### 3. WiFi Configuration
```bash
# Interactive WiFi setup wizard
esp-linker setup-wifi

# Quick setup with credentials
esp-linker setup-wifi --ssid "MyWiFi" --password "MyPassword"

# Setup via serial port
esp-linker setup-wifi --port COM3
```

### 4. Device Discovery
```bash
# Find all ESP-Linker devices on network
esp-linker discover

# Set custom timeout
esp-linker discover --timeout 15

# Example output:
# [+] Found 2 ESP-Linker device(s):
# 1. ESP-Linker v1.3.0 at 192.168.1.100
# 2. ESP-Linker v1.3.0 at 192.168.1.101
```

### 5. Device Testing
```bash
# Comprehensive device testing
esp-linker test 192.168.1.100

# Test specific IP address
esp-linker test --ip 192.168.1.100

# The test includes:
# - Device status verification
# - GPIO pin testing
# - PWM functionality
# - Servo control
# - Analog reading
```

### 6. Device Management
```bash
# List saved devices
esp-linker devices list

# Add a device
esp-linker devices add --name "Living Room" --ip 192.168.1.100

# Remove a device
esp-linker devices remove "Living Room"

# Show device details
esp-linker devices info "Living Room"
```

### 7. Web Dashboard
```bash
# Launch web dashboard
esp-linker dashboard

# Custom port
esp-linker dashboard --port 8080

# Access at: http://localhost:5000
```

### 8. WiFi Management
```bash
# Enable AP mode (for configuration)
esp-linker wifi enable-ap --ip 192.168.1.100

# Disable AP mode
esp-linker wifi disable-ap --ip 192.168.1.100

# Check WiFi status
esp-linker wifi status --ip 192.168.1.100
```

---

## Python API Reference

### Connection Methods

#### Auto-Discovery (Recommended)
```python
from esp_linker import connect_auto

# Automatically find and connect to ESP8266
board = connect_auto()

# With timeout
board = connect_auto(timeout=15)
```

#### Manual IP Connection
```python
from esp_linker import ESPBoard

# Connect to specific IP
board = ESPBoard("192.168.1.100")

# With custom timeout
board = ESPBoard("192.168.1.100", timeout=10)
```

#### Context Manager (Recommended)
```python
# Automatically closes connection
with ESPBoard("192.168.1.100") as board:
    board.write(2, 1)
    # Connection automatically closed
```

### GPIO Control Methods

#### Digital I/O
```python
# Set pin mode (optional - auto-set by default)
board.set_mode(2, 'OUTPUT')  # For digital output
board.set_mode(3, 'INPUT')   # For digital input

# Digital write (auto-sets OUTPUT mode)
board.write(2, 1)      # HIGH
board.write(2, 0)      # LOW
board.write(2, True)   # HIGH (boolean)
board.write(2, False)  # LOW (boolean)

# Digital read
value = board.read(3)  # Returns 0 or 1
```

#### PWM Control
```python
# PWM output (auto-sets PWM mode)
board.pwm(4, 512)    # 50% duty cycle (0-1023 range)
board.pwm(4, 0)      # 0% (OFF)
board.pwm(4, 1023)   # 100% (full ON)

# Calculate percentage
percentage = 75
pwm_value = int(percentage * 1023 / 100)
board.pwm(4, pwm_value)
```

#### Servo Control
```python
# Servo control (auto-sets SERVO mode)
board.servo(5, 90)   # 90 degrees (0-180 range)
board.servo(5, 0)    # Minimum angle
board.servo(5, 180)  # Maximum angle
```

#### Analog Input
```python
# Read analog pin A0 (0-1024 range)
value = board.read('A0')

# Convert to voltage (ESP8266 = 3.3V max)
voltage = value * 3.3 / 1024

# Convert to percentage
percentage = value * 100 / 1024
```

---

## 🔧 Troubleshooting Guide

### ❌ Common Issues and Solutions

#### 1. "No ESP8266 boards detected"
```bash
# Problem: esp-linker detect shows no devices
# Solutions:
1. Check USB cable connection
2. Install USB drivers (CP210x or CH340)
3. Try different USB port
4. Specify port manually: esp-linker flash --port COM3
```

#### 2. "Failed to connect to ESP8266"
```bash
# Problem: Can't connect to device IP
# Solutions:
1. Check WiFi connection: esp-linker wifi status --ip YOUR_IP
2. Verify device is on same network
3. Try auto-discovery: esp-linker discover
4. Check firewall settings
5. Restart ESP8266: esp-linker restart --ip YOUR_IP
```

#### 3. "Pin not set to OUTPUT mode" (v1.2.1 and earlier)
```python
# Problem: GPIO error when using write()
# Solution: Update to v1.3.0 or set pin mode manually
board.set_mode(2, 'OUTPUT')  # Set pin mode first
board.write(2, 1)            # Then write value

# Or update ESP-Linker:
# pip install --upgrade esp-linker
```

#### 4. "Device not found during discovery"
```bash
# Problem: esp-linker discover finds no devices
# Solutions:
1. Ensure ESP8266 is connected to WiFi
2. Check if on same network subnet
3. Disable VPN if active
4. Try manual IP: esp-linker test --ip 192.168.1.100
5. Check router's connected devices list
```

#### 5. "Firmware flashing failed"
```bash
# Problem: Flashing fails or times out
# Solutions:
1. Hold BOOT button during flashing (some boards)
2. Try lower baud rate: esp-linker flash --baud 115200
3. Use different USB cable
4. Close other serial programs (Arduino IDE, etc.)
5. Try different USB port
```

### 🔍 Diagnostic Commands

```bash
# Check ESP-Linker installation
esp-linker --version
python -c "import esp_linker; print('✅ ESP-Linker installed')"

# Test device connection
esp-linker test 192.168.1.100

# Check device status
esp-linker wifi status --ip 192.168.1.100

# Scan for devices
esp-linker discover --timeout 30

# Check serial ports
esp-linker detect
```

### 📊 Performance Tips

#### For ESP8266 Optimization:
- **Use auto-mode**: Let ESP-Linker set pin modes automatically
- **Batch operations**: Use `board.batch()` for multiple GPIO operations
- **Connection pooling**: Reuse board connections instead of creating new ones
- **Timeout settings**: Adjust timeouts for slow networks

```python
# Optimized code example
with ESPBoard("192.168.1.100", timeout=15) as board:
    # Batch multiple operations
    operations = [
        {'type': 'write', 'pin': 2, 'value': 1},
        {'type': 'pwm', 'pin': 4, 'value': 512},
        {'type': 'servo', 'pin': 5, 'angle': 90}
    ]
    board.batch(operations)
```

---

## 📚 API Reference Summary

### 🔌 Connection Classes
```python
# Auto-discovery connection
board = connect_auto(timeout=10)

# Manual IP connection
board = ESPBoard("192.168.1.100", timeout=10)

# Context manager (auto-close)
with ESPBoard("192.168.1.100") as board:
    # Your code here
```

### 🎛️ GPIO Control Methods
```python
# Digital I/O
board.write(pin, value, auto_mode=True)    # Digital write
board.read(pin)                            # Digital/analog read
board.set_mode(pin, mode)                  # Set pin mode manually

# PWM Control
board.pwm(pin, value, auto_mode=True)      # PWM output (0-1023)

# Servo Control
board.servo(pin, angle, auto_mode=True)    # Servo angle (0-180)

# Device Information
board.status()                             # Device status
board.capabilities()                       # Pin capabilities
board.ping()                              # Test connection
board.close()                             # Close connection
```

### 📡 Supported Pin Modes
- **INPUT**: Digital input reading
- **OUTPUT**: Digital output writing
- **PWM**: Pulse Width Modulation output
- **SERVO**: Servo motor control

### 📍 ESP8266 Pin Reference
```
GPIO Pin | NodeMCU Pin | Function
---------|-------------|----------
GPIO0    | D3          | Digital I/O
GPIO2    | D4          | Digital I/O, Built-in LED
GPIO4    | D2          | Digital I/O, PWM
GPIO5    | D1          | Digital I/O, PWM
GPIO12   | D6          | Digital I/O, PWM
GPIO13   | D7          | Digital I/O, PWM
GPIO14   | D5          | Digital I/O, PWM
GPIO15   | D8          | Digital I/O, PWM
GPIO16   | D0          | Digital I/O (no PWM)
A0       | A0          | Analog Input (0-1024)
```

---

## 🆘 Support and Community

### 📞 Get Help
- **📧 Email**: [skrelectronicslab@gmail.com](mailto:skrelectronicslab@gmail.com)
- **🌐 Website**: [www.skrelectronicslab.com](https://www.skrelectronicslab.com)
- **📺 YouTube**: [SKR Electronics Lab](https://www.youtube.com/@skr_electronics_lab)
- **📱 Instagram**: [@skr_electronics_lab](https://www.instagram.com/skr_electronics_lab)
- **☕ Support**: [Buy me a coffee](https://buymeacoffee.com/skrelectronics)

### 🐛 Report Issues
Found a bug? Have a feature request? Please report it!

### 🤝 Contributing
ESP-Linker is open source! Contributions are welcome.

### 📄 License
ESP-Linker is released under the MIT License.

---

## 🎉 What's New in v1.3.0

### ✨ New Features
- **🤖 Auto-Mode Setting**: Pins automatically configured - no manual setup needed
- **🔄 Smart AP Management**: AP mode auto-disables when WiFi connects
- **⚡ Ultra-Lightweight Web UI**: Optimized for ESP8266 performance
- **📊 Enhanced Dashboard**: Modern, responsive web interface
- **🛡️ Better Error Handling**: Improved error messages and recovery

### 🔧 Improvements
- **📱 Mobile-Friendly**: Web interfaces work perfectly on phones
- **🚀 Performance**: Faster GPIO operations and reduced memory usage
- **🎯 User Experience**: More intuitive CLI commands and better documentation
- **🔒 Stability**: Enhanced connection reliability and error recovery

### 🆕 New CLI Commands
```bash
esp-linker wifi enable-ap    # Enable AP mode manually
esp-linker wifi disable-ap   # Disable AP mode
esp-linker wifi status       # Check WiFi status
```

---

**🚀 Ready to start your IoT journey? Install ESP-Linker now and transform your ESP8266 into a powerful wireless device!**

```bash
pip install esp-linker
```

*Made with ❤️ by [SK Raihan](https://www.skrelectronicslab.com) / SKR Electronics Lab*
