import pytest
from circuit_rs import isolate_subcircuit, isolate_subcircuit_np_edgelist
import numpy as np

# Type aliases to match Rust types
NeuronID = int
CMatIdx = int


def test_simple_source_to_sink_np():
    """Test simple path from one source to one sink"""
    edge_list = np.asarray([(1, 2), (2, 3), (3, 4), (4, 5)])
    sources = {1}
    sinks = {5}
    max_depth = 10
    max_paths = 100
    nid_to_cidx_map = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}

    # Expected: all nodes on the path from source to sink
    expected = {10, 20, 30, 40, 50}
    actual = isolate_subcircuit_np_edgelist(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"Test: Simple source to sink")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_simple_source_to_sink():
    """Test simple path from one source to one sink"""
    edge_list = [(1, 2), (2, 3), (3, 4), (4, 5)]
    sources = {1}
    sinks = {5}
    max_depth = 10
    max_paths = 100
    nid_to_cidx_map = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}

    # Expected: all nodes on the path from source to sink
    expected = {10, 20, 30, 40, 50}
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"Test: Simple source to sink")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_multiple_sources_one_sink():
    """Test multiple sources converging to one sink"""
    edge_list = [(1, 3), (2, 3), (3, 4), (4, 5)]
    sources = {1, 2}
    sinks = {5}
    max_depth = 5
    max_paths = 100
    nid_to_cidx_map = {1: 11, 2: 22, 3: 33, 4: 44, 5: 55}

    # Expected: all nodes on paths from any source to sink
    expected = {11, 22, 33, 44, 55}
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Multiple sources to one sink")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_one_source_multiple_sinks():
    """Test one source diverging to multiple sinks"""
    edge_list = [(1, 2), (2, 3), (2, 4), (3, 5), (4, 6)]
    sources = {1}
    sinks = {5, 6}
    max_depth = 5
    max_paths = 100
    nid_to_cidx_map = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}

    # Expected: all nodes on paths from source to any sink
    expected = {100, 200, 300, 400, 500, 600}
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: One source to multiple sinks")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_one_source_multiple_sinks_np():
    """Test one source diverging to multiple sinks"""
    edge_list = np.asarray([(1, 2), (2, 3), (2, 4), (3, 5), (4, 6)])
    sources = {1}
    sinks = {5, 6}
    max_depth = 5
    max_paths = 100
    nid_to_cidx_map = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}

    # Expected: all nodes on paths from source to any sink
    expected = {100, 200, 300, 400, 500, 600}
    actual = isolate_subcircuit_np_edgelist(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: One source to multiple sinks")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_diamond_pattern():
    """Test diamond pattern with multiple paths"""
    edge_list = [(1, 2), (1, 3), (2, 4), (3, 4)]
    sources = {1}
    sinks = {4}
    max_depth = 5
    max_paths = 100
    nid_to_cidx_map = {1: 1000, 2: 2000, 3: 3000, 4: 4000}

    # Expected: all nodes in the diamond
    expected = {1000, 2000, 3000, 4000}
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Diamond pattern")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_no_mapping_provided():
    """Test with nid_to_cidx_map = None (should create identity mapping)"""
    edge_list = [(10, 20), (20, 30), (30, 40)]
    sources = {10}
    sinks = {40}
    max_depth = 5
    max_paths = 100

    # Expected: identity mapping, so NeuronID == CMatIdx
    expected = {0, 1, 2, 3}
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths)
    assert actual == expected

    print(f"\nTest: No mapping provided (None)")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"Expected: {expected}")


def test_disconnected_source_sink():
    """Test when sources and sinks are not connected"""
    edge_list = [(1, 2), (3, 4), (5, 6)]
    sources = {1}
    sinks = {6}
    max_depth = 10
    max_paths = 100
    nid_to_cidx_map = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}

    # Expected: empty set (no paths from source to sink)
    expected = set()
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Disconnected source and sink")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_disconnected_source_sink():
    """Test when sources and sinks are not connected"""
    edge_list = np.asarray([(1, 2), (3, 4), (5, 6)])
    sources = {1}
    sinks = {6}
    max_depth = 10
    max_paths = 100
    nid_to_cidx_map = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}

    # Expected: empty set (no paths from source to sink)
    expected = set()
    actual = isolate_subcircuit_np_edgelist(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Disconnected source and sink")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_complex_network():
    """Test complex network with multiple sources and sinks"""
    edge_list = [(1, 3), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (4, 7), (5, 8), (6, 9), (7, 9), (8, 9)]
    sources = {1, 2}
    sinks = {7, 8, 9}
    max_depth = 8
    max_paths = 200
    nid_to_cidx_map = {i: i * 10 for i in range(1, 10)}

    # Expected: all nodes on any path from {1,2} to {7,8,9}
    expected = {10, 20, 30, 40, 50, 60, 70, 80, 90}

    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Complex network")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_depth_limited():
    """Test with restrictive depth limit"""
    edge_list = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
    sources = {1}
    sinks = {6}
    max_depth = 3  # Too shallow to reach sink
    max_paths = 100
    nid_to_cidx_map = {i: i * 100 for i in range(1, 7)}

    # Expected: empty set (depth limit prevents reaching sink)
    expected = set()
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Depth limited")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"max_depth={max_depth}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_cycles_with_sources_sinks():
    """Test with cycles between sources and sinks"""
    edge_list = [
        (1, 2),
        (2, 3),
        (3, 2),  # Cycle between 2-3
        (3, 4),
        (4, 5),
    ]
    sources = {1}
    sinks = {5}
    max_depth = 8
    max_paths = 100
    nid_to_cidx_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

    # Expected: path from 1 to 5, avoiding infinite cycle
    expected = {1, 2, 3, 4, 5}
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Cycles between sources and sinks")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_large_sparse_ids():
    """Test with large, sparse neuron IDs"""
    edge_list = [(1000, 5000), (5000, 10000), (10000, 20000)]
    sources = {1000}
    sinks = {20000}
    max_depth = 5
    max_paths = 100
    nid_to_cidx_map = {1000: 0, 5000: 1, 10000: 2, 20000: 3}

    expected = {0, 1, 2, 3}
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Large sparse IDs")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_empty_sources():
    """Test with empty sources set"""
    edge_list = [(1, 2), (2, 3)]
    sources = set()
    sinks = {3}
    max_depth = 5
    max_paths = 100
    nid_to_cidx_map = {1: 10, 2: 20, 3: 30}

    expected = set()  # No sources = no paths
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Empty sources")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_empty_sinks():
    """Test with empty sinks set"""
    edge_list = [(1, 2), (2, 3)]
    sources = {1}
    sinks = set()
    max_depth = 5
    max_paths = 100
    nid_to_cidx_map = {1: 10, 2: 20, 3: 30}

    expected = set()  # No sinks = no paths
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Empty sinks")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


def test_overlapping_sources_sinks():
    """Test when sources and sinks overlap"""
    edge_list = [(1, 2), (2, 3), (3, 4), (1, 4)]
    sources = {1, 3}
    sinks = {3, 4}
    max_depth = 5
    max_paths = 100
    nid_to_cidx_map = {1: 100, 2: 200, 3: 300, 4: 400}

    # Expected: paths from 1->3, 1->4, 3->4, plus 3 itself
    expected = {100, 200, 300, 400}
    actual = isolate_subcircuit(edge_list, sources, sinks, max_depth, max_paths, nid_to_cidx_map)
    assert actual == expected

    print(f"\nTest: Overlapping sources and sinks")
    print(f"edge_list={edge_list}")
    print(f"sources={sources}, sinks={sinks}")
    print(f"nid_to_cidx_map={nid_to_cidx_map}")
    print(f"Expected: {expected}")


# Test runner
def run_all_tests():
    """Run all test cases"""
    test_functions = [
        test_simple_source_to_sink,
        test_multiple_sources_one_sink,
        test_one_source_multiple_sinks,
        test_diamond_pattern,
        test_no_mapping_provided,
        test_disconnected_source_sink,
        test_source_is_sink,
        test_complex_network,
        test_depth_limited,
        test_path_limited,
        test_cycles_with_sources_sinks,
        test_large_sparse_ids,
        test_empty_sources,
        test_empty_sinks,
        test_overlapping_sources_sinks,
    ]

    print("Testing isolate_subcircuit function:")
    print("=" * 60)

    for i, test_func in enumerate(test_functions, 1):
        print(f"\n{i}. {test_func.__name__}:")
        print(f"   {test_func.__doc__}")
        test_func()
        print("-" * 50)


if __name__ == "__main__":
    run_all_tests()
