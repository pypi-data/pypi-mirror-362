use std::collections::{HashMap, HashSet};

use implementation::{
    circuit_common::{
        CMatIdx, NeuronID, adjacency_map_and_cmat_idxs_from_edge_list, map_neuron_id_to_cmat_idx,
    },
    isolate::find_subcircuit_from_edge_list,
};
use pyo3::prelude::*;

use crate::implementation;

/// Isolate the smallest subcircuit that includes all paths from all sources to sinks,
/// considering some prior biology information
#[pyfunction]
#[pyo3(signature = (edge_list, sources, sinks, max_depth=10, max_paths=1_000, nid_to_cidx_map=None))]
pub(crate) fn isolate_subcircuit(
    edge_list: Vec<(NeuronID, NeuronID)>,
    sources: HashSet<NeuronID>,
    sinks: HashSet<NeuronID>,
    max_depth: usize,
    max_paths: usize,
    nid_to_cidx_map: Option<HashMap<NeuronID, CMatIdx>>,
) -> HashSet<CMatIdx> {
    match nid_to_cidx_map {
        Some(map) => {
            find_subcircuit_from_edge_list(edge_list, sources, sinks, max_depth, max_paths, map)
        }
        None => {
            let nid_to_cidx_map = map_neuron_id_to_cmat_idx(&edge_list);
            find_subcircuit_from_edge_list(
                edge_list,
                sources,
                sinks,
                max_depth,
                max_paths,
                nid_to_cidx_map,
            )
        }
    }
}

/// Generate a default mapping from neuron IDs to some index in a adjacency matrix
#[pyfunction]
#[pyo3(signature = (edge_list))]
pub(crate) fn map_neuron_ids_to_cmat_idxs(
    edge_list: Vec<(NeuronID, NeuronID)>,
) -> HashMap<NeuronID, CMatIdx> {
    map_neuron_id_to_cmat_idx(&edge_list)
}

/// Generate an adjacency map, which enables searching across large matrices, optionally
/// accepting a mapping from neuron IDs to some place in a connectivity matrix
#[pyfunction]
#[pyo3(signature = (edge_list, nid_to_cidx_map=None))]
pub(crate) fn adjacency_map_from_edge_list(
    edge_list: Vec<(NeuronID, NeuronID)>,
    nid_to_cidx_map: Option<HashMap<NeuronID, CMatIdx>>,
) -> HashMap<CMatIdx, HashSet<CMatIdx>> {
    match nid_to_cidx_map {
        Some(v) => {
            let (map, _, _) = adjacency_map_and_cmat_idxs_from_edge_list(&edge_list, &v);
            map
        }
        None => {
            let tracker = map_neuron_id_to_cmat_idx(&edge_list);
            let (map, _, _) = adjacency_map_and_cmat_idxs_from_edge_list(&edge_list, &tracker);
            map
        }
    }
}
