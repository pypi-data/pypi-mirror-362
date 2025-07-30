
class Benchmarking:
    def __init__(self, parameters):
        self.parameters = parameters

        # Imports
        from BEASTsim.modules.benchmarking.simulation.simulation_benchmark import SimulationBenchmark

        # Modules
        self.SimulationBenchmark = SimulationBenchmark(self.parameters)
