import pytest
import pandas as pd
from plot_plasmids import main
import os
import argparse

@pytest.fixture
def temp_dir(tmpdir):
    """Create a temporary directory for test outputs."""
    return str(tmpdir)

def test_clean_plasmid_id():
    assert main.clean_plasmid_id("plasmid1.fasta") == "plasmid1"
    assert main.clean_plasmid_id("/path/to/plasmid2.fa") == "plasmid2"
    assert main.clean_plasmid_id("plasmid3") == "plasmid3"

def test_load_distance_matrix():
    matrix = main.load_distance_matrix("tests/data/dist_matrix.csv")
    assert isinstance(matrix, pd.DataFrame)
    assert matrix.shape == (4, 4)
    assert "plasmid1" in matrix.index
    assert "plasmid2" in matrix.columns

def test_parse_amr_results():
    amr_map = main.parse_amr_results("tests/data/amr.tsv")
    assert isinstance(amr_map, pd.Series)
    assert amr_map["plasmid1"] == "blaKPC-2"
    assert amr_map["plasmid2"] == "blaNDM-1"
    assert amr_map["plasmid3"] == "blaOXA-48"
    assert amr_map["plasmid4"] == "blaKPC-2"

def test_parse_mob_results():
    mob_map = main.parse_mob_results("tests/data/mob.tsv")
    assert isinstance(mob_map, pd.Series)
    assert mob_map["plasmid1"] == "IncFIB;IncFII"
    assert mob_map["plasmid2"] == "IncA/C2"
    assert mob_map["plasmid3"] == "IncA/C2"
    assert mob_map["plasmid4"] == "IncX3"

def test_run_ordination():
    dist_matrix = pd.DataFrame(
        [[0.0, 0.1], [0.1, 0.0]],
        index=["p1", "p2"],
        columns=["p1", "p2"]
    )
    pcoa_res = main.run_ordination(dist_matrix, method='pcoa')
    assert pcoa_res is not None
    nmds_res = main.run_ordination(dist_matrix, method='nmds')
    assert nmds_res is not None

def test_run_plot(temp_dir):
    output_path_pcoa = os.path.join(temp_dir, "pcoa_plot.png")
    output_path_nmds = os.path.join(temp_dir, "nmds_plot.png")

    # Test PCoA plot
    args_pcoa = argparse.Namespace(
        dist_matrix="tests/data/dist_matrix.csv",
        amr="tests/data/amr.tsv",
        mob="tests/data/mob.tsv",
        output=output_path_pcoa,
        plot_type='pcoa'
    )
    main.run_plot(args_pcoa)
    assert os.path.exists(output_path_pcoa)

    # Test NMDS plot
    args_nmds = argparse.Namespace(
        dist_matrix="tests/data/dist_matrix.csv",
        amr="tests/data/amr.tsv",
        mob="tests/data/mob.tsv",
        output=output_path_nmds,
        plot_type='nmds'
    )
    main.run_plot(args_nmds)
    assert os.path.exists(output_path_nmds)
