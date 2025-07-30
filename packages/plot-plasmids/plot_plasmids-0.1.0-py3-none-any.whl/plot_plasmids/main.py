#!/usr/bin/env python3

import argparse
import pandas as pd
import numpy as np
import skbio
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import seaborn as sns
from adjustText import adjust_text
import os

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a PCoA or NMDS plot for plasmids, colored by carbapenemase genes and rep types.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-d", "--dist_matrix",
        required=True,
        help="Path to the plasmid distance matrix (CSV or TSV format)."
    )
    parser.add_argument(
        "-a", "--amr",
        required=True,
        help="Path to the AMRfinderPlus summary results file (TSV format)."
    )
    parser.add_argument(
        "-m", "--mob",
        required=True,
        help="Path to the MOB-typer mob_recon_results.txt file (TSV format)."
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path for the output plot file (e.g., plot.png, plot.svg)."
    )
    parser.add_argument(
        "-p", "--plot_type",
        choices=['pcoa', 'nmds'],
        default='pcoa',
        help="Type of ordination plot to generate. (default: pcoa)"
    )
    return parser.parse_args()

def clean_plasmid_id(id_str):
    """Remove common file extensions from plasmid IDs to standardize them."""
    base = os.path.basename(id_str)
    return os.path.splitext(base)[0]

def load_distance_matrix(filepath):
    """Load the distance matrix and standardize plasmid IDs."""
    try:
        # Auto-detect separator
        sep = ',' if filepath.endswith('.csv') else '\t'
        matrix = pd.read_csv(filepath, sep=sep, index_col=0)
        
        # Standardize IDs in index and columns
        matrix.index = matrix.index.map(clean_plasmid_id)
        matrix.columns = matrix.columns.map(clean_plasmid_id)
        
        print(f"✅ Loaded distance matrix with {len(matrix)} plasmids.")
        return matrix
    except FileNotFoundError:
        print(f"❌ Error: Distance matrix file not found at {filepath}")
        exit(1)
    except Exception as e:
        print(f"❌ Error loading distance matrix: {e}")
        exit(1)

def parse_amr_results(filepath):
    """Parse AMRfinderPlus results to find carbapenemase genes."""
    try:
        amr_df = pd.read_csv(filepath, sep='\t')
        # Filter for carbapenemases
        carb_df = amr_df[amr_df['Subclass'] == 'CARBAPENEM'].copy()
        
        if carb_df.empty:
            print("⚠️ Warning: No carbapenemase genes found in AMRfinderPlus results.")
            return pd.Series(dtype=str)

        # Standardize IDs and aggregate genes for plasmids with multiple carbapenemases
        carb_df['Plasmid'] = carb_df['plasmidID'].apply(lambda x: clean_plasmid_id(x.split('/')[0]))
        
        # For each plasmid, get a sorted list of unique gene symbols
        amr_map = carb_df.groupby('Plasmid')['Element symbol'].unique().apply(lambda x: ';'.join(sorted(x)))
        
        print(f"🧬 Found carbapenemase genes for {len(amr_map)} plasmids.")
        return amr_map
    except FileNotFoundError:
        print(f"❌ Error: AMRfinderPlus file not found at {filepath}")
        exit(1)
    except Exception as e:
        print(f"❌ Error parsing AMRfinderPlus results: {e}")
        exit(1)


def parse_mob_results(filepath):
    """Parse MOB-typer results to get replicon types."""
    try:
        mob_df = pd.read_csv(filepath, sep='\t')
        mob_df.set_index(mob_df['sample_id'].map(clean_plasmid_id), inplace=True)
        
        # Extract and standardize rep types
        # Handles cases with multiple rep types, e.g., "IncFIB(pB2-2),IncFII(pB2-1)"
        rep_types = mob_df['rep_type(s)'].dropna().apply(
            lambda reps: ';'.join(sorted(r.split('(')[0] for r in reps.split(',')))
        )
        
        print(f"🧬 Found replicon types for {len(rep_types)} plasmids.")
        return rep_types
    except FileNotFoundError:
        print(f"❌ Error: MOB-typer file not found at {filepath}")
        exit(1)
    except Exception as e:
        print(f"❌ Error parsing MOB-typer results: {e}")
        exit(1)

def run_ordination(dist_matrix, method='pcoa'):
    """Perform PCoA or NMDS ordination."""
    print(f"⚙️ Running {method.upper()}...")
    if method == 'pcoa':
        try:
            # PCoA requires a skbio.DistanceMatrix
            dm = skbio.DistanceMatrix(dist_matrix)
            ordination_result = skbio.stats.ordination.pcoa(dm)

            # Assign original plasmid IDs to the ordination result
            ordination_result.samples.index = dist_matrix.index

            # Add stress score for consistency with NMDS output
            ordination_result.stress = 'N/A' 
            return ordination_result
        except Exception as e:
            print(f"❌ Error during PCoA: {e}")
            exit(1)
    elif method == 'nmds':
        try:
            # NMDS from scikit-learn
            nmds = MDS(n_components=2, dissimilarity='precomputed', random_state=42, n_init=100, max_iter=1000)
            coords = nmds.fit_transform(dist_matrix)
            
            # Format results similar to skbio for consistency
            result_df = pd.DataFrame(coords, index=dist_matrix.index, columns=['PC1', 'PC2'])
            ordination_result = skbio.stats.ordination.OrdinationResults(
                'NMDS', 'Non-metric Multidimensional Scaling',
                eigvals=pd.Series(np.nan, index=['PC1', 'PC2']),
                samples=result_df
            )
            ordination_result.stress = nmds.stress_
            return ordination_result
        except Exception as e:
            print(f"❌ Error during NMDS: {e}")
            exit(1)

def create_plot(ordination_result, metadata, output_path, plot_type):
    """Create and save the final plot."""
    print("🎨 Generating plot...")
    
    # === Prepare data for plotting ===
    coords = ordination_result.samples[['PC1', 'PC2']]
    
    # Align metadata with coordinates
    plot_data = coords.join(metadata)

    # Reorder metadata to match the order of samples in the ordination result
    if plot_type == 'pcoa':
        plot_data = plot_data.loc[ordination_result.samples.index]

    plot_data.fillna({'carb_gene': 'None', 'rep_type': 'None'}, inplace=True)

    # === Generate Color Maps ===
    # Explode the dataframe to handle multiple genes/reps per plasmid
    plot_data['carb_gene_list'] = plot_data['carb_gene'].str.split(';')
    plot_data['rep_type_list'] = plot_data['rep_type'].str.split(';')

    # Create comprehensive lists of unique genes and rep types
    all_carbs = sorted(list(set(g for sublist in plot_data['carb_gene_list'].dropna() for g in sublist)))
    all_reps = sorted(list(set(r for sublist in plot_data['rep_type_list'].dropna() for r in sublist)))

    # Carbapenemase (fill color)
    carb_palette = sns.color_palette("viridis", n_colors=len(all_carbs))
    carb_color_map = dict(zip(all_carbs, carb_palette))
    carb_color_map['None'] = '#d3d3d3'

    # Rep type (ring color)
    rep_palette = sns.color_palette("husl", n_colors=len(all_reps))
    rep_color_map = dict(zip(all_reps, rep_palette))
    rep_color_map['None'] = '#404040'

    # === Create Plot ===
    fig, ax = plt.subplots(figsize=(16, 14))

    # Plot points with specific colors for each gene/rep
    for idx, row in plot_data.iterrows():
        x, y = row['PC1'], row['PC2']
        carb_genes = row['carb_gene_list'] if isinstance(row['carb_gene_list'], list) and row['carb_gene_list'][0] != 'None' else []
        rep_types = row['rep_type_list'] if isinstance(row['rep_type_list'], list) and row['rep_type_list'][0] != 'None' else []

        # Determine fill and edge colors based on the number of genes/reps
        fill_color = carb_color_map.get(row['carb_gene'], carb_color_map['None'])
        edge_color = rep_color_map.get(row['rep_type'], rep_color_map['None'])

        # Plot points with specific colors
        ax.scatter(x, y, s=400,
                   facecolors=fill_color,
                   edgecolors=edge_color,
                   linewidths=3,
                   alpha=0.9)

        # For multiple rep types, we can use a dashed edge or a different marker
        # For simplicity, we'll stick to a solid edge for now.

    # === Add Labels ===

    # === Add Labels ===
    texts = []
    for plasmid_id, (x, y) in plot_data[['PC1', 'PC2']].iterrows():
        texts.append(ax.text(x, y, plasmid_id, fontsize=9, ha='center', va='center'))
    
    # Adjust labels to avoid overlap
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

    # === Create Legends ===
    # Carbapenemase Legend
    carb_patches = [mpatches.Patch(color=color, label=gene) for gene, color in carb_color_map.items() if gene != 'None']
    carb_patches.append(mpatches.Patch(color=carb_color_map['None'], label='None'))
    carb_legend = ax.legend(handles=carb_patches, title='Carbapenemase (Fill)', loc='upper left', bbox_to_anchor=(1.02, 1), frameon=False)
    ax.add_artist(carb_legend)

    # Rep Type Legend
    rep_lines = [Line2D([0], [0], marker='o', color='w', label=rep,
                        markerfacecolor='lightgray', markeredgecolor=color, markersize=10)
                 for rep, color in rep_color_map.items() if rep != 'None']
    rep_lines.append(Line2D([0], [0], marker='o', color='w', label='None',
                            markerfacecolor='lightgray', markeredgecolor=rep_color_map['None'], markersize=10))

    # Marker Legend
    marker_legend_handles = [
        Line2D([0], [0], marker='o', color='w', label='Single Gene/Rep', markeredgecolor='black', markersize=10),
        Line2D([0], [0], marker='*', color='w', label='Multiple Genes/Reps', markeredgecolor='black', markersize=12)
    ]

    # Combine rep and marker legends
    rep_legend = ax.legend(handles=rep_lines, title='Rep Type (Ring)', loc='lower left', bbox_to_anchor=(1.02, 0), frameon=False)
    ax.add_artist(rep_legend)

    ax.legend(handles=marker_legend_handles, title='Plasmid Type', loc='lower left', bbox_to_anchor=(1.02, 0.4), frameon=False)

    # === Final Touches ===
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    title = f'{plot_type.upper()} of Plasmid Distances'
    if plot_type == 'nmds':
        title += f' (Stress = {ordination_result.stress:.4f})'
    ax.set_title(title, fontsize=16, weight='bold')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    sns.despine(ax=ax)
    
    # Adjust layout to prevent legend overlap
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # === Save Plot ===
    try:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Plot successfully saved to {output_path}")
    except Exception as e:
        print(f"❌ Error saving plot: {e}")
        exit(1)

def main():
    """Main execution function."""
    args = parse_arguments()
    
    # 1. Load data
    dist_matrix = load_distance_matrix(args.dist_matrix)
    
    # Ensure matrix is symmetric
    if not np.allclose(dist_matrix.values, dist_matrix.values.T):
        print("⚠️ Warning: Distance matrix is not symmetric. Taking the maximum of (i,j) and (j,i).")
        dist_matrix = np.maximum(dist_matrix.values, dist_matrix.values.T)
        dist_matrix = pd.DataFrame(dist_matrix, index=dist_matrix.index, columns=dist_matrix.columns)
        
    plasmid_ids_in_matrix = set(dist_matrix.index)
    
    # 2. Parse annotations
    amr_map = parse_amr_results(args.amr)
    mob_map = parse_mob_results(args.mob)
    
    # 3. Create combined metadata DataFrame
    metadata = pd.DataFrame(index=list(plasmid_ids_in_matrix))
    metadata = metadata.join(amr_map.rename('carb_gene')).join(mob_map.rename('rep_type'))
    
    # Check for missing annotations
    missing_amr = plasmid_ids_in_matrix - set(amr_map.index)
    if missing_amr:
        print(f"ℹ️ {len(missing_amr)} plasmids have no carbapenemase annotation.")
    missing_mob = plasmid_ids_in_matrix - set(mob_map.index)
    if missing_mob:
        print(f"ℹ️ {len(missing_mob)} plasmids have no MOB-typer annotation.")

    # 4. Perform ordination
    ordination_result = run_ordination(dist_matrix, args.plot_type)

    # 5. Generate and save the plot
    create_plot(ordination_result, metadata, args.output, args.plot_type)

if __name__ == "__main__":
    main()
