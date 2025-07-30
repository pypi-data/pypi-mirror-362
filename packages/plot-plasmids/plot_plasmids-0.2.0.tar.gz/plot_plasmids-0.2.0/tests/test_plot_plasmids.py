import pytest
import pandas as pd
import numpy as np
from plot_plasmids import main
import os

@pytest.fixture
def temp_dir(tmpdir):
    return tmpdir

def test_clean_plasmid_id():
    assert main.clean_plasmid_id("plasmid1.fasta") == "plasmid1"
    assert main.clean_plasmid_id("/path/to/plasmid2.fa") == "plasmid2"
    assert main.clean_plasmid_id("plasmid3") == "plasmid3"

def test_load_distance_matrix(temp_dir):
    # Create a dummy distance matrix file
    dist_matrix_path = os.path.join(temp_dir, "dist_matrix.csv")
    with open(dist_matrix_path, "w") as f:
        f.write(",plasmid1,plasmid2\n")
        f.write("plasmid1,0.0,0.1\n")
        f.write("plasmid2,0.1,0.0\n")

    matrix = main.load_distance_matrix(dist_matrix_path)
    assert isinstance(matrix, pd.DataFrame)
    assert matrix.shape == (2, 2)
    assert "plasmid1" in matrix.index
    assert "plasmid2" in matrix.columns

def test_parse_amr_results(temp_dir):
    amr_path = os.path.join(temp_dir, "amr.tsv")
    with open(amr_path, "w") as f:
        f.write("plasmidID\tElement symbol\tSubclass\n")
        f.write("plasmid1/1\tblaKPC-2\tCARBAPENEM\n")
        f.write("plasmid2/1\tblaNDM-1\tCARBAPENEM\n")
        f.write("plasmid3/1\tblaOXA-48\tCARBAPENEM\n")
        f.write("plasmid4/1\tblaKPC-2\tCARBAPENEM\n")

    amr_map = main.parse_amr_results(amr_path)
    assert isinstance(amr_map, pd.Series)
    assert amr_map["plasmid1"] == "blaKPC-2"
    assert amr_map["plasmid2"] == "blaNDM-1"
    assert amr_map["plasmid3"] == "blaOXA-48"
    assert amr_map["plasmid4"] == "blaKPC-2"

def test_parse_mob_results(temp_dir):
    mob_path = os.path.join(temp_dir, "mob.tsv")
    with open(mob_path, "w") as f:
        f.write("sample_id\trep_type(s)\n")
        f.write("plasmid1\tIncFIB(pB2-2),IncFII(pB2-1)\n")
        f.write("plasmid2\tIncA/C2\n")
        f.write("plasmid3\tIncA/C2\n")
        f.write("plasmid4\tIncX3\n")

    mob_map = main.parse_mob_results(mob_path)
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

from PIL import Image
import imagehash

def test_create_plot(temp_dir):
    # expected plot
    expected_plot_path = "tests/expected_output/expected_plot.png"

    # generate plot
    dist_matrix = main.load_distance_matrix("tests/data/dist_matrix.csv")
    amr_map = main.parse_amr_results("tests/data/amr.tsv")
    mob_map = main.parse_mob_results("tests/data/mob.tsv")
    metadata = pd.DataFrame({"carb_gene": amr_map, "rep_type": mob_map})

    # Test PCoA plot
    ordination_result_pcoa = main.run_ordination(dist_matrix, method='pcoa')
    output_path_pcoa = os.path.join(temp_dir, "pcoa_plot.png")
    main.create_plot(ordination_result_pcoa, metadata, output_path_pcoa, 'pcoa')

    # Add a test to check that the plot is created and is correct
    assert os.path.exists(output_path_pcoa)

    # Compare the generated plot with the expected plot
    expected_hash_pcoa = imagehash.average_hash(Image.open(expected_plot_path))
    output_hash_pcoa = imagehash.average_hash(Image.open(output_path_pcoa))
    assert expected_hash_pcoa == output_hash_pcoa

    # Test NMDS plot
    ordination_result_nmds = main.run_ordination(dist_matrix, method='nmds')
    output_path_nmds = os.path.join(temp_dir, "nmds_plot.png")
    main.create_plot(ordination_result_nmds, metadata, output_path_nmds, 'nmds')

    # Add a test to check that the plot is created and is correct
    assert os.path.exists(output_path_nmds)

    # Compare the generated plot with the expected plot
    expected_hash_nmds = imagehash.average_hash(Image.open(expected_plot_path.replace('.png', '_nmds.png')))
    output_hash_nmds = imagehash.average_hash(Image.open(output_path_nmds))
    assert expected_hash_nmds == output_hash_nmds
