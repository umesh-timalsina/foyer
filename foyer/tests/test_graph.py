from foyer.smarts_graph import SMARTSGraph


TEST_BANK = [
    'O([H&X1])(H)',
    '[O;X2]([C;X4](F)(*)(*))[C;X4]',
    '[#6][#1](C)H',
    '[#6][#6][#6][#6][#6][#6]',
    '[#6]1[#6][#6][#6][#6][#6]1',
    '[#6]12[#6][#6][#6][#6][#6]1[#6][#6][#6][#6]2',
]


def test_init():
    """Initialization test. """
    for smarts in TEST_BANK:
        graph = SMARTSGraph(smarts)
        atoms = graph.ast.select('atom')
        for atom in atoms:
            assert atom in graph.nodes()


def test_graph_isomorphism():
    """Whole graph isomorphism. """
    assert SMARTSGraph(TEST_BANK[0]) == SMARTSGraph(TEST_BANK[0])
    assert not SMARTSGraph(TEST_BANK[0]) == SMARTSGraph(TEST_BANK[1])
    assert SMARTSGraph(TEST_BANK[3]) == SMARTSGraph(TEST_BANK[3])
    assert not SMARTSGraph(TEST_BANK[3]) == SMARTSGraph(TEST_BANK[4])
    assert not SMARTSGraph(TEST_BANK[3]) == SMARTSGraph(TEST_BANK[5])


def test_subgraph_isomorphism():
    """Sub-graph isomorphism. """
    assert SMARTSGraph(TEST_BANK[0]) in SMARTSGraph(TEST_BANK[0])
    assert SMARTSGraph(TEST_BANK[0]) not in SMARTSGraph(TEST_BANK[1])
    assert SMARTSGraph(TEST_BANK[3]) in SMARTSGraph(TEST_BANK[3])
    assert SMARTSGraph(TEST_BANK[3]) in SMARTSGraph(TEST_BANK[5])
    assert SMARTSGraph(TEST_BANK[5]) not in SMARTSGraph(TEST_BANK[3])
    assert SMARTSGraph(TEST_BANK[3]) not in SMARTSGraph(TEST_BANK[4])
    assert SMARTSGraph(TEST_BANK[4]) in SMARTSGraph(TEST_BANK[5])
    assert SMARTSGraph(TEST_BANK[3]) in SMARTSGraph(TEST_BANK[5])
