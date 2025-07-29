#%%
import io
from firecloud import api as fapi
from typing import Collection, Hashable, List, Union, Dict
import numpy as np
import pandas as pd
from pathlib import Path
from google.cloud import storage
import warnings

# GEMSTONE workspace environment variables
PROJECT = {"P1": "gemstone-P1", "DSSC": "gemstone-DSSC", "P2": "gemstone-P2", "NIH": "gemstone-NIH"}
WORKSPACE = {"P1": "GEMSTONE - P1", "DSSC": "GEMSTONE - DSSC", "P2": "GEMSTONE - P2", "NIH": "GEMSTONE - NIH", 
    "storage": "GEMSTONE - Storage", "test": "GEMSTONE - Test"}
BUCKET = {
    "P2": "fc-secure-e8e2005f-511a-4f92-9127-33041e906b12",
    "DSSC": "fc-secure-25c41ed3-a783-497b-9da1-003883b49136",
    "storage": "fc-secure-35ef90c7-0633-4a72-ac51-b1ecc6f1fe20",
    "test": "fc-secure-7751772e-8b9f-48be-9267-d7a815a23b02"
}
GOOGLE_PROJECT_ID = {
    "DSSC": "terra-6ee53ddf",
    "P2": "terra-23d996c8"
}

def _config_project(project: str) -> Dict[str, str]:

    if project not in WORKSPACE.keys():
        raise ValueError(f"Got invalid project {project}. Must be one of {', '.join(list(WORKSPACE.keys()))}.")
    elif project in ["test", "storage", "DSSC"]: 
        return {"project": PROJECT["DSSC"], "workspace": WORKSPACE[project], 
            "bucket": BUCKET[project], "google_proj_id": GOOGLE_PROJECT_ID["DSSC"]}
    else:
        return {"project": PROJECT[project], "workspace": WORKSPACE[project], 
            "bucket": BUCKET[project], "google_proj_id": GOOGLE_PROJECT_ID[project]}
    
def _clean_entity_tsv(data: str) -> str:

    # Deal with Array parsing issues
    return data.replace("[null]", "[]").replace("[null,null]", "[]").replace("\"\"", "\"").replace("\"[", "[").replace("]\"", "]")

def read_entity(path: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(Path(path).read_text().replace("Sites\n", "Sites ")), index_col=0, sep='\t')

def get_entity(
        name: str, 
        project: str = "DSSC", 
        attrs: Union[Collection[Hashable], None] = None
    ) -> pd.DataFrame:
    """
    Loads an entity data table from a Terra workspace and returns it as a Pandas DataFrame.

    Parameters
    ----------
    name: str
        Entity table name.
    project: "P1", "P2", "NIH", "DSSC", "test" or "storage". Default is "DSSC"
        Workspace from which to load the table.

    Returns
    -------
    table: Pandas DataFrame
    """

    config = _config_project(project)
    response = fapi.get_entities_tsv(
        config["project"], 
        config["workspace"], 
        name, 
        model = "flexible", 
        attrs=attrs
    ).text

    if response.startswith("{"): 
        raise ValueError(f"Failed to fetch entity {name} from project {project}. FAPI message: {response}")
        
    return pd.read_csv(io.StringIO(response.replace("Sites\n", "Sites ")), index_col=0, sep='\t')

def get_entity_set(
    name: str, 
    project: str = "DSSC", 
):
    
    config = _config_project(project)

    # Query Terra and get JSON response
    response = fapi.get_entity(
        config["project"], 
        config["workspace"], 
        "", name, 
    )

    if response.status_code != 200: 
        raise ValueError(f"Failed to fetch entity {name} from project {project}. FAPI message: {response}")
    
    response = response.json()

    # Remove references to other tables and format as json
    fmt_json = {
        x["name"]: {
            k: v 
            for k,v in x["attributes"].items()
            if k != (name.removesuffix("_set") + "s")
        } 
        for x in response
    }

    df = pd.DataFrame.from_dict(
        fmt_json
    ).transpose()

    df.index.name = "id"

    return df


def table_to_entity_set(table: pd.DataFrame, entity_name: str) -> pd.DataFrame:

    table.index.name = f"membership:{entity_name}_set_id"
    if isinstance(table, pd.Series): table.name = entity_name
    else: table.columns = [entity_name]
    
    return table

def get_file(filepath: str, destination: str, project: str = "DSSC") -> Path:

    config = _config_project(project)
    client = storage.Client(config["google_proj_id"])
    bucket = client.bucket(config["bucket"])
    # Check if the bucket ID is appended to the filepath. If so, remove it
    if config["bucket"] in filepath:
        bucket_path = filepath \
            .removeprefix("gs://" + config["bucket"] + "/") \
            .removeprefix(config["bucket"]+"/")
    else: bucket_path = filepath
    # Download
    bucket.blob(bucket_path) \
        .download_to_filename(destination)
    return Path(destination)

def read_text(
    filepath: str,
    project: str = "DSSC"
) -> str:
    
    config = _config_project(project)
    client = storage.Client(config["google_proj_id"])
    bucket = client.bucket(config["bucket"])

    # Check if the bucket ID is appended to the filepath. If so, remove it
    if config["bucket"] in filepath:
        bucket_path = filepath \
            .removeprefix("gs://" + config["bucket"] + "/") \
            .removeprefix(config["bucket"]+"/")
    else: 
        bucket_path = filepath
    
    # Download
    return bucket.blob(bucket_path) \
        .download_as_string() \
        .decode("utf-8")
    
def get_bucket(bucket: str, project_id: Union[None, str], project_name: Union[str, None] = None) -> storage.Bucket:

    if project_name is not None:
        # Get config from project name
        if project_id is not None: 
            warnings.warn("Got a 'project_name' and a 'project_id'. The 'project_id' will be ignored.")
        if bucket is not None:
            warnings.warn("Got a 'bucket' and a 'project_name'. The 'bucket' will be ignored.")
        config = _config_project(project_name)
        project_id, bucket = config["google_proj_id"], config["bucket"]
    
    # Connect to GCP and return bucket
    client = storage.Client(config["google_proj_id"])
    return client.bucket(config["bucket"])

def get_filesize(bucket: storage.Bucket, prefix: str = "") -> dict:
    """Returns the sizes in bytes of files matching a specified prefix.

    Args:
        bucket (storage.Bucket): Google Bucket containing the files to evaluate.
        prefix (str, optional): The function returns the sizes of all files matching this prefix.
            Must not contain the bucket id. Defaults to "" (all files in the bucket).

    Returns:
        dict: Dictionary with filenames as keys and sizes in bytes as values.
    """

    return {blob.name: blob.size for blob in bucket.list_blobs(prefix=prefix)}

def upload_entity(data: pd.DataFrame, name: str, project: str = "DSSC", 
    chunksize: Union[None, int] = None):

    if chunksize is None: chunksize = len(data)
    chunksize = np.minimum(chunksize, len(data))

    config = _config_project(project)
    # Rename data index
    data.index.name = f"entity:{name}_id"
    # Split data into chunks and upload
    i = 0
    while i < len(data): 
        max_i = np.minimum(i+chunksize, len(data))
        rc = fapi.upload_entities_tsv(
            config["project"], config["workspace"], 
            io.StringIO(_clean_entity_tsv(data.iloc[i:max_i].to_csv(sep='\t'))), 
            model = "flexible")
        if not rc.status_code == 200:
            warnings.warn(f"Got response code {rc.status_code} when uploading chunk {i//chunksize}.")
        i += chunksize

def get_filenames(prefix: str = "", project: str = "DSSC") -> List[str]:

    config = _config_project(project)
    client = storage.Client(config["google_proj_id"])
    bucket = client.bucket(config["bucket"])
    # Check if the bucket ID is appended to the prefix. If so, remove it
    if config["bucket"] in prefix:
        prefix = prefix.removeprefix("gs://").removeprefix(config["bucket"]+"/")
    return [
        blob.name.removeprefix(prefix+"/") 
        for blob in bucket.list_blobs(prefix=prefix)
    ]

def prepare_entity_tsv(path: str):

    with open(path) as file:
        content = file.read()
    content = content.replace("\"\"", "\"").replace("\"[", "[").replace("]\"", "]") \
        .replace("[null,null]", "[]").replace("[null]", "[]").replace("True", "true") \
        .replace("False", "false").replace("nan", "").replace("null,","").replace("null]","]")
    with open(path, "w") as file:
        file.write(content)
# %%
