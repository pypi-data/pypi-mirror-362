use bindings::list_bindings::{
    adjacency_map_from_edge_list, isolate_subcircuit, map_neuron_ids_to_cmat_idxs,
};
use bindings::np_bindings::{
    adjacency_map_from_np_edge_list, isolate_subcircuit_np_edgelist, map_neuron_ids_to_cmat_idxs_np,
};
use pyo3::prelude::*;
pub mod bindings;
pub mod implementation;
/// Module for some fast circuit functions in Rust
#[pymodule]
fn circuit_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(isolate_subcircuit, m)?)?;
    m.add_function(wrap_pyfunction!(isolate_subcircuit_np_edgelist, m)?)?;

    m.add_function(wrap_pyfunction!(map_neuron_ids_to_cmat_idxs, m)?)?;
    m.add_function(wrap_pyfunction!(map_neuron_ids_to_cmat_idxs_np, m)?)?;
    m.add_function(wrap_pyfunction!(adjacency_map_from_edge_list, m)?)?;
    m.add_function(wrap_pyfunction!(adjacency_map_from_np_edge_list, m)?)?;

    Ok(())
}
