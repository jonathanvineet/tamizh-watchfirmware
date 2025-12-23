"""
Battery scheduling algorithms for smartwatch task management
"""

def greedy_algorithm(battery_capacity, initial_battery, tasks, charge_rate):
    """
    Charges before each task as needed
    Returns total time to complete all tasks, or -1 if impossible
    """
    if not tasks:
        return 0.0
    
    for duration, drain_rate in tasks:
        if duration * drain_rate > battery_capacity:
            return -1.0
    
    if charge_rate <= 0:
        return -1.0
    
    total_time = 0.0
    current_battery = initial_battery
    
    for duration, drain_rate in tasks:
        energy_needed = duration * drain_rate
        optimal_start = min(energy_needed, battery_capacity)
        
        if current_battery < optimal_start:
            charge_time = (optimal_start - current_battery) / charge_rate
            total_time += charge_time
            current_battery = optimal_start
        
        total_time += duration
        current_battery -= energy_needed
        
    return round(total_time, 1)


def segmented_charge_planner(battery_capacity, initial_battery, tasks, charge_rate):
    """
    Looks ahead and charges for multiple tasks at once
    Returns total time to complete all tasks, or -1 if impossible
    """
    if not tasks:
        return 0.0
    
    if charge_rate <= 0:
        for duration, drain_rate in tasks:
            if duration * drain_rate > battery_capacity:
                return -1.0
        return -1.0
    
    battery = initial_battery
    total_time = 0.0
    i = 0
    n_tasks = len(tasks)
    epsilon = 1e-9
    
    while i < n_tasks:
        duration, drain_rate = tasks[i]
        drain = duration * drain_rate
        
        if drain > battery_capacity + epsilon:
            return -1.0
        
        if battery >= drain - epsilon:
            battery -= drain
            total_time += duration
            i += 1
        else:
            # Need to charge - see how many tasks we can cover with one charge
            j = i
            energy_needed = 0.0
            
            while j < n_tasks:
                task_duration, task_drain_rate = tasks[j]
                task_energy = task_duration * task_drain_rate
                
                if task_energy > battery_capacity + epsilon:
                    return -1.0
                
                if energy_needed + task_energy > battery_capacity + epsilon:
                    break
                
                energy_needed += task_energy
                j += 1
            
            target = min(energy_needed, battery_capacity)
            charge_needed = target - battery
            idle_time = charge_needed / charge_rate
            
            total_time += idle_time
            battery += idle_time * charge_rate
            battery = min(battery, battery_capacity)
    
    return round(total_time, 1)
