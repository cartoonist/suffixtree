#!/usr/bin/env python3
# coding=utf-8

# Suffix tree library
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Ali Ghaffaari
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test Tree class."""

from os import path
import random
import string
from nose.tools import raises
from context import Tree, Edge

CWDIR = path.dirname(path.realpath(__file__))
VIEW = False


def test_edge():
    """Test Edge class."""
    # Testing `is_dangling` and `is_loop` functoins
    edge1 = Edge(1, "An edge")
    assert edge1.is_dangling()
    assert not edge1.is_loop()
    edge1.src = 0
    assert not edge1.is_dangling()
    edge2 = Edge(2, 12, 1)
    assert not edge2.is_dangling()
    edge3 = Edge(2, src=2)
    assert edge3.is_loop()
    assert str(edge1) == "An edge"
    assert str(edge2) == "12"
    assert str(edge3) == ""


# pylint: disable=too-many-locals
def test_main():
    """Test tree methods and initialization."""
    tree1 = Tree()
    rootid = tree1.root_id
    assert tree1.root_id is not None
    assert tree1.root_data is None
    assert tree1.parent_edge is None
    assert Tree.nof_trees > 0
    assert tree1.is_root()
    assert tree1.is_leaf()

    strlen = 6
    rndid1 = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for _ in range(strlen))
    strlen = 40
    rnddata1 = ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(strlen))
    tree2 = Tree(root_data=rnddata1, root_id=rndid1)
    edge1 = tree1.add_subtree(tree2, '1', "an edge")
    assert tree2.root_id == rndid1
    assert tree2.root_data == rnddata1
    assert tree2.parent_edge == edge1
    assert Tree.nof_trees > 1
    assert not tree2.is_root()
    assert not tree1.is_leaf()
    assert tree2.is_leaf()

    strlen = 6
    rndid2 = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for _ in range(strlen))
    strlen = 40
    rnddata2 = ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(strlen))
    tree3 = Tree(root_data=rnddata2, root_id=rndid2)
    edge2 = Edge(dst=tree3, data="another edge")
    tree1.root_edges['2'] = edge2
    assert tree3.parent_edge == edge2
    assert tree3.is_leaf()
    assert not tree3.is_root()
    assert tree1.get_subtree('1') == tree2
    assert tree1.get_subtree('2') == tree3

    assert tree2 in list(tree1.subtrees) and tree3 in list(tree1.subtrees)

    strlen = 6
    rndid3 = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for _ in range(strlen))
    strlen = 40
    rnddata3 = ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(strlen))
    tree4 = Tree(root_data=rnddata3, root_id=rndid3)
    tree2.add_subtree(tree4, edge_id='3', edge_data="Last edge")

    assert tree1.is_root()

    # Check visualize function manually
    def do_more(dot, tree):
        """A test function working with dot file."""
        dot.edge(rndid3, str(tree.root_id), style='dotted',
                 color="red", arrowhead="dot")

    tree2.visualize('Subtree', 'Visualize subtree with default parameters',
                    hl_nodes=[tree2],
                    directory=path.join(CWDIR, 'figures', 'trees'),
                    view=VIEW, cleanup=True)
    tree1.visualize('Test', 'Visualize the tree with customized parameters',
                    pro_do=do_more,
                    filename='tree1', fmt='png', hl_nodes=[tree2],
                    graph_attr={'graph_attr': {'bgcolor': 'lightyellow'},
                                'node_attr': {'shape': 'doublecircle'},
                                'edge_attr': {'arrowhead': 'open'}},
                    leaves_attr={'style': 'filled',
                                 'fillcolor': 'lightblue'},
                    hl_nodes_attr={'style': 'filled',
                                   'fillcolor': 'orange'},
                    directory=path.join(CWDIR, 'figures', 'trees'),
                    view=VIEW, cleanup=True)

    assert [n.root_id for n in tree1.dfs()] == [rootid, rndid1, rndid3, rndid2]
    assert [n.root_id for n in tree1.bfs()] == [rootid, rndid1, rndid2, rndid3]

    assert str(tree1) == ""
    assert str(tree2) == rnddata1
    assert str(tree3) == rnddata2
    assert str(tree4) == rnddata3

    assert repr(tree1) == "<Tree ID:" + str(rootid) + ", root_data:None, " + \
        "root_edges:['1', '2'], parent_ID:None>"
    assert repr(tree2) == "<Tree ID:" + rndid1 + ", root_data:'" + rnddata1 + \
        "', root_edges:['3'], parent_ID:" + str(rootid) + ">"
    assert repr(tree3) == "<Tree ID:" + rndid2 + ", root_data:'" + rnddata2 + \
        "', root_edges:[], parent_ID:" + str(rootid) + ">"
    assert repr(tree4) == "<Tree ID:" + rndid3 + ", root_data:'" + rnddata3 + \
        "', root_edges:[], parent_ID:" + rndid1 + ">"


@raises(AttributeError)
def test_readonly_attr1():
    """Test tree readonly member variable: root_edges"""
    tree = Tree()
    tree.root_edges = {'a': 2, 'c': 1}


@raises(AttributeError)
def test_readonly_attr2():
    """Test tree readonly member variable: root_id"""
    tree = Tree()
    tree.root_id = 'new_id'


if __name__ == "__main__":
    test_edge()
    test_main()
    test_readonly_attr1()
    test_readonly_attr2()
