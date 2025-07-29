#%%
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns 
from colorcet import glasbey 
import numpy as np
import pandas as pd
from typing import Union

def read_coords(filepath: str) -> pd.DataFrame:

    columns = ["ref_start", "ref_end", "query_start", "query_end", "ref_len", "query_len", "identity", "ref_contig"]
    content = []

    with open(filepath) as f:
        header=True
        for n, line in enumerate(f):
            if header and line.startswith("===="):
                header = False
            elif not header:
                cols, contig = line.split("\t")
                cols = np.hstack([x.split(" ") for x in cols.split("|")])
                cols = cols[cols!=""]

                # Check if all columns were parsed
                if len(cols) != len(columns):
                    raise ValueError(f"Error reading {filepath}, line {n}:{line}. Expected {len(columns)} columns, \
got {len(cols)}: {', '.join(cols)}")
                
                content.append(np.hstack([contig.split("\n")[0], cols]))

    return pd.DataFrame(content, columns=["query_contig"]+columns)

def plot_coords(filepath: str, figsize=(20, 10), lw=3, color="black", style="seaborn-v0_8-whitegrid", 
    y_axis: str = "query_contig", min_len=0, fill: bool = True, title=None, save_path: Union[str, None]=None,
    merge_refs: bool = False, y_min: float=0, fill_alpha=.5):

    assert y_axis in ["query_contig", "identity"], f"Got y_axis '{y_axis}'. Must be one of 'query_contig' or 'identity'."
    
    coords = read_coords(filepath)
    # map references to axes
    if not merge_refs:
        ax_map = {v:k for k,v in coords["ref_contig"].drop_duplicates().reset_index(drop=True).sort_values().items()}
        y_map = {v:0 for k,v in coords["query_contig"].drop_duplicates().reset_index(drop=True).sort_values().items()}
        n_axes = len(ax_map)
        n_y_axes = 1
    else:
        ax_map = {v:0 for k,v in coords["ref_contig"].drop_duplicates().reset_index(drop=True).sort_values().items()}
        n_axes = 1
        y_map = {v:k for k,v in coords["query_contig"].drop_duplicates().reset_index(drop=True).sort_values().items()}
        n_y_axes = len(y_map)

        ref_lim = np.maximum(coords.groupby("ref_contig")["ref_end"].max(), 
            coords.groupby("ref_contig")["ref_start"].max()).astype(int)
        ref_offset = pd.Series(np.hstack([[0], ref_lim.cumsum().values[:-1]]), index=ref_lim.index, name="ref_offset")
        coords = coords.join(ref_offset, on="ref_contig")
        coords["ref_start"] = coords["ref_start"].astype(int) + coords["ref_offset"]
        coords["ref_end"] = coords["ref_end"].astype(int) + coords["ref_offset"]

    with plt.style.context(style):
        f, axs = plt.subplots(n_y_axes, n_axes, constrained_layout=True, figsize=figsize, sharey=True, sharex=True)
        if n_axes == 1 and n_y_axes == 1: axs = np.array([[axs]])
        elif n_axes == 1: axs = np.array([axs]).transpose()
        elif n_y_axes == 1: axs = np.array([axs])

        if y_axis == "query_contig":
            # map contig ids to the y axis
            y_map = {v:k for k,v in coords["query_contig"].drop_duplicates().reset_index(drop=True).sort_values().items()}
            
            for _, row in coords.iterrows():
                if int(row["ref_len"]) > min_len and int(row["query_len"]) > min_len:
                    ax = axs[y_map[row["query_contig"]], ax_map[row["ref_contig"]]]
                    ax.plot([int(row["ref_start"]), int(row["ref_end"])], [y_map[row["query_contig"]]]*2,
                        lw=lw, color=color)
            for ax in axs.flatten():
                ax.set_yticks(list(y_map.values()), list(y_map.keys()))
                ax.set_ylabel("Query contig")
                ax.grid()
        else:
            # Assign a color to each query contig
            cmap = {k:v for k,v in zip(coords["query_contig"].unique(), 
                sns.color_palette(color, coords["query_contig"].nunique()))}
            
            for _, row in coords.iterrows():
                if int(row["ref_len"]) > min_len and int(row["query_len"]) > min_len:
                    ax = axs[y_map[row["query_contig"]], ax_map[row["ref_contig"]]]
                    if fill:
                        patch = Rectangle((int(row["ref_start"]), float(row["identity"])), 
                            int(row["ref_end"])-int(row["ref_start"]), -float(row["identity"]), 
                            edgecolor=cmap[row["query_contig"]], facecolor=cmap[row["query_contig"]], alpha=fill_alpha,
                            zorder=110-float(row["identity"]))
                        ax.add_patch(patch)
                    ax.plot([int(row["ref_start"]), int(row["ref_end"])], [float(row["identity"])]*2,
                        lw=lw, color=cmap[row["query_contig"]], zorder=110-float(row["identity"]))
            if merge_refs:
                for x in ref_offset.values[1:]:
                    for ax in axs.flatten(): 
                        ax.axvline(x, ls="--", color="gray", lw=.5, alpha=.2)
                        ax.grid(False)

            for id_, ax in zip(ax_map.keys(), axs.flatten()):
                ax.set_ylabel("% Identity")
                ax.set_ylim(y_min, 101)
                if merge_refs: x_lim = np.maximum(coords["ref_start"].max(), coords["ref_end"].max())
                else: x_lim = np.maximum(coords[coords["ref_contig"]==id_]["ref_end"].astype(int).max(),
                    coords[coords["ref_contig"]==id_]["ref_start"].astype(int).max())
                ax.set_xlim(0, x_lim)
                    
        for id_, id_y, ax in zip(ax_map.keys(), y_map.keys(), axs.flatten()):
            if not merge_refs: ax.set_xlabel(f"Ref: {id_}")
            else: 
                ax.set_title(f"Query: {id_y}")

        if merge_refs: axs[-1, 0].set_xlabel(f"Merged reference contigs")
        
        if title: f.suptitle(title, fontweight="bold", fontsize="large")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
    plt.show()
# %%
