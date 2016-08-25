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

"""Test SuffixTree class."""

from os import path
import random
from context import SuffixTree

CWDIR = path.dirname(path.realpath(__file__))
FIGDIR = path.join(CWDIR, 'figures', 'suffixtrees')
VIEW = False


def test_main():
    """Test SuffixTree methods and initialization"""
    suftree = SuffixTree("VALARMORGHULISDOHAERIS")
    suftree.visualize(filename="suffix_tree1", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("MORGH"))
    assert len(indices) == 1
    assert indices[0] == 5

    suftree = SuffixTree("mississippi", case_sensitive=True)
    suftree.visualize(hl_nodes=[suftree.traverse("").subtree],
                      filename="suffix_tree2", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("si"))
    assert len(indices) == 2
    assert 3 in indices
    assert 6 in indices
    indices = list(suftree.find("Si"))
    assert len(indices) == 0

    suftree = SuffixTree("Ghaffaari")
    suftree.visualize(hl_nodes=[suftree.traverse("g").subtree],
                      filename="suffix_tree3", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("GhAf"))
    assert len(indices) == 1
    assert indices[0] == 0

    suftree = SuffixTree("peeper", case_sensitive=True)
    suftree.visualize(hl_nodes=[suftree.traverse("pee").subtree],
                      filename="suffix_tree4", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("e"))
    assert len(indices) == 3
    assert 1 in indices
    assert 2 in indices
    assert 4 in indices

    suftree = SuffixTree("babacacb")
    suftree.visualize(hl_nodes=[suftree.traverse("cb").subtree],
                      filename="suffix_tree5", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("cacb"))
    assert len(indices) == 1
    assert indices[0] == 4

    suftree = SuffixTree("banana", case_sensitive=True)
    suftree.visualize(hl_nodes=[suftree.traverse("ana").subtree],
                      filename="suffix_tree6", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("banana"))
    assert len(indices) == 1
    assert indices[0] == 0

    strlen = 100
    bases = ['A', 'C', 'G', 'T']
    rndseq = "".join(random.choice(bases) for _ in range(strlen))
    suftree = SuffixTree(rndseq)
    suftree.visualize(filename="suffix_tree_seq", directory=FIGDIR,
                      no_suffixlink=True, view=VIEW, cleanup=True)

if __name__ == "__main__":
    test_main()
