import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union
from numpy.typing import ArrayLike
from tqdm import tqdm
from pysam import VariantFile

_VCF_HEADER = ["chrom", "pos", "id", "ref", "alt", "qual", "filter", "info", "format", "sample"]

def get_info_value(s:str, tag:str, delim:str = ";", dtype = float):
    return dtype(s.split(tag+"=")[-1].split(delim)[0]) if tag in s else None

def filter_vcf(filename: Union[str, Path], out: Union[str, Path], comment: str = "#", **kwargs):
    """Filters a VCF file.

    Args:
        filename (Union[str, Path]): Path to the input VCF file.
        out (Union[str, Path]): Output VCF file.
        comment (str, optional): Comment character. Defaults to "#".
        **kwargs: Argument names should be the names of the fields to be filtered. These names are
            case sensitive and should match the column names in the VCF file. May also be tags in the
            INFO column. Values should be functions returning True if the feature passes the filter
            and False otherwise. These functions should take a single string as input, so take care
            to cast it to the correct data type for comparison.
    """
    colnames = None
    with open(out, "w") as outfile:
        with open(filename) as infile:
            for line in tqdm(infile):
                if line.startswith(comment): 
                    outfile.write(line)
                    if line.startswith(comment+"CHROM"):
                        # Save as the column names
                        colnames = np.array(line.removeprefix(comment).split("\t"))
                elif colnames is not None:
                    write_ln = True
                    for k, v in kwargs.items():
                        if v is not None:
                            if k in colnames:
                                # Field to be filtered is part of the columns and not in the info field
                                field = line.split("\t")[np.argmax(colnames==k)]
                            else:
                                # Field is in the info column
                                field = get_info_value(line.split("\t")[np.argmax(colnames=="INFO")], k)
                            write_ln = v(field)
                        if not write_ln: break
                    if write_ln: outfile.write(line)
    return outfile

def filter_pilon_vcf(filename: str, out: str, min_base_quality: Union[int, None] = None, snp_only: bool = True, 
    remove_ref: bool = True, min_cov: int = 0, max_cov: Union[int, None] = None, min_freq: Union[float, None] = None):

    min_bq_f = (lambda x: int(x) > min_base_quality) if min_base_quality is not None else None
    alt_f = (lambda x: x != ".") if (snp_only or remove_ref) else None
    filter_f = (lambda x: x in ["PASS", "Amb"]) if snp_only else None
    dp_f = (lambda x: int(x) >= min_cov and int(x) <= max_cov) if max_cov is not None else (lambda x: int(x) >= min_cov)
    af_f = (lambda x: float(x) >= min_freq) if min_freq is not None else None

    return filter_vcf(filename, out, BQ = min_bq_f, ALT = alt_f, FILTER = filter_f,
        DP = dp_f, AF = af_f)

def vcf_to_dataframe(file:str, mode:str = "r"):

    df = pd.read_csv(file, sep="\t", comment="#", header=None)
    df.columns = _VCF_HEADER[:df.shape[1]]
    return df