use numpy::PyReadonlyArray2;

use std::collections::{HashMap, HashSet};

use crate::implementation;
use implementation::{
    circuit_common::{
        CMatIdx, NeuronID, adjacency_map_and_cmat_idxs_from_edge_list, map_neuron_id_to_cmat_idx,
    },
    isolate::find_subcircuit_from_edge_list,
};
use pyo3::prelude::*;

#[pyfunction]
#[pyo3(signature = (edge_array, sources, sinks, max_depth=10, max_paths=1_000, nid_to_cidx_map=None))]
pub(crate) fn isolate_subcircuit_np_edgelist(
    edge_array: PyReadonlyArray2<i64>,
    sources: HashSet<u32>,
    sinks: HashSet<u32>,
    max_depth: usize,
    max_paths: usize,
    nid_to_cidx_map: Option<HashMap<u32, u32>>,
) -> HashSet<CMatIdx> {
    let edge_array = edge_array.as_array();
    let mut edge_list = Vec::new();

    for row in edge_array.outer_iter() {
        if row.len() >= 2 {
            let source = row[0] as u32; // Cast from i64 to u32
            let target = row[1] as u32;
            edge_list.push((source, target));
        }
    }

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
#[pyo3(signature = (edge_array))]
pub(crate) fn map_neuron_ids_to_cmat_idxs_np(
    edge_array: PyReadonlyArray2<i64>,
) -> HashMap<NeuronID, CMatIdx> {
    let edge_array = edge_array.as_array();
    let mut edge_list = Vec::new();

    for row in edge_array.outer_iter() {
        if row.len() >= 2 {
            let source = row[0] as u32; // Cast from i64 to u32
            let target = row[1] as u32;
            edge_list.push((source, target));
        }
    }

    map_neuron_id_to_cmat_idx(&edge_list)
}

/// Generate an adjacency map, which enables searching across large matrices, optionally
/// accepting a mapping from neuron IDs to some place in a connectivity matrix
#[pyfunction]
#[pyo3(signature = (edge_array, nid_to_cidx_map=None))]
pub(crate) fn adjacency_map_from_np_edge_list(
    edge_array: PyReadonlyArray2<i64>,
    nid_to_cidx_map: Option<HashMap<NeuronID, CMatIdx>>,
) -> HashMap<CMatIdx, HashSet<CMatIdx>> {
    let edge_array = edge_array.as_array();
    let mut edge_list = Vec::new();

    for row in edge_array.outer_iter() {
        if row.len() >= 2 {
            let source = row[0] as u32; // Cast from i64 to u32
            let target = row[1] as u32;
            edge_list.push((source, target));
        }
    }

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
