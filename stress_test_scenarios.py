"""
Stress testing algorithm for battery segmented planner.
Tests complex, realistic smartwatch scenarios with comprehensive analysis.
"""

from battery_segmented_planner import segmented_charge_planner
from datetime import datetime


class StressTestScenario:
    """Represents a stress test scenario with realistic parameters"""
    
    def __init__(self, name, battery_capacity, initial_battery, charge_rate, tasks):
        self.name = name
        self.battery_capacity = battery_capacity
        self.initial_battery = initial_battery
        self.charge_rate = charge_rate
        self.tasks = tasks
        self.result = None
        self.analysis = {}
    
    def run(self):
        """Execute the test scenario"""
        self.result = segmented_charge_planner(
            self.battery_capacity, 
            self.initial_battery, 
            self.tasks, 
            self.charge_rate
        )
        self._analyze()
    
    def _analyze(self):
        """Analyze test results"""
        total_energy_drain = sum(duration * drain_rate for duration, drain_rate in self.tasks)
        total_duration = sum(duration for duration, drain_rate in self.tasks)
        
        self.analysis = {
            'total_tasks': len(self.tasks),
            'total_energy_drain': total_energy_drain,
            'total_duration': total_duration,
            'avg_drain_rate': total_energy_drain / total_duration if total_duration > 0 else 0,
            'battery_capacity_needed': total_energy_drain,
            'feasible': self.result > 0,
            'overhead': self.result - total_duration if self.result > 0 else None
        }
    
    def display(self):
        """Display test results in formatted output"""
        print(f"\n{'='*90}")
        print(f"SCENARIO: {self.name}")
        print(f"{'='*90}")
        print(f"Battery Capacity:    {self.battery_capacity} mAh")
        print(f"Initial Battery:     {self.initial_battery} mAh")
        print(f"Charge Rate:         {self.charge_rate} mAh/s")
        print(f"Number of Tasks:     {self.analysis['total_tasks']}")
        print(f"Total Energy Drain:  {self.analysis['total_energy_drain']:.1f} mAh")
        print(f"Total Duration:      {self.analysis['total_duration']:.1f}s")
        print(f"Avg Drain Rate:      {self.analysis['avg_drain_rate']:.2f} mAh/s")
        
        print(f"\n{'Task Details:':<50}")
        for i, (duration, drain_rate) in enumerate(self.tasks):
            energy = duration * drain_rate
            print(f"  Task {i+1:<2} | Duration: {duration:>6.1f}s | Drain: {drain_rate:>6.1f} mAh/s | Energy: {energy:>7.1f} mAh")
        
        print(f"\n{'Results:':<50}")
        if self.result == -1:
            print(f"  Status:            ❌ INFEASIBLE")
            print(f"  Reason:            Task(s) exceed battery capacity")
        else:
            print(f"  Status:            ✓ FEASIBLE")
            print(f"  Total Time:        {self.result:.1f}s")
            print(f"  Charging Overhead: {self.analysis['overhead']:.1f}s ({(self.analysis['overhead']/self.result*100):.1f}%)")
            print(f"  Efficiency:        {(self.analysis['total_duration']/self.result*100):.1f}%")


# Base battery parameters (common for user profiles)
BASE_BATTERY_CAPACITY = 400  # mAh
BASE_CHARGE_RATE = 2.0       # mAh/s

# Define realistic stress test scenarios
STRESS_SCENARIOS = [
    # Profile 1: Athlete (Heavy User) - Hard Case
    StressTestScenario(
        name="Profile: Athlete (Heavy User) - Hard Case",
        battery_capacity=BASE_BATTERY_CAPACITY,
        initial_battery=160,  # 40%
        charge_rate=BASE_CHARGE_RATE,
        tasks=[
            (30, 1.2),   # check workout plan (display + notifications)
            (60, 5.0),   # GPS run (GPS + HR + display)
            (45, 2.5),   # heart rate check (HR + display)
            (120, 6.0),  # intense workout (GPS + HR + display) -> impossible
            (60, 1.0),   # post-workout summary (display)
        ],
    ),

    # Profile 2: Average User (Moderate User)
    StressTestScenario(
        name="Profile: Average (Moderate User)",
        battery_capacity=BASE_BATTERY_CAPACITY,
        initial_battery=240,  # 60%
        charge_rate=BASE_CHARGE_RATE,
        tasks=[
            (30, 1.0),   # check notifications (display)
            (60, 1.8),   # heart rate check (HR + display)
            (45, 1.2),   # view calendar (display)
            (60, 4.0),   # GPS navigation (GPS + HR + display)
            (30, 0.8),   # quick glance (display)
        ],
    ),

    # Profile 3: Senior (Light User)
    StressTestScenario(
        name="Profile: Senior (Light User)",
        battery_capacity=BASE_BATTERY_CAPACITY,
        initial_battery=120,  # 30%
        charge_rate=BASE_CHARGE_RATE,
        tasks=[
            (30, 1.0),   # check medication reminder (display)
            (60, 1.5),   # heart rate check (HR + display)
            (45, 1.6),   # receive call (Bluetooth + display)
            (30, 0.8),   # view weather (display)
        ],
    ),
    # Scenario 1: Morning routine (light usage)
    StressTestScenario(
        name="Morning Routine - Light Usage",
        battery_capacity=400,           # 400 mAh battery (typical smartwatch)
        initial_battery=350,            # 87.5% charge
        charge_rate=30,                 # 30 mAh/s charging speed
        tasks=[
            (5, 15),    # 5s heart rate check, 15 mAh/s drain
            (10, 20),   # 10s notifications check, 20 mAh/s drain
            (30, 10),   # 30s weather app, 10 mAh/s drain
            (8, 18),    # 8s quick call, 18 mAh/s drain
            (15, 12),   # 15s step counting, 12 mAh/s drain
        ]
    ),
    
    # Scenario 2: Workout session (high drain)
    StressTestScenario(
        name="Workout Session - High Intensity",
        battery_capacity=400,
        initial_battery=300,            # 75% charge
        charge_rate=25,                 # Slower charging during workout
        tasks=[
            (300, 60),  # 5min GPS running, 60 mAh/s drain (very high)
            (60, 50),   # 1min heart rate monitoring, 50 mAh/s drain
            (30, 55),   # 30s real-time tracking, 55 mAh/s drain
            (120, 45),  # 2min GPS recording, 45 mAh/s drain
            (45, 40),   # 45s post-workout analysis, 40 mAh/s drain
        ]
    ),
    
    # Scenario 3: All-day mixed usage (realistic)
    StressTestScenario(
        name="All-Day Mixed Usage - Realistic",
        battery_capacity=500,           # Higher capacity for all-day
        initial_battery=500,            # Full charge
        charge_rate=35,
        tasks=[
            (2, 10),    # Wake up - home screen
            (5, 25),    # Notification check
            (120, 15),  # Morning exercise (2min)
            (8, 30),    # Phone call
            (60, 12),   # Standby mode (background)
            (15, 40),   # Navigation (high drain)
            (180, 8),   # Standby (3min passive)
            (10, 35),   # Text reply
            (300, 20),  # Afternoon workout (5min)
            (120, 10),  # More standby
            (20, 45),   # Video call
            (60, 12),   # Evening app usage
        ]
    ),
    
    # Scenario 4: Extreme usage (pushing limits)
    StressTestScenario(
        name="Extreme Usage - Stress Test",
        battery_capacity=400,
        initial_battery=200,            # 50% charge
        charge_rate=20,                 # Slower charger
        tasks=[
            (10, 70),   # Intense GPS recording
            (5, 65),    # Video streaming preview
            (15, 75),   # 3D game (if supported)
            (20, 60),   # Continuous heart rate + SpO2
            (8, 80),    # Peak usage scenario
            (12, 55),   # More gaming
            (6, 85),    # Maximum drain spike
        ]
    ),
    
    # Scenario 5: Multiple charging cycles (daily realistic)
    StressTestScenario(
        name="Multiple Charging Cycles - Daily Use",
        battery_capacity=450,
        initial_battery=400,
        charge_rate=40,
        tasks=[
            (30, 35),   # Morning: exercise
            (20, 45),   # Navigation to work
            (600, 8),   # Work day: mostly idle (10min)
            (25, 40),   # Lunch: notifications
            (30, 35),   # Afternoon exercise
            (45, 15),   # Commute back: music
            (90, 12),   # Evening: leisure apps
            (20, 25),   # Sleep tracking setup
        ]
    ),
    
    # Scenario 6: Edge case - Minimal battery
    StressTestScenario(
        name="Edge Case - Minimal Initial Battery",
        battery_capacity=400,
        initial_battery=30,             # Very low: 7.5%
        charge_rate=45,                 # Fast charger
        tasks=[
            (5, 20),
            (10, 25),
            (8, 22),
            (15, 18),
            (12, 20),
        ]
    ),
    
    # Scenario 7: Edge case - Very slow charging
    StressTestScenario(
        name="Edge Case - Slow Charging Speed",
        battery_capacity=400,
        initial_battery=350,
        charge_rate=5,                  # Very slow charger (wireless?)
        tasks=[
            (15, 20),
            (20, 25),
            (25, 22),
            (18, 24),
            (22, 20),
        ]
    ),
    
    # Scenario 8: Smart assistant continuous use
    StressTestScenario(
        name="Smart Assistant - Continuous Interaction",
        battery_capacity=400,
        initial_battery=400,
        charge_rate=30,
        tasks=[
            (5, 50),    # Voice command processing
            (3, 45),    # Response playback
            (7, 55),    # Network communication
            (4, 48),    # Voice command
            (6, 52),    # Processing
            (5, 50),    # Network response
            (8, 60),    # Complex query
            (3, 45),    # Simple response
        ]
    ),
    
    # Scenario 9: Sleep tracking + background services
    StressTestScenario(
        name="Sleep Tracking + Background Services",
        battery_capacity=400,
        initial_battery=350,
        charge_rate=28,
        tasks=[
            (28800, 2),     # 8 hours sleep with heart rate tracking: 2 mAh/s
            (3600, 5),      # 1 hour morning data sync: 5 mAh/s
            (1800, 8),      # 30min morning apps: 8 mAh/s
            (3600, 12),     # 1 hour workout: 12 mAh/s
            (36000, 3),     # 10 hours standby: 3 mAh/s
        ]
    ),
    
    # Scenario 10: Impossible scenario (should fail gracefully)
    StressTestScenario(
        name="Impossible Scenario - Task Exceeds Capacity",
        battery_capacity=200,
        initial_battery=150,
        charge_rate=50,
        tasks=[
            (10, 30),
            (25, 50),       # This task alone: 25*50 = 1250 mAh > 200 capacity
            (8, 20),
        ]
    ),
]


def run_all_tests():
    """Run all stress test scenarios"""
    print("\n")
    print("╔" + "="*88 + "╗")
    print("║" + " "*20 + "BATTERY SCHEDULER STRESS TEST SUITE" + " "*33 + "║")
    print("║" + " "*15 + f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " "*40 + "║")
    print("╚" + "="*88 + "╝")
    
    # Run all scenarios
    for scenario in STRESS_SCENARIOS:
        scenario.run()
        scenario.display()
    
    # Print summary
    print_summary()


def print_summary():
    """Print comprehensive test summary"""
    print("\n")
    print("╔" + "="*88 + "╗")
    print("║" + " "*31 + "TEST SUMMARY" + " "*45 + "║")
    print("╚" + "="*88 + "╝\n")
    
    total_tests = len(STRESS_SCENARIOS)
    feasible_tests = sum(1 for s in STRESS_SCENARIOS if s.result > 0)
    infeasible_tests = total_tests - feasible_tests
    
    print(f"Total Scenarios Tested:  {total_tests}")
    print(f"Feasible Scenarios:      {feasible_tests} ({feasible_tests/total_tests*100:.1f}%)")
    print(f"Infeasible Scenarios:    {infeasible_tests} ({infeasible_tests/total_tests*100:.1f}%)")
    
    # Performance metrics
    feasible_scenarios = [s for s in STRESS_SCENARIOS if s.result > 0]
    
    if feasible_scenarios:
        print(f"\n{'Performance Metrics (Feasible Scenarios):':<50}")
        total_times = [s.result for s in feasible_scenarios]
        total_durations = [s.analysis['total_duration'] for s in feasible_scenarios]
        overheads = [s.analysis['overhead'] for s in feasible_scenarios]
        efficiencies = [s.analysis['total_duration']/s.result*100 for s in feasible_scenarios]
        
        print(f"  Average Total Time:    {sum(total_times)/len(total_times):.1f}s")
        print(f"  Average Task Duration: {sum(total_durations)/len(total_durations):.1f}s")
        print(f"  Average Overhead:      {sum(overheads)/len(overheads):.1f}s")
        print(f"  Average Efficiency:    {sum(efficiencies)/len(efficiencies):.1f}%")
        
        min_overhead = min(overheads)
        max_overhead = max(overheads)
        print(f"  Min Overhead:          {min_overhead:.1f}s")
        print(f"  Max Overhead:          {max_overhead:.1f}s")
    
    print(f"\n{'Scenario Breakdown:':<50}")
    for scenario in STRESS_SCENARIOS:
        status = "✓ PASS" if scenario.result > 0 else "✗ FAIL"
        print(f"  {status} | {scenario.name}")
    
    print(f"\n{'='*90}")
    print("✓ Stress testing completed successfully!")
    print(f"{'='*90}\n")


def run_specific_scenario(index):
    """Run a specific scenario by index"""
    if 0 <= index < len(STRESS_SCENARIOS):
        scenario = STRESS_SCENARIOS[index]
        scenario.run()
        print("\n")
        print("╔" + "="*88 + "╗")
        print("║" + " "*31 + "DETAILED ANALYSIS" + " "*41 + "║")
        print("╚" + "="*88 + "╝")
        scenario.display()
    else:
        print(f"Invalid scenario index. Choose between 0 and {len(STRESS_SCENARIOS)-1}")


if __name__ == "__main__":
    run_all_tests()
