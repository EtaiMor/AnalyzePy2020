from pyqtgraph.dockarea import Dock
from GateDocView import GateDocView
# from Pkgs.Ascan.AscanView import AScanView
import os
import importlib

class GateView(Dock):
    def __init__(self, parent, gate_docview :GateDocView):
        super().__init__(gate_docview.name())
        self.parent = parent
        self.gate_docview = gate_docview
        self.load_gateview_pkgs()


    def load_gateview_pkgs(self):
        for pkg_dir in os.listdir('./Pkgs/GateViewPkgs/'):
            module_name = 'Pkgs.GateViewPkgs.{0}.{1}View'.format(pkg_dir, pkg_dir)
            class_name = '{0}View'.format(pkg_dir)
            module = importlib.import_module(module_name)
            klass = getattr(module, class_name)
            klass.init_instance(self, self.gate_docview)
