class TreeStruct:
    """
    TreeStruct enables structured, tree-like rendering of nested operations
    using Unicode line-drawing characters (e.g. ├─, └─, │) for visual clarity.

    It is especially useful for displaying progress or hierarchical steps
    in command-line tools, such as loading modules or benchmarking results.

    Example output:

        Loading modules...
        ├──torch [ ok ]
        ├──aidge_backend_cpu [ ok ]
        └──onnxruntime [ ok ]

        Benchmarking...
        ├─┬─torch
        │ ├──time [ 5.70e-04 ± 1.45e-04 ] (seconds)
        │ └──comp [ xx ]
        ├─┬─aidge_backend_cpu
        │ ├──time [ 5.70e-04 ± 1.45e-04 ] (seconds)
        │ └──comp [ xx ]
        └─┬─onnxruntime
          ├──time [ 5.70e-04 ± 1.45e-04 ] (seconds)
          └──comp [ xx ]

    Usage:
        tree = TreeStruct()
        print(tree.grow(branch=True, leaf=False) + "torch")
        print(tree.grow(branch=False, leaf=True) + "comp [ ok ]")
        tree.reset()
    """

    def __init__(self):
        self.branches = " "

    def _stack_to_str() -> str:
        str_conversion_table = " │├┬└─"

    def grow(self, branch: bool, leaf: bool) -> str:
        """
        Advances the tree depth and returns the prefix string for the current line,
        automatically adjusting indentation and connection characters.

        Args:
            branch (bool): Whether the current node will have children.
            leaf (bool): Whether this is the last item at the current depth.
        """
        self.branches += "└" if leaf else "├"
        self.branches += "─"
        self.branches += "┬" if branch else "─"
        tmp_branches = self.branches + "─"
        self._truncate(branch, leaf)

        return tmp_branches

    def __str__(self):
        return self.branches

    def _truncate(self, branch: bool, leaf: bool):
        if len(self.branches):
            # truncate
            self.branches = self.branches[:-3]
            # add
            if branch:
                self.branches += "  " if leaf else "│ "
            # remove
            elif leaf and len(self.branches):
                index = len(self.branches) - 1
                while index > 0 and self.branches[index] != "│":
                    index -= 1
                self.branches = self.branches[:index]

    def reset(self):
        """Resets the internal state, allowing reuse for a new tree."""
        self.branches = " "
