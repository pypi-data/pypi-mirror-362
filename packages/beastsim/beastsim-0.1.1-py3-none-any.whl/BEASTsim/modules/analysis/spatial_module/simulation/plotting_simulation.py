
class PlottingSimulation:
    def __init__(self, parameters):
        self.parameters = parameters

        # imports
        from BEASTsim.modules.analysis.spatial_module.simulation.plotting.cell_type_plotting import CellTypePlotting
        from BEASTsim.modules.analysis.spatial_module.simulation.plotting.neighborhood_plotting import NeighborhoodPlotting
        from BEASTsim.modules.analysis.spatial_module.simulation.plotting.similarity_plotting import SimilarityPlotting
        from BEASTsim.modules.analysis.spatial_module.simulation.plotting.SVG_plotting import SVGPlotting

        # modules
        self.cell_type_plotting = CellTypePlotting(self.parameters)
        self.neighborhood_plotting = NeighborhoodPlotting(self.parameters)
        self.similarity_plotting = SimilarityPlotting(self.parameters)
        self.SVG_plotting = SVGPlotting(self.parameters)