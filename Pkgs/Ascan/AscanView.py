import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
from Pkgs.Ascan.AscanDocView import AscanDocView
from GateDocView import GateDocView
from MainView import MainView
import numpy as np


class AscanView(Dock):
    @staticmethod
    def init_instance(parent_view, gate_docview: GateDocView):
        i_pos = int(gate_docview.getValues()[GateDocView.I_POS_STR][0])
        j_pos = int(gate_docview.getValues()[GateDocView.J_POS_STR][0])
        a_scan = gate_docview.hdf_doc.get_a_scan(i_pos, j_pos)
        ascan_docview = AscanDocView(gate_docview, 'A-Scan', gate_docview.hdf_doc, a_scan)
        view = AscanView(parent_view, ascan_docview)
        return view

    def __init__(self, parent_view, ascan_docview):
        super().__init__(ascan_docview.name(), closable=True)
        self.ascan_docview = ascan_docview
        self.gate_docview: GateDocView = ascan_docview.gate_docview
        gate_view = parent_view
        file_view = gate_view.parent
        main_view:MainView = file_view.parent

        self.signal_view = pg.PlotWidget(self)
        self.signal_view.plot(ascan_docview.a_scan)
        self.addWidget(self.signal_view)
        ascan_docview.attach_ascanUpdatedEvent(self.ascanChangedEvent)
        t_min = self.gate_docview.get_tmin_param().value()
        t_max = self.gate_docview.get_tmax_param().value()
        self.time_region = pg.LinearRegionItem(values=[t_min, t_max])
        self.signal_view.addItem(self.time_region)
        self.time_region.sigRegionChangeFinished.connect(self.time_region_changed_finished)
        main_view.dock_area.addDock(self)

    def ascanChangedEvent(self, ascan):
        self.signal_view.plotItem.dataItems[0].setData(ascan)

    def time_region_changed_finished(self, event):
        t_min_val, t_max_val = event.getRegion()
        self.gate_docview.get_tmin_param().setValue(t_min_val)
        self.gate_docview.get_tmax_param().setValue(t_max_val)
