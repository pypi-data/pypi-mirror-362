import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import aidge_core

class ExecTime(aidge_core.ExecTime):
    def log(self, filename, title=None, log_scale=False):
        stats = {k: v for k, v in self.get().items() if k.type() != "Producer"}
        names = [x.name() if x.name() != "" else x.type() + "#" for x in stats.keys()]
        values = stats.values()
        values_mean = [x.mean() for x in values]
        values_std_dev = [x.std_dev() for x in values]

        fig, ax = plt.subplots(figsize=(max(5, len(names)/4), 5))
        plt.bar(range(0, len(names)), values_mean)
        ax.set_xticks(range(0, len(names)))
        ax.set_xticklabels(names)
        plt.xlabel('Node')
        plt.ylabel('Mean execution time (µs)')
        plt.errorbar(range(0, len(names)), values_mean, values_std_dev, color='Black', linestyle='None', marker='None', capsize=5)
        if callable(getattr(ax.yaxis, 'minorticks_on', None)):
            ax.yaxis.minorticks_on() # introduced in matplotlib 3.9.x
        plt.grid(axis='y', which='major', linestyle='--', color='gray')
        plt.grid(axis='y', which='minor', linestyle=':', color='lightgray')
        plt.gca().set_axisbelow(True)
        plt.xticks(rotation='vertical')
        if log_scale: plt.yscale('log')
        if title is not None: plt.title(title)
        plt.savefig(filename, bbox_inches='tight')
