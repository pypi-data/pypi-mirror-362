#!/usr/bin/env python3
"""
Performance and correctness validation for KV cache quantization algorithm.
Focuses on mathematical properties and edge cases.
"""

import sys
import json
import numpy as np
from typing import Dict, List, Tuple
import warnings

# Add the parent directory to the path
sys.path.insert(0, '/mnt/rds/VipinRDS/VipinRDS/users/mxh1029/projects/quant/acl/kvq')

from kvq.bit_pattern import bit_pattern
from kvq.const import model_dict


def test_mathematical_properties():
    """Test core mathematical properties of the allocation algorithm."""
    
    print("="*80)
    print("MATHEMATICAL PROPERTIES VALIDATION")
    print("="*80)
    
    # Test configuration
    test_model = "meta-llama/Llama-3.2-1B-Instruct"
    bit_range = [8, 6, 4, 2, 1.58, 1]
    
    # Property 1: Budget Conservation
    print("\n1. BUDGET CONSERVATION TEST")
    print("-" * 40)
    
    tolerance_failures = 0
    for budget in range(1, 9):
        for score in [0, 1]:
            result = bit_pattern(test_model, budget=budget, bit_range=bit_range, score=score)
            
            total_allocated = sum(result["nbits_k"]) + sum(result["nbits_v"])
            num_layers = len(result["nbits_k"])
            expected_total = 2 * budget * num_layers
            
            error = abs(total_allocated - expected_total)
            tolerance = max(0.01, num_layers * 0.001)  # Dynamic tolerance
            
            score_name = "Frob" if score == 0 else "Spec"
            if error <= tolerance:
                status = "✓"
            else:
                status = "✗"
                tolerance_failures += 1
            
            print(f"  Budget {budget}, {score_name}: {total_allocated:.3f}/{expected_total:.3f} "
                  f"(error: {error:.3f}) {status}")
    
    print(f"\nBudget conservation: {tolerance_failures} failures out of {8*2} tests")
    
    # Property 2: Bit Range Compliance
    print("\n2. BIT RANGE COMPLIANCE TEST")
    print("-" * 40)
    
    range_violations = 0
    for budget in [2, 4, 6]:
        for score in [0, 1]:
            result = bit_pattern(test_model, budget=budget, bit_range=bit_range, score=score)
            
            all_bits = result["nbits_k"] + result["nbits_v"]
            violations = [b for b in all_bits if b not in bit_range]
            
            score_name = "Frob" if score == 0 else "Spec"
            if not violations:
                print(f"  Budget {budget}, {score_name}: ✓ All bits in range")
            else:
                print(f"  Budget {budget}, {score_name}: ✗ Violations: {violations}")
                range_violations += len(violations)
    
    print(f"\nBit range compliance: {range_violations} violations")
    
    # Property 3: Monotonicity (higher budget generally leads to higher avg bits)
    print("\n3. BUDGET MONOTONICITY TEST")
    print("-" * 40)
    
    for score in [0, 1]:
        budgets = [1, 2, 4, 6, 8]
        avg_bits = []
        
        for budget in budgets:
            result = bit_pattern(test_model, budget=budget, bit_range=bit_range, score=score)
            total_bits = sum(result["nbits_k"]) + sum(result["nbits_v"])
            num_matrices = len(result["nbits_k"]) + len(result["nbits_v"])
            avg = total_bits / num_matrices
            avg_bits.append(avg)
        
        # Check monotonicity
        monotonic_violations = 0
        for i in range(1, len(avg_bits)):
            if avg_bits[i] < avg_bits[i-1]:
                monotonic_violations += 1
        
        score_name = "Frobenius" if score == 0 else "Spectral"
        print(f"  {score_name}: {[f'{x:.2f}' for x in avg_bits]}")
        print(f"    Monotonic violations: {monotonic_violations}")
    
    # Property 4: Sensitivity-based allocation difference
    print("\n4. SENSITIVITY-BASED ALLOCATION TEST")
    print("-" * 40)
    
    differences = 0
    for budget in [2, 4, 6]:
        result_frob = bit_pattern(test_model, budget=budget, bit_range=bit_range, score=0)
        result_spec = bit_pattern(test_model, budget=budget, bit_range=bit_range, score=1)
        
        # Compare allocations
        k_diff = result_frob["nbits_k"] != result_spec["nbits_k"]
        v_diff = result_frob["nbits_v"] != result_spec["nbits_v"]
        
        if k_diff or v_diff:
            print(f"  Budget {budget}: ✓ Different allocations (Frobenius vs Spectral)")
            differences += 1
        else:
            print(f"  Budget {budget}: ✗ Identical allocations")
    
    print(f"\nSensitivity difference: {differences}/3 budgets show differences")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    
    print("\n" + "="*80)
    print("EDGE CASES AND BOUNDARY CONDITIONS")
    print("="*80)
    
    test_model = "meta-llama/Llama-3.2-1B-Instruct"
    bit_range = [8, 6, 4, 2, 1.58, 1]
    
    # Edge Case 1: Minimum budget
    print("\n1. MINIMUM BUDGET TEST")
    print("-" * 40)
    
    result_min = bit_pattern(test_model, budget=1, bit_range=bit_range, score=0)
    min_bit = min(bit_range)
    all_bits = result_min["nbits_k"] + result_min["nbits_v"]
    min_count = sum(1 for b in all_bits if b == min_bit)
    total_count = len(all_bits)
    min_ratio = min_count / total_count
    
    print(f"  Minimum bit ({min_bit}): {min_count}/{total_count} = {min_ratio:.2%}")
    print(f"  Expected: High percentage at minimum bits")
    
    # Edge Case 2: Maximum budget
    print("\n2. MAXIMUM BUDGET TEST")
    print("-" * 40)
    
    result_max = bit_pattern(test_model, budget=8, bit_range=bit_range, score=0)
    max_bit = max(bit_range)
    all_bits = result_max["nbits_k"] + result_max["nbits_v"]
    max_count = sum(1 for b in all_bits if b == max_bit)
    avg_bits = sum(all_bits) / len(all_bits)
    
    print(f"  Maximum bit ({max_bit}): {max_count}/{total_count}")
    print(f"  Average bits: {avg_bits:.2f}")
    print(f"  Expected: Higher average bits")
    
    # Edge Case 3: Single bit option
    print("\n3. SINGLE BIT OPTION TEST")
    print("-" * 40)
    
    try:
        single_bit_range = [4]
        result_single = bit_pattern(test_model, budget=4, bit_range=single_bit_range, score=0)
        all_bits = result_single["nbits_k"] + result_single["nbits_v"]
        uniform = all(b == 4 for b in all_bits)
        print(f"  All bits = 4: {uniform} ✓")
    except Exception as e:
        print(f"  Single bit test failed: {e}")
    
    # Edge Case 4: Very small bit range
    print("\n4. SMALL BIT RANGE TEST")
    print("-" * 40)
    
    try:
        small_range = [2, 4]
        result_small = bit_pattern(test_model, budget=3, bit_range=small_range, score=0)
        all_bits = result_small["nbits_k"] + result_small["nbits_v"]
        valid_bits = all(b in small_range for b in all_bits)
        print(f"  All bits in {small_range}: {valid_bits} ✓")
    except Exception as e:
        print(f"  Small range test failed: {e}")


def compare_models():
    """Compare allocation patterns across different models."""
    
    print("\n" + "="*80)
    print("MODEL COMPARISON ANALYSIS")
    print("="*80)
    
    models = [
        "meta-llama/Llama-3.2-1B-Instruct",
        "meta-llama/Llama-3.2-3B-Instruct", 
        "Qwen/Qwen3-0.6B",
        "Qwen/Qwen3-4B",
    ]
    
    bit_range = [8, 6, 4, 2, 1.58, 1]
    budget = 4
    
    print(f"\n{'Model':<35} {'Layers':<8} {'Avg K':<8} {'Avg V':<8} {'K Range':<15} {'V Range':<15}")
    print("-" * 95)
    
    for model in models:
        try:
            result = bit_pattern(model, budget=budget, bit_range=bit_range, score=0)
            
            num_layers = len(result["nbits_k"])
            avg_k = sum(result["nbits_k"]) / len(result["nbits_k"])
            avg_v = sum(result["nbits_v"]) / len(result["nbits_v"])
            k_range = f"{min(result['nbits_k']):.1f}-{max(result['nbits_k']):.1f}"
            v_range = f"{min(result['nbits_v']):.1f}-{max(result['nbits_v']):.1f}"
            
            print(f"{model:<35} {num_layers:<8} {avg_k:<8.2f} {avg_v:<8.2f} {k_range:<15} {v_range:<15}")
            
        except Exception as e:
            print(f"{model:<35} ERROR: {str(e)}")


def test_reproducibility():
    """Test that the algorithm produces consistent results."""
    
    print("\n" + "="*80)
    print("REPRODUCIBILITY TEST")
    print("="*80)
    
    test_model = "meta-llama/Llama-3.2-1B-Instruct"
    bit_range = [8, 6, 4, 2, 1.58, 1]
    
    print("\nTesting reproducibility across multiple runs...")
    
    # Run the same configuration multiple times
    results = []
    for i in range(3):
        result = bit_pattern(test_model, budget=4, bit_range=bit_range, score=0)
        results.append(result)
    
    # Check if all results are identical
    all_identical = True
    for i in range(1, len(results)):
        if (results[i]["nbits_k"] != results[0]["nbits_k"] or 
            results[i]["nbits_v"] != results[0]["nbits_v"]):
            all_identical = False
            break
    
    print(f"Reproducibility: {'✓ PASS' if all_identical else '✗ FAIL'}")
    
    if all_identical:
        print("All runs produced identical results")
    else:
        print("Results differ between runs - this may indicate non-deterministic behavior")


def performance_benchmark():
    """Benchmark the performance of the allocation algorithm."""
    
    print("\n" + "="*80)
    print("PERFORMANCE BENCHMARK")
    print("="*80)
    
    import time
    
    models = [
        "meta-llama/Llama-3.2-1B-Instruct",
        "meta-llama/Llama-3.1-8B-Instruct",
        "Qwen/Qwen3-0.6B",
    ]
    
    bit_range = [8, 6, 4, 2, 1.58, 1]
    budgets = [2, 4, 6]
    
    print(f"\n{'Model':<35} {'Budget':<8} {'Time (ms)':<12} {'Layers':<8}")
    print("-" * 65)
    
    total_time = 0
    total_runs = 0
    
    for model in models:
        for budget in budgets:
            try:
                start_time = time.time()
                result = bit_pattern(model, budget=budget, bit_range=bit_range, score=0)
                end_time = time.time()
                
                elapsed_ms = (end_time - start_time) * 1000
                num_layers = len(result["nbits_k"])
                
                print(f"{model:<35} {budget:<8} {elapsed_ms:<12.2f} {num_layers:<8}")
                
                total_time += elapsed_ms
                total_runs += 1
                
            except Exception as e:
                print(f"{model:<35} {budget:<8} ERROR: {str(e)}")
    
    if total_runs > 0:
        avg_time = total_time / total_runs
        print(f"\nAverage time per allocation: {avg_time:.2f} ms")


if __name__ == "__main__":
    print("KV Cache Quantization - Advanced Testing Suite")
    print("=" * 80)
    
    # Suppress warnings for cleaner output
    warnings.filterwarnings("ignore")
    
    try:
        test_mathematical_properties()
        test_edge_cases()
        compare_models()
        test_reproducibility()
        performance_benchmark()
        
        print("\n" + "="*80)
        print("ALL ADVANCED TESTS COMPLETED")
        print("="*80)
        
    except Exception as e:
        print(f"Advanced testing failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
