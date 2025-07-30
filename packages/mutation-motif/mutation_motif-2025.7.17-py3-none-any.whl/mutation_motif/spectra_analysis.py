import json
import os

from cogent3 import make_table

from mutation_motif import draw, log_lin, util
from mutation_motif.util import load_table_from_delimited_file, pdf_writer

write_fig = pdf_writer()


def dump_json(data, outfile_path) -> None:
    with open(outfile_path, mode="w") as outfile:
        json.dump(data, outfile)


def main(
    countsfile,
    outpath,
    countsfile2,
    strand_symmetry,
    force_overwrite,
    dry_run,
    verbose,
    LOGGER,
) -> None:
    args = locals()

    table = load_table_from_delimited_file(countsfile, sep="\t")
    if not dry_run:
        log_file_path = os.path.join(util.abspath(outpath), "spectra_analysis.log")
        LOGGER.log_file_path = log_file_path
        LOGGER.log_message(str(args), label="vars")

    LOGGER.input_file(countsfile)
    # if there's a strand symmetry argument then we don't need a second file
    if strand_symmetry:
        group_label = "strand"
        counts_table = util.spectra_table(table, group_label)

    if not strand_symmetry:
        group_label = "group"

        # be sure there's two files
        assert countsfile2, "must provide second counts file"
        counts_table2 = load_table_from_delimited_file(countsfile2, sep="\t")
        LOGGER.input_file(countsfile2)
        counts_table2 = counts_table2.with_new_column(
            "group",
            lambda x: "2",
            columns=counts_table2.header[0],
        )
        counts_table1 = table.with_new_column(
            "group",
            lambda x: "1",
            columns=table.header[0],
        )

        counts_table1 = util.spectra_table(counts_table1, group_label)
        counts_table2 = util.spectra_table(counts_table2, group_label)
        # now combine
        header = ["group", *list(counts_table2.header[:-1])]
        counts_table = counts_table1.appended(None, counts_table2)
        counts_table = counts_table.get_columns(header)

    if verbose:
        print(counts_table)

    # spectra table has [count, start, end, group] order
    # we reduce comparisons to a start base
    results = []
    saveable = {}
    for start_base in counts_table.distinct_values("start"):
        subtable = select_mutating_base(counts_table, start_base)
        result = log_lin.spectra_difference(
            subtable,
            group_label,
        )
        r = [list(x) for x in result.df.to_records(index=False)]

        if not strand_symmetry:
            grp_labels = {"1": countsfile, "2": countsfile2}
            grp_index = list(result.df.columns).index("group")
            for row in r:
                row[grp_index] = grp_labels[row[grp_index]]

        p = result.pvalue
        prob = f"{p:.2e}" if p < 1e-6 else f"{p:.6f}"
        for row in r:
            row.insert(0, start_base)
            row.append(prob)

        results += r

        significance = [
            f"RE={result.relative_entropy:.6f}",
            f"Dev={result.deviance:.2f}",
            f"df={result.nfp}",
            f"p={p}",
        ]

        stats = "  :  ".join(significance)
        print(f"Start base={start_base}  {stats}")
        saveable[start_base] = {
            "rel_entropy": result.relative_entropy,
            "deviance": result.deviance,
            "df": result.nfp,
            "prob": result.pvalue,
            "formula": result.formula,
            "stats": result.df.to_json(),
        }

    table = make_table(
        header=["start_base", *list(result.df.columns), "prob"],
        rows=results,
        digits=5,
    ).sorted(columns="ret")
    json_path = None

    outpath = util.abspath(outpath)
    if not dry_run:
        util.makedirs(outpath)
        json_path = os.path.join(outpath, "spectra_analysis.json")
        dump_json(saveable, json_path)
        LOGGER.output_file(json_path)
        table_path = os.path.join(outpath, "spectra_summary.txt")
        table.write(table_path, sep="\t")
        LOGGER.output_file(table_path)
        LOGGER.log_message(str(significance), label="significance")
        fig_path = os.path.join(outpath, "spectra.pdf")
        fig = draw.get_spectra_grid_drawable(json_path, group_label=group_label)
        write_fig(fig, fig_path)
        LOGGER.shutdown()


def select_mutating_base(counts_table, start_base):
    subtable = counts_table.filtered(f'start == "{start_base}"')
    columns = [c for c in counts_table.header if c != "start"]
    return subtable.get_columns(columns)
