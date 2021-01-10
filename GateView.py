from pyqtgraph.dockarea import Dock
from GateDocView import GateDocView
# from Pkgs.Ascan.AscanView import AScanView
import os
import importlib

class GateView(Dock):
    def __init__(self, file_view, gate_docview :GateDocView):
        super().__init__(gate_docview.name())
        self.gate_docview = gate_docview
        file_view = file_view
        main_view = file_view.parent
        self.load_gateview_pkgs(main_view)


    def load_gateview_pkgs(self, parent_view):
        for pkg_dir in os.listdir('./Pkgs/GateViewPkgs/'):
            module_name = 'Pkgs.GateViewPkgs.{0}.{1}View'.format(pkg_dir, pkg_dir)
            class_name = '{0}View'.format(pkg_dir)
            module = importlib.import_module(module_name)
            klass = getattr(module, class_name)
            klass.init_instance(parent_view, self.gate_docview)
