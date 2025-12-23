"""
Interactive battery scheduler - gets input from user
"""

from battery_scheduler import greedy_algorithm, segmented_charge_planner
from utils import print_task_analysis, format_time


def get_float_input(prompt, min_val=None, max_val=None):
    """Get validated float input from user"""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")


def get_tasks():
    """Get task list from user"""
    print("\n--- Task Input ---")
    tasks = []
    
    num_tasks = int(get_float_input("How many tasks? ", min_val=0))
    
    for i in range(num_tasks):
        print(f"\nTask {i+1}:")
        duration = get_float_input("  Duration (seconds): ", min_val=0)
        drain_rate = get_float_input("  Power drain (mAh/s): ", min_val=0)
        tasks.append([duration, drain_rate])
    
    return tasks


def display_results(greedy_time, scp_time):
    """Show results in a nice format"""
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    if greedy_time == -1:
        print("❌ Impossible to complete tasks!")
        print("   One or more tasks require more energy than battery capacity")
    else:
        print(f"Greedy Algorithm:     {greedy_time}s")
        print(f"Segmented Planning:   {scp_time}s")
        
        if abs(greedy_time - scp_time) < 0.1:
            print("\n✓ Both algorithms take the same time (optimal!)")
        else:
            print(f"\n⚠️  Different results (Δ = {abs(greedy_time - scp_time)}s)")


def main():
    """Main interactive loop"""
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║              SMARTWATCH BATTERY SCHEDULER                             ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    
    while True:
        print("\n" + "=" * 80)
        print("BATTERY PARAMETERS")
        print("=" * 80)
        
        battery_capacity = get_float_input("Battery capacity (mAh): ", min_val=0)
        initial_battery = get_float_input(
            f"Initial battery (0-{battery_capacity} mAh): ", 
            min_val=0, 
            max_val=battery_capacity
        )
        charge_rate = get_float_input("Charge rate (mAh/s): ", min_val=0)
        
        tasks = get_tasks()
        
        if not tasks:
            print("\nNo tasks to schedule!")
        else:
            print_task_analysis(tasks, battery_capacity)
            
            print("\nCalculating optimal schedule...")
            
            greedy_time = greedy_algorithm(battery_capacity, initial_battery, tasks, charge_rate)
            scp_time = segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate)
            
            display_results(greedy_time, scp_time)
        
        print("\n" + "=" * 80)
        again = input("Run another calculation? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("\nThanks for using the battery scheduler!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
