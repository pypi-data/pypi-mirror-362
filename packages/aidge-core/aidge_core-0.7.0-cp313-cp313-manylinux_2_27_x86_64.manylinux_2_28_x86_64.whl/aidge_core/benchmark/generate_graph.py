import argparse
import json
import sys
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import manage_config

# Set a default style
sns.set_theme(style="ticks", palette="flare")


def parse_args():
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--show-available-config", action="store_true")
    known_args, _ = pre_parser.parse_known_args()

    # Handle --show-available-config early and exit
    if known_args.show_available_config:
        manage_config.show_available_config()
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="Compare time performance of operator kernels by plotting relative differences."
    )
    parser.add_argument(
        "--config-file",
        "-cf",
        type=str,
        help="Path to a JSON configuration file containing an ONNX operator description with reference and tested parameter values."
    )
    parser.add_argument(
        "--results-directory", type = str, default="benchmark_results",
        help="Directory to add to the search path for results."
    )
    parser.add_argument(
        "--ref", "-r", type=str, required=True,
        help="Path to the JSON file with reference results"
    )
    parser.add_argument(
        "--libs", "-l", type=str, nargs='+', required=True,
        help=("Paths to one or more JSON files with benchmark results.")
    )
    return parser.parse_args()


def compute_pairwise_ratios(
    test_parameters: dict[str, list],
    ref_times: dict[str, dict[str, list[float]]],
    libraries: list[tuple[str, dict]]
) -> pd.DataFrame:
    """Compute all pairwise ratios a_i / b_j."""
    results = {}
    for param_name, param_values in test_parameters.items():
        data = []
        for val in param_values:
            val_str = str(val)
            ref_arr = np.array(ref_times[param_name][val_str])

            for lib_name, lib_times in libraries:
                lib_arr = np.array(lib_times[param_name][val_str])
                ratios = np.ravel(np.divide.outer(lib_arr, ref_arr))
                # median of ratios to
                for ratio in ratios:
                    data.append((val_str, lib_name, ratio))
        results[param_name] = pd.DataFrame(data, columns=[param_name, 'Library', 'Ratio'])

    return results

def plot_relative_differences(ratio_data: dict[str, pd.DataFrame]):
    n_params = len(ratio_data)
    n_cols = 1
    if n_params > 1 and n_params <= 4 :
        n_cols = 2
    elif n_params > 4:
        n_cols = 3
    n_rows = (n_params + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(10 if n_params == 1 else 15, 5 * n_rows))
    # Ensure axes is always iterable
    axes = np.atleast_1d(axes).flatten()

    for idx, (param_name, df) in enumerate(ratio_data.items()):
        ax = axes[idx]
        sns.barplot(
            data=df,
            x=param_name,
            y='Ratio',
            hue='Library',
            # palette='cividis',
            # palette='gist_rainbow',
            # palette='rainbow',
            palette='hls',
            # palette='gist_ncar',
            ax=ax,
            estimator=np.median,
            edgecolor='black',
            linewidth=1,
            errorbar='ci'  # seaborn default CI
        )
        ax.axhline(1.0, color="k", ls='--', alpha=0.8)
        ax.set_yticks([1.0])
        ax.set_yticklabels(["1.0"])
        ax.grid(True, axis='y', alpha=0.5)

        # Annotate bars with their ratio values
        for container in ax.containers:
            labels = [f'{h:.2f}' if h > 1e-6 else '' for h in container.datavalues]
            ax.bar_label(container, labels=labels, padding=3)
        ax.set_ylim(0, max(ax.get_ylim()[1] * 1.05, 1.05))

    # Remove any unused subplots
    for idx in range(len(ratio_data), len(axes)):
        fig.delaxes(axes[idx])
    if n_params == 1:
        plt.tight_layout(rect=[0, 0.05, 1, 0.88])
    else:
        plt.tight_layout(rect=[0, 0.05, 1, 0.93])

    # Create a common legend (if any) at the top center
    common_handles, common_labels = None, None
    for ax in fig.axes:
        leg = ax.get_legend()
        if leg is not None:
            common_handles, common_labels = ax.get_legend_handles_labels()
            break
    if common_handles is not None and common_labels is not None:
        fig.legend(common_handles, common_labels, loc='upper center', ncol=len(common_labels),
                   bbox_to_anchor=(0.5, 0.99), title="Library")
    # Remove legends from individual subplots
    for ax in axes:
        if ax.get_legend() is not None:
            ax.get_legend().remove()

    return fig, axes


def main():
    args = parse_args()
    config = manage_config.load_json(args.config_file)
    ref_results = manage_config.load_json(args.ref, args.results_directory)
    library_files = args.libs

    operator = config["operator"]
    test_parameters = config["test_configurations"]

    # Load reference times and library name from reference JSON
    ref_times = ref_results.get("time")
    ref_library = ref_results.get("library")
    if ref_times is None:
        print("Reference JSON does not contain time results.")
        sys.exit(1)

    libraries = []
    for lib_file in library_files:
        lib_results = manage_config.load_json(lib_file, args.results_directory)
        lib_times = lib_results.get("time")
        lib_name = lib_results.get("library")
        if lib_name == ref_library:
            continue
        if lib_times is None:
            print(f"Library JSON {lib_file} does not contain time results. Skipping.")
            continue
        libraries.append((lib_name, lib_times))
    if not libraries:
        print("No valid library results available for bar plot.")
        sys.exit(1)
    ratio_data = compute_pairwise_ratios(test_parameters, ref_times, libraries)
    fig, axes = plot_relative_differences(ratio_data)

    filename = f"{operator}_inference_time_comparison.svg"


    ##############################
    # Prepare footer texts
    footer_title = f'[{operator}] kernel inference time ratios (relative to {ref_library})'
    default_config = config.get("base_configuration", {})

    # Wrap the default configuration text to a given width.
    wrapped_config = textwrap.wrap(f'Base configuration: {default_config}', width=160)
    n_lines = len(wrapped_config)
    config_text = "\n".join(wrapped_config)

    # Adjust the figure layout to provide extra space at the bottom.
    if len(test_parameters) == 1:
        plt.subplots_adjust(bottom=0.2+0.02*n_lines)
    else:
        plt.subplots_adjust(bottom=0.14+0.02*n_lines)

    # Add the footer title (bottom center) with fontsize 16.
    fig.text(0.5, 0.035+n_lines*0.025, footer_title, ha='center', va='bottom', fontsize=18)

    # Add the default configuration text just below the title with the computed fontsize.
    fig.text(0.5, 0.02, config_text, ha='center', va='bottom', fontsize=12)

    ############################
    # save
    plt.savefig(filename)
    print(f"Plot saved as {filename}")


if __name__ == "__main__":
    main()
