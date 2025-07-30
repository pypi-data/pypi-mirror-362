use crate::implementation::circuit_common::{
    CMatIdx, NeuronID, adjacency_map_and_cmat_idxs_from_edge_list,
};
/// Given a set of sink and source nodes with some number of max-hops, isolate the smallest
/// sub-circuit that includes all paths between all elements in the sink and source.
///
/// NOTE: the max_depth is really important and you want to set this for sure. Finding all
/// paths is in O(n!), so this grows QUICK
use log;
use std::collections::VecDeque;
use std::collections::{HashMap, HashSet};
use tqdm::pbar;

fn _find_subcircuit_from_edges(
    sources: HashSet<CMatIdx>,
    sinks: HashSet<CMatIdx>,
    adjacency_map: HashMap<CMatIdx, HashSet<CMatIdx>>,
    max_depth: usize,
    max_paths: usize,
) -> HashSet<CMatIdx> {
    let mut nodes_on_path: HashSet<CMatIdx> = HashSet::new();
    let mut viable_pairs: Vec<(CMatIdx, CMatIdx)> = Vec::new();

    // First, get all the viable pairs i.e. where we have smth from source
    // to sink factoring in the max_depth

    for source in sources.iter() {
        let mut reachable: HashSet<CMatIdx> = HashSet::new();
        let mut queue: VecDeque<(CMatIdx, u64)> = VecDeque::new();
        queue.push_back((*source, 0 as u64));

        let mut visited: HashSet<CMatIdx> = HashSet::new();
        visited.insert(*source);

        while !queue.is_empty() {
            let (node, depth) = queue.pop_front().unwrap();
            if depth as usize >= max_depth {
                continue;
            }

            for neighbor in adjacency_map.get(&node).unwrap_or(&HashSet::new()) {
                if !visited.contains(neighbor) {
                    visited.insert(*neighbor);
                    reachable.insert(*neighbor);
                    queue.push_back((*neighbor, depth + 1));
                }
            }
        }
        // Now, given everything that the current source has seen, determine if
        // the sink is reachable and the connection is viable.
        for sink in sinks.iter() {
            if reachable.contains(sink) {
                viable_pairs.push((*source, *sink));
            }
        }
    }

    let log_msg = format!(
        "Found #{} viable pairs from #{} possible",
        viable_pairs.len(),
        sources.len() * sinks.len()
    );
    log::info!("{}", log_msg.as_str());

    // Now that we have viable pairs, get the nodes between, in the paths
    let mut pbar = pbar(Some(viable_pairs.len()));
    let mut counter = 0;

    for (source, sink) in viable_pairs.iter() {
        pbar.update(counter).unwrap();
        counter += 1;
        let paths: Vec<Vec<CMatIdx>> =
            find_paths_with_progress(*source, *sink, adjacency_map.clone(), max_depth, max_paths);

        for path in paths.iter() {
            nodes_on_path.extend(path.iter());
        }
    }

    nodes_on_path
}

fn find_paths_with_progress(
    start: CMatIdx,
    end: CMatIdx,
    adjacency: HashMap<CMatIdx, HashSet<CMatIdx>>,
    max_depth: usize,
    max_paths: usize,
) -> Vec<Vec<CMatIdx>> {
    let mut paths = Vec::new();
    let mut queue = VecDeque::new();

    let mut start_visited = HashSet::new();
    start_visited.insert(start);
    queue.push_back((start, vec![start], start_visited));

    while !queue.is_empty() && paths.len() < max_paths {
        let (current, path, visited) = queue.pop_front().unwrap();

        if current == end {
            paths.push(path);
            continue;
        }

        if path.len() >= max_depth {
            continue;
        }

        for neighbor in adjacency.get(&current).unwrap_or(&HashSet::new()) {
            if !visited.contains(neighbor) {
                // This is the key fix!
                let mut new_visited = visited.clone();
                new_visited.insert(*neighbor);
                let mut new_path = path.clone();
                new_path.push(*neighbor);
                queue.push_back((*neighbor, new_path, new_visited));
            }
        }
    }

    paths
}
// Requires an already-constructed connectivity matrix
// Assumes that the edge_list format is (pre-neuron, post-neuron) aka (sender, receiver)
pub fn find_subcircuit_from_edge_list(
    edge_list: Vec<(NeuronID, NeuronID)>,
    sources: HashSet<NeuronID>,
    sinks: HashSet<NeuronID>,
    max_depth: usize,
    max_paths: usize,
    nid_to_cidx_map: HashMap<NeuronID, CMatIdx>,
) -> HashSet<CMatIdx> {
    let (pre_to_post_map, _, _) =
        adjacency_map_and_cmat_idxs_from_edge_list(&edge_list, &nid_to_cidx_map);

    let source_cidxs = sources
        .iter()
        .map(|nid| *nid_to_cidx_map.get(nid).unwrap())
        .collect();
    let sink_cidxs = sinks
        .iter()
        .map(|nid| *nid_to_cidx_map.get(nid).unwrap())
        .collect();

    _find_subcircuit_from_edges(
        source_cidxs,
        sink_cidxs,
        pre_to_post_map,
        max_depth,
        max_paths,
    )
}
