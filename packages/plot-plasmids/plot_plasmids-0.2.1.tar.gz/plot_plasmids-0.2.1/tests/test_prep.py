import pytest
import pandas as pd
from plot_plasmids import prep
import os
import shutil

@pytest.fixture
def temp_dir(tmpdir):
    """Create a temporary directory for test outputs."""
    return str(tmpdir)

def test_process_skani_matrix(temp_dir):
    """Test the process_skani_matrix function."""
    input_file = "tests/data/skani.dist.matrix.tsv"
    output_file = os.path.join(temp_dir, "skani.dist.matrix.modified.tsv")
    prep.process_skani_matrix(input_file, output_file)

    assert os.path.exists(output_file)
    df = pd.read_csv(output_file, sep='\t', index_col=0)
    assert df.shape == (4, 4)
    assert df.index.name is None
    assert (df.values == df.values.T).all()

def test_process_mob_typer_results(temp_dir):
    """Test the process_mob_typer_results function."""
    input_dir = os.path.join(temp_dir, "mob_typer_outputs")
    os.makedirs(input_dir, exist_ok=True)
    shutil.copy("tests/data/mob_single.tsv", os.path.join(input_dir, "SRR28860688_1.fasta.tsv"))
    shutil.copy("tests/data/mob_single.tsv", os.path.join(input_dir, "SRR28860689_1.fasta.tsv"))
    output_file = os.path.join(temp_dir, "mob_typer.results.tsv")
    prep.process_mob_typer_results(input_dir, output_file)

    assert os.path.exists(output_file)
    df = pd.read_csv(output_file, sep='\t')
    assert "plasmidID" in df.columns
    assert len(df) == 2
    assert sorted(df["plasmidID"].tolist()) == ["SRR28860688_1", "SRR28860689_1"]

def test_process_amrfinder_results(temp_dir):
    """Test the process_amrfinder_results function."""
    input_dir = os.path.join(temp_dir, "amrfinder_outputs")
    os.makedirs(input_dir, exist_ok=True)
    shutil.copy("tests/data/amr_single.tsv", os.path.join(input_dir, "SRR28860688_1.fasta.tsv"))
    shutil.copy("tests/data/amr_single.tsv", os.path.join(input_dir, "SRR28860689_1.fasta.tsv"))
    output_file = os.path.join(temp_dir, "amrfinder.results.tsv")
    prep.process_amrfinder_results(input_dir, output_file)

    assert os.path.exists(output_file)
    df = pd.read_csv(output_file, sep='\t')
    assert "plasmidID" in df.columns
    assert len(df) > 0
    assert sorted(list(set(df["plasmidID"].tolist()))) == sorted(["SRR28860688_1", "SRR28860689_1"])
