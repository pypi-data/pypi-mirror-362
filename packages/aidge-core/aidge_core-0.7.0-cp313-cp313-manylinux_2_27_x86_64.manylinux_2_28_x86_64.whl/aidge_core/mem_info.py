import os
import subprocess
import shutil
from pathlib import Path
import aidge_core
from typing import Tuple, List

import matplotlib.pyplot as plt
import aidge_core.mem_info
import numpy as np

# Default memory management, which can be used for development
def compute_default_mem_info(scheduler: aidge_core.Scheduler) -> Tuple[int, List]:
    """Basic memory management concatenate memory block, no memory reuse !

    :param scheduler: Aidge scheduler
    :type scheduler: :py:class:`aidge_core.Scheduler`
    :return: The total memory size (in number of elements) and a list (of size nb node) of list (of size nb output) of dictionnary (size, offset)
    :rtype: Tuple[int, list]
    """
    mem_info = {}
    mem_size = 0

    # Exclude Producers and the last layers (because the results are stored outside the export)
    for i, node in enumerate(scheduler.get_sequential_static_scheduling()):
        if node.type() != "Producer":
            node_mem_info = []
            for out_id in range(node.get_nb_outputs()):
                dims = node.get_operator().get_output(out_id).dims()
                mem = 1
                for dim in dims:
                    mem *= dim

                # Add memeory info
                node_mem_info.append({
                    "size": mem,
                    "offset": mem_size
                })

                # Increment offset for the next layer
                mem_size += mem
            mem_info[node] = node_mem_info
        else:
            mem_info[node] = [] # No meminfo for producer
    return mem_size, mem_info

def log_meminfo(mem_manager:aidge_core.MemoryManager, path: Path, diplay_names:bool):
    """Generate a graph representing the memory allocation of each ouputs.

    Block with the smae color correspond to the same memory plane.

    :param mem_manager: Memory manager to log
    :type mem_manager: aidge_core.memory_manager
    :param path: Path where to save the figure
    :type path: Path
    :param diplay_names: If True Node names are diplayed alongside their block
    :type diplay_names: bool
    """

    max_lifetime = mem_manager.get_max_lifetime()

    # peak_usage in kbytes
    peak_usage = mem_manager.get_peak_usage() / 1024

    # Set figure size 1920x1080 px
    plt.figure(figsize=(19.20, 10.80))
    # Same color for each planes
    colors = plt.cm.viridis(np.linspace(0, 1, len(mem_manager.get_planes()) + 1))
    color_id = 1
    for node, planes in mem_manager.get_planes().items():
        for plane in planes:
            cont_offset    = plane.get_contiguous_offset()
            cont_size      = plane.get_contiguous_size()
            allocated      = plane.mem_space.allocated
            released       = plane.mem_space.released
            is_released    = released >= 0 and not plane.mem_space.dependencies
            x_start        = allocated
            y_start        = cont_offset / 1024.0
            y_end          = (cont_offset + cont_size) / 1024.0
            x_end          = max_lifetime if not is_released else released

            plt.fill_betweenx(
                [y_start, y_end],
                x_start,
                x_end + 1,
                color=colors[color_id % len(colors)]
            )

            if diplay_names:
                # Rotation for lisibility!
                plt.text(x_end,y_end, node.name(), rotation=45)
        color_id += 1

    plt.xlim(0, max_lifetime + 1)
    plt.ylim(0, peak_usage)
    plt.axhline(y=peak_usage, color='red', linestyle='--')
    plt.text(0, peak_usage, f'Peak usage = {peak_usage} KBytes', color='red')
    plt.xlabel("Time")
    plt.ylabel("Memory usage (KBytes)")
    plt.title("Memory Usage Over Time")
    plt.grid(True)
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    folder_path = path.parent
    folder_path.mkdir(parents=True, exist_ok=True)
    plt.savefig(path)
    plt.close()
    aidge_core.Log.notice(f"Generated memory management info at: {path}")

def log_meminfo_text(mem_manager:aidge_core.MemoryManager, path: Path, scheduler: aidge_core.Scheduler = None):
    ordered_planes = []
    if scheduler is not None:
        for node in scheduler.get_sequential_static_scheduling():
            if node in mem_manager.get_planes():
                ordered_planes.append((node, mem_manager.get_planes()[node]))
    else:
        for node, planes in mem_manager.get_planes().items():
            ordered_planes.append((node, planes))

    with open(path, 'w') as mem_data:
        for node, planes in ordered_planes:
            mem_data.write(f"{node.name()}:\n")

            for idx, plane in enumerate(planes):
                contiguous_offset = plane.get_contiguous_offset()
                contiguous_size = plane.get_contiguous_size()
                wrapped_offset = plane.get_wrapped_offset()
                wrapped_size = plane.get_wrapped_size()

                allocated = plane.allocated
                released = plane.mem_space.released
                is_released = released >= 0 and not plane.mem_space.dependencies

                mem_data.write(
                    f"  {idx} {contiguous_offset} "
                    f"(0x{contiguous_offset:08X}U) -> "
                    f"{contiguous_offset + contiguous_size} "
                    f"(0x{contiguous_offset + contiguous_size:08X}U)"
                )

                if wrapped_size > 0:
                    mem_data.write(
                        f" + {wrapped_offset} "
                        f"(0x{wrapped_offset:08X}U) -> "
                        f"{wrapped_offset + wrapped_size} "
                        f"(0x{wrapped_offset + wrapped_size:08X}U)"
                    )

                mem_data.write(
                    f" [{plane.get_size()}] @ {allocated}"
                )

                if is_released:
                    mem_data.write(f" to {released}")

                mem_data.write("\n")

            mem_data.write("\n")

def generate_optimized_memory_info(scheduler: aidge_core.SequentialScheduler, stats_folder: Path = None, wrapping: bool = False, auto_concat: bool = False, display_names: bool=True, mem_optimize_strategy: aidge_core.OptimizeStrategy = None) -> Tuple[int, List[dict]]:
    """Generates optimized memory information for a computation graph managed by a scheduler.

    This function analyzes the memory usage of a computation graph, determining the memory peak
    and detailed memory management information for each node in the scheduler. It supports optional
    wrapping of memory buffers and logs memory usage statistics to facilitate memory optimization.

    :param scheduler: Scheduler instance that organizes the computation graph. It manages the
                      nodes and facilitates memory planning by invoking its `generate_memory` method.
    :type scheduler: aidge_core.Scheduler
    :param stats_folder: Directory path to store memory statistics and plots generated by `mem_manager`.
                         If provided as a string, it is converted to a `Path` object, default=None.
    :type stats_folder: Path, optional
    :param wrapping: Boolean flag to enable or disable wrap-around buffer optimization.
                     Defaults to `False`.
    :type wrapping: bool, optional
    :param auto_concat: Boolean flag to enable or disable auto-concatenation optimization.
                     Defaults to `False`.
    :type auto_concat: bool, optional
    :param diplay_names: If True Node names are diplayed in the memory plot alongside their block, defaults to False
    :type diplay_names: bool, optional
    :return: A tuple containing the peak memory size and a list of memory information for each
             scheduled node. The memory information for each node includes details such as size,
             offset, stride, length, count, and optional wrap-around details.
    :rtype: Tuple[int, List[dict]]
    """
    # The forward dims has to done outside the function
    # Also supposed the generation of the scheduler has been performed outside
    # Otherwise decomment the following line
    # scheduler.generate_scheduling()
    # Generate the memory manager
    # So far, the Producers are not take in consideration in the meory manager => inc_producers=False
    if auto_concat:
        mem_manager = scheduler.generate_memory_auto_concat(
            inc_producers=False, wrap_around_buffer=wrapping)
    else:
        mem_manager = scheduler.generate_memory(
            inc_producers=False, wrap_around_buffer=wrapping)
    if mem_optimize_strategy != None:
        mem_manager.optimize(mem_optimize_strategy)

    if stats_folder is not None:
        log_meminfo(mem_manager, Path(stats_folder) / "memory_info.png", display_names)
        log_meminfo_text(mem_manager, Path(stats_folder) / "memory_info.txt", scheduler)

    # In the export, we currently use an unified memory buffer whose size
    # is determined by the memory peak usage
    mem_size = mem_manager.get_peak_usage()
    mem_info = {}

    mem_planes = mem_manager.get_planes()

    for node in scheduler.get_sequential_static_scheduling():
        node_mem_info = []
        if node in mem_planes:
            for out_id in range(node.get_nb_outputs()):
                if out_id < len(mem_planes[node]):
                    plane = mem_planes[node][out_id]
                    node_mem_info.append({
                        "size": plane.size,
                        "offset": plane.get_contiguous_offset(),
                        "stride": plane.stride,
                        "length": plane.length,
                        "count": plane.count,
                        "cont_offset": plane.get_contiguous_offset(),
                        "cont_size": plane.get_contiguous_size(),
                        "wrap_offset": plane.get_wrapped_offset(),
                        "wrap_size": plane.get_wrapped_size()
                    })
                else:
                    # If the node output is not in the memory planes, it means 
                    # it is likely ignored (unused optional output).
                    node_mem_info.append({
                        "size": 0,
                        "offset": 0,
                        "stride": 0,
                        "length": 0,
                        "count": 0,
                        "cont_offset": 0,
                        "cont_size": 0,
                        "wrap_offset": 0,
                        "wrap_size": 0
                    })
        else:
            # Memory allocated outside the memory manager
            for out_id in range(node.get_nb_outputs()):
                tensor = node.get_operator().get_output(out_id)
                if tensor is None:
                    continue
                sizeof = (aidge_core.dtype_bit_width(tensor.dtype()) + 8 - 1) // 8

                if tensor.dformat() == aidge_core.dformat.nhwc or tensor.dformat() == aidge_core.dformat.nwc:
                    node_mem_info.append({
                            "size": tensor.dims()[-1] * sizeof,
                            "offset": 0, # Standalone pointer: offset = 0
                            "stride": tensor.dims()[-1] * sizeof,
                            "length": tensor.dims()[-2],
                            "count":  tensor.size() // (tensor.dims()[-1] * tensor.dims()[-2]),
                            "cont_offset": 0, # Standalone pointer: offset = 0
                            "cont_size": tensor.size(),
                            "wrap_offset": 0, # Standalone pointer: no wrapping
                            "wrap_size": 0 # Standalone pointer: no wrapping
                        })
                else:
                    node_mem_info.append({
                            "size": tensor.size() * sizeof,
                            "offset": 0, # Standalone pointer: offset = 0
                            "stride": tensor.size() * sizeof,
                            "length": 1,
                            "count":  1,
                            "cont_offset": 0, # Standalone pointer: offset = 0
                            "cont_size": tensor.size() * sizeof,
                            "wrap_offset": 0, # Standalone pointer: no wrapping
                            "wrap_size": 0 # Standalone pointer: no wrapping
                        })

        mem_info[node] = node_mem_info
    return mem_size, mem_info


