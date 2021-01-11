from pyqtgraph.dockarea import Dock
from GateDocView import GateDocView
# from Pkgs.Ascan.AscanView import AScanView
import os
import importlib
# from MainView import MainView


class GateView(Dock):
    def __init__(self, file_view, gate_docview :GateDocView):
        super().__init__(gate_docview.name())
        self.gate_docview = gate_docview
        file_view = file_view
        main_view = file_view.parent
        self.load_gateview_pkgs(main_view)


    def load_gateview_pkgs(self, main_view):
        num_pkgs = 0
        prv_dock = None
        for pkg_dir in os.listdir('./Pkgs/GateViewPkgs/'):
            module_name = 'Pkgs.GateViewPkgs.{0}.{1}View'.format(pkg_dir, pkg_dir)
            class_name = '{0}View'.format(pkg_dir)
            module = importlib.import_module(module_name)
            klass = getattr(module, class_name)
            dock_view = klass.init_instance(self.gate_docview)
            if prv_dock is not None:
                if (num_pkgs % 2 ==0):
                    main_view.dock_area.addDock(dock_view, position='right', relativeTo=prv_dock)
                else:
                    main_view.dock_area.addDock(dock_view, position='bottom', relativeTo=prv_dock)
            else:
                main_view.dock_area.addDock(dock_view, position='right')
            prv_dock = dock_view
            num_pkgs += 1


