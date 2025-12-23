"""
Comprehensive test suite for battery scheduling algorithms
"""

from battery_scheduler import greedy_algorithm, segmented_charge_planner


def test_optimality():
    """Compare greedy vs SCP on various scenarios"""
    print("=" * 80)
    print("OPTIMALITY TESTING: Greedy vs SCP")
    print("=" * 80)
    
    test_cases = [
        ("Single task, no charge", 100, 50, [[10, 4]], 2),
        ("Single task, need charge", 100, 20, [[10, 4]], 2),
        ("Two tasks, no charge", 100, 100, [[10, 4], [10, 4]], 2),
        ("Three light tasks", 100, 50, [[10, 4], [10, 4], [10, 4]], 2),
        ("Mixed drain rates", 100, 30, [[10, 3], [15, 4], [20, 2]], 5),
        ("Impossible task", 50, 50, [[20, 5]], 2),
        ("Zero charge rate", 100, 0, [[50, 1]], 0),
        ("Exact capacity needed", 100, 10, [[10, 10]], 5),
        ("Many small tasks", 100, 50, [[5, 2]] * 10, 3),
        ("Alternating loads", 200, 100, [[10, 5], [5, 2], [10, 5], [5, 2]], 10),
    ]
    
    all_match = True
    mismatches = []
    
    for name, capacity, initial, tasks, rate in test_cases:
        greedy_result = greedy_algorithm(capacity, initial, tasks, rate)
        scp_result = segmented_charge_planner(capacity, initial, tasks, rate)
        
        match = abs(greedy_result - scp_result) < 0.01
        status = "✓" if match else "✗"
        
        print(f"\n{status} {name}")
        print(f"   Greedy: {greedy_result}s")
        print(f"   SCP:    {scp_result}s")
        
        if not match:
            all_match = False
            mismatches.append((name, greedy_result, scp_result))
            print(f"   ⚠️  Mismatch: Δ = {abs(greedy_result - scp_result)}s")
    
    print("\n" + "=" * 80)
    if all_match:
        print("✅ Both algorithms produce identical results")
    else:
        print(f"❌ Found {len(mismatches)} mismatches")
        for name, greedy, scp in mismatches:
            print(f"   - {name}: Greedy={greedy}, SCP={scp}")
    
    return all_match


def test_edge_cases():
    """Test boundary conditions and weird inputs"""
    print("\n" + "=" * 80)
    print("EDGE CASE TESTING")
    print("=" * 80)
    
    edge_cases = [
        ("Empty task list", 100, 50, [], 2, 0.0),
        ("Zero initial battery", 100, 0, [[10, 5]], 5, 20.0),
        ("Full battery", 100, 100, [[10, 5]], 5, 10.0),
        ("Zero drain task", 100, 50, [[10, 0]], 5, 10.0),
        ("Task = exact capacity", 100, 0, [[10, 10]], 10, 20.0),
        ("Task > capacity", 100, 100, [[20, 10]], 5, -1.0),
        ("Zero charge rate", 100, 50, [[10, 1]], 0, -1.0),
        ("Tiny values", 1.0, 0.5, [[0.1, 1]], 1, 0.6),
        ("Float precision", 100.0, 33.33, [[7.77, 4.44]], 2.22, 18.1),
    ]
    
    all_pass = True
    
    for name, capacity, initial, tasks, rate, expected in edge_cases:
        greedy_result = greedy_algorithm(capacity, initial, tasks, rate)
        scp_result = segmented_charge_planner(capacity, initial, tasks, rate)
        
        greedy_ok = abs(greedy_result - expected) < 0.2
        scp_ok = abs(scp_result - expected) < 0.2
        both_match = abs(greedy_result - scp_result) < 0.1
        
        status = "✓" if (greedy_ok and scp_ok and both_match) else "✗"
        
        print(f"\n{status} {name}")
        print(f"   Expected: {expected}s")
        print(f"   Greedy:   {greedy_result}s")
        print(f"   SCP:      {scp_result}s")
        
        if not both_match:
            all_pass = False
            print(f"   ⚠️  Algorithms don't match!")
    
    return all_pass


def trace_execution(algorithm_name, algorithm_func, capacity, initial, tasks, rate):
    """Show step-by-step execution of an algorithm"""
    print("\n" + "=" * 80)
    print(f"EXECUTION TRACE: {algorithm_name}")
    print("=" * 80)
    print(f"Battery Capacity: {capacity} mAh")
    print(f"Initial Battery: {initial} mAh")
    print(f"Charge Rate: {rate} mAh/s")
    print(f"Tasks: {tasks}")
    print()
    
    result = algorithm_func(capacity, initial, tasks, rate)
    
    print(f"\nFinal Result: {result}s")
    return result


def run_all_tests():
    """Run the complete test suite"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════════╗")
    print("║         BATTERY SCHEDULER - COMPLETE TEST SUITE                      ║")
    print("╚═══════════════════════════════════════════════════════════════════════╝")
    print()
    
    optimality_pass = test_optimality()
    edge_case_pass = test_edge_cases()
    
    # Show a detailed trace example
    print("\n" + "=" * 80)
    print("DETAILED TRACE EXAMPLE")
    print("=" * 80)
    test_case = (100, 30, [[10, 4], [15, 3], [20, 2]], 5)
    trace_execution("Greedy", greedy_algorithm, *test_case)
    trace_execution("SCP", segmented_charge_planner, *test_case)
    
    # Final verdict
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    if optimality_pass and edge_case_pass:
        print("✅ All tests passed!")
        print("   Both algorithms are correct and optimal")
    else:
        print("⚠️  Some tests failed - review results above")
    
    return optimality_pass and edge_case_pass


if __name__ == "__main__":
    run_all_tests()
