# coding=utf-8

"""
    test.test_suffixtree
    ~~~~~~~~~~~~~~~~~~~~

    Test SuffixTree class.

    :copyright: (c) 2016 by Ali Ghaffaari.
    :license: MIT, see LICENSE for more details.
"""

from os import path
import random

from .context import suffixtree as st

CWDIR = path.dirname(path.realpath(__file__))
FIGDIR = path.join(CWDIR, 'figures', 'suffixtrees')
VIEW = False


def test_main():
    """Test SuffixTree methods and initialization"""
    suftree = st.SuffixTree("VALARMORGHULISDOHAERIS")
    suftree.visualize(filename="suffix_tree1", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("MORGH"))
    assert len(indices) == 1
    assert indices[0] == 5

    suftree = st.SuffixTree("mississippi", case_sensitive=True)
    suftree.visualize(hl_nodes=[suftree.traverse("").subtree],
                      filename="suffix_tree2", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("si"))
    assert len(indices) == 2
    assert 3 in indices
    assert 6 in indices
    indices = list(suftree.find("Si"))
    assert len(indices) == 0

    suftree = st.SuffixTree("Ghaffaari")
    suftree.visualize(hl_nodes=[suftree.traverse("g").subtree],
                      filename="suffix_tree3", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("GhAf"))
    assert len(indices) == 1
    assert indices[0] == 0

    suftree = st.SuffixTree("peeper", case_sensitive=True)
    suftree.visualize(hl_nodes=[suftree.traverse("pee").subtree],
                      filename="suffix_tree4", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("e"))
    assert len(indices) == 3
    assert 1 in indices
    assert 2 in indices
    assert 4 in indices

    suftree = st.SuffixTree("babacacb")
    suftree.visualize(hl_nodes=[suftree.traverse("cb").subtree],
                      filename="suffix_tree5", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("cacb"))
    assert len(indices) == 1
    assert indices[0] == 4

    suftree = st.SuffixTree("banana", case_sensitive=True)
    suftree.visualize(hl_nodes=[suftree.traverse("ana").subtree],
                      filename="suffix_tree6", directory=FIGDIR,
                      view=VIEW, cleanup=True)
    indices = list(suftree.find("banana"))
    assert len(indices) == 1
    assert indices[0] == 0

    strlen = 100
    bases = ['A', 'C', 'G', 'T']
    rndseq = "".join(random.choice(bases) for _ in range(strlen))
    suftree = st.SuffixTree(rndseq)
    suftree.visualize(filename="suffix_tree_seq", directory=FIGDIR,
                      no_suffixlink=True, view=VIEW, cleanup=True)

if __name__ == "__main__":
    test_main()
