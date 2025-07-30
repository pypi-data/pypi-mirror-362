import aidge_core
from pathlib import Path

import numpy as np

from typing import Dict, Optional, List, Union
from dataclasses import dataclass
from collections import defaultdict, deque
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

"""This script defines a data structures OutputTensorMap that hold the intermediate results of each output of a graph, A function to generate an OutputTensorMap with any aidge backend has been made available with run_aidge_inferences. It also defines function to compare two OutputTensorMap, generating for each output an OutputComparison which hold wether or not the outputs are the same. Each output comparison are aggregated in a list ComparisonResult which can be parsed to render the result of the test in a tabular fashion.
"""

# Define data structures
OutputName = str
TensorValue = np.ndarray
OutputTensorMap = Dict[OutputName, TensorValue]

@dataclass
class RunResult:
    """Hold the result of the test
    """
    edge_tensor_map: OutputTensorMap
    topological_order: List[OutputName]

@dataclass
class OutputComparison:
    # Name of the output
    output_name: OutputName
    # Wether or not it is in the reference
    in_ref: bool
    # Wether or not it is in the test
    in_test: bool
    # Wether or not both run result are equal
    # If the output is in one model but not in the other
    # is_equal is None
    is_equal: Optional[bool]
    # The average error
    # If the output is in one model but not in the other
    # avg_error is None
    avg_error: Optional[float]
    # Index of different values
    diff_idx: List[int]
    # List of error values (the order match the diff_idx list)
    # The error is defined as abs(val0 - val1)
    diff_error: List[float]
    # Reference tensor
    # If is_equal = False, the reference value is saved
    ref_val: Optional[np.ndarray]
    # Test tensor
    # If is_equal = False, the test value is saved
    test_val: Optional[np.ndarray]

ComparisonResult = List[OutputComparison]

def run_aidge_outputwise_benchmark(
        graph_view: aidge_core.GraphView,
        inputs: Dict[str, np.ndarray],
        backend="cpu") -> RunResult:

    if len(inputs) != 1:
        raise ValueError("Current script only support onnx with one input")
    else:
        input_val = next(iter(inputs.values()))
        input_name = next(iter(inputs.keys()))
        input_tensor = aidge_core.Tensor(np.array(input_val))
        input_node = aidge_core.Producer(input_tensor, f"{input_name}")
        graph_inputs_list = []
        for graph_input in graph_view.get_ordered_inputs():
            if graph_input[0].get_operator().is_optional_input(graph_input[1]): continue
            graph_inputs_list.append(graph_input)
        if len(graph_inputs_list) != 1: raise ValueError("Current script only support onnx with one input")
        input_node.add_child(graph_view, 0, graph_inputs_list[0])
        graph_view.add(input_node)
    graph_view.set_backend(backend)
    graph_view.forward_dtype()
    graph_view.forward_dims()
    scheduler = aidge_core.SequentialScheduler(graph_view)
    scheduler.forward(False)
    return RunResult(
        edge_tensor_map={n.output_name(i): np.array(n.get_operator().get_output(i)) for n in graph_view.get_nodes() for i in range(n.get_nb_outputs()) if n.type() != "Producer"},
        topological_order=[n.output_name(i) for n in scheduler.get_sequential_static_scheduling() for i in range(n.get_nb_outputs()) if n.type() != "Producer"]
    )



# Utils function to merge two ordered list
def merge_topological_orders(list1: List[OutputName], list2: List[OutputName]) -> List[OutputName]:
    """Given two topological orders with missing nodes in either of one.
    Return a list that preserve the topological order and with the missing nodes in between.
    For example: ["a", "b", "c"] + ["a", "c", "d"] = ["a", "b", "c", "d"].

    Raise ValueError if the graphs are cyclic.
    """
    # Build the graph from the pairwise orderings in both lists
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    nodes = set()

    def add_edges(lst):
        for i in range(len(lst) - 1):
            u, v = lst[i], lst[i + 1]
            if v not in graph[u]:  # Avoid duplicate edges
                graph[u].add(v)
                in_degree[v] += 1
            nodes.add(u)
            nodes.add(v)
        if lst:
            nodes.add(lst[-1])

    add_edges(list1)
    add_edges(list2)

    # Initialize in-degrees for all nodes
    for node in nodes:
        in_degree.setdefault(node, 0)

    # Topological sort (Kahn's algorithm)
    queue = deque([node for node in nodes if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycles
    if len(result) != len(nodes):
        raise ValueError("Cycle detected, input lists are not compatible topological orderings.")
    return result

# Benchmark function
def compare_outputs(
        ref_result: RunResult,
        test_result: RunResult,
        atol: Optional[float] =1e-5,
        rtol: Optional[float]=1e-3) -> ComparisonResult:
    """Given two benchmark results (`RunResults`), return a comparison output wise stored in `ComparisonResult`.
    """
    tensor_map_ref = ref_result.edge_tensor_map
    topological_order_ref = ref_result.topological_order
    tensor_map_test = test_result.edge_tensor_map
    topological_order_test = test_result.topological_order
    results: ComparisonResult = []
    try:
        topo_order = merge_topological_orders(topological_order_ref, topological_order_test)
    except ValueError as e:
        # If clean merge fail resort to random list
        aidge_core.Log.notice(f"Failed to merge topologically, due to Exception:\n{e}\nOutputs will be displayed in a random order.")
        topo_order = sorted(
            set(tensor_map_ref.keys()) | set(tensor_map_test.keys())
        )
    for key in topo_order:
        in_ref = key in tensor_map_ref
        in_test = key in tensor_map_test
        is_equal = None
        avg_error = None
        diff_idx = []
        diff_error = []
        saved_ref_value = None
        saved_test_value = None
        if in_ref and in_test:
            ref = tensor_map_ref[key]
            test = tensor_map_test[key]
            if ref.shape == test.shape:
                abs_error = np.abs(ref - test)
                is_equal = np.allclose(ref, test, atol=atol, rtol=rtol)
                avg_error = np.mean(abs_error)
                mask = ~np.isclose(ref, test, atol=atol, rtol=rtol)
                flat_mask = mask.flatten()
                flat_abs_error = abs_error.flatten()
                diff_idx = np.nonzero(flat_mask)[0].tolist()
                diff_error = flat_abs_error[flat_mask].tolist()
                saved_ref_value = ref.copy()
                saved_test_value = test.copy()
            else:
                is_equal = False
                avg_error = float("inf")

        results.append(OutputComparison(
            output_name=key,
            in_ref=in_ref,
            in_test=in_test,
            is_equal=is_equal,
            avg_error=avg_error,
            diff_idx=diff_idx,
            diff_error=diff_error,
            ref_val=saved_ref_value,
            test_val=saved_test_value,
        ))

    return results



# Rendering functions
def render_results_table(results:ComparisonResult,
                         framework_0_name: str,
                         framework_1_name: str,
                         model_name: str) -> None:
    framework_0_only = 0
    framework_0_edges = 0
    framework_1_only = 0
    framework_1_edges = 0
    matches = 0
    mismatches = 0

    table = Table(title=f"{framework_0_name} vs {framework_1_name} Inference Comparison for {model_name}")
    table.add_column("Edge Name", style="cyan")
    table.add_column(f"{framework_0_name}", justify="center")
    table.add_column(f"{framework_1_name}", justify="center")
    table.add_column("Equal", justify="center")
    table.add_column("Avg Error", justify="right")

    for edge_comparison in results:
        output_name = edge_comparison.output_name
        in_ref = edge_comparison.in_ref
        in_test = edge_comparison.in_test
        is_equal = edge_comparison.is_equal
        avg_error = edge_comparison.avg_error

        table.add_row(
            output_name, #
            "✅" if in_ref else "❌",
            "✅" if in_test else "❌",
            "N/A" if is_equal is None else "✅" if is_equal else "❌",
            f"{avg_error:.4e}" if avg_error is not None else "N/A"
        )

        framework_1_edges += in_test
        framework_0_edges += in_ref
        if in_ref and not in_test:
            framework_0_only += 1
        elif in_test and not in_ref:
            framework_1_only += 1
        elif in_ref and in_test:
            if is_equal:
                matches += 1
            else:
                mismatches += 1

    console = Console()
    console.print(table)

    # Summary panel
    summary = (
        f"[bold yellow]{framework_0_name} edges with no {framework_1_name} is_equal:[/bold yellow] {framework_0_only} / {framework_0_edges} ({((framework_0_only / framework_0_edges)*100):.2e}%)\n"
        f"[bold magenta]Aidge edges with no ONNX is_equal:[/bold magenta] {framework_1_only} / {framework_1_edges} ({((framework_1_only / framework_1_edges)*100):.2e}%)\n"
        f"[bold green]Matching outputs:[/bold green] {matches}\n"
        f"[bold red]Mismatching outputs:[/bold red] {mismatches}"
    )
    console.print(Panel(summary, title=f"Comparison Summary for {model_name} ({framework_0_name} vs {framework_1_name})", expand=False))

def save_comparison_differences(
        comparison_result: ComparisonResult,
        output_dir: str = "output_comparison") -> None:
    output_dir = Path(output_dir)
    for comp in comparison_result:
        if comp.in_ref and comp.in_test and not comp.is_equal:
            output_dir.mkdir(parents=True, exist_ok=True)
            file_path = output_dir / f"{comp.output_name}.txt"
            flatten_ref  = comp.ref_val.flatten()
            flatten_test = comp.test_val.flatten()
            with file_path.open("w") as f:
                for idx, err in zip(comp.diff_idx, comp.diff_error):
                    f.write(f"{idx}; {err}; {flatten_ref[idx]}; {flatten_test[idx]}\n")