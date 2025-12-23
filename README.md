# Smartwatch Battery Scheduler

A battery scheduling system for smartwatches that optimizes task execution with charging constraints.

## 🚀 Quick Start

### Easiest Way (Menu Interface)
```bash
python main.py
```

### Interactive Mode (User Input)
```bash
python run_interactive.py
```

### Run Tests
```bash
python test_battery_scheduler.py
```

### View Examples
```bash
python examples.py
```

---

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `main.py` | 🚀 Main launcher with menu |
| `battery_scheduler.py` | ⚙️ Core algorithms |
| `utils.py` | 🛠️ Helper functions |
| `test_battery_scheduler.py` | ✅ Test suite |
| `run_interactive.py` | 💬 Interactive CLI |
| `examples.py` | 📚 Usage examples |

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for details.

---

## 💡 Usage Examples

### As a Library
Import and use the algorithms directly:
```python
from battery_scheduler import greedy_algorithm, segmented_charge_planner

tasks = [[10, 4], [15, 3], [20, 2]]  # [duration, drain_rate]
time = greedy_algorithm(
    battery_capacity=100,
    initial_battery=30,
    tasks=tasks,
    charge_rate=5
)
print(f"Total time: {time}s")
```

## Algorithms

### Greedy Algorithm
Charges before each task as needed. Simple and optimal for sequential task execution.

### Segmented Charge Planning (SCP)
Looks ahead and charges for multiple tasks at once. More realistic for modern devices.

Both algorithms produce identical optimal results but model different charging behaviors.

## Input Format

- **Battery Capacity**: Maximum battery charge (mAh)
- **Initial Battery**: Starting charge level (mAh)
- **Charge Rate**: Charging speed (mAh/s)
- **Tasks**: List of `[duration, drain_rate]` pairs
  - Duration: How long the task runs (seconds)
  - Drain Rate: Power consumption (mAh/s)

## Return Values

- **Positive number**: Total time in seconds to complete all tasks
- **-1**: Impossible (task requires more than battery capacity)