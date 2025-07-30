import pytest
import numpy as np
from aidge_core.benchmark.output_wise_comparison import(
    merge_topological_orders,
    compare_outputs,
    RunResult
)

def test_compare_equal_outputs():
    tensor = np.array([1.0, 2.0, 3.0])
    run0 = RunResult({"out": tensor}, ["out"])
    run1 = RunResult({"out": tensor.copy()}, ["out"])
    result = compare_outputs(run0, run1)[0]

    assert result.is_equal is True
    assert result.avg_error == 0.0
    assert result.diff_idx == []
    assert result.diff_error == []

def test_compare_within_tolerance():
    ref = np.array([1.0, 2.0, 3.0])
    test = np.array([1.00001, 2.0001, 3.00001])
    run0 = RunResult({"out": ref}, ["out"])
    run1 = RunResult({"out": test}, ["out"])
    result = compare_outputs(run0, run1, atol=1e-3)[0]

    assert result.is_equal is True
    assert result.avg_error > 0
    assert result.diff_idx == []
    assert result.diff_error == []


def test_compare_exceeds_tolerance():
    ref = np.array([1.0, 2.0, 3.0])
    test = np.array([1.0, 2.5, 2.8])
    run0 = RunResult({"out": ref}, ["out"])
    run1 = RunResult({"out": test}, ["out"])
    result = compare_outputs(run0, run1, atol=1e-3)[0]

    assert result.is_equal is False
    assert result.avg_error > 0
    assert result.diff_idx == [1, 2]
    assert len(result.diff_error) == 2
    assert all(e > 0 for e in result.diff_error)


def test_compare_different_shapes():
    ref = np.array([[1.0, 2.0]])
    test = np.array([1.0, 2.0])
    run0 = RunResult({"out": ref}, ["out"])
    run1 = RunResult({"out": test}, ["out"])
    result = compare_outputs(run0, run1)[0]

    assert result.is_equal is False
    assert result.avg_error == float("inf")
    assert result.diff_idx == []
    assert result.diff_error == []


def test_compare_missing_outputs():
    tensor = np.array([1.0])
    run0 = RunResult({"ref_only": tensor}, ["ref_only"])
    run1 = RunResult({"test_only": tensor}, ["test_only"])
    results = compare_outputs(run0, run1)

    ref_result = next(r for r in results if r.output_name == "ref_only")
    test_result = next(r for r in results if r.output_name == "test_only")

    assert not ref_result.in_test
    assert not test_result.in_ref
    assert ref_result.is_equal is None
    assert ref_result.avg_error is None
    assert ref_result.diff_idx == []
    assert ref_result.diff_error == []

    assert test_result.is_equal is None
    assert test_result.avg_error is None
    assert test_result.diff_idx == []
    assert test_result.diff_error == []

def test_compare_outputs_within_tolerance():
    ref = np.array([1.0, 2.0, 3.0])
    test = np.array([1.0, 2.001, 3.0001])
    run0 = RunResult({"out": ref}, ["out"])
    run1 = RunResult({"out": test}, ["out"])
    results = compare_outputs(run0, run1, atol=1e-3, rtol=1e-2)
    r = results[0]
    assert r.is_equal is True
    assert r.avg_error > 0

def test_compare_outputs_exceed_tolerance():
    ref = np.array([1.0, 2.0])
    test = np.array([1.0, 3.0])
    run0 = RunResult({"out": ref}, ["out"])
    run1 = RunResult({"out": test}, ["out"])
    results = compare_outputs(run0, run1)
    r = results[0]
    assert r.is_equal is False
    assert r.avg_error > 0


# Test topological merge
def test_merge_topological_orders_simple():
    list1 = ["a", "b", "c"]
    list2 = ["a", "c", "d"]
    result = merge_topological_orders(list1, list2)
    # Ensure correct topological order
    assert result.index("a") < result.index("b")
    assert result.index("b") < result.index("c")
    assert result.index("c") < result.index("d")

def test_merge_topological_orders_disjoint():
    list1 = ["a", "b"]
    list2 = ["c", "d"]
    result = merge_topological_orders(list1, list2)
    # All nodes must be in result
    for node in ["a", "b", "c", "d"]:
        assert node in result
    # Preserve individual list orderings
    assert result.index("a") < result.index("b")
    assert result.index("c") < result.index("d")

def test_merge_topological_orders_with_common_node():
    list1 = ["x", "y"]
    list2 = ["y", "z"]
    result = merge_topological_orders(list1, list2)
    assert result.index("x") < result.index("y") < result.index("z")

def test_merge_topological_orders_cycle_detection():
    # These two imply a cycle: a -> b -> a
    list1 = ["a", "b"]
    list2 = ["b", "a"]
    with pytest.raises(ValueError, match="Cycle detected"):
        merge_topological_orders(list1, list2)

def test_merge_topological_orders_empty_lists():
    assert merge_topological_orders([], []) == []

def test_merge_topological_orders_one_empty_list():
    assert merge_topological_orders(["a", "b", "c"], []) == ["a", "b", "c"]
    assert merge_topological_orders([], ["x", "y"]) == ["x", "y"]
