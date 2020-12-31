import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
from AscanDocView import AscanDocView
from GateDocView import GateDocView
import numpy as np

class AScanView(Dock):
    def __init__(self, parent, ascan_docview: AscanDocView):
        super().__init__(ascan_docview.name(), closable=True)
        self.ascan_docview = ascan_docview
        self.gate_docview: GateDocView = ascan_docview.gate_docview
        gate_view = parent
        file_view = gate_view.parent
        main_view = file_view.parent

        self.signal_view = pg.PlotWidget(self)
        self.signal_view.plot(ascan_docview.a_scan)
        self.addWidget(self.signal_view)
        ascan_docview.attach_ascanUpdatedEvent(self.ascanChangedEvent)
        t_min = self.gate_docview.get_tmin_param().value()
        t_max = self.gate_docview.get_tmax_param().value()
        self.time_region = pg.LinearRegionItem(values=[t_min, t_max])
        self.signal_view.addItem(self.time_region)

        self.time_region.sigRegionChangeFinished.connect(self.time_region_changed_finished)

    def ascanChangedEvent(self, ascan):
        self.signal_view.plotItem.dataItems[0].setData(ascan)

    def time_region_changed_finished(self, event):
        t_min_val, t_max_val = event.getRegion()
        self.gate_docview.get_tmin_param().setValue(t_min_val)
        self.gate_docview.get_tmax_param().setValue(t_max_val)
