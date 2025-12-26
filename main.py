#!/usr/bin/env python3
"""
Quick launcher for battery scheduler tools

Adds Upgraded Smartwatch Battery Scheduler (v2) interactive mode
with priority-based scheduling, charge efficiency, and health cap.
"""

import sys
from typing import List, Dict, Any


def upgraded_battery_scheduler(
    tasks: List[Dict[str, Any]],
    battery_capacity: float,
    initial_battery: float,
    charge_rate: float,
    charge_efficiency: float = 0.95,
    full_limit: float = 0.90,
) -> float:
    """
    Real-time battery scheduler with smart charging.

    Args:
        tasks: List of dicts [{duration, drain_rate, priority}]
        battery_capacity: Max battery level (mAh)
        initial_battery: Starting battery (mAh)
        charge_rate: Charging rate in mAh/s
        charge_efficiency: Fractional charge efficiency (<1.0 simulates energy loss)
        full_limit: Charge cap for health (e.g. 0.90 means avoid going above 90%)

    Returns:
        Total time to run tasks OR -1 if critical task is impossible
    """
    time = 0.0
    battery = initial_battery
    i = 0
    n = len(tasks)

    while i < n:
        task = tasks[i]
        energy_needed = task["duration"] * task["drain_rate"]

        # Check if task is physically impossible
        if energy_needed > battery_capacity:
            if task["priority"] == "high":
                return -1.0  # Critical task can't be run
            else:
                i += 1
                continue  # Skip low-priority task

        # Run if enough battery
        if battery >= energy_needed:
            battery -= energy_needed
            time += task["duration"]
            i += 1
        else:
            # Estimate future tasks to charge for
            j = i
            total_energy = 0.0
            segment = []
            while j < n:
                t = tasks[j]
                e = t["duration"] * t["drain_rate"]
                if total_energy + e > battery_capacity:
                    break
                if t["priority"] == "high":
                    segment.append(t)
                    total_energy += e
                elif t["priority"] == "med" and battery < full_limit * battery_capacity:
                    segment.append(t)
                    total_energy += e
                j += 1

            # Charge just enough for segment (apply efficiency and cap)
            base_target = min(max(total_energy, energy_needed), battery_capacity)
            cap_limit = full_limit * battery_capacity
            if energy_needed > cap_limit:
                # Override health cap for mandatory energy needs
                target = base_target
            else:
                target = min(base_target, cap_limit)

            if target <= battery:
                # Already enough for the planned target; try executing the task.
                continue

            to_charge = (target - battery) / charge_efficiency
            idle_time = to_charge / charge_rate
            time += idle_time
            battery += idle_time * charge_rate * charge_efficiency
            battery = min(battery, battery_capacity)  # Cap at full

    return round(time, 2)


def show_menu():
    print("\n╔═══════════════════════════════════════════════════════════════════════╗")
    print("║              SMARTWATCH BATTERY SCHEDULER                             ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print("\nWhat would you like to do?\n")
    print("  1. Run interactive mode (legacy v1)")
    print("  2. Run upgraded interactive (v2)")
    print("  3. Run test suite (automated testing)")
    print("  4. View examples")
    print("  5. Exit")
    print()


def _get_float(prompt: str, min_val: float | None = None, max_val: float | None = None) -> float:
    while True:
        try:
            val = float(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return val
        except ValueError:
            print("Please enter a valid number")


def upgraded_interactive():
    print("\n" + "=" * 80)
    print("UPGRADED SMARTWATCH BATTERY SCHEDULER (v2) - INTERACTIVE")
    print("=" * 80)

    battery_capacity = _get_float("Battery capacity (mAh): ", min_val=0)
    initial_battery = _get_float(
        f"Initial battery (0-{battery_capacity} mAh): ", min_val=0, max_val=battery_capacity
    )
    charge_rate = _get_float("Charge rate (mAh/s): ", min_val=0)

    # Optional advanced parameters
    charge_efficiency = _get_float("Charge efficiency (default 0.95): ", min_val=0.5, max_val=1.0)
    full_limit = _get_float("Health cap full_limit (default 0.90): ", min_val=0.5, max_val=1.0)

    print("\nEnter tasks. Provide duration (s), drain rate (mAh/s), priority [high/med/low].")
    print("Type 'done' when finished.\n")
    tasks: List[Dict[str, Any]] = []

    idx = 1
    while True:
        raw = input(f"Task {idx} (e.g., 30 2.5 med): ").strip()
        if raw.lower() in {"", "done", "d"}:
            break
        parts = raw.split()
        if len(parts) != 3:
            print("Please enter exactly 3 values: duration drain_rate priority")
            continue
        try:
            duration = float(parts[0])
            drain_rate = float(parts[1])
            priority = parts[2].lower()
            if priority not in {"high", "med", "low"}:
                print("Priority must be one of: high, med, low")
                continue
            tasks.append({"duration": duration, "drain_rate": drain_rate, "priority": priority})
            idx += 1
        except ValueError:
            print("Invalid numeric values. Try again.")

    if not tasks:
        print("\nNo tasks entered. Returning to menu.")
        return

    print("\nCalculating schedule...")
    total_time = upgraded_battery_scheduler(
        tasks,
        battery_capacity=battery_capacity,
        initial_battery=initial_battery,
        charge_rate=charge_rate,
        charge_efficiency=charge_efficiency,
        full_limit=full_limit,
    )

    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    total_energy = sum(t["duration"] * t["drain_rate"] for t in tasks)
    total_duration = sum(t["duration"] for t in tasks)
    print(f"Total tasks: {len(tasks)}")
    print(f"Total energy required: {total_energy:.2f} mAh")
    print(f"Total task duration: {total_duration:.2f}s")
    if total_time == -1.0:
        print("Status: ❌ Critical task impossible (exceeds capacity)")
    else:
        overhead = total_time - total_duration
        efficiency = (total_duration / total_time * 100) if total_time > 0 else 0.0
        print(f"Status: ✓ Feasible")
        print(f"Total time including charging: {total_time:.2f}s")
        print(f"Charging overhead: {overhead:.2f}s")
        print(f"Efficiency: {efficiency:.1f}%")


def main():
    while True:
        show_menu()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            print("\n" + "=" * 80)
            print("Launching interactive mode (legacy v1)...")
            print("=" * 80)
            import run_interactive
            run_interactive.main()

        elif choice == "2":
            print("\n" + "=" * 80)
            print("Launching upgraded interactive mode (v2)...")
            print("=" * 80)
            upgraded_interactive()

        elif choice == "3":
            print("\n" + "=" * 80)
            print("Running test suite...")
            print("=" * 80)
            import test_battery_scheduler
            test_battery_scheduler.run_all_tests()

        elif choice == "4":
            print("\n" + "=" * 80)
            print("Running examples...")
            print("=" * 80)
            import examples

        elif choice == "5":
            print("\nGoodbye!")
            sys.exit(0)

        else:
            print("\n❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
