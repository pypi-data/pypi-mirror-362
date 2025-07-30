class SpatialAnalysis:
    def __init__(self, parameters) -> None:
        self.parameters = parameters

        # Imports
        from BEASTsim.modules.analysis.spatial_module.simulation_analysis import SimulationAnalysis
        from BEASTsim.modules.analysis.spatial_module.cell_mapping.cell_mapping_analysis import CellMappingAnalysis

        # Modules
        self.simulation_analysis = SimulationAnalysis(parameters)
        self.cell_mapping_analysis = CellMappingAnalysis(parameters)

