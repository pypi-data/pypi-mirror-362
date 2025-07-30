import peyes._utils.constants as cnst
from peyes._DataModels.DatasetLoader import (
    Lund2013DatasetLoader, IRFDatasetLoader, HFCDatasetLoader, GazeComDatasetLoader
)


def get_metadata(dataset_name: str, show: bool = True) -> dict:
    """ Returns the metadata for the specified dataset, and optionally prints the metadata to the console. """
    dataset_name_lower = dataset_name.lower().strip()
    if dataset_name_lower == "lund2013":
        loader_class = Lund2013DatasetLoader
    elif dataset_name_lower == "irf":
        loader_class = IRFDatasetLoader
    elif dataset_name_lower == "hfc":
        loader_class = HFCDatasetLoader
    elif dataset_name_lower == "gazecom":
        loader_class = GazeComDatasetLoader
    else:
        raise NotImplementedError(f"Unknown dataset: {dataset_name}")
    try:
        name = loader_class.name()
    except AttributeError:
        name = ""
    try:
        url = loader_class.url()
    except AttributeError:
        url = ""
    try:
        articles = loader_class.articles()
    except AttributeError:
        articles = []
    try:
        license = loader_class.license()
    except AttributeError:
        license = ""
    metadata = {cnst.NAME_STR: name, cnst.URL_STR: url, cnst.ARTICLES_STR: articles, cnst.LICENSE_STR: license}
    if show:
        print(f"Dataset {cnst.NAME_STR.capitalize()}:\t{name}")
        print(f"{cnst.URL_STR.upper()}:\t{url}")
        print(f"{cnst.LICENSE_STR.capitalize()}:\t{license}")
        print(f"{cnst.ARTICLES_STR.capitalize()}:")
        for article in articles:
            print(f"\t{article}")
    return metadata

