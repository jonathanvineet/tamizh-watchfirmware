"""
Example usage of the battery scheduler
"""

from battery_scheduler import greedy_algorithm, segmented_charge_planner
from utils import validate_inputs, print_task_analysis, format_time


def example_1_basic():
    """Simple example with 3 tasks"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    battery_capacity = 100
    initial_battery = 30
    charge_rate = 5
    tasks = [
        [10, 4],   # 10s task that drains 4 mAh/s = 40 mAh total
        [15, 3],   # 15s task that drains 3 mAh/s = 45 mAh total
        [20, 2],   # 20s task that drains 2 mAh/s = 40 mAh total
    ]
    
    print(f"\nBattery: {initial_battery}/{battery_capacity} mAh")
    print(f"Charge rate: {charge_rate} mAh/s")
    print_task_analysis(tasks, battery_capacity)
    
    greedy_time = greedy_algorithm(battery_capacity, initial_battery, tasks, charge_rate)
    scp_time = segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate)
    
    print(f"\nGreedy algorithm: {format_time(greedy_time)}")
    print(f"Segmented planning: {format_time(scp_time)}")


def example_2_impossible():
    """Example with an impossible task"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Impossible Task")
    print("="*80)
    
    battery_capacity = 50
    initial_battery = 50
    charge_rate = 5
    tasks = [
        [10, 3],   # 30 mAh - OK
        [20, 5],   # 100 mAh - exceeds capacity!
    ]
    
    print(f"\nBattery: {initial_battery}/{battery_capacity} mAh")
    print(f"Charge rate: {charge_rate} mAh/s")
    print_task_analysis(tasks, battery_capacity)
    
    greedy_time = greedy_algorithm(battery_capacity, initial_battery, tasks, charge_rate)
    scp_time = segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate)
    
    print(f"\nGreedy algorithm: {format_time(greedy_time)}")
    print(f"Segmented planning: {format_time(scp_time)}")


def example_3_no_charging():
    """Example where battery is sufficient"""
    print("\n" + "="*80)
    print("EXAMPLE 3: No Charging Needed")
    print("="*80)
    
    battery_capacity = 100
    initial_battery = 100
    charge_rate = 5
    tasks = [
        [10, 2],   # 20 mAh
        [10, 2],   # 20 mAh
        [10, 2],   # 20 mAh
    ]
    
    print(f"\nBattery: {initial_battery}/{battery_capacity} mAh")
    print(f"Charge rate: {charge_rate} mAh/s")
    print_task_analysis(tasks, battery_capacity)
    
    greedy_time = greedy_algorithm(battery_capacity, initial_battery, tasks, charge_rate)
    scp_time = segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate)
    
    print(f"\nGreedy algorithm: {format_time(greedy_time)}")
    print(f"Segmented planning: {format_time(scp_time)}")


def example_4_validation():
    """Show input validation"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Input Validation")
    print("="*80)
    
    test_cases = [
        ("Negative capacity", -100, 50, [[10, 2]], 5),
        ("Initial > capacity", 100, 150, [[10, 2]], 5),
        ("Negative charge rate", 100, 50, [[10, 2]], -5),
        ("Invalid task format", 100, 50, [[10]], 5),
        ("Negative duration", 100, 50, [[-10, 2]], 5),
    ]
    
    for name, capacity, initial, tasks, rate in test_cases:
        error = validate_inputs(capacity, initial, tasks, rate)
        status = "✗" if error else "✓"
        print(f"\n{status} {name}")
        if error:
            print(f"   Error: {error}")


if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║              BATTERY SCHEDULER EXAMPLES                               ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    
    example_1_basic()
    example_2_impossible()
    example_3_no_charging()
    example_4_validation()
    
    print("\n" + "="*80)
    print("Done! Check run_interactive.py for user input mode")
    print("="*80)
