from tqdm import tqdm
from BEASTsim.beast_data import BEAST_Data
from typing import Union, List

class CellMappingAnalysis():
    def __init__(self, parameters):
        self.parameters = parameters

        # Imports
        from BEASTsim.modules.analysis.spatial_module.cell_mapping.cell2location import Cell2Location

        # Modules
        self.cell2location = Cell2Location(self.parameters)
