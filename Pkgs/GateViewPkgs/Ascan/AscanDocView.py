import numpy as np
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
from GateDocView import GateDocView
from Event import Event

class AscanDocView(pTypes.GroupParameter):
    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, a_scan, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.a_scan = a_scan
        self.signal_ascanUpdatedEvent = None
        self.gate_docview: GateDocView = gate_docview
        self.gate_docview.ij_change_event += self.on_update_ij_pos
        self.ascan_changed_event = Event()

        self.add_to_parent()
        self.fwf_roi = self.get_fwfroi_default_location()

    def add_to_parent(self):
        self.gate_docview.addChild(self)

    def set_ascan(self, a_scan):
        self.a_scan = a_scan
        self.ascan_changed_event(self.a_scan)

    def on_update_ij_pos(self, i_indx, j_indx):
        a_scan = self.hdf_doc.get_a_scan(i_indx, j_indx)
        self.set_ascan(a_scan)

    def get_fwfroi_default_location(self):
        signal_len = len(self.a_scan)
        left = signal_len / 10
        top = 0.5 * np.max(self.a_scan)
        bottom = 0.5 * np.min(self.a_scan)
        width = left
        height = top - bottom
        return {'left': left, 'bottom': bottom, 'width': width, 'height': height}

    def set_fwf_roi(self, left, bottom, width, height):
        self.fwf_roi = {'left': left, 'bottom': bottom, 'width': width, 'height': height}
        self.gate_docview.set_fwf_arr(left, bottom, width, height)

    def get_fwf_roi(self):
        return self.fwf_roi

    def save_ascan_to_txt_file(self, file_name):
        t_min = self.gate_docview.get_tmin_param().value()
        t_max = self.gate_docview.get_tmax_param().value()
        np.savetxt(file_name, self.a_scan[t_min:t_max])
