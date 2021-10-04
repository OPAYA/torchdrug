import os

from torchdrug import data, utils
from torchdrug.core import Registry as R
from torchdrug.utils import doc


@R.register("datasets.PCQM4M")
@doc.copy_args(data.MoleculeDataset.load_csv, ignore=("smiles_field", "target_fields"))
class PCQM4M(data.MoleculeDataset):
    """
    Log-scale water solubility of molecules.

    Statistics:
        - #Molecule: 1,128
        - #Regression task: 1

    Parameters:
        path (str): path to store the dataset
        verbose (int, optional): output verbose level
        **kwargs
    """

    url = "https://dgl-data.s3-accelerate.amazonaws.com/dataset/OGB-LSC/pcqm4m_kddcup2021.zip"
   
    target_fields = ["homolumogap"]

    def __init__(self, path, verbose=1, **kwargs):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
        
        zip_file = utils.download(self.url, path)
        folder_name = utils.extract(zip_file)
        file_name = utils.extract(os.path.join(folder_name, 'pcqm4m_kddcup2021/raw/data.csv.gz'))

        self.load_csv(file_name, smiles_field="smiles", target_fields=self.target_fields,
                      verbose=verbose, **kwargs)