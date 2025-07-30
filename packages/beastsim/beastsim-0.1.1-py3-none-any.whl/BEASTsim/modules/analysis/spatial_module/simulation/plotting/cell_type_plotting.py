import os
import math

import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns
import matplotlib as mpl
from BEASTsim.beast_data import *
from BEASTsim.utils.utils import _cluster_cell_distributions

class CellTypePlotting:
    def __init__(self, parameters):
        self.parameters = parameters
        self.spatial_analysis_parameters = self.parameters["Analysis"]["Spatial"]
        self.dir = self.spatial_analysis_parameters["output"]

    def ctd_pcs_plot(self, real: BEAST_Data, sim: Optional[BEAST_Data]=None, save=True, show=False, save_path=None, save_name=None, pcx=0, pcy=1, redo_color=True, redo_cluster=True, redo_cell_type=True):
        """
           PCA plotting of cell-type distribution (CTD) vectors.

            If only real is given, PCA is fitted on the real dataset real.data.obsm['cell_type_distribution'] and plotted
             in 2-D in terms of principal components pcx (x-axis) and pcy (y-axis).
            If both real and sim are given, PCA is fitted on CTDs real.data.obsm['cell_type_distribution'] and the
             simulation sim.data.obsm["cell_type_distribution"] is projected with the same loadings.

           Parameters
           ----------
           real : BEAST_Data
               Input we consider as the real data to analyze and compare with the simulated data.
           sim : Optional[BEAST_Data], default None
               Input we consider as the simulated data to analyze and compare with the real data.
           save : bool, default True
               Indicating if we want to save the created plots at the set path.
           show : bool, default False
               Indicating if we want to show the created plots interactively.
           save_name : Optional[str], default None
               String parameter setting the name prefix saved output files will start with, in case `save` was set to `True`.
           save_path : Optional[str], default self.dir
               Path string parameter pointing to where we want to save the created plots,
                in case `save` was set to `True`. If set to `None`,
                the default path from the `parameters.json` file will be used at `self.parameters["Analysis"]["Spatial"]["output"]`
           pcx : int, default 0
               Index of the principal component on the x-axis, sorted in terms of decreasing variance (highest variance = 0).
           pcy : int, default 1
               Index of the principal component on the y-axis, sorted in terms of decreasing variance (highest variance = 0).
           redo_color : bool, default True
                Set to True if either dataset lacks ``adata.uns["colors"]`` for color coding cell type neighborhoods (CTD clusters).
                Having the same colours across plots aids interpretability; if you
                chain calls, reuse the output datasets to keep colours consistent.
          redo_cluster : bool, default True
                Set to True if either dataset lacks ``adata.uns["centroids"]``; if
                present and this is set to True they will be overwritten.
           redo_cell_type : bool, default True
                Set to True if either dataset lacks ``adata.obs["cell_type"]``; if
                present and this is set to True, they will be overwritten.

           Returns
           -------
           Tuple[BEAST_Data, BEAST_Data]
               ``(real, sim)`` with updated clustering and colours in their
               ``.data`` AnnData objects.
           """
        adata_real = real.data
        adata_real_name = real.name
        adata_sim = sim.data
        adata_sim_name = sim.name
        if save_path is None:
            save_path =  self.dir
        if adata_sim is None:
            adata_real = self._cluster_cell_types(adata_real, redo_cluster=redo_cluster, redo_cell_type=redo_cell_type)
            adata_real = self._pca_cell_types(adata_real, adata_sim, save=save, show=show, save_name=save_name, pcx=pcx, pcy=pcy, save_path=save_path, redo_color=redo_color, real_name=adata_real_name, sim_name=adata_sim_name)
            real.data = adata_real
            return real, real
        else:
            adata_real, adata_sim = self._pca_cell_types(adata_real, adata_sim, save=save, show=show, save_name=save_name, pcx=pcx, pcy=pcy, save_path=save_path, redo_color=redo_color, real_name=adata_real_name, sim_name=adata_sim_name)
            real.data = adata_real
            sim.data = adata_sim
            return real, sim

    def ctd_full_cluster_plot(self, real: BEAST_Data, sim: Optional[BEAST_Data]=None, save=True, show=False, save_name=None, small_plots=False, save_path=None, redo_color=True, redo_cluster=True, redo_cell_type=True):
        """
        Analysis of cell-type neighbourhood clusters of cell-type distributions. Creates plots:

        1. Large CTD heatmap separately visualizing real.data.obsm['cell_type_distribution'] and sim.data.obsm['cell_type_distribution']
        2. (Optional) Small companion plots

        Parameters
        ----------
        real : BEAST_Data
            Input we consider as the real data to analyse and compare with the
            simulated data.
        sim : Optional[BEAST_Data], default None
            Input we consider as the simulated data to analyse and compare with
            the real data.
        save : bool, default True
            Indicating if we want to save the created plots at the set path.
        show : bool, default False
            Indicating if we want to show the created plots interactively.
        save_name : Optional[str], default None
            Name prefix saved output files will start with when save is True.
        small_plots : bool, default False
            Also calculate and save the two auxiliary plots (abundance vector & cluster-mean
            matrix).
        save_path : Optional[str], default self.dir
            Directory in which to save plots. If None, the default path from
            ``parameters["Analysis"]["Spatial"]["output"]`` is used.
        redo_color : bool, default True
            Set to True if either dataset lacks ``adata.uns["colors"]``
            for color coding cell type neighborhoods (CTD clusters).
            Having the same colours across plots aids interpretability; if you
            chain calls, reuse the output datasets to keep colours consistent.
        redo_cluster : bool, default True
            Set to True if either dataset lacks ``adata.uns["centroids"]``; if
            present and this is set to True they will be overwritten.
        redo_cell_type : bool, default True
            Set to True if either dataset lacks ``adata.obs["cell_type"]``; if
            present and this is set to True, they will be overwritten.

        Returns
        -------
        Tuple[BEAST_Data, BEAST_Data]
            ``(real, sim)`` with updated clustering and colours in their
            ``.data`` AnnData objects.
        """
        adata_real = real.data
        adata_real_name = real.name
        adata_sim = sim.data
        adata_sim_name = sim.name
        if save_path is None:
            save_path =  self.dir
        if adata_sim is None:
            adata_real = self._cluster_cell_types(adata_real, redo_cluster=redo_cluster, redo_cell_type=redo_cell_type)
            adata_real = self._large_ctd_plot(adata_real, save=save, show=show, save_name=save_name, save_path=save_path, redo_color=redo_color, name=adata_real_name, real_or_sim='Real')
            real.data = adata_real
            if small_plots:
                self._small_ctd_plots(adata_real, save=save, show=show, type='CT_Abundance_vector', save_name=save_name, save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
                self._small_ctd_plots(adata_real, save=save, show=show, type='cluster_mean_matrix', save_name=save_name, save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
            return real, real
        else:
            adata_real = self._cluster_cell_types(adata_real, redo_cluster=redo_cluster, redo_cell_type=redo_cell_type)
            adata_sim.uns['centroids'] = adata_real.uns['centroids']
            adata_sim = self._cluster_cell_types(adata_sim, redo_cluster=False, redo_cell_type=redo_cell_type)
            adata_real = self._large_ctd_plot(adata_real, save=save, show=show, save_name=f'{save_name}_real', save_path=save_path, redo_color=redo_color, name=adata_real_name, real_or_sim='Real')
            adata_sim = self._large_ctd_plot(adata_sim, save=save, show=show, save_name=f'{save_name}_sim', save_path=save_path, redo_color=redo_color, name=adata_sim_name, real_or_sim='Sim')
            if small_plots:
                self._small_ctd_plots(adata_real, save=save, show=show, type='CT_Abundance_vector', save_name=f'{save_name}_real', save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
                self._small_ctd_plots(adata_real, save=save, show=show, type='cluster_mean_matrix', save_name=f'{save_name}_real', save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
                self._small_ctd_plots(adata_sim, save=save, show=show, type='CT_Abundance_vector', save_name=f'{save_name}_sim', save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
                self._small_ctd_plots(adata_sim, save=save, show=show, type='cluster_mean_matrix', save_name=f'{save_name}_sim', save_path=save_path, real_name=adata_real_name, sim_name=adata_sim_name)
            real.data = adata_real
            sim.data = adata_sim
            return real, sim

    def _cluster_cell_types(self, adata, redo_cluster=False, redo_cell_type=False):
        from scipy.spatial.distance import cdist
        if 'cell_type_distribution' not in adata.obsm:
            print("adata.obsm['cell_type_distribution'] is not found. Calculate cell type distributions before running this analysis tool.")
        else:
            cell_type_distribution = adata.obsm['cell_type_distribution']
        if redo_cluster:
            _, centroids = _cluster_cell_distributions(cell_type_distribution, k_start=2, k_end=20,
                                                       weights={"silhouette": 0.35, "davies": 0.35, "aic": 0.30},
                                                       seed=42, use_log=self.parameters["Analysis"]["Spatial"]["Cell_Mapping"]["Cell2Location"]["use_log"])
            adata.uns['centroids'] = centroids
        else:
            centroids = adata.uns['centroids']
        if redo_cell_type:
            if not isinstance(cell_type_distribution, np.ndarray):
                ct_dist_np = cell_type_distribution.to_numpy()
            else:
                ct_dist_np = cell_type_distribution
            distances = cdist(ct_dist_np, centroids)
            cell_type = np.argmin(distances, axis=1)
            adata.obs['cell_type'] = pd.Series(cell_type, index=adata.obs.index).astype('category')
        else:
            cell_type = adata.obs['cell_type'].values
            adata.obs['cell_type'] = pd.Series(cell_type, index=adata.obs.index).astype('category')
        return adata

    def _pca_cell_types(self, adata_real, adata_sim=None, save=True, show=False, save_name='_', pcx=0, pcy=1, save_path=None, redo_color=True, real_name='Real', sim_name='Simulated'):
        if adata_sim is None:
            adata_real, adata_sim = self._pca_cell_types_seaborn(adata_real, save=save, show=show, save_name=save_name, pcx=pcx, pcy=pcy, save_path=save_path, redo_color=redo_color, real_name=real_name)
            return adata_real
        else:
            adata_real, adata_sim = self._pca_cell_types_dual_seaborn_2_same_loadings(adata_real, adata_sim, save=save, show=show, save_name=save_name,
                                                pcx=pcx, pcy=pcy, save_path=save_path, redo_color=redo_color, real_name=real_name, sim_name=sim_name)
            return adata_real, adata_sim

    def _pca_cell_types_seaborn(self, adata, save=True, show=False, save_name='_', pcx=0, pcy=1, save_path=None, redo_color=True, real_name=''):
        with mpl.rc_context():
            cell_type_distribution = adata.obsm["cell_type_distribution"].values
            cell_type = adata.obs['cell_type'].values
            pca = sklearn.decomposition.PCA()
            pca.fit(cell_type_distribution)
            comps = pca.transform(cell_type_distribution)
            explained_variance_ratio = pca.explained_variance_ratio_
            df = pd.DataFrame({
                f"PC{pcx}": comps[:, pcx],
                f"PC{pcy}": comps[:, pcy],
                "Cell_type": cell_type
            })
            unique_labels = np.unique(cell_type)
            cmap = plt.get_cmap("jet_r")
            if 'colors' not in adata.uns or redo_color:
                colors = cmap(np.linspace(0, 1, len(unique_labels)))
                label_color_map = {label: color for label, color in zip(unique_labels, colors)}
                adata.uns['colors'] = label_color_map
            else:
                label_color_map = adata.uns['colors']
            plt.figure(figsize=(8, 8))
            sns.set(style="whitegrid")
            scatter = sns.scatterplot(
                data=df,
                x=f"PC{pcx}",
                y=f"PC{pcy}",
                hue="Cell_type",
                palette=label_color_map,
                marker='.',
                s=30,
                legend=False
            )
            handles = [plt.Line2D([0], [0], marker='o', color=label_color_map[label],
                                  linestyle='', markersize=5) for label in unique_labels]
            plt.legend(handles, unique_labels, title="Predictions", loc='upper right', fontsize=14)
            plt.xlabel(f'PC{pcx} ({explained_variance_ratio[pcx]:.2%})')
            plt.ylabel(f'PC{pcy} ({explained_variance_ratio[pcy]:.2%})')
            plt.rcParams['figure.dpi'] = 300
            plt.tight_layout()
            if save:
                filename = f"{save_name}_pca_plot_real_{real_name}.pdf"
                full_path = os.path.join(save_path, filename)
                plt.savefig(full_path, format='pdf')
            if show:
                plt.show()
                plt.close()
            else:
                plt.close()
            return adata

    def _pca_cell_types_dual_seaborn_2_same_loadings(
            self,
            adata_real,
            adata_sim,
            save=True,
            show=False,
            save_name='_',
            pcx=0,
            pcy=1,
            save_path=None,
            redo_color=True,
            real_name='',
            sim_name=''):
        from matplotlib.lines import Line2D  # <-- add this import
        from matplotlib.font_manager import FontProperties
        with mpl.rc_context():
            bold = FontProperties(weight='bold')
            X_real = adata_real.obsm['cell_type_distribution'].values
            cell_type_real = adata_real.obs['cell_type'].values
            pca = sklearn.decomposition.PCA()
            pca.fit(X_real)
            comps_real = pca.transform(X_real)
            evr = pca.explained_variance_ratio_
            X_sim = adata_sim.obsm['cell_type_distribution'].values
            cell_type_sim = adata_sim.obs['cell_type'].values
            comps_sim = pca.transform(X_sim)
            df_real = pd.DataFrame({
                f'PC{pcx}': comps_real[:, pcx],
                f'PC{pcy}': comps_real[:, pcy],
                'Cell_type': cell_type_real,
                'Dataset': 'Real',
                'Marker': 'P'
            })
            df_sim = pd.DataFrame({
                f'PC{pcx}': comps_sim[:, pcx],
                f'PC{pcy}': comps_sim[:, pcy],
                'Cell_type': cell_type_sim,
                'Dataset': 'Sim',
                'Marker': 'o'
            })
            combined_df = pd.concat([df_real, df_sim], ignore_index=True)
            all_labels = np.unique(combined_df['Cell_type'])
            cmap = plt.get_cmap('jet_r')
            if ('colors' not in adata_real.uns and 'colors' not in adata_sim.uns) or redo_color:
                colors = cmap(np.linspace(0, 1, len(all_labels)))
                label_color_map = {label: color for label, color in zip(all_labels, colors)}
                adata_real.uns['colors'] = adata_sim.uns['colors'] = label_color_map
            elif 'colors' not in adata_sim.uns:
                label_color_map = adata_sim.uns['colors'] = adata_real.uns['colors']
            elif 'colors' not in adata_real.uns:
                label_color_map = adata_real.uns['colors'] = adata_sim.uns['colors']
            else:
                label_color_map = adata_real.uns['colors']
            fig, ax = plt.subplots(figsize=(10, 10))
            sns.set(style='whitegrid')
            sub1 = combined_df[combined_df['Dataset'] == 'Real']
            sns.scatterplot(
                data=sub1, x=f'PC{pcx}', y=f'PC{pcy}',
                hue='Cell_type', palette=label_color_map,
                marker='P',
                s=37,
                legend=False, ax=ax
            )
            sub2 = combined_df[combined_df['Dataset'] == 'Sim']
            sns.scatterplot(
                data=sub2, x=f'PC{pcx}', y=f'PC{pcy}',
                hue='Cell_type', palette=label_color_map,
                marker='o', s=20, legend=False, ax=ax
            )
            centroids = adata_real.uns.get('centroids')
            if centroids is not None:
                for i, label in enumerate(all_labels):
                    vec = centroids[i].reshape(1, -1)
                    pc_x, pc_y = pca.transform(vec)[0, [pcx, pcy]]
                    ax.scatter(
                        pc_x, pc_y,
                        s=200,
                        marker='x',
                        facecolors=label_color_map[label],
                        linewidths=1.5,
                        label=f'{label}'
                    )
            handles_ct, labels_ct = ax.get_legend_handles_labels()
            max_rows = 6
            ncol_ct = math.ceil(len(labels_ct) / max_rows)
            leg_ct = ax.legend(
                handles_ct, labels_ct,
                title="Cell Type\nNeighborhoods",
                loc="lower right",
                prop=bold, title_fontproperties=bold,
                ncol=ncol_ct,
                labelspacing=0.8,
                columnspacing=0.8,
                borderpad=0.4,
                handletextpad=0.4,
            )
            handles_ds = [
                Line2D([], [], marker="P", linestyle="", markersize=10,
                       markeredgewidth=0.8, markeredgecolor="k",
                       markerfacecolor="k", label="Real"),
                Line2D([], [], marker="o", linestyle="", markersize=9,
                       markeredgewidth=0.8, markeredgecolor="k",
                       markerfacecolor="k", label="Sim"),
            ]
            leg_ds = ax.legend(
                handles=handles_ds,
                labels=["Real", "Sim"],
                loc="upper right",
                frameon=True,
            )
            ax.add_artist(leg_ct)
            ax.set_xlabel(f'PC{pcx} ({evr[pcx]:.2%})', fontweight='bold')
            ax.set_ylabel(f'PC{pcy} ({evr[pcy]:.2%})', fontweight='bold')
            ax.set_title(f'PCA cell type distributions (shared loadings) \nReal: {real_name} \nSim: {sim_name}', fontweight='bold')
            plt.tight_layout()
            plt.rcParams['figure.dpi'] = 400
            if save:
                path = os.path.join(
                    save_path,
                    f"{save_name}_pca_pcx{pcx}_pcy{pcy}_full_dual_real_{real_name}_sim_{sim_name}.pdf"
                )
                fig.savefig(path, format='pdf')
            if show:
                plt.show()
                plt.close(fig)
            else:
                plt.close(fig)
            return adata_real, adata_sim

    def _add_numbers(self, plt, matrix, fontsize=8):
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if abs(matrix[i, j]) < 0.01 and matrix[i, j] != 0:
                    plt.text(j, i, f"{matrix[i, j]:.0e}", ha="center", va="center", color="green", fontsize=fontsize,
                             weight="bold")
                else:
                    plt.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="green", fontsize=fontsize,
                             weight="bold")

    def _large_ctd_plot(self, adata, save_name=None, save=True, show=False, save_path=None, redo_color=True, name='', real_or_sim='real'):
        with mpl.rc_context():
            if save_name is None:
                save_name = ''
            CTD_matrix = adata.obsm["cell_type_distribution"].values
            CT = adata.obs['cell_type'].values
            sorted_indices = np.argsort(CT)
            CTD_matrix = CTD_matrix[sorted_indices]
            sorted_labels = CT[sorted_indices]
            data = pd.DataFrame(CTD_matrix)
            data['Cluster'] = sorted_labels
            plt.rcParams['figure.dpi'] = 300
            unique_labels = np.unique(CT)
            if 'colors' not in adata.uns or redo_color:
                cmap = plt.get_cmap('jet_r')
                colors = cmap(np.linspace(0, 1, len(unique_labels)))
                label_color_map = {label: color for label, color in zip(unique_labels, colors)}
                adata.uns['colors'] = label_color_map
            else:
                label_color_map = adata.uns['colors']
            row_colors = [label_color_map[label] for label in sorted_labels]
            g = sns.clustermap(
                data.iloc[:, :-1],
                row_cluster=False,
                col_cluster=False,
                row_colors=row_colors,
                cmap="plasma",
                figsize=(12, 15),
                dendrogram_ratio=(0.1, 0.05),
            )
            g.fig.suptitle(f'Cell type neighborhoods \n{real_or_sim}: {name}', fontsize=22, y=0.99)
            if save:
                filename = f"CTD {save_name} {real_or_sim} {name}.png"
                full_path = os.path.join(save_path, filename)
                plt.savefig(full_path, format='png')
            if show:
                plt.show()
                plt.close()
            else:
                plt.close()
            return adata

    def _small_ctd_plots(self, adata, save_name=None, save=True, show=False, type=None, save_path=None, real_name='', sim_name=''):
        if save_name is None:
            save_name = type
        else:
            save_name = f'{save_name}_{type}'
        CTD_matrix = adata.obsm["cell_type_distribution"]
        CT = adata.obs['cell_type'].values
        CT_Abundance_vector = np.expand_dims(np.array([np.sum(CT == i) for i in np.unique(CT)]) / len(CT), axis=1)
        cluster_mean_matrix = adata.clust

        sorted_indices = np.argsort(CT)
        CTD_matrix = CTD_matrix[sorted_indices]
        sorted_labels = CT[sorted_indices]
        data = pd.DataFrame(CTD_matrix)
        data['Cluster'] = sorted_labels
        plt.rcParams['figure.dpi'] = 300
        if type == 'CT_Abundance_vector':
            plt.figure(figsize=(7, 7))
            plt.imshow(CT_Abundance_vector, cmap='plasma', vmin=0, vmax=1)
            plt.title("CT_Abundance_vector", fontsize=18, weight="bold")
            self._add_numbers(plt, CT_Abundance_vector)
            plt.yticks(
                ticks=np.arange(CT_Abundance_vector.shape[0]),
                labels=[f'{i}' for i in range(CT_Abundance_vector.shape[0])],
                fontsize=12, weight="bold"
            )
            plt.tight_layout()
        elif type == 'cluster_mean_matrix':
            plt.figure(figsize=(15, 7))
            plt.imshow(cluster_mean_matrix, cmap='plasma', vmin=0, vmax=1)
            plt.title("Cluster_mean_matrix", fontsize=18, weight="bold")
            self._add_numbers(plt, cluster_mean_matrix, fontsize=8)
            plt.yticks(
                ticks=np.arange(cluster_mean_matrix.shape[0]),
                labels=[f'{i}' for i in range(cluster_mean_matrix.shape[0])],
                fontsize=12, weight="bold"
            )
            plt.tight_layout()
        if save:
            filename = f"CTD_{save_name}_real_{real_name}_sim_{sim_name}.pdf"
            full_path = os.path.join(save_path, filename)
            plt.savefig(full_path, format='pdf')
        if show:
            plt.show()
        else:
            plt.close()