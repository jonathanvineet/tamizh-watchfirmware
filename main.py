#!/usr/bin/env python3
"""
Quick launcher for battery scheduler tools
"""

import sys


def show_menu():
    print("\n╔═══════════════════════════════════════════════════════════════════════╗")
    print("║              SMARTWATCH BATTERY SCHEDULER                             ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print("\nWhat would you like to do?\n")
    print("  1. Run interactive mode (enter custom inputs)")
    print("  2. Run test suite (automated testing)")
    print("  3. View examples")
    print("  4. Exit")
    print()


def main():
    while True:
        show_menu()
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            print("\n" + "="*80)
            print("Launching interactive mode...")
            print("="*80)
            import run_interactive
            run_interactive.main()
            
        elif choice == "2":
            print("\n" + "="*80)
            print("Running test suite...")
            print("="*80)
            import test_battery_scheduler
            test_battery_scheduler.run_all_tests()
            
        elif choice == "3":
            print("\n" + "="*80)
            print("Running examples...")
            print("="*80)
            import examples
            
        elif choice == "4":
            print("\nGoodbye!")
            sys.exit(0)
            
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
