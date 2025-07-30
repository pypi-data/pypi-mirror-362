#!/usr/bin/env python3
"""
Quantum Data Embedding Suite License Information Utility

This script provides comprehensive license information and support details
for users of the Quantum Data Embedding Suite.
"""

import sys
from quantum_data_embedding_suite.licensing import (
    get_machine_id, 
    get_system_info, 
    check_license_status,
    LicenseManager
)


def display_license_info():
    """Display comprehensive license information."""
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║              🚀 QUANTUM DATA EMBEDDING SUITE - LICENSE INFO                  ║")
    print("╠═══════════════════════════════════════════════════════════════════════════════╣")
    
    # Get license status
    status = check_license_status()
    system_info = get_system_info()
    machine_id = get_machine_id()
    
    print(f"║ 📦 Package: quantum-data-embedding-suite                                     ║")
    print(f"║ 💻 Machine ID: {machine_id:<59} ║")
    print(f"║ 🔍 License Status: {status['status'].upper():<51} ║")
    print(f"║                                                                               ║")
    
    if status["status"] == "valid":
        print(f"║ ✅ License is active and valid                                               ║")
    else:
        print(f"║ ❌ License validation failed                                                ║")
        print(f"║ 🔸 Error: {status.get('error', 'Unknown error')[:63]:<63} ║")
    
    print(f"║                                                                               ║")
    print(f"║ 💻 System Information:                                                       ║")
    print(f"║    • OS: {system_info['system']:<67} ║")
    print(f"║    • Platform: {system_info['platform'][:60]:<60} ║")
    print(f"║    • Architecture: {system_info['architecture']:<55} ║")
    print(f"║    • Python: {system_info['python_version']:<61} ║")
    print(f"║    • Hostname: {system_info['hostname'][:59]:<59} ║")
    print(f"║                                                                               ║")
    print(f"║ 🎯 Available License Tiers:                                                  ║")
    print(f"║    • Basic: Core embedding and kernel functionality                          ║")
    print(f"║    • Pro: Advanced algorithms, optimization, and visualization               ║")
    print(f"║    • Enterprise: Full feature set with priority support                      ║")
    print(f"║                                                                               ║")
    print(f"║ 📧 License Support:                                                          ║")
    print(f"║    • Email: bajpaikrishna715@gmail.com                                       ║")
    print(f"║    • Include your Machine ID in license requests                             ║")
    print(f"║    • Specify required features and use case                                   ║")
    print(f"║                                                                               ║")
    print(f"║ 📚 Documentation: https://github.com/krish567366/quantum-data-embedding-suite║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")


def display_machine_id_only():
    """Display just the machine ID for license activation."""
    machine_id = get_machine_id()
    print(f"Machine ID: {machine_id}")


def main():
    """Main function for license information utility."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--machine-id":
            display_machine_id_only()
            return
        elif sys.argv[1] == "--help":
            print("Quantum Data Embedding Suite License Information Utility")
            print("")
            print("Usage:")
            print("  python license_info.py           Show full license information")
            print("  python license_info.py --machine-id    Show machine ID only")
            print("  python license_info.py --help         Show this help message")
            return
    
    display_license_info()


if __name__ == "__main__":
    main()
