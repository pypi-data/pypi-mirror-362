from pandas import DataFrame, Series
from anndata import AnnData
from typing import Optional, Dict, Union, List
from numpy import ndarray

def perform_clustering(correlations: DataFrame) -> ndarray:
    from scipy.cluster.hierarchy import linkage, fcluster
    from scipy.spatial.distance import squareform
    from numpy import argsort
    """
    Perform hierarchical clustering and return column order.

    Args:
        correlations (DataFrame): Correlation matrix.

    Returns:
        ndarray: Ordered column indices.
    """
    dissimilarity = 1 - abs(correlations)
    Z = linkage(squareform(dissimilarity), "complete")
    threshold = 0.8
    labels = fcluster(Z, threshold, criterion="distance")
    return (argsort(labels))

def plot_heatmap(
        ax, correlations: DataFrame, title: str, index: int, first_correlations: Optional[DataFrame] = None
) -> None:
    from scipy.stats import pearsonr

    """
    Plot a heatmap for the given correlation matrix.

    Args:
        ax (plt.Axes): Axes object to draw the heatmap on.
        correlations (DataFrame): Correlation matrix.
        title (str): Title of the heatmap.
        index (int): Index of the dataset being processed.
        first_correlations (Optional[DataFrame]): Correlation matrix of the first dataset.
    """
    from seaborn import heatmap
    heatmap(
        round(correlations, 2),
        cmap="RdBu",
        vmin=-1,
        vmax=1,
        annot=False,
        fmt=".2f",
        xticklabels=False,
        yticklabels=False,
        ax=ax,
    )
    ax.set_title(title)

    if index != 0 and first_correlations is not None:
        # Compute and annotate the Pearson correlation
        r_val, _ = pearsonr(
            first_correlations.values.flatten(), correlations.values.flatten()
        )
        ax.text(
            0.5,
            -0.1,
            f"R = {r_val:.2f}",
            horizontalalignment="center",
            verticalalignment="center",
            transform=ax.transAxes,
        )


def create_spider_chart(data_dict: Dict[str, Dict[str, Union[DataFrame, Series]]], save_path: str,
                        title: Optional[str] = None, color_palette: Optional[List[str]] = None) -> None:
    """
    Create multiple interactive spider charts using Plotly from a dictionary of datasets.

    Args:
        data_dict (Dict[str, Dict]): Dictionary where:
            - Keys are subplot titles (str).
            - Values are dictionaries where keys are simulation technique names,
              and values are DataFrames or Series.
        save_path (str): Path to save the figure.
        title (Optional[str]): Title of the chart.
    """
    from BEASTsim.utils.utils import _format_name_html
    from math import ceil
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    sub_titles = list(data_dict.keys())  # Extract subplot titles
    data_list = list(data_dict.values())  # Extract datasets for subplots

    cols = len(data_list)  # One row, multiple columns
    rows = 1

    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f"<b>{sub_title}</b>" for sub_title in sub_titles],
        specs=[[{'type': 'polar'}] * cols for _ in range(rows)],
        vertical_spacing=0.2,
        horizontal_spacing=0.05
    )

    # Extract benchmark names per subplot while preserving order
    benchmark_titles_dict = {}

    for idx, data in enumerate(data_list):
        benchmarks = []

        # Get unique benchmarks in order of appearance
        for df in data.values():
            if isinstance(df, (DataFrame, Series)):
                for item in df.index.tolist():
                    if item not in benchmarks:
                        benchmarks.append(item)

        benchmarks.append(benchmarks[0])  # Close the loop
        benchmark_titles_dict[idx] = [_format_name_html(b) for b in benchmarks]

    # Extract simulation technique names in order of appearance
    ordered_sim_names = []
    for data in data_list:
        for sim_name in data.keys():
            if sim_name not in ordered_sim_names:
                ordered_sim_names.append(sim_name)

    # Assign colors to each simulation technique
    if color_palette is None:
        color_palette = [
        "darkslategray", "maroon", "green", "blue", "darkorange",
        "gold", "lightgreen", "darkturquoise", "cornflowerblue",
        "hotpink", "darkcyan", "red"
        ]

    if len(ordered_sim_names) > len(color_palette):
        raise ValueError(
            f"Number of simulation methods ({len(ordered_sim_names)}) exceeds the available colors ({len(color_palette)}). "
            "Please provide additional colors.")

    color_map = {name: color for name, color in zip(ordered_sim_names, color_palette)}

    # Add traces to the plot
    for idx, data in enumerate(data_list):
        row, col = divmod(idx, cols)

        for sim_name in ordered_sim_names:
            df = data.get(sim_name, None)
            scores = df.iloc[:, 0].tolist() if isinstance(df, DataFrame) else (
                df.tolist() if isinstance(df, Series) else [])

            if scores:  # Only add non-empty data
                scores.append(scores[0])  # Close the loop

                fig.add_trace(go.Scatterpolar(
                    r=scores,
                    theta=benchmark_titles_dict[idx],
                    fill=None,
                    name=sim_name,
                    showlegend=(idx == 0),  # Show legend only once
                    line=dict(color=color_map.get(sim_name, 'black'))
                ), row=row + 1, col=col + 1)

    # Define polar layout settings
    polar_layouts = {
        f"polar{idx + 1 if idx > 0 else ''}": dict(
            radialaxis=dict(
                visible=True,
                range=[-0.1, 1],
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                showline=False
            ),
            angularaxis=dict(
                rotation=90,
                tickfont=dict(size=12, weight="bold"),
                tickangle=0,
                direction="clockwise",
                ticks="outside",
                showline=False,
                tickvals=[i for i in range(len(benchmark_titles_dict[idx]))],
                ticktext=benchmark_titles_dict[idx],
                ticklen=10
            ),
            gridshape="linear"
        ) for idx in range(len(data_list))
    }

    # Update layout with legend and formatting
    fig.update_layout(
        **polar_layouts,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2 - 0.05 * ceil(len(ordered_sim_names) / 3),
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(size=12, weight="bold"),
            bgcolor="rgba(255,255,255,0.7)",
            itemsizing="constant"
        ),
        showlegend=True,
        width=700 * cols,
        height=700 * rows,
        margin=dict(t=150, b=0, l=0, r=0)
    )

    if title is not None:
        fig.update_layout(
            title=title,
            title_x=0.5,
            title_y=0.98,
            title_font=dict(size=24, family="Arial, sans-serif", color="black", weight="bold"),
        )

    # Adjust subplot title positions
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=18, family="Arial, sans-serif", color="black", weight="bold")
        annotation['y'] += 0.2  # Moves subplot titles up slightly

    fig.write_image(save_path, scale=3)


def plot_cell_type_locations(adata: AnnData, save_path): # TODO: 0 usage?? Holm code?
    from matplotlib.pyplot import scatter, xlabel, ylabel, colorbar, savefig
    x = adata.obs.X.values
    y = adata.obs.Y.values
    probs = adata.obsm["probabilities"].to_numpy()
    selected_cell_type_probs = probs[:, 3]
    scatter(x, y, c=selected_cell_type_probs, cmap="viridis", s=10)
    xlabel("X")
    ylabel("Y")
    colorbar(label="Probability")
    savefig(save_path)

def plot_robustness(
    adatas: list[AnnData], cell_types: list[int], save_path
):
    """
    Plots a robustness plot given an array of AnnData objets containing proper cell type location probabilities. Outputs a figure that dynamically scales to to add room for more each run and cell type.

    Parameters:
        adatas:
            Array containing AnnData Objects representing multiple applications of some spatial cellular abbundance model.
            Each AnnData Object needs to have a "probabilities" value in the obsm field, containing a DataFrame with the probabilities for each celltype to be a each cell location.
            The Rows in the DataFrame should be the cell locations, each row should represent a given cell location, and the columns should be the probabilities for each cell type to be at a given location.
        cell_types:
            Array containing the indexes of the celltypes that the robustness is measured on.
        save_path:
            Path to save the generated figure to.
    """
    from matplotlib.pyplot import ioff, subplots, tight_layout, savefig, ion
    from random import sample
    assert (
        len(adatas) > 0
    ), "No Adata objects were detected, please make certain to pass the data from the runs"
    if len(cell_types) < 1:
        cell_types = len(adatas[0].obsm["probabilities"].columns.tolist())
        potential_choices = range(0, cell_types)
        if cell_types < 4:
            samples = cell_types
        else:
            samples = 4
        cell_types = sample(potential_choices, k=samples)
    cols = len(adatas)
    rows = len(cell_types)
    ioff()
    figure, axs = subplots(rows, cols, figsize=(cols * 7.5, rows * 5))
    for i, cell_type in enumerate(cell_types):
        for j, data in enumerate(adatas):
            ax = axs[i, j]
            x = data.obs.X.values
            y = data.obs.Y.values
            cell_type_name = data.obsm["probabilities"].columns.tolist()[cell_type]
            probs = data.obsm["probabilities"].to_numpy()
            probs_cell_type = probs[:, cell_type]
            scatter_plot = ax.scatter(x, y, c=probs_cell_type, cmap="viridis", s=10)
            figure.colorbar(scatter_plot, ax=ax, label="Probability")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title(f"Cell type {cell_type_name}")
    figure.suptitle("Robustness benchmark")
    tight_layout()
    savefig(save_path)
    ion()

def calc_width_ratios(datas):
    total_length = 0
    dfs = []
    for data in datas:
        df = data
        dfs.append(df)
        total_length += len(df.columns)
    return [len(df.columns)/total_length for df in dfs]

def create_comparison_benchmarks(datas,max_dot_size,min_dot_size,names,save_path):
    from seaborn import color_palette, set_theme, scatterplot, despine
    from matplotlib.gridspec import GridSpec
    import matplotlib.pyplot as plt

    if not isinstance(datas, list) or not all(isinstance(df, DataFrame) for df in datas):
        raise ValueError("datas must be a list of pandas DataFrames.")
    if len(datas) != len(names):
        raise ValueError("The length of datas and names must be the same.")
    width_ratios = calc_width_ratios(datas)
    fig = plt.figure(figsize=(8*len(datas), 8))
    gs = GridSpec(2,len(datas),width_ratios = width_ratios,height_ratios = [1,0.3])
    cmap = color_palette("Blues", as_cmap=True)
    axis = []
    set_theme(style='whitegrid')
    plt.rcParams["font.family"] = "DejaVu Sans"
    for i,data in enumerate(datas):
        df = data
        current_ax = fig.add_subplot(gs[0,i])
        # Melt the dataframe for easier plotting with seaborn
        df_melted = df.melt(id_vars='Method', var_name='Category', value_name='Rank')
        min_val = df_melted['Rank'].min()
        max_val =df_melted['Rank'].max()
        keys = list(range(max_val,min_val - 1,-1))
        values = list(range(min_val,max_val + 1))
        size_mapping = dict(zip(keys,values))
        #calculate slope for scaling dot sizes linearly
        slope = max_dot_size/max_val

        df_melted['size'] = df_melted['Rank'].map(size_mapping)*slope + min_dot_size
        scatter = scatterplot(data=df_melted, x='Category', y='Method', size='size', hue='Rank', palette=cmap, sizes=(50, 500),ax=current_ax,legend=False,edgecolor='black')
        current_ax.set_title(names[i])
        if i != 0:
            current_ax.spines["left"].set_visible(False)
            current_ax.get_yaxis().set_ticks([]) # TODO find alternative for this.
            current_ax.set_xlabel("")
            current_ax.set_ylabel("")
        axis.append(current_ax)
    normalized = plt.Normalize(df_melted['Rank'].min(),df_melted['Rank'].max())
    scalar_map = plt.cm.ScalarMappable(cmap=cmap,norm=normalized)
    scalar_map.set_array([])
    cbar_ax = fig.add_subplot(gs[1,:])
    fig.colorbar(scalar_map,label="Rank",ax=cbar_ax,orientation = "horizontal",fraction = 0.1, pad= 0)
    despine()
    for i in range(len(datas)):
        plt.sca(axis[i])
        plt.xticks(rotation=45, ha='right')
    handles = [plt.Line2D([], [], marker='o', color='w', markerfacecolor='grey', markersize=size_mapping[cat]*slope + min_dot_size, label=cat) for cat in sorted(size_mapping.keys())]
    cbar_ax.axis("off")
    cbar_ax.legend(title='Rank', loc='lower center',labelspacing = 1,handles = handles,ncol=len(size_mapping.keys()))
    cbar_ax.set_aspect(0.01)
    plt.gca().set(xlabel='', ylabel='')

    plt.tight_layout()
    plt.savefig(save_path)

def create_comparison_benchmarks_new_suggestion(datas, max_dot_size, min_dot_size, names, save_path): #TODO: What is this? 0 usage?
    """
    Creates a comparison benchmark plot with custom colorbar position and size legend.

    Parameters:
    - datas: List of pandas DataFrames containing the data.
    - max_dot_size: Maximum size for the dots.
    - min_dot_size: Minimum size for the dots.
    - names: List of names for each subplot.
    - save_path: Path to save the output plot.

    Returns:
    - None
    """
    from pandas import concat
    from seaborn import set_theme, scatterplot
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from sklearn.preprocessing import MinMaxScaler
    from numpy import linspace

    if not isinstance(datas, list) or not all(isinstance(df, DataFrame) for df in datas):
        raise ValueError("datas must be a list of pandas DataFrames.")
    if len(datas) != len(names):
        raise ValueError("The length of datas and names must be the same.")

    all_ranks = concat([
        df.melt(id_vars='Method', var_name='Category', value_name='Rank')['Rank']
        for df in datas
    ])
    global_min_rank = all_ranks.min()
    global_max_rank = all_ranks.max()

    set_theme(style='whitegrid')

    fig, axes = plt.subplots(1, len(datas), figsize=(8 * len(datas), 14), sharey=True)
    if len(datas) == 1:
        axes = [axes]

    scaler = MinMaxScaler(feature_range=(min_dot_size, max_dot_size))

    for i, (df, ax) in enumerate(zip(datas, axes)):
        df_melted = df.melt(id_vars='Method', var_name='Category', value_name='Rank')
        df_melted['SizeRank'] = global_max_rank - df_melted['Rank'] + global_min_rank
        df_melted['ScaledSize'] = scaler.fit_transform(df_melted[['SizeRank']])

        scatter = scatterplot(
            data=df_melted,
            x='Category',
            y='Method',
            size='ScaledSize',
            hue='Rank',
            palette='coolwarm',
            ax=ax,
            legend=False
        )
        ax.set_title(names[i])
        if i != 0:
            ax.set_ylabel('')
        ax.set_xlabel('Category')
        ax.tick_params(axis='x', rotation=45)

    fig.text(0.04, 0.5, 'Method', va='center', rotation='vertical')

    norm = plt.Normalize(global_min_rank, global_max_rank)
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=norm)
    sm.set_array([])

    cbar_ax = fig.add_axes([0.15, 0.07, 0.4, 0.02])  # [left, bottom, width, height]
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Rank')

    # Select representative rank values
    size_legend_ranks = linspace(global_min_rank, global_max_rank, num=len(df)).astype(int)
    size_legend_sizes = scaler.transform(size_legend_ranks.reshape(-1, 1)).flatten()


    legend_handles = [
        Line2D(
            [], [], marker='o', color='w', markerfacecolor='gray',
            markersize=size, label=str(rank), linestyle='None'
        )
        for rank, size in zip(size_legend_ranks, size_legend_sizes)
    ]

    legend_ax = fig.add_axes([0.15, 0.02, 0.4, 0.02])
    legend_ax.axis('off')
    legend_ax.legend(
        handles=legend_handles, title='Rank (Size)',
        loc='center', ncol=len(size_legend_ranks), frameon=False
    )

    plt.tight_layout(rect=[0, 0.1, 1, 1])

    plt.savefig(save_path)
    plt.close(fig)
