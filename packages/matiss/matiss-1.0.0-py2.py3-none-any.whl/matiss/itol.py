import pandas as pd
import seaborn as sns
import numpy as np
from colorcet import glasbey

def get_itol_rgba_colors(labels: list, palette=None):
    if palette is None: palette = sns.color_palette(glasbey, len(labels))
    # Map to 8 bit RGB
    colors = [np.hstack([np.round(np.array(x)*256), 1]).astype(int).astype(str) for x in palette]
    return {k:f"rgba({','.join(v)})" for k,v in zip(labels, colors)}
    
def itol_color_annotation(dataset: pd.DataFrame, column, dataset_name: str, label_to_color=None):
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