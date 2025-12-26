# Smartwatch Battery Scheduler

A battery scheduling system for smartwatches that optimizes task execution with charging constraints.

## 🚀 Quick Start

### Easiest Way (Menu Interface)
```bash
python main.py
```

### Interactive Modes

#### Upgraded (v2) via menu
```bash
python main.py
```
Choose option "Run upgraded interactive (v2)".

Features:
- Priority-based tasks (`high`, `med`, `low`)
- Charge efficiency modeling (e.g., 0.95)
- Battery health cap (`full_limit`, e.g., 0.90)
- Rolling-window planning

#### Legacy (v1)
```bash
python run_interactive.py
```
or via menu choose "Run interactive mode (legacy v1)".

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
| `run_interactive.py` | 💬 Legacy interactive CLI (v1) |
| `stress_test_upgraded_scheduler.py` | 🔧 v2 stress test suite |
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
Looks ahead and charges for multiple tasks at once.

### Upgraded Smartwatch Battery Scheduler (v2)
- Priority-aware scheduling with critical task protection
- Charge efficiency losses modeled (< 1.0)
- Battery preservation via `full_limit` cap
- Rolling window to plan minimal necessary charge

## Input Format (v2)

- **Battery Capacity**: Maximum battery charge (mAh)
- **Initial Battery**: Starting charge level (mAh)
- **Charge Rate**: Charging speed (mAh/s)
- **Charge Efficiency**: Charging effectiveness (0.5–1.0)
- **Full Limit**: Health cap fraction (0.5–1.0)
- **Tasks**: List of `[duration, drain_rate]` pairs
  - Duration: How long the task runs (seconds)
  - Drain Rate: Power consumption (mAh/s)
  - Priority: `high` | `med` | `low`

## Return Values

- **Positive number**: Total time in seconds to complete all tasks
- **-1**: Impossible (task requires more than battery capacity)

---

## 🧪 Stress Testing (v2)
Run curated stress scenarios for the upgraded scheduler:
```bash
python stress_test_upgraded_scheduler.py
```

---

## 📝 Example Interactive Session
```text
Battery capacity (mAh): 320
Initial battery (0-320 mAh): 140
Charge rate (mAh/s): 15
Charge efficiency (default 0.95): 0.95
Health cap full_limit (default 0.90): 0.90

Task 1 (e.g., 30 2.5 med): 25 3 med
Task 2 (e.g., 30 2.5 med): 40 4.5 high
Task 3 (e.g., 30 2.5 med): 35 2.2 med
Task 4 (e.g., 30 2.5 med): 20 5.5 high
Task 5 (e.g., 30 2.5 med): 15 1.5 low
Task 6 (e.g., 30 2.5 med): 30 3.8 med
Task 7 (e.g., 30 2.5 med): done
```