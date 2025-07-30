use std::collections::{HashMap, HashSet};

/// Common functions that might be useful for the user, and for the scripts we've got
///

pub(crate) type NeuronID = u32;
pub(crate) type CMatIdx = u32;

pub fn map_neuron_id_to_cmat_idx(
    edge_list: &Vec<(NeuronID, NeuronID)>,
) -> HashMap<NeuronID, CMatIdx> {
    let mut tracker = HashMap::new();
    for (pre, post) in edge_list.iter() {
        if !tracker.contains_key(pre) {
            tracker.insert(*pre, tracker.len() as u32);
        }
        if !tracker.contains_key(post) {
            tracker.insert(*post, tracker.len() as u32);
        }
    }

    tracker
}

pub fn adjacency_map_and_cmat_idxs_from_edge_list(
    edge_list: &Vec<(NeuronID, NeuronID)>,
    nid_to_cidx: &HashMap<NeuronID, CMatIdx>,
) -> (
    HashMap<CMatIdx, HashSet<CMatIdx>>,
    HashSet<CMatIdx>,
    HashSet<CMatIdx>,
) {
    let mut source_cidxs: HashSet<CMatIdx> = HashSet::new();
    let mut sink_cidxs: HashSet<CMatIdx> = HashSet::new();
    let mut pre_to_post_map: HashMap<CMatIdx, HashSet<CMatIdx>> = HashMap::new();

    for (source_nid, sink_nid) in edge_list.iter() {
        // Note: on the python end, when constructing the CMat, we're already
        //   guaranteed that all sinks and sources exist in the `nid_to_cidx` map
        let source_cidx = *nid_to_cidx.get(source_nid).unwrap();
        let sink_cidx = *nid_to_cidx.get(sink_nid).unwrap();

        pre_to_post_map
            .entry(source_cidx)
            .or_insert_with(HashSet::new)
            .insert(sink_cidx);
        source_cidxs.insert(source_cidx);
        sink_cidxs.insert(sink_cidx);
    }
    (pre_to_post_map, source_cidxs, sink_cidxs)
}
