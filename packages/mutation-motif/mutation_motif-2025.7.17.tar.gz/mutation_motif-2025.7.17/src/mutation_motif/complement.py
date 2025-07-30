from cogent3 import DNA, make_table

MUTATION_COMPLEMENTS = {
    "CtoG": "GtoC",
    "CtoA": "GtoT",
    "AtoT": "TtoA",
    "CtoT": "GtoA",
    "AtoC": "TtoG",
    "AtoG": "TtoC",
}


def _reverse_complement(table):
    """returns a table with sequences reverse complemented"""
    pos_indices = [i for i, c in enumerate(table.header) if c.startswith("pos")]

    rows = table.to_list()
    for row in rows:
        # we use the cogent3 DnaSeq object to do reverse complementing
        seq = DNA.make_seq(seq="".join(row[i] for i in pos_indices))
        seq = list(seq.rc())
        for i, index in enumerate(pos_indices):
            row[index] = seq[i]
    return make_table(header=table.header, rows=rows) if rows else None


def add_strand_column(rows, strand):
    for row in rows:
        row.append(strand)
    return rows


def make_strand_symmetric_table(table):
    """takes a combined counts table and returns a table with reverse
    complemented seqs

    Uses MUTATION_COMPLEMENTS"""

    new_data = []
    direction_index = next(
        i for i in range(len(table.header)) if table.header[i] == "direction"
    )
    for plus, minus in list(MUTATION_COMPLEMENTS.items()):
        plus_table = table.filtered(f'direction=="{plus}"')
        plus_data = add_strand_column(plus_table.to_list(), "+")
        new_data.extend(plus_data)

        minus_table = table.filtered(f'direction=="{minus}"')
        if minus_table.shape[0] == 0:
            continue
        minus_table = _reverse_complement(minus_table)
        minus_data = minus_table.to_list()
        for row in minus_data:
            row[direction_index] = plus
        minus_data = add_strand_column(minus_data, "-")
        new_data.extend(minus_data)

    return make_table(header=[*list(table.header[:]), "strand"], rows=new_data)
