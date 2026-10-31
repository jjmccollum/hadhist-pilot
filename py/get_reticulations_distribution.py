#!/usr/bin/env python3

from pathlib import Path
import argparse
import re
import math
from ete3 import Tree, TreeNode
from tqdm import tqdm # for progress bar

"""
Regular expression pattern for metadata in a tree.
"""
metadata_pattern = re.compile(r"(\[[^\[\]]+\])")

"""
Regular expression patterns for reticulation nodes.
"""
reticulation_source_pattern = re.compile(r"\)(\#\d+):([\d\.]+)")
reticulation_destination_pattern = re.compile(r",(\#\d+):0\.00001")

"""
Given a .trees file, counts the number of trees in the file.
"""
def get_trees_count(trees_file: Path):
    trees_count = 0
    with open(trees_file, "r") as f:
        for line in f:
            if line.strip().startswith("tree"):
                trees_count += 1
    return trees_count

"""
Given a TreeNode, recursively traverse it and populate a dictionary
whose keys are the reticulation ID numbers and whose values are lists containing two lists of strings,
where the two lists contain the indices of leaves under the source and destination branches, respectively.
This method returns a list containing the indices of leaves under the current node.
"""
def extract_reticulations(node: TreeNode, reticulations_by_id: dict[str, list[list[str]]]):
    # Proceed according to whether the current node is a leaf or an internal node:
    if node.is_leaf():
        # If it is a leaf, then check if it is the destination node of a reticulation:
        if node.name.startswith("#"):
            # If it is, then return an empty list (we will handle this node when we process its parent):
            return []
        else:
            # If it is a true leaf node, then return a list containing its index:
            return [int(node.name)]
    # If the current node is an internal node, then first recurse over its children, populating a list of all their leaves under it:
    leaves = []
    for child in node.children:
        leaves += extract_reticulations(child, reticulations_by_id)
    # If any child is the destination node of a reticulation, then add an entry for it to the dictionary using the current list of leaves
    # (a child could also be the source node of a reticulation, but we will already have processed it in the previous loop):
    for child in node.children:
        if child.name.startswith("#") and child.name[-2:] == "_2":
            reticulation_id = child.name.strip("#")[:-2]
            if reticulation_id not in reticulations_by_id:
                reticulations_by_id[reticulation_id] = [None, None]
            reticulations_by_id[reticulation_id][1] = leaves.copy()
    # Otherwise, if this node is the source node of a reticulation, then add an entry for it to the dictionary using the current list of leaves:
    if node.name.startswith("#"):
        reticulation_id = node.name.strip("#")[:-2]
        if reticulation_id not in reticulations_by_id:
            reticulations_by_id[reticulation_id] = [None, None]
        reticulations_by_id[reticulation_id][0] = leaves.copy()
    # Finally, pass the set of leaves under this node up to its parent node:
    return leaves

"""
Given a .trees file, returns a dictionary mapping contact edges in the sampled trees to their posterior probabilities.
Optionally, a burn-in proportion can be specified.
The contact edges will be represented by the clades under their source and destination branches.
"""
def get_contact_edge_distribution(trees_file: Path, burnin: float=0.0):
    posteriors_by_source_dest_tuple = {}
    total_trees = get_trees_count(trees_file)
    burnin_trees = math.ceil(burnin*total_trees)
    trees_processed = 0
    tree = None # placeholder for the current tree being processed
    parsing_translate = False
    with tqdm(total=total_trees-burnin_trees) as pbar:
        with open(trees_file, "r") as f:
            indices_by_id = {}
            ids_by_index = {}
            for line in f:
                # Switch upon reaching the Translate block:
                if not parsing_translate and line.strip().startswith("Translate"):
                    parsing_translate = True
                    continue
                # Switch upon reaching the end of the Translate block:
                if parsing_translate and line.strip().startswith(";"):
                    parsing_translate = False
                    continue
                # Switch for processing all other lines in the translate block:
                if parsing_translate:
                    components = line.strip().strip(",").split()
                    wit_index = int(components[0])
                    wit_id = components[1]
                    indices_by_id[wit_id] = wit_index
                    ids_by_index[wit_index] = wit_id
                    continue
                # Switch for reaching the first tree specification:
                if line.strip().startswith("tree"):
                    # If we are still within the burn-in bound, then do nothing except increment the processed trees count:
                    if trees_processed < burnin_trees:
                        trees_processed += 1
                        continue
                    # Get the string containing the Newick representation of the tree:
                    newick = line.strip().split(" = ")[1]
                    # Remove the reticulation prefix and all metadata sequences in the tree:
                    newick = newick.strip("[&R] ")
                    newick = re.sub(metadata_pattern, "", newick)
                    # Then relabel all paired reticulation nodes so that they are distinct:
                    newick = re.sub(reticulation_source_pattern, r")\1_1:\2", newick)
                    newick = re.sub(reticulation_destination_pattern, r",\1_2:0.0", newick)
                    # Then initialize a tree object from this reformatted string:
                    tree = Tree(newick, format=1)
                    # Then extract the data for contact edges:
                    reticulations_by_id = {}
                    extract_reticulations(tree.get_tree_root(), reticulations_by_id)
                    # For each contact edge, convert the lists of leaf indices under its source and destination to sorted lists of leaf names,
                    # and increment the count for this pair of lists (making sure to avoid double-counting if there are multiple, which should be rare):
                    processed_tuples = set()
                    for reticulation_id in reticulations_by_id:
                        source_leaf_indices = sorted(reticulations_by_id[reticulation_id][0])
                        destination_leaf_indices = sorted(reticulations_by_id[reticulation_id][1])
                        source_leaf_names = [ids_by_index[index] for index in source_leaf_indices]
                        destination_leaf_names = [ids_by_index[index] for index in destination_leaf_indices]
                        source_dest_tuple = tuple(["(" + ",".join(source_leaf_names) + ")", "(" + ",".join(destination_leaf_names) + ")"])
                        # Do not increment the count for this tuple if another contact edge in this tree has already done so:
                        if source_dest_tuple in processed_tuples:
                            continue
                        if source_dest_tuple not in posteriors_by_source_dest_tuple:
                            posteriors_by_source_dest_tuple[source_dest_tuple] = 0
                        posteriors_by_source_dest_tuple[source_dest_tuple] += 1
                        processed_tuples.add(source_dest_tuple)
                    trees_processed += 1
                    pbar.update(1)
    # Finally, normalize the frequencies of the observed contact edges:
    for source_dest_tuple in posteriors_by_source_dest_tuple:
        posteriors_by_source_dest_tuple[source_dest_tuple] = posteriors_by_source_dest_tuple[source_dest_tuple] / (trees_processed - burnin_trees)
    return posteriors_by_source_dest_tuple

"""
Entry point to the script. Parses command-line arguments and calls the core functions.
"""
def main():
    parser = argparse.ArgumentParser(description="Extract a dictionary of posterior probabilities for contact edges from the sampled networks in a given .trees file.\nThe source and destination branches of the contact edges are described in terms of the clades beneath them.")
    parser.add_argument("--burnin", "-b", type=float, default=0.0, help="Burn-in proportion for sampled trees.")
    parser.add_argument("trees_input", type=str, help="Input .trees file.")
    parser.add_argument("log_output", type=str, help="Output file.")
    # Parse the command-line arguments:
    args = parser.parse_args()
    trees_input = args.trees_input
    log_output = args.log_output
    burnin = args.burnin
    # Do not allow burn-in proportions outside of [0, 1):
    if burnin < 0.0 or burnin >= 1.0:
        print("ERROR: burn-in proportion must be at least 0.0 and less than 1.0.")
        exit(1)
    # Then process the file:
    posteriors_by_source_dest_tuple = get_contact_edge_distribution(trees_input, burnin)
    with open(log_output, "w") as f:
        for source_dest_tuple, p in sorted(posteriors_by_source_dest_tuple.items(), key=lambda item: item[1], reverse=True):
            f.write("%s -> %s: %f\n" % (str(source_dest_tuple[0]), str(source_dest_tuple[1]), p))
    exit(0)

if __name__=="__main__":
    main()
