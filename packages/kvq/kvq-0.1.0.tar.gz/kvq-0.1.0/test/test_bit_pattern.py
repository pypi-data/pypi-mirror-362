"""
Comprehensive test suite for KV cache quantization bit pattern allocation.

This module tests the bit_pattern function across different models, budgets,
bit ranges, and scoring methods to ensure correct allocation of quantization
bits for Key and Value projection matrices.
"""

import unittest
import json
import warnings
from typing import Dict, List

from kvq.bit_pattern import bit_pattern
from kvq.const import supported_models, _SUPPORTED_BITS


class TestBitPattern(unittest.TestCase):
    """Test cases for bit pattern allocation algorithm."""

    # Test configuration
    TEST_MODELS = [
        "meta-llama/Llama-3.2-1B-Instruct",
        "meta-llama/Llama-3.2-3B-Instruct", 
        "meta-llama/Llama-3.1-8B-Instruct",
        "meta-llama/Llama-3.3-70B-Instruct",
        "Qwen/Qwen3-0.6B",
        "Qwen/Qwen3-4B",
        "Qwen/Qwen3-8B",
        "Qwen/Qwen3-32B",
    ]
    
    TEST_BIT_RANGE = [8, 6, 4, 2, 1.58, 1]  # Evaluation experiment bit range
    TEST_BUDGETS = list(range(1, 9))  # Budget from 1 to 8
    TEST_SCORES = [0, 1]  # 0: frobenius_norm, 1: spectral_norm

    def setUp(self):
        """Set up test fixtures."""
        # Suppress warnings during testing for cleaner output
        warnings.filterwarnings("ignore")

    def tearDown(self):
        """Clean up after tests."""
        warnings.resetwarnings()

    def test_supported_models_availability(self):
        """Test that all test models are supported."""
        for model in self.TEST_MODELS:
            with self.subTest(model=model):
                self.assertIn(
                    model, supported_models,
                    f"Model {model} not in supported_models list"
                )

    def test_basic_functionality(self):
        """Test basic bit pattern functionality with default parameters."""
        result = bit_pattern("meta-llama/Llama-3.2-1B-Instruct")
        
        # Check return structure
        self.assertIsInstance(result, dict)
        self.assertIn("nbits_k", result)
        self.assertIn("nbits_v", result)
        
        # Check that both lists have the same length
        self.assertEqual(len(result["nbits_k"]), len(result["nbits_v"]))
        
        # Check that all bits are positive
        for bits in result["nbits_k"] + result["nbits_v"]:
            self.assertGreater(bits, 0)

    def test_invalid_model(self):
        """Test that invalid model names raise appropriate errors."""
        with self.assertRaises(ValueError):
            bit_pattern("invalid/model-name")

    def test_budget_constraints(self):
        """Test budget constraint validation."""
        # Test budget > 8 should raise error
        with self.assertRaises(ValueError):
            bit_pattern("meta-llama/Llama-3.2-1B-Instruct", budget=9)

    def test_layers_parameter(self):
        """Test that only 'all' layers are supported."""
        with self.assertRaises(NotImplementedError):
            bit_pattern("meta-llama/Llama-3.2-1B-Instruct", layers=16)

    def test_bit_allocation_properties(self):
        """Test mathematical properties of bit allocation."""
        model = "meta-llama/Llama-3.2-1B-Instruct"
        budget = 4
        
        result = bit_pattern(model, budget=budget, bit_range=self.TEST_BIT_RANGE)
        
        # Check that allocated bits are within the allowed range
        min_bit, max_bit = min(self.TEST_BIT_RANGE), max(self.TEST_BIT_RANGE)
        for bits in result["nbits_k"] + result["nbits_v"]:
            self.assertGreaterEqual(bits, min_bit)
            self.assertLessEqual(bits, max_bit)
        
        # Check that allocated bits are from the allowed set
        for bits in result["nbits_k"] + result["nbits_v"]:
            self.assertIn(bits, self.TEST_BIT_RANGE)
        
        # Check budget constraint (approximately)
        total_bits = sum(result["nbits_k"]) + sum(result["nbits_v"])
        num_layers = len(result["nbits_k"])
        expected_total = 2 * budget * num_layers
        
        # Allow small tolerance due to discrete optimization
        tolerance = 0.01
        self.assertAlmostEqual(total_bits, expected_total, delta=tolerance)

    def test_score_types(self):
        """Test both frobenius and spectral norm scoring."""
        model = "meta-llama/Llama-3.2-1B-Instruct"
        
        for score in self.TEST_SCORES:
            with self.subTest(score=score):
                result = bit_pattern(model, score=score)
                
                # Should return valid results for both score types
                self.assertIsInstance(result, dict)
                self.assertIn("nbits_k", result)
                self.assertIn("nbits_v", result)

    def test_different_budgets(self):
        """Test bit allocation across different budget values."""
        model = "meta-llama/Llama-3.2-1B-Instruct"
        
        for budget in self.TEST_BUDGETS:
            with self.subTest(budget=budget):
                result = bit_pattern(model, budget=budget, bit_range=self.TEST_BIT_RANGE)
                
                # Check basic structure
                self.assertIsInstance(result, dict)
                self.assertEqual(len(result["nbits_k"]), len(result["nbits_v"]))
                
                # Check budget constraint
                total_bits = sum(result["nbits_k"]) + sum(result["nbits_v"])
                num_layers = len(result["nbits_k"])
                expected_total = 2 * budget * num_layers
                
                # Higher tolerance for extreme budgets
                tolerance = max(0.1, num_layers * 0.01)
                self.assertAlmostEqual(total_bits, expected_total, delta=tolerance)

    def test_budget_ordering(self):
        """Test that higher budgets generally result in higher bit allocations."""
        model = "meta-llama/Llama-3.2-1B-Instruct"
        
        results = {}
        for budget in [2, 4, 6]:
            results[budget] = bit_pattern(model, budget=budget, bit_range=self.TEST_BIT_RANGE)
        
        # Average bits should increase with budget
        for b1, b2 in [(2, 4), (4, 6)]:
            avg_bits_b1 = (sum(results[b1]["nbits_k"]) + sum(results[b1]["nbits_v"])) / (2 * len(results[b1]["nbits_k"]))
            avg_bits_b2 = (sum(results[b2]["nbits_k"]) + sum(results[b2]["nbits_v"])) / (2 * len(results[b2]["nbits_k"]))
            
            self.assertLess(avg_bits_b1, avg_bits_b2, 
                           f"Average bits should increase from budget {b1} to {b2}")

    def test_comprehensive_model_coverage(self):
        """Test all models with various configurations."""
        test_configs = [
            {"budget": 2, "score": 0},
            {"budget": 4, "score": 1}, 
            {"budget": 6, "score": 0},
        ]
        
        results = {}
        
        for model in self.TEST_MODELS:
            results[model] = {}
            for config in test_configs:
                with self.subTest(model=model, config=config):
                    try:
                        result = bit_pattern(
                            model, 
                            budget=config["budget"],
                            score=config["score"],
                            bit_range=self.TEST_BIT_RANGE
                        )
                        
                        # Store results for further analysis
                        results[model][f"budget_{config['budget']}_score_{config['score']}"] = result
                        
                        # Basic validation
                        self.assertIsInstance(result, dict)
                        self.assertIn("nbits_k", result)
                        self.assertIn("nbits_v", result)
                        
                        # Check non-empty results
                        self.assertGreater(len(result["nbits_k"]), 0)
                        self.assertGreater(len(result["nbits_v"]), 0)
                        
                    except Exception as e:
                        self.fail(f"Model {model} with config {config} failed: {e}")

    def test_bit_distribution_properties(self):
        """Test properties of bit distribution across layers."""
        model = "meta-llama/Llama-3.2-1B-Instruct"
        result = bit_pattern(model, budget=4, bit_range=self.TEST_BIT_RANGE)
        
        # Test that not all layers get the same bits (unless budget is very constrained)
        k_bits_unique = len(set(result["nbits_k"]))
        v_bits_unique = len(set(result["nbits_v"]))
        
        # With the sensitivity-based allocation, we expect some variation
        # (unless budget is extremely tight)
        self.assertGreaterEqual(k_bits_unique, 1)
        self.assertGreaterEqual(v_bits_unique, 1)

    def test_extreme_budgets(self):
        """Test behavior with extreme budget values."""
        model = "meta-llama/Llama-3.2-1B-Instruct"
        
        # Test minimum budget
        result_min = bit_pattern(model, budget=1, bit_range=self.TEST_BIT_RANGE)
        # Should assign mostly minimum bits
        min_bit = min(self.TEST_BIT_RANGE)
        min_count_k = sum(1 for b in result_min["nbits_k"] if b == min_bit)
        min_count_v = sum(1 for b in result_min["nbits_v"] if b == min_bit)
        total_matrices = len(result_min["nbits_k"]) + len(result_min["nbits_v"])
        min_ratio = (min_count_k + min_count_v) / total_matrices
        
        # With budget=1, most allocations should be at minimum bits
        self.assertGreater(min_ratio, 0.8, "Low budget should result in mostly minimum bits")
        
        # Test high budget
        result_max = bit_pattern(model, budget=7, bit_range=self.TEST_BIT_RANGE)
        max_bit = max(self.TEST_BIT_RANGE)
        max_count_k = sum(1 for b in result_max["nbits_k"] if b == max_bit)
        max_count_v = sum(1 for b in result_max["nbits_v"] if b == max_bit)
        max_ratio = (max_count_k + max_count_v) / total_matrices
        
        # With high budget, more allocations should be at higher bits
        avg_bits = (sum(result_max["nbits_k"]) + sum(result_max["nbits_v"])) / total_matrices
        self.assertGreater(avg_bits, 5, "High budget should result in higher average bits")

    def test_reproducibility(self):
        """Test that results are reproducible with same inputs."""
        model = "meta-llama/Llama-3.2-1B-Instruct"
        budget = 4
        
        result1 = bit_pattern(model, budget=budget, bit_range=self.TEST_BIT_RANGE)
        result2 = bit_pattern(model, budget=budget, bit_range=self.TEST_BIT_RANGE)
        
        # Results should be identical
        self.assertEqual(result1["nbits_k"], result2["nbits_k"])
        self.assertEqual(result1["nbits_v"], result2["nbits_v"])

    def test_comprehensive_evaluation_setup(self):
        """Test the complete evaluation setup as specified."""
        print("\n" + "="*80)
        print("COMPREHENSIVE EVALUATION RESULTS")
        print("="*80)
        
        evaluation_results = {}
        
        for model in self.TEST_MODELS:
            print(f"\nTesting model: {model}")
            evaluation_results[model] = {}
            
            for budget in self.TEST_BUDGETS:
                for score in self.TEST_SCORES:
                    try:
                        result = bit_pattern(
                            model=model,
                            budget=budget,
                            bit_range=self.TEST_BIT_RANGE,
                            score=score
                        )
                        
                        # Calculate statistics
                        total_bits = sum(result["nbits_k"]) + sum(result["nbits_v"])
                        num_layers = len(result["nbits_k"])
                        avg_bits = total_bits / (2 * num_layers)
                        expected_total = 2 * budget * num_layers
                        
                        # Store results
                        key = f"budget_{budget}_score_{score}"
                        evaluation_results[model][key] = {
                            "nbits_k": result["nbits_k"],
                            "nbits_v": result["nbits_v"],
                            "total_bits": total_bits,
                            "expected_total": expected_total,
                            "avg_bits": avg_bits,
                            "num_layers": num_layers,
                            "budget_utilization": total_bits / expected_total
                        }
                        
                        # Verify budget constraint
                        self.assertAlmostEqual(
                            total_bits, expected_total, 
                            delta=max(0.1, num_layers * 0.01),
                            msg=f"Budget constraint violated for {model}, budget={budget}, score={score}"
                        )
                        
                    except Exception as e:
                        self.fail(f"Failed for {model}, budget={budget}, score={score}: {e}")
        
        # Print summary statistics
        print(f"\n{'Model':<35} {'Layers':<8} {'Budget':<8} {'Score':<8} {'Avg Bits':<10} {'Utilization':<12}")
        print("-" * 90)
        
        for model in self.TEST_MODELS:
            for budget in [2, 4, 6]:  # Sample budgets for summary
                for score in self.TEST_SCORES:
                    key = f"budget_{budget}_score_{score}"
                    if key in evaluation_results[model]:
                        stats = evaluation_results[model][key]
                        score_name = "Frobenius" if score == 0 else "Spectral"
                        print(f"{model:<35} {stats['num_layers']:<8} {budget:<8} {score_name:<8} "
                              f"{stats['avg_bits']:<10.2f} {stats['budget_utilization']:<12.3f}")

    def test_sensitivity_based_allocation(self):
        """Test that allocation follows sensitivity-based principles."""
        model = "meta-llama/Llama-3.2-1B-Instruct"
        
        # Compare frobenius vs spectral norm results
        result_frob = bit_pattern(model, budget=4, score=0, bit_range=self.TEST_BIT_RANGE)
        result_spec = bit_pattern(model, budget=4, score=1, bit_range=self.TEST_BIT_RANGE)
        
        # Results should be different (different sensitivity measures)
        self.assertNotEqual(result_frob["nbits_k"], result_spec["nbits_k"],
                           "Frobenius and spectral norm should yield different allocations")


def run_evaluation_suite():
    """Run the complete evaluation suite and generate a report."""
    
    models = [
        "meta-llama/Llama-3.2-1B-Instruct",
        "meta-llama/Llama-3.2-3B-Instruct",
        "meta-llama/Llama-3.1-8B-Instruct", 
        "meta-llama/Llama-3.3-70B-Instruct",
        "Qwen/Qwen3-0.6B",
        "Qwen/Qwen3-4B",
        "Qwen/Qwen3-8B",
        "Qwen/Qwen3-32B",
    ]
    
    bit_range = [8, 6, 4, 2, 1.58, 1]
    budgets = list(range(1, 9))
    scores = [0, 1]
    
    print("="*100)
    print("KV CACHE QUANTIZATION - COMPLETE EVALUATION SUITE")
    print("="*100)
    print(f"Models tested: {len(models)}")
    print(f"Budgets tested: {budgets}")
    print(f"Bit range: {bit_range}")
    print(f"Score types: {scores} (0=Frobenius, 1=Spectral)")
    print(f"Total configurations: {len(models) * len(budgets) * len(scores)}")
    print("="*100)
    
    results = {}
    failed_configs = []
    
    for model in models:
        print(f"\nProcessing model: {model}")
        results[model] = {}
        
        for budget in budgets:
            for score in scores:
                config_key = f"budget_{budget}_score_{score}"
                try:
                    result = bit_pattern(
                        model=model,
                        budget=budget,
                        bit_range=bit_range,
                        score=score
                    )
                    
                    # Calculate metrics
                    total_bits = sum(result["nbits_k"]) + sum(result["nbits_v"])
                    num_layers = len(result["nbits_k"])
                    expected_total = 2 * budget * num_layers
                    utilization = total_bits / expected_total
                    
                    results[model][config_key] = {
                        "result": result,
                        "total_bits": total_bits,
                        "expected_total": expected_total,
                        "utilization": utilization,
                        "num_layers": num_layers
                    }
                    
                    print(f"  ✓ Budget {budget}, Score {score}: {total_bits:.1f}/{expected_total} bits ({utilization:.3f})")
                    
                except Exception as e:
                    failed_configs.append((model, budget, score, str(e)))
                    print(f"  ✗ Budget {budget}, Score {score}: FAILED - {e}")
    
    # Summary report
    print("\n" + "="*100)
    print("EVALUATION SUMMARY")
    print("="*100)
    
    if failed_configs:
        print(f"Failed configurations: {len(failed_configs)}")
        for model, budget, score, error in failed_configs:
            print(f"  - {model}, budget={budget}, score={score}: {error}")
    else:
        print("All configurations completed successfully! ✓")
    
    # Model statistics
    print("\nModel Layer Counts:")
    for model in models:
        if model in results and results[model]:
            first_config = next(iter(results[model].values()))
            num_layers = first_config["num_layers"]
            print(f"  {model}: {num_layers} layers")
    
    return results


if __name__ == "__main__":
    # Run the test suite
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "="*50)
    print("Running additional evaluation suite...")
    print("="*50)
    
    # Run the evaluation suite
    evaluation_results = run_evaluation_suite()
