import pandas as pd
import os
import glob

def process_skani_matrix(input_file, output_file):
    """Processes the skani triangle matrix into a square matrix."""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    num_genomes = int(lines[0].strip())
    data = [line.strip().split('\t') for line in lines[1:]]

    plasmids = [row[0] for row in data]

    # Create an empty DataFrame
    df = pd.DataFrame(index=plasmids, columns=plasmids)

    # Fill the DataFrame
    for i in range(num_genomes):
        df.iloc[i, i] = 0.0
        for j in range(i):
            distance = float(data[i][j + 1])
            df.iloc[i, j] = distance
            df.iloc[j, i] = distance

    df.to_csv(output_file, sep='\t')
    print(f"✅ Processed skani matrix saved to {output_file}")


def process_mob_typer_results(input_dir, output_file):
    """Consolidates mob_typer results into a single file."""
    all_files = glob.glob(os.path.join(input_dir, '*.tsv'))
    df_list = []
    for f in all_files:
        df = pd.read_csv(f, sep='\t')
        plasmid_id = os.path.basename(f).replace('.fasta.tsv', '')
        df['plasmidID'] = plasmid_id
        df_list.append(df)

    if not df_list:
        print("⚠️ No mob_typer files found.")
        return

    concatenated_df = pd.concat(df_list, ignore_index=True)
    concatenated_df.to_csv(output_file, sep='\t', index=False)
    print(f"✅ Consolidated mob_typer results saved to {output_file}")

def process_amrfinder_results(input_dir, output_file):
    """Consolidates amrfinderplus results into a single file."""
    all_files = glob.glob(os.path.join(input_dir, '*.tsv'))
    df_list = []
    for f in all_files:
        df = pd.read_csv(f, sep='\t')
        plasmid_id = os.path.basename(f).replace('.fasta.tsv', '')
        df['plasmidID'] = plasmid_id
        df_list.append(df)

    if not df_list:
        print("⚠️ No amrfinderplus files found.")
        return

    concatenated_df = pd.concat(df_list, ignore_index=True)
    concatenated_df.to_csv(output_file, sep='\t', index=False)
    print(f"✅ Consolidated amrfinderplus results saved to {output_file}")


def run_prep(args):
    """Main function for the prep command."""
    os.makedirs(args.output_dir, exist_ok=True)

    # Process skani
    skani_out = os.path.join(args.output_dir, 'skani.dist.matrix.modified.tsv')
    process_skani_matrix(args.skani, skani_out)

    # Process mob_typer
    mob_out = os.path.join(args.output_dir, 'mob_typer.results.tsv')
    process_mob_typer_results(args.mob_dir, mob_out)

    # Process amrfinderplus
    amr_out = os.path.join(args.output_dir, 'amrfinder.results.tsv')
    process_amrfinder_results(args.amr_dir, amr_out)
