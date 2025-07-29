"""Helper functions for StrainGE
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import seaborn as sns
import numpy as np
from matiss.plots import config_axes, get_figure
from matiss.distance import get_idx_from_dense
from typing import Hashable, Tuple, Union, Callable
from colorcet import glasbey
from numpy.typing import ArrayLike
from scipy.spatial.distance import jaccard, pdist
from matiss.kraken import get_cmap

def plot_strains(strains: pd.DataFrame, *, marker_size:int = 250, mlst_col: Union[None, Hashable] = None, 
    palette: Union[Callable, Hashable, str] = glasbey, strain_col: Union[str, Hashable] = "strain",
    figsize: Tuple[float, float] = (22,12)):

    MS=marker_size

    def label_transform_f(x, mlst=None):
        parts = x.split("_")
        if mlst is not None: 
            try: st = f" ({mlst[x]})"
            except: st = ""
        else: st=""
        return parts[0][0]+". "+parts[1]+" "+"_".join(parts[2:])+st

    strains = strains.sort_values(strain_col)
    if "gambit_predicted_taxon" not in strains:
        strains.loc[:, "gambit_predicted_taxon"] = strains[strain_col].apply(lambda x: x.split("_")[0])

    f, ax = get_figure(figsize=figsize)
    sns.scatterplot(strains, y=strain_col, x="record_id", hue="gambit_predicted_taxon", sizes=(10, MS), alpha=.8,
        palette=palette, size="rapct")
    sns.scatterplot(strains, y=strain_col, x="record_id", color="white", s=MS, alpha=1, zorder=0)
    config_axes(ax, xlabel="Record ID", ylabel="Strain", xrotation=90)
    if mlst_col is not None:
        strain_mlst = strains[[strain_col, mlst_col]].sort_values(strain_col)
        mlsts = strain_mlst.groupby(strain_col)[mlst_col].agg(pd.Series.mode)
        ax.set_yticks(ax.get_yticks(), [label_transform_f(x.get_text(), mlsts) for x in ax.get_yticklabels()])
    ax.set_xlim(-1, ax.get_xlim()[1])

    plt.show()

def strain_matrix(X: pd.DataFrame, group_col: Hashable, value_col: Hashable = "strain"):

    return pd.pivot_table(X.reset_index(), columns=value_col, index=group_col, values=X.index.name, 
        aggfunc="size", fill_value=0).astype(bool)

def strain_dissimilarity(X: Union[pd.DataFrame, ArrayLike], distance_f: Callable=jaccard) -> pd.DataFrame:
    
    jacc = pdist(X, distance_f)
    contents = []
    for i, id1 in enumerate(X.index):
        for j, id2 in enumerate(X.index):
            if i < j: contents.append([id1, id2, get_idx_from_dense(i, j, jacc, len(X))])

    return pd.DataFrame(contents, columns=[f"{X.index.name}_1", f"{X.index.name}_2", "distance"])

def simplify_strain_name(name: str):

    parts = name.split("_")
    return " ".join([parts[0][0]+"."] + parts[1:])

def plot_straingst_abundances(X: pd.DataFrame, sample_col: str, *, 
    palette: Union[Callable, Hashable, str] = glasbey, strain_col: Union[str, Hashable] = "strain", 
    figsize: Tuple[float, float] = (15, 7), ax: Union[None, Axes] = None, style: str = "seaborn-v0_8-white", 
    legend: bool=True, legend_ncols: int = 2, cmap: Union[dict, None] = None, title: str = "") -> Axes:

    if ax is None:
        with plt.style.context(style):
            fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=figsize)
    
    # Get genera
    X.loc[:, "genus"] = X[strain_col].apply(lambda x: x.split("_")[0])
    abundances = pd.pivot_table(X, index=strain_col, columns=sample_col, 
                                values="rapct", fill_value=0.0).sort_index()
    # Build color map based on genera
    if cmap is None: cmap = get_cmap(X, palette, "genus", "strain")
    else: assert isinstance(cmap, dict), f"cmap must be a dict. Got type {type(cmap)}."

    with plt.style.context(style):
        bottom = np.zeros_like(abundances.values[0])
        for lower_lvl, values in abundances.iterrows():
            color = cmap[lower_lvl]
            ax.bar(np.arange(len(values)), values, label=lower_lvl, color=color, bottom=bottom)
            bottom += values.values
    
    ax.set_xticks(np.arange(abundances.shape[1]), abundances.columns.to_list(), ha="center", va="top", rotation=90)
    ax.set_ylabel("Relative abundance (%)")
    ax.set_title(title, fontweight="bold")
    if legend: ax.legend(loc="upper left", bbox_to_anchor=(1, 1), frameon=False, title="Strain", ncol=legend_ncols)
    sns.despine(ax=ax)
    return ax