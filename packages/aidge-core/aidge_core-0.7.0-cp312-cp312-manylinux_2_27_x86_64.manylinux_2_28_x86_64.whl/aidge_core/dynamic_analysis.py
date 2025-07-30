import matplotlib
import matplotlib.pyplot as plt
from functools import partial
import numpy as np
import aidge_core

class DynamicAnalysis(aidge_core.DynamicAnalysis):
    def log_nb_arithm_ops(self, filename, title=None, log_scale=False):
        return self._log_callback(aidge_core.OperatorStats.get_nb_arithm_ops, filename, title, log_scale)

    def log_nb_logic_ops(self, filename, title=None, log_scale=False):
        return self._log_callback(aidge_core.OperatorStats.get_nb_logic_ops, filename, title, log_scale)

    def log_nb_comp_ops(self, filename, title=None, log_scale=False):
        return self._log_callback(aidge_core.OperatorStats.get_nb_comp_ops, filename, title, log_scale)

    def log_nb_nl_ops(self, filename, title=None, log_scale=False):
        return self._log_callback(aidge_core.OperatorStats.get_nb_nl_ops, filename, title, log_scale)

    def log_nb_mac_ops(self, filename, title=None, log_scale=False):
        return self._log_callback(aidge_core.OperatorStats.get_nb_mac_ops, filename, title, log_scale)

    def log_nb_ops(self, filename, title=None, log_scale=False):
        return self._log_callback(aidge_core.OperatorStats.get_nb_ops, filename, title, log_scale)

    def log_nb_arithm_int_ops(self, filename, title=None, log_scale=False):
        return self._log_callback(aidge_core.OperatorStats.get_nb_arithm_int_ops, filename, title, log_scale)

    def log_nb_arithm_fp_ops(self, filename, title=None, log_scale=False):
        return self._log_callback(aidge_core.OperatorStats.get_nb_arithm_fp_ops, filename, title, log_scale)

    def log_nb_ops_by_type(self, filename, title=None, log_scale=False):
        return self._log_callback([aidge_core.OperatorStats.get_nb_arithm_int_ops,
                                  aidge_core.OperatorStats.get_nb_arithm_fp_ops,
                                  aidge_core.OperatorStats.get_nb_logic_ops,
                                  aidge_core.OperatorStats.get_nb_comp_ops,
                                  aidge_core.OperatorStats.get_nb_nl_ops], filename, title, log_scale)

    def _log_callback(self, callback, filename, title=None, log_scale=False):
        """
        Log a statistic given by an OperatorStats callback member function.
        Usage:

            stats = DynamicAnalysis(model)
            stats.log_callback(aidge_core.OperatorStats.get_nb_params, "stats.png", "Nb params per operator")

        :param func: OperatorStats member function to call.
        :param filename: Output graph file name.
        :type filename: str
        :param title: Title of the graph.
        :type title: str
        """

        namePtrTable = self.get_graph().get_ranked_nodes_name("{0} ({1}#{3})");
        nodes = self.get_graph().get_ordered_nodes()
        series = []
        legend = None

        for node in nodes:
            if node.type() == "Producer":
                continue

            stats = aidge_core.OperatorStats.get_op_stats(node)
            name = namePtrTable[node]
            attr = {}
            if type(node.get_operator()) is aidge_core.GenericOperatorOp:
                # Display Generic Op in orange
                attr = {'color': 'orange'}
            elif not node.get_operator().is_atomic():
                # Display Meta Op in bold
                attr = {'fontweight': 'bold'}
            elif node.type() not in aidge_core.get_keys_OperatorStats():
                # Display unsupported operator in red labels
                attr = {'color': 'red'}
            if attr:
                name = (name, attr)
            if isinstance(callback, list):
                series.append([name, [partial(cb, stats)() for cb in callback]])
                legend = [cb.__name__ for cb in callback]
                if title is None: title = str(legend)
            else:
                series.append([name, partial(callback, stats)()])
                if title is None: title = callback.__name__

        if title is None: title = str(callback)
        if filename is not None:
            self._log_bar(series, filename, title, legend, log_scale)
        return series

    def _log_bar(self, series, filename, title=None, legend=None, log_scale=False):
        names, values = zip(*series)
        names_only = [item[0] if isinstance(item, tuple) else item for item in names]
        fig, ax = plt.subplots(figsize=(max(5, len(names)/4), 5))
        plt.xlim(-0.5, len(names) - 0.5)
        if isinstance(values[0], list):
            series = [list(i) for i in zip(*values)]
            bot = np.zeros(len(series[0]))
            for i, serie in enumerate(series):
                plt.bar(names_only, serie, bottom=bot)
                bot += serie
        else:
            plt.bar(names_only, values)
        if callable(getattr(ax.yaxis, 'minorticks_on', None)):
            ax.yaxis.minorticks_on() # introduced in matplotlib 3.9.x
        plt.grid(axis='y', which='major', linestyle='--', color='gray')
        plt.grid(axis='y', which='minor', linestyle=':', color='lightgray')
        formatter0 = matplotlib.ticker.EngFormatter(unit='')
        ax.yaxis.set_major_formatter(formatter0)
        plt.gca().set_axisbelow(True)

        labels = plt.gca().get_xticks()
        tick_labels = plt.gca().get_xticklabels()
        for i, label in enumerate(labels):
            if isinstance(names[i], tuple):
                if 'color' in names[i][1]:
                    tick_labels[i].set_color(names[i][1]['color'])
                elif 'fontweight' in names[i][1]:
                    tick_labels[i].set_fontweight(names[i][1]['fontweight'])

        plt.xticks(rotation='vertical')
        if log_scale: plt.yscale('log')
        if title is not None: plt.title(title)
        if legend is not None: plt.legend(legend)
        plt.savefig(filename, bbox_inches='tight')

    def _log_barh(self, series, filename, title=None, legend=None, log_scale=False):
        names, values = zip(*series)
        names_only = [item[0] if isinstance(item, tuple) else item for item in names]
        fig, ax = plt.subplots(figsize=(10, max(5, len(names)/4)))
        plt.ylim(-0.5, len(names) - 0.5)
        if isinstance(values[0], list):
            series = [list(i) for i in zip(*values)]
            left = np.zeros(len(series[0]))
            for i, serie in enumerate(series):
                plt.barh(names_only, serie, left=left)
                left += serie
        else:
            plt.barh(names_only, values)
        if callable(getattr(ax.xaxis, 'minorticks_on', None)):
            ax.xaxis.minorticks_on() # introduced in matplotlib 3.9.x
        plt.grid(axis='x', which='major', linestyle='--', color='gray')
        plt.grid(axis='x', which='minor', linestyle=':', color='lightgray')
        formatter0 = matplotlib.ticker.EngFormatter(unit='')
        ax.xaxis.set_major_formatter(formatter0)
        plt.gca().set_axisbelow(True)
        plt.gca().xaxis.set_label_position('top')
        plt.gca().xaxis.tick_top()

        labels = plt.gca().get_yticks()
        tick_labels = plt.gca().get_yticklabels()
        for i, label in enumerate(labels):
            if isinstance(names[i], tuple):
                if 'color' in names[i][1]:
                    tick_labels[i].set_color(names[i][1]['color'])
                elif 'fontweight' in names[i][1]:
                    tick_labels[i].set_fontweight(names[i][1]['fontweight'])

        if log_scale: plt.xscale('log')
        if title is not None: plt.title(title)
        if legend is not None: plt.legend(legend)
        plt.savefig(filename, bbox_inches='tight')
