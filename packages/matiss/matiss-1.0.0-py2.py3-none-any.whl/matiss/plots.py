#%%
from pyvis.network import Network
import pandas as pd
from typing import Tuple, Hashable, Collection, Callable, Union, Literal
from colorcet import glasbey
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import get_font_names
import glob
from matplotlib.font_manager import fontManager, FontProperties
from matplotlib.axes import Axes
from matplotlib.ticker import PercentFormatter
from pathlib import Path
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# seaborn and matplotlib helper functions

def get_figure(
    nrows: int = 1, 
    ncols: int = 1, 
    figsize: Tuple[int, int] = (10,7),
    **kwargs
) -> Tuple[Figure, Axes]:
    return plt.subplots(nrows, ncols, constrained_layout=True, figsize=figsize, **kwargs)

def list_fonts():

    return [x.split("/")[-1].replace(".tff", "") for x in 
        glob.glob("/usr/share/fonts/truetype/*/*")]

def set_font(fontname: str):
    path = glob.glob("/usr/share/fonts/truetype/*/"+fontname+".ttf")[0]
    fontManager.addfont(path)

    prop = FontProperties(fname=path)
    sns.set_theme(font=prop.get_name())

def config_axes(ax:Axes, *, move_legend:bool=True, grid:bool=True, 
    legend_title=None, xlabel=None, ylabel=None, xlog:bool=False, ylog:bool=False,
    xrotation=None, ypercent:bool = False, xpercent: bool = False,
    title=None, xlim=None, ylim=None, despine: bool = True):

    if despine: sns.despine(ax=ax)
    if ax.get_legend(): 
        sns.move_legend(ax, loc="best", frameon=False, title=legend_title)
    if move_legend:
        try: 
            sns.move_legend(ax, loc="center left", bbox_to_anchor=(1, 0.5), 
                            frameon=False, title=legend_title)
        except:
            ax.legend()
            sns.move_legend(ax, loc="center left", bbox_to_anchor=(1, 0.5), 
                            frameon=False, title=legend_title)
    if grid: ax.grid(alpha=.3)
    ax.set(ylabel=ylabel, xlabel=xlabel, title=title)
    if xlog: ax.set_xscale("log")
    if ylog: ax.set_yscale("log")
    if xrotation: ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), va="top", 
            ha="right" if xrotation != 90 else "center", rotation=xrotation)
    if xlim is not None: ax.set_xlim(xlim)
    if ylim is not None: ax.set_ylim(ylim)
    if ypercent: ax.yaxis.set_major_formatter(PercentFormatter(1, 0))
    if xpercent: ax.xaxis.set_major_formatter(PercentFormatter(1, 0))
    return ax

def add_significance(ax: Axes, *, p_table: pd.DataFrame, g1_col: str = "group_1", g2_col: str = "group_2",
    p_col: str = "p", axis: str = "x", thresh: float = .05, pad: float = .1, 
    color: str = "black", lw: float = 1.0) -> Axes:

    assert axis in ["x", "y"], f"Axis must be one of 'x' or 'y'. Got {axis}."

    # Drop duplicated pairs
    p_table = p_table.assign(
        hash = p_table.apply(
            lambda x: " - ".join(
                np.sort(
                    [
                        x[g1_col],
                        x[g2_col]
                    ]
                )
            ),
            axis = 1
        )
    ).drop_duplicates("hash")
    
    iterator = zip(ax.get_xticks(), ax.get_xticklabels()) if axis=="x" else zip(ax.get_yticks(), ax.get_yticklabels())
    y, y_whisk, gap = ax.get_ylim()[1]*(1+pad), ax.get_ylim()[1]*(1+pad*.5), ax.get_ylim()[1]*pad

    coords = pd.DataFrame([[l.get_text(), x] for x, l in iterator], columns=["label", "pos"]).set_index("label")
    for _, x in p_table[p_table[p_col].le(thresh)].iterrows():
        coord1, coord2 = coords.loc[x[g1_col]], coords.loc[x[g2_col]]
        
        ax.plot([coord1,coord2], [y,y], color=color, lw=lw)
        ax.plot([coord1,coord1], [y,y_whisk], color=color, lw=lw)
        ax.plot([coord2,coord2], [y,y_whisk], color=color, lw=lw)
        y, y_whisk = y+gap, y_whisk+gap

    return ax

def rgba_to_hex(rgba) -> str:
        
        if isinstance(rgba, str) and rgba.startswith("#"): return rgba
        rgba_ = np.array(deepcopy(rgba))
        # Convert to [0, 255]
        rgba_ *= 255
        rgba_ = rgba_.astype(int)
        rgba_ = np.minimum(255, rgba_)
        return "#{0:02x}{1:02x}{2:02x}".format(*rgba_)

def network(X: pd.DataFrame, nodes: Hashable, weight: Hashable, shape: Hashable = "circle", shape_map: dict = {}, 
    color: Hashable = "black", palette: Callable = glasbey, width: str = "600px", height: str = "600px", *, 
    directed: bool = False, notebook: bool = True, net_kwargs: dict = {}, is_distance: bool = False, 
    hide_label: bool=False):

    network = Network(height, width, notebook=notebook, directed=directed, **net_kwargs)

    # Get color map
    if (((color+"_1") in X.columns) and ((color+"_2") in X.columns)):
        unique_colors = pd.concat([X[color+"_1"], X[color+"_2"]]).unique()
        cmap = {c: rgba_to_hex(rgb) for c, rgb in zip(unique_colors, palette)}
        var_color = True
    else: var_color = False

    var_shape =  (shape+"_1" in X.columns and shape+"_2" in X.columns)
    
    for n, row in X.iterrows():
        for num in [1, 2]:
            title = "\n".join([
                f"Name: {row[f'{nodes}_{num}']}",
                f"Color: {row[f'{color}_{num}']}",
                f"Shape: {row[f'{shape}_{num}']}"
            ])
            network.add_node(row[f"{nodes}_{num}"], label="" if hide_label else row[f"{nodes}_{num}"], 
                color=cmap[row[f"{color}_{num}"]] if var_color else color, 
                shape=shape_map[row[f"{shape}_{num}"]] if var_shape else shape,
                title=title)
        
        weight_ = (1-row[weight]) if is_distance else row[weight]
        if weight_ > 0: 
            network.add_edge(row[f"{nodes}_1"], row[f"{nodes}_2"], value=weight_)

    network.toggle_physics(False)
    network.show_buttons(["physics"])

    return network

def phylo_tree_labels(x: str, kind="straingst", nodes_to_display: Union[None, Collection[str]] = None) -> str:
    """
    Auxiliary function to transform the node labels of a phylogenetic tree.
    """
    if nodes_to_display is not None:
        if x.name is not None and x.name.endswith(".fa"): trunc_name = x.name[:-3]
        else: trunc_name = x.name
        if (not x.name in nodes_to_display) and (not trunc_name in nodes_to_display): 
            return None
    if kind == "straingst":
        
        try:
            genus, species, strain = x.name.split("_")[0:3]
            genus = genus[0]+"."
            if strain.endswith(".fa"): strain = strain[:-3]
            return " ".join([genus, species, strain])
        except: return None
    if kind == "straingst_no_species":
        
        try:
            strain = x.name.split("_")[2]
            if strain.endswith(".fa"): strain = strain[:-3]
            return strain
        except: return None
    else: raise ValueError(f"Got invalid kind {kind}")

# Functions for iTOL annotations
def get_itol_rgba_colors(labels: list, palette=None):
    if palette is None: palette = sns.color_palette(glasbey, len(labels))
    # Map to 8 bit RGB
    colors = [np.hstack([np.round(np.array(x)*256), 1]).astype(int).astype(str) for x in palette]
    return {k:f"rgba({','.join(v)})" for k,v in zip(labels, colors)}
    
def itol_color_annotation(dataset: pd.DataFrame, column, dataset_name: str, label_to_color=None, dataset_color="#ff0000"):
    unique_labels = dataset[column].unique()
    if label_to_color is None: label_to_color = get_itol_rgba_colors(unique_labels)
    
    header="\n".join([
        "DATASET_COLORSTRIP",
        "SEPARATOR SPACE",
        f"DATASET_LABEL {dataset_name}",
        "COLOR #ff0000",
        "", "DATA"
    ])
    
    data = "\n".join([
        f"{idx} {label_to_color[val]} {val}"
        for idx, val in dataset[column].items()
    ])
    
    return "\n".join([header, data])

def itol_multiple_binary_annotation(dataset: pd.DataFrame, columns: list, colnames: list=None, 
    dataset_name: str="binary", plot_type="ring"):
    
    assert plot_type in ["ring", "symbol"], f"plot_type must be one of 'ring' or 'symbol'. Got {plot_type}."
    
    n_cols = len(columns)
    if colnames is None: colnames = columns
    assert len(columns)==len(colnames), f"The number of columns ({n_cols}) does not match the number \
of column names ({len(colnames)})."
    label_to_color = get_itol_rgba_colors(colnames)
        
    if plot_type == "ring":
        annotations = {}
        neg_color = "rgba(255,255,255,0)"
        for col, colname in zip(columns, colnames):
            pos_color = label_to_color[colname]
            colors = {True: pos_color, False: neg_color}
            annotation_name = dataset_name+'_'+colname.replace(' ','_')
            annotations[annotation_name] = itol_color_annotation(dataset, col, annotation_name, colors, pos_color)
        return annotations
    else:

        header="\n".join([
            "DATASET_BINARY",
            "SEPARATOR SPACE",
            f"DATASET_LABEL {dataset_name}",
            "COLOR #ff0000",
            f"FIELD_SHAPES {' '.join(['1']*n_cols)}",
            f"FIELD_LABELS {' '.join(colnames)}",
            f"FIELD_COLORS {' '.join([v for v in label_to_color.values()])}",
            "", "DATA"
        ])

        codes = dataset[columns].replace(False, -1).replace(True, 1).astype(str)
        data = "\n".join([
            f"{idx} {' '.join(val.values)}"
            for idx, val in codes.iterrows()
        ])

        return "\n".join([header, data])

def wig(file: str, ax: Axes, kind: str = "line", style: str = "seaborn-v0_8-white", lw: float = 1, subset: int = 10):

    if kind not in ["line"]: raise NotImplementedError(f"Kind must be 'line'.")
    # Read file
    y, vlines = [], []
    with open(file) as f: 
        for n, line in enumerate(f):
            if line.startswith("track type"): continue
            if line.isalnum(): 
                if (n % subset) == 0: y.append(float(line.replace("\n", "")))
            else: 
                vlines.append(n)
                y.append(0)

    with plt.style.context(style):
        ax.plot(np.arange(len(y)), y, color=(.1, .1, .1), lw=lw)
        ax.vlines(vlines, min(y), max(y), ls="--", color="gray")
    return ax

def save(
    path: Union[str, Path],
    format: list = ["png"]
):
    for fmt in format:
        plt.savefig(
            str(path) + "." + fmt
        )

def set_style(
    *,
    font: str = "Helvetica",
    fontsize: int = 50,
    titleweight: int = 600,
    titlesize: int = 20,
    labelweight: int = 600,
    labelsize: int = 15,
    seaborn_style: Literal["white", "whitegrid", "ticks", "dark", "darkgrid"] = "whitegrid"
):

    sns.set_theme(
        rc = {
            "font.size": fontsize,
            "axes.labelsize": labelsize,
            "axes.labelweight": labelweight,
            "axes.titlesize": titlesize,
            "axes.titleweight": titleweight,
            "font.family": font
        },
        style = seaborn_style,
        font = font
    )

# %%
