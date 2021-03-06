import ast
import argparse

from cfg import Node, AssignmentNode, CFG, generate_ast
from reaching_definitions import ReachingDefinitionsAnalysis
from liveness import LivenessAnalysis

class FixedPointAnalysis():
    """Run the fix point analysis."""

    def __init__(self, cfg, analysis):
        """Fixed point analysis

        analysis must be a dataflow analysis containing a 'fixpointmethod' method that analyzes one CFG node"""
        self.analysis = analysis(cfg)
        self.cfg = cfg
    
    def constraints_changed(self):
        """Return true if any constraint has changed."""
        return any(node.old_constraint != node.new_constraint for node in self.cfg.nodes)
        
    def swap_constraints(self):
        """Set odl constraint to new constraint and set new constraint to None."""
        for node in self.cfg.nodes:
            node.old_constraint = node.new_constraint
            node.new_constraint = None
            
    def fixpoint_runner(self):
        """Runs the fixpoint algorithm."""
        self.fixpoint_iteration()
        while self.constraints_changed():
            self.swap_constraints()
            self.fixpoint_iteration()
        
    def fixpoint_iteration(self):
        """A fixpoint iteration."""
        for node in self.cfg.nodes:
            self.analysis.fixpointmethod(node)
            

def analyse(cfg_list, *, analysis_type):
    """Analyse a list of control flow graphs with a given analysis type."""
    for cfg in cfg_list:
        analysis = FixedPointAnalysis(cfg, analysis_type)
        analysis.fixpoint_runner()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('filename', help='Filename of the file that should be analysed.', type=str)
    parser.add_argument('-l', '--liveness', help='Toggle liveness analysis.', action='store_true')
    parser.add_argument('-r', '--reaching', help='Toggle reaching definitions analysis', action='store_true')

    args = parser.parse_args()

    tree = generate_ast(args.filename)
    cfg = CFG()
    cfg.create(tree)

    def run_analysis(cfg, analysis_type):
        analysis = fixed_point_analysis(cfg, analysis_type)
        analysis.fixpoint_runner()
        for cfg_node in cfg.nodes:
            print(cfg_node)
            print(cfg_node.new_constraint)

    if args.liveness:
        run_analysis(cfg, LivenessAnalysis)
    if args.reaching:
        run_analysis(cfg, ReachingDefinitionsAnalysis)

