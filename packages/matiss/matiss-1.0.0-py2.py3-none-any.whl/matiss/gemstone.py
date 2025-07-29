#%%
import pandas as pd
from typing import List, Union, Tuple, Callable, Dict, Hashable, Collection
from copy import copy
from numpy.typing import ArrayLike
import numpy as np
import tqdm
from pathlib import Path
import re

species_map = {"ABAUMANNII": "Acinetobacter baumannii", "C.AMALOTICU": "Citrobacter amalonaticus",
    "C.FREUNDII": "Citrobacter freundii", "KOZAE": "Klebsiella ozaenae", "KOXY": "Klebsiealla oxytoca",
    "KAERO": "Klebsiella aerogenes", "KPNEUMO": "Klebsiella pneumoniae", "H.ALVEI": "Hafnia alvei",
    "PMIRA": "Proteus mirabilis", "ECOLI": "Escherichia coli", np.nan: "unknown", "unknown":"unknown",
    "SAUREUS": "Staphylococcus aureus", "ENTEROCOCCUS SPP": "Enterococcus", 
    "ENTEROROCCUS SPP": "Enterococcus", "CAURIS": "Candida auris"}

isolate_dtypes = dtypes = {
    "freezer_box_row": "Int64",
    "CLEAN_phase": "Int8",
    "CLEAN_sweep": "Int8",
    "assembly_length": "Int64",
    "dzd_rack_column": "Int64",
    "dzd_rack_position": "Int64",
    "freezer_box_number": "Int64",
    "freezer_box_row": "Int64",
    "num_reads_clean1": "Int64",
    "num_reads_clean2": "Int64",
    "num_reads_clean_pairs": "Int64",
    "num_reads_raw1": "Int64",
    "num_reads_raw2": "Int64",
    "num_reads_raw_pairs": "Int64",
    "number_contigs": "Int64",
    "uci_id": "Int64"
}

def drop_contaminated(X: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:

    return X[X["checkm2_contamination"] < threshold]

def get_correct_mdro_type(X: pd.DataFrame) -> pd.Series:
    return X["gambit_predicted_taxon"].apply(_get_correct_mdro_type_aux)

def _get_correct_mdro_type_aux(x: str) -> str:
    if not isinstance(x, str): return "Unknown"
    genus = x.split(" ")[0].split("/")[0]
    if genus == "Staphylococcus": return "MRSA"
    elif genus == "Enterococcus": return "VRE"
    elif genus == "Candida": return "CAURIS"
    else: return "Unknown"

def get_strains(samples: pd.DataFrame):

    id_colname = samples.index.name

    strains = []
    for idx, straingst_files in tqdm.tqdm(
        samples["straingst_strains"].dropna().items(),
        total = len(samples["straingst_strains"].dropna())
    ):
        if not isinstance(straingst_files, str): continue
        for straingst_file in straingst_files.split("\"")[1:-1]:
            if straingst_file==",": continue
            try:
                i_strains = pd.read_table(straingst_file)
            except Exception as e:
                print(f"Failed to read StrainGST strains output at {straingst_file} ({idx}) with exception {e}. Ignoring this sample...")
                continue
            n_strains = len(i_strains)
            i_strains[id_colname] = [idx]*n_strains
            strains.append(i_strains)
    strains = pd.concat(strains, ignore_index=True)
    strains.drop("i", axis="columns", inplace=True)
    return strains

def get_assembly_lengths(samples: pd.DataFrame):

    return samples["quast_report"].apply(_parse_quast_report)

def filter_table(table: pd.DataFrame, *, project=None, mdro=None, swab_site=None, species=None, predicted_taxon=None,
    drop_no_analysis=True) -> pd.DataFrame:

    out = copy(table)
    for var, colname in zip([project, mdro, swab_site, species, predicted_taxon], ["project", "organism", "site", 
        "species", "gambit_predicted_taxon"]):
        if var is not None: out = _filter(out, colname, var)
    
    if drop_no_analysis: out = out.dropna(subset="analysis_date")
    return out

def get_clean_phase_sweep(samples: pd.DataFrame):

    if "record_id" not in samples.columns:
        raise ValueError("Expected a column named 'record_id' in the DataFrame, but found none.")
    samples_clean = filter_table(samples, project="CLEAN")
    phase = samples_clean["record_id"].apply(lambda x: int(x.split(" ")[-1][0]))
    sweep = samples_clean["record_id"].apply(lambda x: int(x.split(" ")[-1][1]))

    out = pd.concat([phase, sweep], axis=1)
    out.columns = ["CLEAN_phase", "CLEAN_sweep"]
    return out

def _parse_quast_report(path: str):

    try: 
        metrics = pd.read_csv(path, sep="\t", index_col=0).iloc[:,0]
        return int(metrics["Total length"])
    except: return None

def _filter(table: pd.DataFrame, colname: Hashable, query: Union[Collection[Hashable], Hashable]) -> pd.DataFrame:

    if isinstance(query, Collection) and not isinstance(query, str):
        return table[table[colname].isin(query)]
    else: return table[table[colname] == query]

def parse_env_codes(X: pd.DataFrame, project="CLEAN", colname: str = "record_id") -> pd.Series:

    if project == "CLEAN":

        env_codes = {"E1": "Footboard", "E2": "Call light/TV/bed remote", 
            "E3": "Nightstand", "E4": "Overbed table", "E5": "bathroom handrails", "Resident": "Resident"}
        return X[colname].apply(lambda x: env_codes[x[-2:]] if len(x)>9 else None)
    else: raise NotImplementedError()

def sort_room_codes(codes: Union[ArrayLike, pd.Series]):

    def auxf(c):
        room, bed = c.split("-")
        return int(room)+ord(bed)/100

    if isinstance(codes, pd.Series):
        sorted = codes.apply(auxf).sort_values()
        return codes[sorted.index]
    else:
        parsed = [auxf(c) for c in codes]
        sorted_idx = np.argsort(parsed)
        return np.array(codes)[sorted_idx]
    
def subset_matched_isolates_plate_swipes(isolates: pd.DataFrame, 
                                         plate_swipes: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    subset_isolate = isolates[isolates["culture_id"].isin(plate_swipes["culture_id"])]
    subset_isolate = subset_isolate[(~subset_isolate["raw_reads1"].isna()) & (~subset_isolate["raw_reads2"].isna())]
    subset_ps = plate_swipes[plate_swipes["culture_id"].isin(subset_isolate["culture_id"])]

    return subset_isolate, subset_ps

def get_bracken(samples: pd.DataFrame) -> pd.DataFrame:
    
    taxa = []
    for id_, row in samples.iterrows():
        sample_report = pd.read_table(row["bracken_report"]) 
        sample_report[samples.index.name] = [id_]*len(sample_report)
        taxa.append(sample_report)
    return pd.concat(taxa)

def is_sample_in_inventory(inventory_path: str, record_id: Union[Collection[str], str], *,
    swab_site: Union[Collection[str], str] = None, mdro: Union[Collection[str], str] = None,
    species: Union[Collection[str], str] = None, morphotype: Union[Collection[str], str] = None,
    box_num: Union[Collection[float], float] = None, box_row: Union[Collection[str], str] = None,
    box_col: Union[Collection[str], str] = None, inv_sheet_name: str = "Data", 
    as_frame: bool = False, df_index = None) -> Union[bool, ArrayLike, pd.DataFrame]:

    # Read inventory
    inv = pd.read_excel(inventory_path, sheet_name=inv_sheet_name)
    inv.loc[:, "Species"] = inv["Species"].replace(species_map)
    return_collection = True
    if isinstance(record_id, str):
        assert not as_frame, "A single record ID was passed and 'as_frame' is True."
        return_collection = False
        record_id = [record_id]
        if swab_site is not None: swab_site = [swab_site]
        if mdro is not None: mdro = [mdro]
        if species is not None: species = [species]
        if morphotype is not None: morphotype = [morphotype]
        if box_num is not None: box_num = [box_num]
        if box_row is not None: box_row = [box_row]
        if box_col is not None: box_col = [box_col]

    true_arr = np.ones(len(inv), dtype=bool)
    results = []
    masks = {}
    for i in range(len(record_id)):
        masks["Record ID"] = inv["Record ID"].eq(record_id[i])
        masks["MDRO"] = inv["Organism"].eq(mdro[i]) if mdro is not None else true_arr
        masks["Species"] = (inv["Species"].replace(species_map) \
            .isin([species[i], "unknown"]) | inv["Species"].isna()) if (
                species is not None and species[i] != "unknown") else true_arr
        masks["Morphotype"] = (inv["Morphotype Indicator"].replace(np.nan, "unknown") \
            .isin([morphotype[i], "unknown"]) | inv["Morphotype Indicator"].isna()) if (
                morphotype is not None and morphotype[i] != "unknown") else true_arr
        masks["Freezer Box Number"] = (inv["Freezer Box Number"].eq(box_num[i]) | 
                                       inv["Freezer Box Number"].isna()) if box_num is not None else true_arr
        masks["Freezer Box Row"] = (inv["Freezer Box Row"].eq(box_row[i]) | 
                                       inv["Freezer Box Row"].isna()) if box_row is not None else true_arr
        masks["Freezer Box Column"] = (inv["Freezer Box Column"].eq(box_col[i]) |
                                       inv["Freezer Box Column"].isna()) if box_col is not None else true_arr

        prev_mask = masks["Record ID"]
        for level in ["Record ID", "MDRO", "Species", "Morphotype", "Freezer Box Number", 
                    "Freezer Box Row", "Freezer Box Column"]:
            mask = prev_mask & masks[level]
            if sum(mask) == 0:
                # No matches found
                results.append([False, level, inv.index.to_numpy()[prev_mask], True if level in ["Freezer Box Number", 
                    "Freezer Box Row", "Freezer Box Column"] else False])
                break
            else: prev_mask = mask
        # Match found
        if sum(mask) != 0: results.append([True, "None", inv.index.to_numpy()[mask], False])
    results = pd.DataFrame(results, index=df_index, columns=["in_inventory", "mismatch_level", 
                                                             "best_match_idx", "freezer_mismatch"])
    if as_frame: return results
    elif return_collection: return results["in_inventory"].values
    else: return results["in_inventory"].values[0]

def add_mlst_to_strain_names(isolate_strains: pd.DataFrame, ps_strains: pd.DataFrame, isolates: pd.DataFrame):
    sts = isolate_strains.join(isolates["ts_mlst_predicted_st"][isolates["qc_check"]=="QC_PASS"], 
        on=isolates.index.name).groupby("strain")["ts_mlst_predicted_st"].agg(pd.Series.mode).astype(str) \
        .replace(["[]", "No ST predicted"], "")
    ps_strains.loc[:, "strain"] = ps_strains["strain"] \
        .apply(lambda x: x+((" ("+sts.loc[x]+")") if x in sts.index else "")) \
        .str.replace(" ()", "")
    isolate_strains.loc[:, "strain"] = isolate_strains["strain"] \
        .apply(lambda x: x+((" ("+sts.loc[x]+")") if x in sts.index else "")) \
        .str.replace(" ()", "")

    return isolate_strains, ps_strains 

def correct_dtypes(X: pd.DataFrame) -> pd.DataFrame:

    for k,v in isolate_dtypes.items():
        if hasattr(X, k): X[k] = X[k].astype(v)
    if hasattr(X, "dzd_batch"):

        def fix_batch(x):

            if pd.isna(x): return pd.NA

            try:
                return str(int(x.removeprefix("batch_")))
            except ValueError:
                return x

        X.dzd_batch = X.dzd_batch \
            .apply(fix_batch)
        
    if hasattr(X, "dzd_plate"):
        X_cauris = X.dzd_plate.str.startswith("GEM Plate CAUR").fillna(False)
        plates = X.loc[~X_cauris, "dzd_plate"]
        X.loc[~X_cauris, "dzd_plate"] = plates \
            .where(plates.isna() | 
            plates.map(lambda x: isinstance(x, str)) |
            plates.str.removeprefix("GEM Plate") \
                .str.removeprefix("Plate") \
                .str.removeprefix("UCI Collections Plate ") \
                .str.removeprefix("UCI P01 Plate ")
                .astype("Int64").astype(str))
        
    return X

def filter_strains(
    table: pd.DataFrame,
    mdro_col: str = "organism",
    strain_col = "strain"
) -> pd.DataFrame:
    """Filters a table containing one StrainGST reference per row, removing contaminant
    StrainGST references (when the genus does not match the MDRO selection for that row).

    Args:
        table (pd.DataFrame): Table containing the StrainGST reference and MDRO type 
    information
        mdro_col (str, optional): Name of the column containing the MDRO type. Defaults 
    to "organism".
        strain_col (str, optional): Name of the column containing the StrainGST reference. 
    Defaults to "strain".

    Returns:
        pd.DataFrame: Table with the contaminant rows removed
    """

    # For MRSA, drop non-Staph
    mrsa = ( 
        table[mdro_col].isin(["MRSA", "MSSA"]) & \
        table[strain_col].str[:4].eq("Stap")
    )

    # For VRE, drop non-enterococci
    vre = ( 
        table[mdro_col].eq("VRE") & \
        table[strain_col].str[:4].eq("Ente")
    )

    # For CRAB, drop non-Acinetobacter
    crab = ( 
        table[mdro_col].eq("CRAB") & \
        table[strain_col].str[:4].eq("Acin")
    )   

    # For ESBL and CRE, drop Staph and enterococci
    esbl = ( 
        table[mdro_col].isin(["CRE", "ESBL"]) & \
        ~table[strain_col].str[:4].isin(["Stap", "Ente"])
    )

    # Drop C. auris
    cauris = table[mdro_col].eq("CAURIS")

    return table[ 
        (
            mrsa | \
            vre | \
            crab | \
            esbl
        ) & ~cauris
    ]

class NHCodes:

    def __init__(
        self,
        code_map_file: Union[str, Path],
        redundant_codes_file: Union[str, Path]
    ) -> None:
        
        self.nh_code_map = pd.read_table(code_map_file, index_col=0) \
            .to_dict()["gemstone_code"]
        self.redundant_codes = pd.read_table(redundant_codes_file, index_col=0) \
            .to_dict()["facility_code"]

    def replace_nh_code(self, x: str) -> str:

        if pd.isna(x): return pd.NA
        nh_code = re.findall("[a-zA-Z]+", x)[0]
        if not nh_code in self.nh_code_map.keys(): 
            return x
        return x.replace(nh_code, self.nh_code_map[nh_code])
    
    def replace_redundant_codes(self, x: str) -> str:

        if pd.isna(x): return pd.NA
        nh_code = re.findall("[a-zA-Z]+", x)[0]
        if not nh_code in self.redundant_codes.keys(): 
            return x
        return x.replace(nh_code, self.redundant_codes[nh_code])
# %%
