# coding=utf-8

"""
    suffixtree.tree
    ~~~~~~~~~~~~~~~

    Tree data structure implementation.

    :copyright: (c) 2016 by Ali Ghaffaari.
    :license: MIT, see LICENSE for more details.
"""

from collections import deque
from graphviz import Digraph


class Edge:
    """Edge class.

    This class is used by Tree class as an edge in a tree. It implements the
    basic functionalities of an edge in the Tree which can be used as a base
    class for implementing any other edge class.
    """
    def __init__(self, dst, data=None, src=None):
        """Constructor for Edge class.

        Args:
            dst (Tree) [required]: The subtree to which this edge goes.
            data: Data associated with the edge.
            src (Tree): The subtree that this edge comes from (optional). It
                will be set or overwritten automatically when it's associated
                with a tree by `__setitem__` function of the `root_edge`
                dictionary of the tree class.
        """
        self.dst = dst
        self.src = src
        self.data = data

    def is_dangling(self):
        """Return True if either `src` or `dst` is not set. False otherwise."""
        return self.src is None or self.dst is None

    def is_loop(self):
        """Return if the edge is loop."""
        return self.src == self.dst

    def __str__(self):
        """Return string representation of the edge data.

        NOTE: This will be used as edge label in graph visualization.
        """
        if self.data is None:
            return ""

        return str(self.data)

    def __repr__(self):
        """Return string representation of the Edge class instance."""
        ptrn = "<Edge data:{}, from:{}, to:{}>"
        src_root_id = None
        if self.src is not None:
            src_root_id = self.src.root_id
        return ptrn.format(str(self.data), str(src_root_id),
                           str(self.dst.root_id))


class Tree:
    """Tree class.

    This class implements a tree data structure recursively. Each tree has some
    trees as its children (subtrees). Obviously, leaf nodes are subtrees with no
    children. Edges to the subtrees of a tree are stored in a member variable
    'root_edges' whose type is EdgeDict. It is dictionary-like data type whose
    keys are edge IDs and values are edge data.

    NOTE:
        Edge data type should have "dst" and "src" properties that refer to the
        child and its parent respectively. Also it should implements `__str__`
        so that it returns edge label (string representation of the edge data).

    NOTE:
        The data type of `root_data` should implements `__str__` to return
        string representation of the root data.
    """
    # No. of trees instantiated so far. It's used as unique ID for each
    # instance.
    nof_trees = 0

    class EdgeDict(dict):
        """EdgeDict class.

        A data type storing edges of a node that can be accessed by their IDs
        as the key. It acts exactly like a dictionary but it assures that all
        required field of the edge data type; i.e. "dst" and "src", will be
        properly set such that the tree structure integrity is gauranteed
        through construction process.
        """
        def __init__(self, root):
            """Constructor for the EdgeDict class.

            Apart from calling `__init__` function of super class, it stores
            the root node whose edges are going to be stored.

            Args:
                root (Tree): Root node whose edges are going to be stored.
            """
            super().__init__()
            self.root = root

        def __setitem__(self, key, value):
            """Add an edge to the edge container.

            It also defines the forward and backward connectivity in an edge by
            setting 'src' property of edge to `self.root` and 'dst.parent_edge'
            to the edge.

            Args:
                key: Edge ID of the edge.
                value: New edge data.
            """
            super().__setitem__(key, value)
            self[key].src = self.root
            self[key].dst.parent_edge = value

    def __init__(self, root_data=None, root_id=None):
        """Constructor for the Tree class.

        Args:
            root_data: Optional data associated with the root node of this tree.
            root_id: Assigns an ID to the root node of this tree. In case that
                it's not provided, `nof_trees` value will be used.
        """
        if root_id is None:
            root_id = Tree.nof_trees
        self._root_id = root_id
        self.root_data = root_data

        # Root node's edge container
        self._root_edges = Tree.EdgeDict(self)
        # parent_edge: Reference to the incoming parent edge if there's any. It
        # ...allows to traverse back in the tree.
        self.parent_edge = None  # default value is None.
        Tree.nof_trees += 1

    @property
    def root_id(self):
        """Read-only variable `root_id`."""
        return self._root_id

    @property
    def root_edges(self):
        """Read-only variable `root_edges`. It can be modified by using common
        dictionary `__getitem__` and `__setitem__` functions.
        """
        return self._root_edges

    def add_subtree(self, stree, edge_id=None, edge_data=None):
        """Add a tree to its subtrees.

        Args:
            stree (Tree): the new subtree.
            edge_id (object): id of the new edge (key for `root_edge` dict).
            edge_data (object): the associated data with the corresponding edge
                linking these two nodes.

        Return:
            the connecting edge.
        """
        if edge_id is None:
            edge_id = len(self.root_edges.keys())
            while edge_id in self.root_edges:
                edge_id += 1

        edge = Edge(dst=stree, data=edge_data)
        self.root_edges[edge_id] = edge

        return edge

    @property
    def subtrees(self):
        """Subtrees generator."""
        for edge in self.root_edges.values():
            yield edge.dst

    def get_subtree(self, edge_id):
        """Get a subtree by edge ID."""
        return self.root_edges[edge_id].dst

    def is_root(self):
        """Whether this subtree is root or not."""
        return self.parent_edge is None

    def is_leaf(self):
        """Whether this subtree is a child or not."""
        return not bool(self.root_edges)

    def visualize(self, name, comment, pro_do=lambda dot, tree: None, **kwargs):
        """Visualize the graph by using graphviz package and dot language.

        Args:
            name (str): Name of the dot graph.
            comment (str): Comment on the dot graph.
            pro_do (function): Higher-order function that will be called right
                before rendering. It gets 'dot' and 'tree' objects as an
                argument and it is useful for the inherited subclasses to
                override this method by adding more things to the final rendered
                graph.

        kwargs:
            filename (str): Name of the output file (default='tree').
            fmt (str): File format of the output (default='svg').
            hl_nodes ([Tree *]): List of highlighted nodes (default=[]). These
                nodes (corresponding subtrees) are highlighted in the rendered
                graph.
            graph_attr (dict): Graph attributes. Default attributes are:
                    For graph: ratio=1
                    For nodes: shape=circle, margin=0.2
                    For edges: fontsize=10
            leaves_attr (dict): Leaves attributes. Default attributes are:
                    style=filled
                    fillcolor=lightgrey
            hl_nodes_attr (dict): Highlighted nodes attributes. Default
                attributes are:
                    style=filled
                    fillcolor=red

            Remaining options passed to dot.render() function. such as:
                'directory':
                    (Sub)directory for source saving and rendering.
                'view':
                    Open the rendered result with the default application.
                'cleanup':
                    Delete the source file after rendering.

                See the full list at:
                    http://graphviz.readthedocs.io/en/latest/api.html#graphviz.Digraph.render
        """
        filename = kwargs.pop('filename', 'tree')
        fmt = kwargs.pop('fmt', 'svg')
        hl_nodes = kwargs.pop('hl_nodes', [])

        graph_attr = {
            'graph_attr': {'ratio': '1'},
            'node_attr': {'shape': 'circle',
                          'margin': '0.2'},
            'edge_attr': {'fontsize': '10'}
        }
        graph_attr = kwargs.pop('graph_attr', graph_attr)

        leaves_attr = {
            'style': 'filled',
            'fillcolor': 'lightgray'
        }
        leaves_attr = kwargs.pop('leaves_attr', leaves_attr)

        hl_nodes_attr = {
            'style': 'filled',
            'fillcolor': 'red'
        }
        hl_nodes_attr = kwargs.pop('hl_nodes_attr', hl_nodes_attr)

        # Create a dot graph by given name, comment, and attributes.
        dot = Digraph(name, comment, **graph_attr)

        # Traverse the tree by DFS.
        for node in self.dfs():
            attributes = {}
            if node.is_leaf():
                attributes = leaves_attr
            if node in hl_nodes:
                attributes = hl_nodes_attr  # Overriding leave attributes.

            # Add the node to dot graph.
            dot.node(str(node.root_id), str(node), **attributes)
            if node != self:  # If node is not the caller, add its parent edge.
                # Add parent edge to the dot graph.
                dot.edge(str(node.parent_edge.src.root_id), str(node.root_id),
                         label=str(node.parent_edge))

        # Do more by subclasses' overrided visualize function!
        pro_do(dot, self)

        dot.format = fmt
        # Rendering... . Remaining kwargs will be passed to the render function.
        dot.render(filename, **kwargs)

    def dfs(self):
        """Traverse the tree by DFS algorithm and yields visiting nodes
        (corresponding subtrees). Children of a node are traversed in order
        based on edge ID ordering; i.e. smaller ID (depends on ordering of edge
        IDs) will be visited first.
        """
        # Add root node (subtree) to the stack.
        stack = [self]
        while stack:
            node = stack.pop()
            # Loop on children "in order"...
            for edge_id in sorted(node.root_edges.keys(), reverse=True):
                # ...and add them to the stack.
                stack.append(node.get_subtree(edge_id))
            yield node

    def bfs(self):
        """Traverse the tree by BFS algorithm and yields visiting nodes
        (corresponding subtrees). Children of a node are traversed in order
        based on edge ID ordering; i.e. smaller ID (depends on ordering of edge
        IDs) will be visited first.
        """
        # Add root node (subtree) to the queue.
        queue = deque([self])
        while queue:
            node = queue.popleft()
            # Loop on children "in order"...
            for edge_id in sorted(node.root_edges.keys()):
                # ...and add them to the queue.
                queue.append(node.get_subtree(edge_id))
            yield node

    def __str__(self):
        """Calling str() on a node (tree) gives you the label of the node (root
        node of the tree).
        """
        if self.root_data is None:
            return ""
        return str(self.root_data)

    def __repr__(self):
        """Return a string representation of the object."""
        ptrn = "<Tree ID:{}, root_data:{}, root_edges:{}, parent_ID:{}>"
        parent_id = None
        if self.parent_edge is not None:
            parent_id = self.parent_edge.src.root_id
        return ptrn.format(str(self.root_id), repr(self.root_data),
                           sorted(self.root_edges.keys()), str(parent_id))
