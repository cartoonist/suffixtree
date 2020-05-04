# coding=utf-8

"""
    suffixtree.suffixtree
    ~~~~~~~~~~~~~~~~~~~~~

    The suffix tree implementation. It can be constructed from a given text
    using Ukkonen's algorithm. It also implements APIs for exact pattern
    search queries and visualisation.

    :copyright: (c) 2016 by Ali Ghaffaari.
    :license: MIT, see LICENSE for more details.
"""

from .tree import Tree, Edge


class SuffixEdge(Edge):
    """An edge in the suffix tree.

    It implements the Edge class containing essential information about an edge
    in a tree data structure while keeping more specific data for a suffix tree
    edge: It stores the substring associated with the edge in the suffix tree by
    keeping its start and end index.

    NOTE:
        In this class, the suffix tree's string is accessed by `string`
        property of the `dst` subtrees, since SuffixTree class implements
        this property to refer to the corresponding string.
    """
    def __init__(self, start, end, **edge_options):
        """Constructor for SuffixEdge class.

        Args:
            start (int) [required]: Start index of the string represented by
                this edge.
            end (int) [required]: End index of the string represented by this
                edge.
            edge_options (dict): Other parameters which will be passed to super
                class (Edge); e.g. `dst` and `src`. See `Edge.__init__()` for
                more information.
        """
        super().__init__(data=(start, end), **edge_options)

    @property
    def start(self):
        """Return start index of the string represented by this edge."""
        return self.data[0]

    @start.setter
    def start(self, _start):
        """Set 'start' attribute."""
        self.data = (_start, self.data[1])

    @property
    def end(self):
        """Return end index of the string represented by this edge."""
        return self.data[1]

    @end.setter
    def end(self, _end):
        """Set 'end' attribute."""
        self.data = (self.data[0], _end)

    @property
    def edge_char(self):
        """Return edge character (edge ID)."""
        return self.dst.string[self.start]

    def __str__(self):
        """Return the corresponding string.

        NOTE: This will be used as edge label in graph visualization.
        """
        return self.dst.string[self.start:self.end]

    def __len__(self):
        """Return length of the corresponding string."""
        return self.end - self.start

    def __repr__(self):
        """Return string representation of the SuffixEdge class instance."""
        ptrn = "<SuffixEdge label:{}->{}, from:{}, to:{}>"
        src_root_id = None
        if self.src is not None:
            src_root_id = self.src.root_id
        return ptrn.format(self.start, self.end, str(src_root_id),
                           str(self.dst.root_id))


class Substr():
    """Represent a substring in the suffix tree.

    A substring starts from the root node and ends either on a node or on an
    edge in the suffix tree. So a node in the suffix tree can be interpreted as
    the substring which starts from the root node and ends on that node. For
    those substrings which end on an edge, we can represents them by the triple
    (t, c, d) where t is a node (tree), c is a character indicating the edge on
    which the substring ends, and d is number of characters should be skipped
    through the edge to reach to the end of the substring in the suffix tree.
    For those ending on a node, the triple would be (t, None, 0) where t is the
    corresponding node (tree). The triple (None, None, 0) is used for showing an
    invalid substring in this class.
    """
    def __init__(self, subtree, string="", edge_char=None, depth=0):
        """Constructor for Substr class.

        Args:
            subtree (SuffixTree): A subtree in the suffix tree. From this node
                we can reach to the desired subtree by consuming the `string`
                (next parameter).
            string (str): The string that should be consumed from the given
                subtree to reach to the end of the desired substring. The triple
                (tree, char, depth) described above will be computed such that
                the subtree would be the deepest node in the tree that is
                formally the longest prefix of the substring that ends on a
                node. String can be anything, but it should be present in the
                suffix tree. Otherwise, the state of class would be invalid:
                (None, None, 0).
            edge_char (char): Initial value of `_edge_char` attribute (see
                below).
            depth (int): Initial value of `_depth` attribute (see below).
        """
        self._subtree = subtree
        # If depth is non-zero, edge_char indicates the edge on which the
        # substring ends. Otherwise, the character is indifferent.
        self._edge_char = edge_char
        # Number of characters should be skipped to reach to the end of the
        # substring from the subtree's root node.
        self._depth = depth
        # Compute the triple (t, c, d) so that t would be corresponding node of
        # the longest prefix of the substring which ends on a node.
        self.extend(string)
        # The actual substring from the root node of the suffix tree which may
        # be different from the provided `string`. It's computed on demand.
        self._substr = None

    @property
    def subtree(self):
        """Read-only property returning `self._subtree`."""
        return self._subtree

    @property
    def edge_char(self):
        """Read-only property returning `self._edge_char`."""
        return self._edge_char

    @property
    def depth(self):
        """Read-only property returning `self._depth`."""
        return self._depth

    def ends_on_node(self):
        """Retrun true if the substring ends on a node rather than on a edge.
        """
        return self._depth == 0

    def _get_substr(self):
        """Return the actual substring (from the root of the tree to the
        character indicated by depth on the edge by 'edge_char' ID of the root
        of the specified subtree).
        """
        edge_str = ""
        if not self.ends_on_node():
            edge = self._subtree.root_edges[self._edge_char]
            edge_str = self._subtree.string[edge.start:edge.start+self._depth+1]

        return self._subtree.pathlabel + edge_str

    def extend(self, string, forced=True):
        """Extend the substring with the given string if the new substring is in
        the tree and returns True. Otherwise, it's rejected and returns False.
        In the latter case, if `forced` is True the object became invalid (see
        `__bool__` function). Otherwise, the object will be set to the last
        state values.

        Args:
            string (str): Extension string.
            forced (bool): Force to update?

        Return:
            True if the string is found. Otherwise it returns False.
        """
        old_subtree = self._subtree
        old_edge_char = self._edge_char
        old_depth = self._depth

        found = True  # We are optimistic!
        while string:  # While string is not fully consumed...
            if self.ends_on_node():
                if string[0] not in self._subtree.root_edges:
                    found = False
                    break
                self._edge_char = string[0]
            edge = self._subtree.root_edges[self._edge_char]
            # pivot = how many characters can be reads in the current state.
            pivot = len(edge) - self._depth
            # Pick a prefix from `string` as much as possible.
            snippet, string = string[:pivot], string[pivot:]
            if not str(edge)[self._depth:].startswith(snippet):
                found = False
                break
            if len(snippet) == pivot:
                self._subtree = edge.dst
                self._edge_char = None
                self._depth = 0
            elif len(snippet) < pivot:
                self._depth += len(snippet)
                assert not string  # All of the string should be consumed here.
            else:
                # `len(snippet)` cannot be greater than `pivot`.
                assert False

        if not found:
            if forced:
                self._subtree = None
                self._edge_char = None
                self._depth = 0
            else:
                self._subtree = old_subtree
                self._edge_char = old_edge_char
                self._depth = old_depth

        if found or forced:
            self._substr = None  # The old value is not valid anymore.

        return found

    def __bool__(self):
        """Does `self` represent a valid substring?"""
        return self._subtree is not None

    def __str__(self):
        """Return the actual substring represented by this class."""
        # The substring is computed when it's needed.
        if self._substr is None:
            self._substr = self._get_substr()
        return self._substr

    def __repr__(self):
        """Return a string representation of Substr class instance."""
        ptrn = "<Substr subtree:{}, edgeID:{}, depth:{}>"
        return ptrn.format(repr(self._subtree), self._edge_char,
                           str(self._depth))


class SuffixTree(Tree):
    """Suffix tree class.

    Implements a compressed trie containing all suffixes of the given string. it
    can be used as an index of the given text for fast string operations.
    """
    # Sentinel character. It will be concatenated at the end of the text.
    sentinel = "$"

    def __init__(self, string, case_sensitive=False, suffix_link=None,
                 **tree_options):
        """Constructor for SuffixTree class.

        Args:
            string (str): The string. If it's provided the suffix tree of the
                string will be constructed. Otherwise, it assumes that this
                object is an internal or leaf node (non-root) rather than a
                complete suffix tree. These nodes are referred to 'abstract'
                nodes. The property `_abstract` is a boolean value indicating
                this state.
            case_sensitive (bool): Boolean variable showing the
                case-sensitiveness of the tree. In non-root nodes, it's set to
                be None while initializing. However, it will be updated when
                it's accessed. The update value will be the root node's value
                got by traversing back in the tree. On the other cases it stores
                case-sensitiveness of the root of the suffix tree.
            suffix_link (SuffixTree): In non-root nodes, it relates current node
                to its suffix node; e.g. this is a sample suffix path in the
                tree: 'abc' -> 'bc' -> 'c'. In root nodes, it's set to be None.
            tree_options (dict): The tree parameters required for Tree class
                initialization. It will be directly passed to the super class
                `__init__` function.

        NOTE:
            Since the two attributes `string` and `case_sensitive` is given just
            to root nodes during instantiation, not abstract (internal and
            leaves) nodes, their values are None for abstract nodes. However,
            they can be access from abstract nodes after `__init__` and get the
            actual value by traversing back the tree to reach the data in the
            root node. For efficiency, this data will be saved in the
            corresponding instance attributes. So they may be not None after
            construction.
        """
        super().__init__(**tree_options)
        self._abstract = False
        # If `string` is not provided (None), this object would be a non-root
        # (internal or leaf) node; i.e. an abstract node. So there's no need to
        # call construct function.
        if string is None:
            self._abstract = True

        # The substring represented by this node (by tree-as-a-node perspective)
        self._pathlabel = None

        if not self._abstract:
            # Processing the string...
            self._case_sensitive = case_sensitive
            if case_sensitive:
                self._string = string
            else:
                self._string = string.lower()
            self._string += SuffixTree.sentinel
            # Suffix link for root node is None.
            self.suffix_link = None
            # Initializing internal variable for construction.
            self._active = None
            # Construct the suffix tree!
            self._construct()
        else:
            self.suffix_link = suffix_link

    @classmethod
    def _as_node(cls, **kwargs):
        """SuffixTree as a node. It creates a non-root node rather than a
        complete suffix tree.
        """
        return cls(string=None, **kwargs)

    def _construct(self):
        """Use Ukkonen's algorithm for suffix tree construction in linear time.
        """
        # Set active state to the root node.
        self._active = Substr(self)
        # Loop on characters of the text from left to right.
        for phase, char in enumerate(self._string):
            extended_successfully = self._active.extend(char, forced=False)
            if extended_successfully:
                # It's already in the tree
                continue

            if not self._active.ends_on_node():
                # Since the active state is not a node, the underlying edge is
                # ...going to be splitted before adding new suffix to the tree.
                self._active = Substr(self._splitedge())
                # Now active state is a node.

            self._extend_prefix(char, phase)

    def _splitedge(self, substr=None):
        """Split an edge from the point indicated by the given substring which
        doesn't end on a node (ends on an edge).

        Args:
            substr (Substr): Split the edge determined by this substr (an
                instance of Substr class). If not provided active state will be
                used.

        Return:
            the new node (tree).
        """
        if not substr:
            substr = self._active

        if substr.ends_on_node():
            # It already ends on a node.
            return substr.subtree

        # Pick the edge should be splitted.
        split_edge = substr.subtree.root_edges[substr.edge_char]
        # New node...
        new_subtree = SuffixTree._as_node()
        # Edge from the `substr.subtree` to the new node: (start, start + depth)
        new_edge = SuffixEdge(start=split_edge.start,
                              end=(split_edge.start + substr.depth),
                              dst=new_subtree)
        # Add the new edge and subtree to the suffix tree. Replacing the
        # ...splitted edge.
        substr.subtree.root_edges[substr.edge_char] = new_edge
        # Edit splitted edge to be: (start + depth, end)
        split_edge.start = split_edge.start + substr.depth
        # Add the splitted edge and its subtree to the new node.
        new_subtree.root_edges[self._string[split_edge.start]] = split_edge

        return new_subtree

    def _extend_prefix(self, char, phase):
        """Add string `str(self._active) + char` as a suffix to the tree. This
        function assumes that this suffix is not in the tree and active state is
        a node. This function adds all other suffixes of the string by following
        the suffix links if exist, otherwise, new suffix links are created.

        Args:
            char (char): The character that should be added to the suffix tree
                based on the position of active state.
            phase (int): Current phase of construction defined in Ukkonen's
                algorithm.
        """
        # Active state should be a node.
        assert self._active.ends_on_node()
        # Suffix 'str(self._active) + char' should not be already in the tree.
        assert char not in self._active.subtree.root_edges

        # Create a new subtree.
        new_subtree = SuffixTree._as_node()
        # Create a new edge.
        new_edge = SuffixEdge(start=phase, end=len(self._string),
                              dst=new_subtree)
        # Add the new subtree to the tree using the new edge.
        self._active.subtree.root_edges[char] = new_edge

        # is_root() == Root node (from Tree class) == No parent edge
        # not-abstract == Root of the suffix tree
        if self._active.subtree.is_root() or \
           not self._active.subtree.abstract:
            return
        # else:
        # Finding the next suffix node and setting the active state to that node
        next_suffix = self._active.subtree.suffix_link
        if next_suffix is not None:
            # Follow the suffix link...
            self._active = Substr(next_suffix)
        else:
            prev_suffix = self._active
            # Find the next suffix node...
            act_parent_edge = self._active.subtree.parent_edge
            act_parent = act_parent_edge.src
            i = act_parent_edge.start
            j = act_parent_edge.end
            if act_parent.is_root():
                target_node = act_parent
                i += 1
            else:
                target_node = act_parent.suffix_link
            assert target_node is not None
            while True:
                c = self._string[i]
                child_edge = target_node.root_edges[c]
                if len(child_edge) > j - i:
                    break
                target_node = child_edge.dst
                i += len(child_edge)
            if j - i == 0:
                c = None
            self._active = Substr(target_node, edge_char=c, depth=j-i)
            # Split the edge if required.
            if not self._active.ends_on_node():
                self._active = Substr(self._splitedge())
            # Add suffix link.
            prev_suffix.subtree.suffix_link = self._active.subtree

        # Check if the new suffix is already in the tree, then extend the active
        # ...state.
        extended_successfully = self._active.extend(char, forced=False)
        if not extended_successfully:
            # If not, call the function recursively until either the new suffix
            # ...is in the tree or reach the root node.
            self._extend_prefix(char, phase)

    def traverse(self, query):
        """Traverse the tree by the given query. The matched position in the
        graph is represented by a Substr instance. The output can be
        post-processed to find the matching positions. In case that query cannot
        be found in the tree, it returns None.

        Args:
            query (string): Query to be searched.

        Return:
            matched position (Substr) if query is found. Otherwise it returns
            None.
        """
        if not self.case_sensitive:
            query = query.lower()

        matched_pos = Substr(self, query)
        if not matched_pos:
            return None
        # else:
        return matched_pos

    def find(self, query):
        """Find the positions of occurrance of the query in the text.

        Args:
            query (string): query string.

        Yield:
            indices of occurrance of the query in the text.
        """
        matched_pos = self.traverse(query)

        if matched_pos is None:
            return
        # else:
        matched_node = matched_pos.subtree
        if not matched_pos.ends_on_node():
            edge = matched_node.root_edges[matched_pos.edge_char]
            matched_node = edge.dst

        for sufidx in matched_node.suffix_indices():
            yield sufidx

    def suffix_indices(self):
        """Find indices of all suffixes in the text started with the common
        prefix denoted by this node (self.pathlabel).

        Yield:
            indices of all suffixes going through this node.
        """
        for node in self.dfs():
            if node.is_leaf():
                yield len(self.string) - len(node.pathlabel)

    def visualize(self, **kwargs):
        """Override visualize function of the Tree (super class).

        Args:
            no_suffixlink (bool): If this is set to be True, the suffix links
                would not be visualized in the dot graph (default=False).
        """
        no_suffixlink = kwargs.pop('no_suffixlink', False)
        comment_text = "Suffix tree for \"" + self._string + "\""

        def visualize_suffix_links(dot, tree):
            """Add suffix links to the dot graph."""
            for node in tree.dfs():
                sufnode = node.suffix_link
                if sufnode:
                    dot.edge(str(node.root_id), str(sufnode.root_id),
                             style="dashed", color="lightgreen")

        if no_suffixlink:
            super().visualize(self.string, comment_text, **kwargs)
        else:
            super().visualize(self.string, comment_text,
                              pro_do=visualize_suffix_links, **kwargs)

    @property
    def string(self):
        """Read-only property returns corresponding string."""
        if not self.is_root():
            return self.parent_edge.src.string
        return self._string

    @property
    def case_sensitive(self):
        """Read-only property returns if the string is case sensitive or not."""
        if not self.is_root():
            return self.parent_edge.src.case_sensitive
        return self._case_sensitive

    @property
    def abstract(self):
        """Read-only property abstract."""
        return self._abstract

    @property
    def pathlabel(self):
        """Substring represented by the root of this subtree. It will be
        calculated when it's needed.
        """
        if self._pathlabel is None:
            self._pathlabel = self.get_pathlabel()

        return self._pathlabel

    def get_pathlabel(self):
        """Return substring represented by the root of this subtree."""
        # is_root() == Root node (from Tree class) == No parent edge
        # not-abstract == Root of the suffix tree
        if self.is_root() or not self._abstract:
            return ""

        pathlabel = ""
        parent_edge = self.parent_edge
        while parent_edge is not None:
            pathlabel = str(parent_edge) + pathlabel
            parent_edge = parent_edge.src.parent_edge

        return pathlabel

    def __str__(self):
        """Get original string without sentinel (for root nodes).

        NOTE: It is used by graph visualization function as node label.
        """
        if not self.is_root() or self._abstract:
            return ""

        return self.string[:-1]

    def __repr__(self):
        """String representation of SuffixTree class instance."""
        sign = ""
        if self._abstract:
            sign = "*"
        ptrn = "<SuffixTree{} string:{}, case_sensitive:{}, suffix_link:{} {}>"
        return ptrn.format(sign, self.string, self.case_sensitive,
                           self.suffix_link, super().__repr__())
