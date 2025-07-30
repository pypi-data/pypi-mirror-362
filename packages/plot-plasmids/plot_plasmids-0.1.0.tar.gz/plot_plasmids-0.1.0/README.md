# plot_plasmids

[![PyPI version](https://badge.fury.io/py/plot-plasmids.svg)](https://badge.fury.io/py/plot-plasmids)
[![codecov](https://codecov.io/gh/jules-corp/plot_plasmids/branch/main/graph/badge.svg?token=placeholder)](https://codecov.io/gh/jules-corp/plot_plasmids)

A tool to generate PCoA or NMDS plots for plasmids, colored by carbapenemase genes and rep types.

## Installation

You can install `plot_plasmids` from PyPI:

```bash
pip install plot-plasmids
```

Or, for development, you can install it from this repository:

```bash
git clone https://github.com/example/plot_plasmids.git
cd plot_plasmids
pip install -e .
```

## Usage

```bash
plot_plasmids -d tests/data/dist_matrix.csv -a tests/data/amr.tsv -m tests/data/mob.tsv -o example.png
```

![Example plot](tests/expected_output/expected_plot_nmds.png)

### Arguments

- `-d`, `--dist_matrix`: Path to the plasmid distance matrix (CSV or TSV format).
- `-a`, `--amr`: Path to the AMRfinderPlus summary results file (TSV format).
- `-m`, `--mob`: Path to the MOB-typer mob_recon_results.txt file (TSV format).
- `-o`, `--output`: Path for the output plot file (e.g., plot.png, plot.svg).
- `-p`, `--plot_type`: Type of ordination plot to generate (`pcoa` or `nmds`). Default is `pcoa`.
