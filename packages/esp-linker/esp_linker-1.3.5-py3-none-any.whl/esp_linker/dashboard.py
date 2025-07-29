"""
ESP-Linker Web Dashboard
(c) 2025 SK Raihan / SKR Electronics Lab

Simple web dashboard for monitoring and controlling ESP-Linker devices.
"""

import json
import threading
import webbrowser
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

try:
    from flask import Flask, render_template_string, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from .device_manager import get_device_manager
from .espboard import ESPBoard


class Dashboard:
    """Simple web dashboard for ESP-Linker devices"""
    
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.port = port
        self.app = None
        self.manager = get_device_manager()
        
        if not FLASK_AVAILABLE:
            raise ImportError("Flask is required for the dashboard. Install with: pip install flask")
    
    def create_app(self):
        """Create Flask application"""
        self.app = Flask(__name__)
        
        # Main dashboard page
        @self.app.route('/')
        def dashboard():
            return render_template_string(DASHBOARD_HTML)
        
        # API endpoints
        @self.app.route('/api/devices')
        def api_devices():
            devices = self.manager.list_devices()
            return jsonify([device.to_dict() for device in devices])
        
        @self.app.route('/api/devices/discover', methods=['POST'])
        def api_discover():
            try:
                new_devices = self.manager.discover_and_add_devices()
                return jsonify({
                    'success': True,
                    'new_devices': len(new_devices),
                    'devices': [device.to_dict() for device in new_devices]
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/devices/<device_ip>/status')
        def api_device_status(device_ip):
            try:
                device = self.manager.get_device(device_ip)
                if not device:
                    return jsonify({'error': 'Device not found'}), 404
                
                board = ESPBoard(ip=device.ip, timeout=3)
                status = board.status()
                board.close()
                
                return jsonify(status)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/devices/<device_ip>/gpio', methods=['POST'])
        def api_gpio_control(device_ip):
            try:
                device = self.manager.get_device(device_ip)
                if not device:
                    return jsonify({'error': 'Device not found'}), 404
                
                data = request.json
                action = data.get('action')
                pin = data.get('pin')
                value = data.get('value')
                
                board = ESPBoard(ip=device.ip, timeout=3)
                
                if action == 'write':
                    board.write(pin, value)
                elif action == 'read':
                    value = board.read(pin)
                elif action == 'pwm':
                    board.pwm(pin, value)
                
                board.close()
                
                return jsonify({'success': True, 'value': value})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/statistics')
        def api_statistics():
            stats = self.manager.get_statistics()
            return jsonify(stats)
        
        return self.app
    
    def run(self, debug: bool = False, open_browser: bool = True):
        """Run the dashboard server"""
        if not self.app:
            self.create_app()
        
        if open_browser:
            # Open browser after a short delay
            def open_browser_delayed():
                import time
                time.sleep(1)
                webbrowser.open(f'http://{self.host}:{self.port}')
            
            threading.Thread(target=open_browser_delayed, daemon=True).start()
        
        print(f"[*] ESP-Linker Dashboard starting at http://{self.host}:{self.port}")
        print("Press Ctrl+C to stop the dashboard")
        
        try:
            self.app.run(host=self.host, port=self.port, debug=debug)
        except KeyboardInterrupt:
            print("\n[!] Dashboard stopped")


# HTML template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP-Linker Dashboard</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo i {
            font-size: 2em;
            color: #667eea;
        }

        .logo h1 {
            font-size: 1.8em;
            font-weight: 700;
            color: #2d3748;
        }

        .header-stats {
            display: flex;
            gap: 20px;
            align-items: center;
        }

        .header-stat {
            text-align: center;
            padding: 8px 16px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 8px;
        }

        .header-stat-number {
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
        }

        .header-stat-label {
            font-size: 0.8em;
            color: #718096;
        }

        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            margin: 20px 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 2px solid #f7fafc;
        }

        .card-title {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.3em;
            font-weight: 600;
            color: #2d3748;
        }

        .card-title i {
            color: #667eea;
        }

        .device-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }

        .device-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .device-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }

        .device-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }

        .device-card.online::before { background: linear-gradient(90deg, #48bb78, #38a169); }
        .device-card.offline::before { background: linear-gradient(90deg, #f56565, #e53e3e); }

        .device-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .device-name {
            font-size: 1.1em;
            font-weight: 600;
            color: #2d3748;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
        }

        .status-online {
            background: linear-gradient(135deg, #48bb78, #38a169);
            color: white;
        }

        .status-offline {
            background: linear-gradient(135deg, #f56565, #e53e3e);
            color: white;
        }

        .device-info {
            margin: 12px 0;
            font-size: 0.9em;
            color: #718096;
        }

        .device-info div {
            margin: 4px 0;
        }

        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }

        .btn-success {
            background: linear-gradient(135deg, #48bb78, #38a169);
        }

        .btn-success:hover {
            box-shadow: 0 4px 16px rgba(72, 187, 120, 0.3);
        }

        .btn-control {
            background: linear-gradient(135deg, #4299e1, #3182ce);
            padding: 6px 12px;
            font-size: 0.8em;
            margin: 2px;
        }

        .btn-control:hover {
            box-shadow: 0 2px 8px rgba(66, 153, 225, 0.3);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .stat-card {
            text-align: center;
            padding: 24px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }

        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 12px;
            opacity: 0.9;
        }

        .stat-number {
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            font-weight: 500;
        }

        .gpio-controls {
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid #e2e8f0;
        }

        .gpio-control {
            margin: 6px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .gpio-label {
            font-size: 0.9em;
            color: #4a5568;
            font-weight: 500;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #718096;
            font-size: 1.1em;
        }

        .loading i {
            font-size: 2em;
            margin-bottom: 12px;
            color: #667eea;
            animation: spin 2s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error {
            background: linear-gradient(135deg, #f56565, #e53e3e);
            color: white;
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }

        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 16px;
            }

            .header-stats {
                flex-wrap: wrap;
                justify-content: center;
            }

            .device-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <i class="fas fa-microchip"></i>
                <h1>ESP-Linker Dashboard</h1>
            </div>
            <div class="header-stats">
                <div class="header-stat">
                    <div class="header-stat-number" id="total-devices">0</div>
                    <div class="header-stat-label">Total Devices</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-number" id="online-devices">0</div>
                    <div class="header-stat-label">Online</div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="card">
            <div class="card-header">
                <div class="card-title">
                    <i class="fas fa-chart-bar"></i>
                    System Statistics
                </div>
            </div>
            <div id="statistics" class="stats">
                <div class="loading">
                    <i class="fas fa-spinner"></i>
                    <div>Loading statistics...</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">
                    <i class="fas fa-wifi"></i>
                    Connected Devices
                </div>
                <button class="btn btn-success" onclick="discoverDevices()">
                    <i class="fas fa-search"></i>
                    Discover Devices
                </button>
            </div>
            <div id="devices" class="device-grid">
                <div class="loading">
                    <i class="fas fa-spinner"></i>
                    <div>Scanning for devices...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let devices = [];

        async function loadStatistics() {
            try {
                const response = await fetch('/api/statistics');
                const stats = await response.json();

                // Update header stats
                document.getElementById('total-devices').textContent = stats.total_devices;
                document.getElementById('online-devices').textContent = stats.online_devices;

                document.getElementById('statistics').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-microchip"></i></div>
                        <div class="stat-number">${stats.total_devices}</div>
                        <div class="stat-label">Total Devices</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-wifi"></i></div>
                        <div class="stat-number">${stats.online_devices}</div>
                        <div class="stat-label">Online Devices</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-exclamation-triangle"></i></div>
                        <div class="stat-number">${stats.offline_devices}</div>
                        <div class="stat-label">Offline Devices</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon"><i class="fas fa-clock"></i></div>
                        <div class="stat-number">${Math.round(stats.uptime / 60)}m</div>
                        <div class="stat-label">Dashboard Uptime</div>
                    </div>
                `;
            } catch (error) {
                document.getElementById('statistics').innerHTML = '<div class="error"><i class="fas fa-exclamation-circle"></i> Error loading statistics</div>';
            }
        }

        async function loadDevices() {
            try {
                const response = await fetch('/api/devices');
                devices = await response.json();

                if (devices.length === 0) {
                    document.getElementById('devices').innerHTML = `
                        <div class="loading">
                            <i class="fas fa-search"></i>
                            <div>No devices found. Click "Discover Devices" to scan your network.</div>
                        </div>
                    `;
                    return;
                }

                const devicesHtml = devices.map(device => `
                    <div class="device-card ${device.status}">
                        <div class="device-header">
                            <div class="device-name">${device.name}</div>
                            <span class="status-badge status-${device.status}">
                                <i class="fas fa-${device.status === 'online' ? 'wifi' : 'times-circle'}"></i>
                                ${device.status.toUpperCase()}
                            </span>
                        </div>

                        <div class="device-info">
                            <div><i class="fas fa-network-wired"></i> <strong>IP:</strong> ${device.ip}</div>
                            <div><i class="fas fa-code"></i> <strong>Firmware:</strong> ${device.firmware_name} v${device.firmware_version}</div>
                            <div><i class="fas fa-clock"></i> <strong>Last Seen:</strong> ${new Date(device.last_seen).toLocaleString()}</div>
                            <div><i class="fas fa-memory"></i> <strong>Memory:</strong> ${device.free_memory || 'N/A'} KB free</div>
                        </div>

                        <div class="gpio-controls">
                            <div class="gpio-control">
                                <span class="gpio-label">LED Control (Pin 2)</span>
                                <button class="btn btn-control" onclick="toggleLED('${device.ip}')">
                                    <i class="fas fa-lightbulb"></i> Toggle
                                </button>
                            </div>
                            <div class="gpio-control">
                                <span class="gpio-label">PWM Test (Pin 4)</span>
                                <button class="btn btn-control" onclick="testPWM('${device.ip}')">
                                    <i class="fas fa-sliders-h"></i> Test PWM
                                </button>
                            </div>
                            <div class="gpio-control">
                                <span class="gpio-label">Device Status</span>
                                <button class="btn btn-control" onclick="getStatus('${device.ip}')">
                                    <i class="fas fa-info-circle"></i> Status
                                </button>
                            </div>
                            <div class="gpio-control">
                                <span class="gpio-label">Analog Reading</span>
                                <button class="btn btn-control" onclick="readAnalog('${device.ip}')">
                                    <i class="fas fa-chart-line"></i> Read A0
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('');

                document.getElementById('devices').innerHTML = devicesHtml;
            } catch (error) {
                document.getElementById('devices').innerHTML = '<div class="error"><i class="fas fa-exclamation-circle"></i> Error loading devices</div>';
            }
        }
        
        async function discoverDevices() {
            const button = event.target;
            const originalHTML = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Discovering...';

            try {
                const response = await fetch('/api/devices/discover', { method: 'POST' });
                const result = await response.json();

                if (result.success) {
                    showNotification(`Discovery complete! Found ${result.new_devices} new device(s).`, 'success');
                    await loadDevices();
                    await loadStatistics();
                } else {
                    showNotification(`Discovery failed: ${result.error}`, 'error');
                }
            } catch (error) {
                showNotification(`Discovery error: ${error.message}`, 'error');
            } finally {
                button.disabled = false;
                button.innerHTML = originalHTML;
            }
        }

        async function toggleLED(deviceIP) {
            try {
                // Use auto-mode setting (ESP-Linker v1.2.2+)
                const response = await fetch(`/api/devices/${deviceIP}/gpio`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        action: 'write',
                        pin: 2,
                        value: Math.random() > 0.5 ? 0 : 1,
                        auto_mode: true
                    })
                });

                if (response.ok) {
                    const result = await response.json();
                    showNotification(`LED toggled! Pin 2 = ${result.value}`, 'success');
                } else {
                    showNotification('Failed to toggle LED', 'error');
                }
            } catch (error) {
                showNotification(`Error: ${error.message}`, 'error');
            }
        }

        async function testPWM(deviceIP) {
            try {
                // Test PWM with 50% duty cycle
                const response = await fetch(`/api/devices/${deviceIP}/gpio`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        action: 'pwm',
                        pin: 4,
                        value: 512,
                        auto_mode: true
                    })
                });

                if (response.ok) {
                    showNotification('PWM test successful! Pin 4 = 50% duty cycle', 'success');
                } else {
                    showNotification('PWM test failed', 'error');
                }
            } catch (error) {
                showNotification(`Error: ${error.message}`, 'error');
            }
        }

        async function readAnalog(deviceIP) {
            try {
                const response = await fetch(`/api/devices/${deviceIP}/gpio`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        action: 'read',
                        pin: 'A0'
                    })
                });

                if (response.ok) {
                    const result = await response.json();
                    const voltage = (result.value * 3.3 / 1024).toFixed(2);
                    showNotification(`Analog reading: ${result.value} (${voltage}V)`, 'info');
                } else {
                    showNotification('Failed to read analog pin', 'error');
                }
            } catch (error) {
                showNotification(`Error: ${error.message}`, 'error');
            }
        }
        
        async function getStatus(deviceIP) {
            try {
                const response = await fetch(`/api/devices/${deviceIP}/status`);
                const status = await response.json();

                if (response.ok) {
                    const uptime = Math.round(status.uptime / 1000);
                    const uptimeStr = uptime > 3600 ? `${Math.round(uptime/3600)}h` : `${Math.round(uptime/60)}m`;
                    const memoryMB = (status.free_heap / 1024).toFixed(1);

                    showNotification(
                        `Device Status: Uptime ${uptimeStr}, Memory ${memoryMB}KB, WiFi: ${status.wifi_ssid}`,
                        'info'
                    );
                } else {
                    showNotification(`Status error: ${status.error}`, 'error');
                }
            } catch (error) {
                showNotification(`Error: ${error.message}`, 'error');
            }
        }

        function showNotification(message, type = 'info') {
            // Remove existing notifications
            const existing = document.querySelector('.notification');
            if (existing) existing.remove();

            // Create notification
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 16px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 1000;
                max-width: 400px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.2);
                transform: translateX(100%);
                transition: transform 0.3s ease;
            `;

            // Set background color based on type
            const colors = {
                success: 'linear-gradient(135deg, #48bb78, #38a169)',
                error: 'linear-gradient(135deg, #f56565, #e53e3e)',
                info: 'linear-gradient(135deg, #4299e1, #3182ce)',
                warning: 'linear-gradient(135deg, #ed8936, #dd6b20)'
            };
            notification.style.background = colors[type] || colors.info;

            // Add icon
            const icons = {
                success: 'fas fa-check-circle',
                error: 'fas fa-exclamation-circle',
                info: 'fas fa-info-circle',
                warning: 'fas fa-exclamation-triangle'
            };

            notification.innerHTML = `
                <i class="${icons[type] || icons.info}"></i>
                <span style="margin-left: 8px;">${message}</span>
            `;

            document.body.appendChild(notification);

            // Animate in
            setTimeout(() => {
                notification.style.transform = 'translateX(0)';
            }, 100);

            // Auto-remove after 5 seconds
            setTimeout(() => {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 300);
            }, 5000);
        }

        // Load data on page load
        window.addEventListener('load', () => {
            loadStatistics();
            loadDevices();

            // Auto-refresh every 30 seconds
            setInterval(() => {
                loadStatistics();
                loadDevices();
            }, 30000);

            // Show welcome message
            setTimeout(() => {
                showNotification('ESP-Linker Dashboard loaded successfully!', 'success');
            }, 1000);
        });
    </script>
</body>
</html>
"""


def run_dashboard(host: str = 'localhost', port: int = 8080, debug: bool = False):
    """
    Run the ESP-Linker web dashboard.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
    """
    dashboard = Dashboard(host, port)
    dashboard.run(debug=debug)
