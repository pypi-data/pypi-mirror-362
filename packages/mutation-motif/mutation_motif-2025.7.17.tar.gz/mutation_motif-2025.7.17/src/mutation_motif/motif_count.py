from collections import Counter
from itertools import product

from cogent3 import get_moltype, make_table

from mutation_motif.util import array_to_str

dna_alpha = get_moltype("DNA").most_degen_alphabet()


def profile_to_seq_counts(data, flank_size):
    """converts data to seqs and returns sequence counts"""
    mp = data.shape[1] // 2
    indices = [i for i in range(mp - flank_size, mp + flank_size + 1) if i != mp]

    data = data.take(indices, axis=1)
    seqs = array_to_str(data)
    return Counter(seqs)


def get_count_table(observed, control, k=None):
    """return table of motif counts

    Each motif position is a separate column. All possible DNA motifs of length
    k are included.

    Arguments:
        - observed: the observed counts as {seq: count}
        - control: the control counts as {seq: count}
        - k: size of the motif"""
    rows = []
    lengths = set(
        list(map(len, list(observed.keys()))) + list(map(len, list(control.keys()))),
    )
    if len(lengths) != 1:
        msg = f"Motifs not all same length: {lengths}"
        raise ValueError(msg)

    length = next(iter(lengths))
    if k and length != k:
        raise ValueError("k[%d] doesn't match motif length [%d]" % (k, length))
    if k is None:
        k = length

    states = sorted(set(observed.keys()) | set(control.keys()))
    for state in states:
        state = "".join(state)
        control_counts = control[state]
        observed_counts = observed[state]
        if control_counts == observed_counts == 0:
            # we skip unobserved states
            continue

        rows.extend(
            (
                [control_counts, *list(state), "R"],
                [observed_counts, *list(state), "M"],
            ),
        )
    header = ["count"] + ["pos%d" % i for i in range(k)] + ["mut"]
    return make_table(header=header, rows=rows)


def reduced_multiple_positions(table, *positions):
    base_counts = {"M": Counter(), "R": Counter()}
    columns = ["count", "mut", *list(positions)]
    for row in table.to_list(columns):
        count = row[0]
        mut = row[1]
        motif = tuple(row[2:])
        base_counts[mut][motif] += count
    return base_counts


def reduced_one_position(table, pos):
    """returns base counts for one position"""
    base_counts = {"M": Counter(), "R": Counter()}
    for count, base, mut in table.to_list(["count", pos, "mut"]):
        base_counts[mut][base] += count
    return base_counts


def get_combined_counts(table, positions):
    bases = "ACGT"
    if type(positions) == str:
        counts = reduced_one_position(table, positions)
        mut_counts = counts["M"]
        unmut_counts = counts["R"]
        states = bases
        header = ["mut", "base", "count"]
    else:
        counts = reduced_multiple_positions(table, *positions)
        mut_counts = counts["M"]
        unmut_counts = counts["R"]
        states = product(*list([bases] * len(positions)))
        header = (
            ["mut"] + ["base%d" % (i + 1) for i in range(len(positions))] + ["count"]
        )

    combined = []
    for state in states:
        combined.extend(
            (
                ["R", *list(state), unmut_counts[state]],
                ["M", *list(state), mut_counts[state]],
            ),
        )
    counts_table = make_table(header=header, rows=combined)
    return counts_table.sorted(columns=header[:-1])
