import pytest
from circuit_rs import map_neuron_ids_to_cmat_idxs, adjacency_map_from_edge_list

NeuronID = int
CMatIdx = int


def test_adjacency_map_from_edge_list_no_prior_map():
    """Test simple linear circuit: 1->2->3->4"""
    edge_list = [(1, 2), (2, 3), (3, 4)]

    #####################################
    # No prior-constructed nid-cidx-map:
    #####################################
    result = adjacency_map_from_edge_list(edge_list, None)
    expected = {0: {1}, 1: {2}, 2: {3}}

    assert result == expected
    print(f"Simple adjacency map from edge list completed")


def test_adjacency_map_from_edge_list_w_prior_map():
    """Test simple linear circuit: 1->2->3->4"""
    edge_list = [(1, 2), (2, 3), (3, 4)]

    #####################################
    # No prior-constructed nid-cidx-map:
    #####################################
    mapping = {1: 10, 2: 20, 3: 30, 4: 40}

    result = adjacency_map_from_edge_list(edge_list, mapping)
    expected = {10: {20}, 20: {30}, 30: {40}}

    assert result == expected
    print(f"Adjacency map from edge list and nid-cidx-map completed")
