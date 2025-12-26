"""
Stress tests for the upgraded smartwatch battery scheduler (v2).
Covers rolling window execution, priority handling, charge efficiency,
battery preservation caps, and low-battery fallback behavior.
"""

from datetime import datetime
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
            # Ensure we at least cover the current task's energy need so we make forward progress.
            base_target = min(max(total_energy, energy_needed), battery_capacity)
            cap_limit = full_limit * battery_capacity
            if energy_needed > cap_limit:
                # Override health cap for mandatory energy needs
                target = base_target
            else:
                target = min(base_target, cap_limit)

            if target <= battery:
                # Already have enough for the planned target; try executing the task.
                continue

            to_charge = (target - battery) / charge_efficiency
            idle_time = to_charge / charge_rate
            time += idle_time
            battery += idle_time * charge_rate * charge_efficiency
            battery = min(battery, battery_capacity)  # Cap at full

    return round(time, 2)


def _energy(t: Dict[str, Any]) -> float:
    return t["duration"] * t["drain_rate"]


class UpgradedStressScenario:
    """Represents a stress scenario for the upgraded scheduler"""

    def __init__(
        self,
        name: str,
        battery_capacity: float,
        initial_battery: float,
        charge_rate: float,
        tasks: List[Dict[str, Any]],
        charge_efficiency: float = 0.95,
        full_limit: float = 0.90,
    ) -> None:
        self.name = name
        self.battery_capacity = battery_capacity
        self.initial_battery = initial_battery
        self.charge_rate = charge_rate
        self.tasks = tasks
        self.charge_efficiency = charge_efficiency
        self.full_limit = full_limit
        self.result: float | None = None
        self.analysis: Dict[str, Any] = {}

    def run(self) -> None:
        self.result = upgraded_battery_scheduler(
            self.tasks,
            self.battery_capacity,
            self.initial_battery,
            self.charge_rate,
            charge_efficiency=self.charge_efficiency,
            full_limit=self.full_limit,
        )
        self._analyze()

    def _analyze(self) -> None:
        total_duration = sum(t["duration"] for t in self.tasks)
        total_energy = sum(_energy(t) for t in self.tasks)
        by_priority = {"high": 0, "med": 0, "low": 0}
        for t in self.tasks:
            by_priority[t["priority"]] = by_priority.get(t["priority"], 0) + 1

        feasible = self.result is not None and self.result > 0
        overhead = self.result - total_duration if feasible else None
        efficiency = (total_duration / self.result * 100) if feasible else 0

        self.analysis = {
            "total_tasks": len(self.tasks),
            "priority_breakdown": by_priority,
            "total_duration": total_duration,
            "total_energy": total_energy,
            "avg_drain_rate": (total_energy / total_duration) if total_duration else 0,
            "feasible": feasible,
            "overhead": overhead,
            "efficiency": efficiency,
        }

    def display(self) -> None:
        if self.result is None:
            return

        print(f"\n{'='*96}")
        print(f"SCENARIO: {self.name}")
        print(f"{'='*96}")
        print(f"Battery Capacity:    {self.battery_capacity:.1f} mAh")
        print(f"Initial Battery:     {self.initial_battery:.1f} mAh")
        print(f"Charge Rate:         {self.charge_rate:.1f} mAh/s")
        print(f"Charge Efficiency:   {self.charge_efficiency:.2f}")
        print(f"Health Cap (full_limit): {self.full_limit*100:.0f}%")
        print(f"Tasks:               {self.analysis['total_tasks']} (H: {self.analysis['priority_breakdown']['high']}, M: {self.analysis['priority_breakdown']['med']}, L: {self.analysis['priority_breakdown']['low']})")
        print(f"Total Energy:        {self.analysis['total_energy']:.1f} mAh")
        print(f"Total Duration:      {self.analysis['total_duration']:.1f}s")
        print(f"Avg Drain Rate:      {self.analysis['avg_drain_rate']:.2f} mAh/s")

        print(f"\n{'Task Details':<50}")
        for idx, t in enumerate(self.tasks):
            energy = _energy(t)
            print(
                f"  Task {idx+1:<2}| Dur: {t['duration']:>6.1f}s | Drain: {t['drain_rate']:>6.1f} mAh/s | Energy: {energy:>7.1f} mAh | Pri: {t['priority']:>4}"
            )

        print(f"\nResults")
        if self.result == -1.0:
            print("  Status:      ❌ Critical task impossible")
        else:
            print("  Status:      ✓ Feasible")
            print(f"  Total Time:  {self.result:.2f}s")
            print(f"  Overhead:    {self.analysis['overhead']:.2f}s")
            print(f"  Efficiency:  {self.analysis['efficiency']:.1f}%")


SCENARIOS: List[UpgradedStressScenario] = [
    UpgradedStressScenario(
        name="Rolling Window - Mixed Priorities",
        battery_capacity=320,
        initial_battery=140,
        charge_rate=15,
        tasks=[
            {"duration": 25, "drain_rate": 3.0, "priority": "med"},
            {"duration": 40, "drain_rate": 4.5, "priority": "high"},
            {"duration": 35, "drain_rate": 2.2, "priority": "med"},
            {"duration": 20, "drain_rate": 5.5, "priority": "high"},
            {"duration": 15, "drain_rate": 1.5, "priority": "low"},
            {"duration": 30, "drain_rate": 3.8, "priority": "med"},
        ],
    ),
    UpgradedStressScenario(
        name="Low Battery Fallback - Critical First",
        battery_capacity=260,
        initial_battery=30,
        charge_rate=25,
        tasks=[
            {"duration": 18, "drain_rate": 5.5, "priority": "high"},
            {"duration": 22, "drain_rate": 4.8, "priority": "high"},
            {"duration": 28, "drain_rate": 2.5, "priority": "med"},
            {"duration": 30, "drain_rate": 1.4, "priority": "med"},
            {"duration": 14, "drain_rate": 2.0, "priority": "low"},
        ],
    ),
    UpgradedStressScenario(
        name="Charge Efficiency Losses",
        battery_capacity=380,
        initial_battery=200,
        charge_rate=20,
        charge_efficiency=0.80,
        full_limit=0.85,
        tasks=[
            {"duration": 45, "drain_rate": 4.0, "priority": "med"},
            {"duration": 60, "drain_rate": 5.0, "priority": "high"},
            {"duration": 55, "drain_rate": 3.5, "priority": "med"},
            {"duration": 35, "drain_rate": 6.0, "priority": "high"},
            {"duration": 25, "drain_rate": 2.5, "priority": "low"},
        ],
    ),
    UpgradedStressScenario(
        name="Battery Preservation Bias",
        battery_capacity=420,
        initial_battery=360,
        charge_rate=18,
        full_limit=0.85,
        tasks=[
            {"duration": 20, "drain_rate": 3.2, "priority": "med"},
            {"duration": 15, "drain_rate": 2.8, "priority": "low"},
            {"duration": 40, "drain_rate": 4.2, "priority": "med"},
            {"duration": 50, "drain_rate": 3.0, "priority": "med"},
            {"duration": 30, "drain_rate": 1.2, "priority": "low"},
        ],
    ),
    UpgradedStressScenario(
        name="Skip Non-Critical Heavy Tasks",
        battery_capacity=300,
        initial_battery=120,
        charge_rate=14,
        tasks=[
            {"duration": 80, "drain_rate": 5.0, "priority": "low"},  # Should run only if affordable
            {"duration": 35, "drain_rate": 6.5, "priority": "high"},
            {"duration": 45, "drain_rate": 3.8, "priority": "med"},
            {"duration": 55, "drain_rate": 2.5, "priority": "low"},
            {"duration": 30, "drain_rate": 5.8, "priority": "high"},
        ],
    ),
    UpgradedStressScenario(
        name="High Priority Marathon",
        battery_capacity=350,
        initial_battery=100,
        charge_rate=22,
        tasks=[
            {"duration": 60, "drain_rate": 4.5, "priority": "high"},
            {"duration": 70, "drain_rate": 4.2, "priority": "high"},
            {"duration": 40, "drain_rate": 3.8, "priority": "med"},
            {"duration": 55, "drain_rate": 4.9, "priority": "high"},
            {"duration": 25, "drain_rate": 2.0, "priority": "med"},
        ],
    ),
]


def run_all_tests() -> None:
    print("\n")
    print("╔" + "=" * 94 + "╗")
    print("║" + " " * 22 + "UPGRADED BATTERY SCHEDULER STRESS SUITE" + " " * 21 + "║")
    print("║" + " " * 18 + f"Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 33 + "║")
    print("╚" + "=" * 94 + "╝")

    for scenario in SCENARIOS:
        scenario.run()
        scenario.display()

    _print_summary()


def _print_summary() -> None:
    print("\n")
    print("╔" + "=" * 94 + "╗")
    print("║" + " " * 37 + "SUMMARY" + " " * 43 + "║")
    print("╚" + "=" * 94 + "╝\n")

    total = len(SCENARIOS)
    feasible = sum(1 for s in SCENARIOS if s.result is not None and s.result > 0)
    infeasible = total - feasible

    print(f"Total Scenarios:     {total}")
    print(f"Feasible:            {feasible}")
    print(f"Infeasible:          {infeasible}")

    feasible_set = [s for s in SCENARIOS if s.result is not None and s.result > 0]
    if feasible_set:
        times = [s.result for s in feasible_set]
        durations = [s.analysis["total_duration"] for s in feasible_set]
        overheads = [s.analysis["overhead"] for s in feasible_set]
        efficiencies = [s.analysis["efficiency"] for s in feasible_set]

        print("\nPerformance (feasible)")
        print(f"  Avg Total Time:    {sum(times)/len(times):.2f}s")
        print(f"  Avg Task Time:     {sum(durations)/len(durations):.2f}s")
        print(f"  Avg Overhead:      {sum(overheads)/len(overheads):.2f}s")
        print(f"  Avg Efficiency:    {sum(efficiencies)/len(efficiencies):.1f}%")

    print("\nScenario Status")
    for scenario in SCENARIOS:
        status = "PASS" if scenario.result is not None and scenario.result > 0 else "FAIL"
        print(f"  [{status}] {scenario.name}")

    print(f"\n{'='*96}")
    print("✓ Upgraded scheduler stress testing complete")
    print(f"{'='*96}\n")


def run_specific_scenario(index: int) -> None:
    if 0 <= index < len(SCENARIOS):
        scenario = SCENARIOS[index]
        scenario.run()
        print("\n")
        print("╔" + "=" * 94 + "╗")
        print("║" + " " * 35 + "DETAILED SCENARIO" + " " * 36 + "║")
        print("╚" + "=" * 94 + "╝")
        scenario.display()
    else:
        print(f"Invalid scenario index. Choose between 0 and {len(SCENARIOS) - 1}")


if __name__ == "__main__":
    run_all_tests()
