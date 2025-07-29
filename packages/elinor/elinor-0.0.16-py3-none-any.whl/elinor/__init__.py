from .ai import summary
from .cv import pil_to_b64, b64_to_pil
from .data import count_files_by_end
from .dataset import BaseDatasetPhoenix2014T
from .loanlib import fast_loadenv_then_append_path
from .misc import o_d

def whoami():
    
    """
    Who am I?
    """
    return "I am Elinor, a Python package for data processing and analysis."