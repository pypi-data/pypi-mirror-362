#!/usr/bin/env python3
"""
ESP-Linker Python Library Setup
(c) 2025 SK Raihan / SKR Electronics Lab - All Rights Reserved.

Professional wireless GPIO control for ESP8266 boards with PyFirmata-inspired interface.
Complete IoT solution with firmware, Python library, CLI tools, and web dashboard.

Author: SK Raihan
Organization: SKR Electronics Lab
Website: https://www.skrelectronicslab.com
Email: skrelectronicslab@gmail.com
YouTube: https://www.youtube.com/@skr_electronics_lab
Instagram: https://www.instagram.com/skr_electronics_lab
GitHub: https://github.com/skr-electronics-lab
Support: https://buymeacoffee.com/skrelectronics
"""

from setuptools import setup, find_packages

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="esp-linker",
    version="1.3.4",
    author="SK Raihan",
    author_email="skrelectronicslab@gmail.com",
    maintainer="SKR Electronics Lab",
    maintainer_email="skrelectronicslab@gmail.com",
    description="Professional wireless GPIO control for ESP8266 boards with PyFirmata-inspired interface, complete IoT solution with firmware, CLI tools, and web dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.skrelectronicslab.com",
    download_url="https://pypi.org/project/esp-linker/",
    project_urls={
        "Homepage": "https://www.skrelectronicslab.com",
        "Documentation": "https://www.skrelectronicslab.com/esp-linker",
        "Source Code": "https://github.com/skr-electronics-lab/esp-linker",
        "Bug Tracker": "https://github.com/skr-electronics-lab/esp-linker/issues",
        "YouTube Channel": "https://www.youtube.com/@skr_electronics_lab",
        "Instagram": "https://www.instagram.com/skr_electronics_lab",
        "Support": "https://buymeacoffee.com/skrelectronics",
        "PyPI": "https://pypi.org/project/esp-linker/",
    },
    license="MIT",
    packages=find_packages(),
    package_data={
        'esp_linker': ['firmware/*.bin'],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: System :: Networking",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Home Automation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Communications",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Natural Language :: English",
        "Framework :: Flask",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dashboard": ["flask>=2.0.0"],
        "all": ["flask>=2.0.0"],
    },
    entry_points={
        "console_scripts": [
            "esp-linker=esp_linker.cli:main",
            "esp-linker-discover=esp_linker.cli:discover_devices_entry",
            "esp-linker-test=esp_linker.cli:test_device_entry",
            "esp-linker-flash=esp_linker.cli:flash_esp8266_entry",
            "esp-linker-detect=esp_linker.cli:detect_esp8266_entry",
            "esp-linker-setup-wifi=esp_linker.cli:wifi_wizard_entry",
            "esp-linker-devices=esp_linker.cli:devices_entry",
            "esp-linker-dashboard=esp_linker.cli:dashboard_entry",
        ],
    },
    keywords=[
        "esp8266", "gpio", "iot", "wireless", "arduino", "microcontroller",
        "automation", "robotics", "electronics", "maker", "diy", "wifi",
        "remote-control", "pyfirmata", "esp-linker", "nodemcu", "wemos",
        "embedded", "hardware", "sensor", "actuator", "smart-home",
        "internet-of-things", "esp32", "micropython", "circuitpython",
        "raspberry-pi", "home-automation", "industrial-iot", "edge-computing",
        "wireless-communication", "web-dashboard", "cli-tools", "firmware",
        "skr-electronics-lab", "professional", "production-ready", "cross-platform"
    ],
    zip_safe=False,
)
