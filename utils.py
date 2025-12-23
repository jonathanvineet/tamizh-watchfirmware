"""
Utility functions for battery scheduling
"""

def validate_inputs(battery_capacity, initial_battery, tasks, charge_rate):
    """
    Validate all inputs and return error message if invalid
    Returns None if all inputs are valid
    """
    if battery_capacity <= 0:
        return "Battery capacity must be positive"
    
    if initial_battery < 0:
        return "Initial battery cannot be negative"
    
    if initial_battery > battery_capacity:
        return "Initial battery cannot exceed capacity"
    
    if charge_rate < 0:
        return "Charge rate cannot be negative"
    
    if not isinstance(tasks, list):
        return "Tasks must be a list"
    
    for i, task in enumerate(tasks):
        if not isinstance(task, (list, tuple)) or len(task) != 2:
            return f"Task {i+1} must be [duration, drain_rate]"
        
        duration, drain_rate = task
        
        if duration < 0:
            return f"Task {i+1} duration cannot be negative"
        
        if drain_rate < 0:
            return f"Task {i+1} drain rate cannot be negative"
    
    return None


def format_time(seconds):
    """Format time in a human-readable way"""
    if seconds < 0:
        return "impossible"
    elif seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def calculate_total_energy(tasks):
    """Calculate total energy needed for all tasks"""
    return sum(duration * drain_rate for duration, drain_rate in tasks)


def estimate_min_charges(tasks, battery_capacity, initial_battery):
    """
    Estimate minimum number of charge cycles needed
    This is a rough estimate, not exact
    """
    total_energy = calculate_total_energy(tasks)
    available_energy = battery_capacity - initial_battery
    
    if total_energy <= initial_battery:
        return 0
    
    remaining = total_energy - initial_battery
    return int((remaining + battery_capacity - 1) / battery_capacity)


def print_task_analysis(tasks, battery_capacity):
    """Print detailed analysis of tasks"""
    print("\nTask Analysis:")
    print("-" * 60)
    
    total_energy = 0
    max_energy = 0
    
    for i, (duration, drain_rate) in enumerate(tasks, 1):
        energy = duration * drain_rate
        total_energy += energy
        max_energy = max(max_energy, energy)
        
        feasible = "✓" if energy <= battery_capacity else "✗"
        print(f"Task {i}: {duration}s × {drain_rate} mAh/s = {energy} mAh {feasible}")
    
    print("-" * 60)
    print(f"Total energy needed: {total_energy} mAh")
    print(f"Max single task: {max_energy} mAh")
    print(f"Battery capacity: {battery_capacity} mAh")
    
    if max_energy > battery_capacity:
        print("\n⚠️  At least one task is impossible (exceeds capacity)")
    elif total_energy > battery_capacity:
        print(f"\n✓ All tasks feasible, but will need charging")
    else:
        print(f"\n✓ All tasks can run on current battery")
