class Analysis:
    def __init__(self, parameters):
        self.parameters = parameters

        # Imports
        from BEASTsim.modules.analysis.gene_expression_module.gene_expression_analysis import GeneExpressionAnalysis
        from BEASTsim.modules.analysis.spatial_module.spatial_analysis import SpatialAnalysis

        # Modules
        self.spatial_analysis = SpatialAnalysis(parameters)
        self.gene_expression_analysis = GeneExpressionAnalysis(parameters)

