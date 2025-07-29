#%%
import pandas as pd
import numpy as np
import seaborn as sns
from colorcet import glasbey
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from typing import Tuple, Union, Collection, Callable

def plot_bracken_abundances(report: pd.DataFrame, sample_col: str, *, ax: Union[None, Axes] = None, 
    figsize: Tuple[float, float] = (10,7), level: str = "genus", style: str = "seaborn-v0_8-white",
    palette: Callable = glasbey, title: str = "Relative abundances per sample", 
    cmap: Union[None, dict] = None, legend_ncols: int = 2, legend: bool = True):

    if level != "genus": raise NotImplementedError

    if ax is None:
        with plt.style.context(style):
            fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=figsize)
    
    # Get genera
    report.loc[:, "genus"] = report["name"].apply(lambda x: x.split(" ")[0])
    abundances = pd.pivot_table(report, index="name", columns=sample_col, 
                                values="fraction_total_reads", fill_value=0.0).sort_index()
    # Build color map based on genera
    if cmap is None: cmap = get_cmap(report, palette, level)
    else: assert isinstance(cmap, dict), f"cmap must be a dict. Got type {type(cmap)}."

    with plt.style.context(style):
        bottom = np.zeros_like(abundances.values[0])
        for lower_lvl, values in abundances.iterrows():
            color = cmap[lower_lvl]
            ax.bar(np.arange(len(values)), values*100, label=lower_lvl, color=color, bottom=bottom)
            bottom += values.values*100
    
    ax.set_xticks(np.arange(abundances.shape[1]), abundances.columns.to_list(), ha="center", va="top", rotation=90)
    ax.set_ylabel("Relative abundance (%)")
    ax.set_title(title, fontweight="bold")
    if legend: ax.legend(loc="upper left", bbox_to_anchor=(1, 1), frameon=False, title="Species", ncol=legend_ncols)
    sns.despine(ax=ax)
    return ax

def get_cmap(report: pd.DataFrame, palette: Callable = glasbey, taxa_col: str = "genus", 
    name_col: str = "name") -> dict:

    cmap = {}
    for taxon, hex in zip(report[taxa_col].unique(), 
                          sns.color_palette(palette, report[taxa_col].nunique()).as_hex()):
        lower_lvl = report.loc[report[taxa_col]==taxon, name_col].sort_values().unique()
        for k,v in zip(lower_lvl, sns.dark_palette(hex, len(lower_lvl)+1, reverse=True)[:len(lower_lvl)]):
            cmap[k] = v
    return cmap
# %%
