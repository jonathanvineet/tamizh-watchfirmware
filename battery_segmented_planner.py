"""
Standalone battery scheduler using segmented planning.
This module provides optimal battery scheduling for smartwatch tasks
by looking ahead and charging for multiple tasks at once.
"""


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


def display_results(total_time):
    """Show results in a nice format"""
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    if total_time == -1:
        print("❌ Impossible to complete tasks!")
        print("   One or more tasks require more energy than battery capacity")
    else:
        print(f"✓ Total time to complete all tasks: {total_time}s")


def segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate):
    """
    Looks ahead and charges for multiple tasks at once.
    
    Args:
        battery_capacity (float): Maximum battery capacity in energy units
        initial_battery (float): Starting battery level in energy units
        tasks (list): List of tuples (duration, drain_rate) where:
                     - duration: time to complete task (in time units)
                     - drain_rate: energy drain per unit time
        charge_rate (float): Energy gained per unit time while charging
    
    Returns:
        float: Total time to complete all tasks, or -1.0 if impossible
    
    Algorithm:
        - Simulates task execution with proactive charging
        - Looks ahead to determine how many upcoming tasks can be handled
          with a single charge cycle
        - Charges only the minimum needed to complete the upcoming batch
        - Ensures no single task requires more than battery capacity
    """
    if not tasks:
        return 0.0
    
    # Check if charging is possible and validate task requirements
    if charge_rate <= 0:
        for duration, drain_rate in tasks:
            if duration * drain_rate > battery_capacity:
                return -1.0
        return -1.0
    
    battery = initial_battery
    total_time = 0.0
    i = 0
    n_tasks = len(tasks)
    epsilon = 1e-9  # Small threshold for floating-point comparisons
    
    while i < n_tasks:
        duration, drain_rate = tasks[i]
        drain = duration * drain_rate
        
        # Check if task itself exceeds battery capacity
        if drain > battery_capacity + epsilon:
            return -1.0
        
        # If we have enough battery, execute the task
        if battery >= drain - epsilon:
            battery -= drain
            total_time += duration
            i += 1
        else:
            # Need to charge - look ahead to see how many tasks we can cover
            j = i
            energy_needed = 0.0
            
            # Calculate total energy needed for upcoming tasks
            while j < n_tasks:
                task_duration, task_drain_rate = tasks[j]
                task_energy = task_duration * task_drain_rate
                
                # Individual task exceeds capacity
                if task_energy > battery_capacity + epsilon:
                    return -1.0
                
                # Would adding this task exceed battery capacity?
                if energy_needed + task_energy > battery_capacity + epsilon:
                    break
                
                energy_needed += task_energy
                j += 1
            
            # Charge to the minimum needed (but not more than capacity)
            target = min(energy_needed, battery_capacity)
            charge_needed = target - battery
            idle_time = charge_needed / charge_rate
            
            total_time += idle_time
            battery += idle_time * charge_rate
            battery = min(battery, battery_capacity)
    
    return round(total_time, 1)


if __name__ == "__main__":
    main()


def main():
    """Main interactive loop"""
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║         SMARTWATCH BATTERY SEGMENTED PLANNER                          ║")
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
            # Display task summary
            print("\n--- Task Summary ---")
            total_drain = sum(d * dr for d, dr in tasks)
            print(f"Total tasks: {len(tasks)}")
            print(f"Total energy required: {total_drain:.1f} mAh")
            print(f"Battery capacity: {battery_capacity} mAh")
            
            print("\nCalculating optimal schedule using segmented planning...")
            
            result = segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate)
            
            display_results(result)
        
        print("\n" + "=" * 80)
        again = input("Run another calculation? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("\nThanks for using the battery segmented planner!")
            break


# Example usage
def run_examples():
    """Run example scenarios"""
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║         BATTERY SEGMENTED PLANNER - EXAMPLE SCENARIOS                 ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝\n")
    
    # Example 1: Simple task sequence
    print("Example 1: Simple Task Sequence")
    print("-" * 80)
    battery_capacity = 100
    initial_battery = 50
    tasks = [(10, 5), (15, 3), (20, 4)]
    charge_rate = 20
    
    print(f"Battery Capacity: {battery_capacity} mAh")
    print(f"Initial Battery: {initial_battery} mAh")
    print(f"Charge Rate: {charge_rate} mAh/s")
    print(f"Tasks: {tasks}")
    
    result = segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate)
    print(f"Result: {result}s\n")
    
    # Example 2: High drain tasks
    print("Example 2: High Drain Tasks")
    print("-" * 80)
    battery_capacity = 200
    initial_battery = 100
    tasks = [(5, 30), (10, 20), (8, 25)]
    charge_rate = 50
    
    print(f"Battery Capacity: {battery_capacity} mAh")
    print(f"Initial Battery: {initial_battery} mAh")
    print(f"Charge Rate: {charge_rate} mAh/s")
    print(f"Tasks: {tasks}")
    
    result = segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate)
    print(f"Result: {result}s\n")
    
    # Example 3: Impossible scenario
    print("Example 3: Impossible Scenario")
    print("-" * 80)
    battery_capacity = 50
    initial_battery = 30
    tasks = [(10, 10)]
    charge_rate = 20
    
    print(f"Battery Capacity: {battery_capacity} mAh")
    print(f"Initial Battery: {initial_battery} mAh")
    print(f"Charge Rate: {charge_rate} mAh/s")
    print(f"Tasks: {tasks}")
    
    result = segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate)
    status = "Feasible" if result > 0 else "Infeasible"
    print(f"Result: {result} ({status})\n")
