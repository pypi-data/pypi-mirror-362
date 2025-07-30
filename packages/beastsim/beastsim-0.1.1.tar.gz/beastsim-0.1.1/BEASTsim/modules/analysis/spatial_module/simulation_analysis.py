from typing import List, Union
from BEASTsim.beast_data import BEAST_Data

class SimulationAnalysis:
    def __init__(self, parameters) -> None:
        self.parameters = parameters

        # imports
        from BEASTsim.modules.analysis.spatial_module.simulation.plotting_simulation import PlottingSimulation

        # modules
        self.plotting_simulation = PlottingSimulation(self.parameters)
