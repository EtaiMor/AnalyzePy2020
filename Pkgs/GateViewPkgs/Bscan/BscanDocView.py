from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
from GateDocView import GateDocView, MyGroupParameter
from Event import Event

from FileDocView import FileDocView
from MainDocView import MainDocView


# from GateDocView import GateDocView

class BscanDocView(MyGroupParameter):
    ORIENTATION_STR = 'Orientation'
    HORIZONTAL_TXT = 'Horizontal'
    VERTICAL_TXT = 'Vertical'
    ORIENTATION_LIST = (HORIZONTAL_TXT, VERTICAL_TXT)

    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, b_scan, orientation, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.b_scan = b_scan
        self.orientation = orientation
        self.gate_docview: GateDocView = gate_docview
        self.file_docview: FileDocView = self.gate_docview.parent()
        self.main_docview: MainDocView = self.file_docview.parent()


        self.gate_docview.ij_change_event += self.on_update_ij_pos
        self.gate_docview.t_range_event += self.on_update_time_range
        self.gate_docview.fwf_changed_event += self.on_update_fwf
        self.bscan_changed_event = Event()

        self._mouse_row = 0
        self._mouse_col = 0

    def set_orientation(self, orientation):
        if (self.orientation != orientation):
            self.orientation = orientation
            self.set_bscan()

    def set_bscan(self):
        dn_0, dn_1 = self.gate_docview.get_dn_min_max()
        fwf_arr = self.gate_docview.get_fwf_arr()

        if (self.orientation == BscanDocView.HORIZONTAL_TXT):
            row = self.gate_docview.get_ipos_param().value()
            self.b_scan = self.hdf_doc.get_b_scan(row, None, dn0=dn_0, dn1=dn_1, fwf_arr=fwf_arr).T
        else:
            col = self.gate_docview.get_jpos_param().value()
            self.b_scan = self.hdf_doc.get_b_scan(None, col, dn0=dn_0, dn1=dn_1, fwf_arr=fwf_arr)

        self.bscan_changed_event(self.b_scan)

    def AddChildWithSlot(self, dict, slot):
        child = self.addChild(dict)
        child.sigValueChanged.connect(slot)

    def on_update_ij_pos(self, i_indx, j_indx):
        self.set_bscan()

    def on_update_time_range(self):
        self.set_bscan()

    def on_update_fwf(self):
        self.set_bscan()

    def set_mouse_ij_pos(self, mouse_row, mouse_col):
        self._mouse_row = mouse_row
        self._mouse_col = mouse_col

        if self.orientation == BscanDocView.HORIZONTAL_TXT:
            time_indx = mouse_row
            j_index = mouse_col
            i_index = self.gate_docview.get_ipos_param().value()

        else:
            time_indx = mouse_col
            i_index = mouse_row
            j_index = self.gate_docview.get_jpos_param().value()

        num_wave, num_row, num_col, wave_len = self.hdf_doc.get_data_dim()
        pos_str = ''
        if (0 <= i_index < num_row) and (0 <= j_index < num_col):
            pos = self.hdf_doc.get_pos(i_index, j_index)
            if 0 <= time_indx < wave_len:
                t_pos = self.hdf_doc.get_time(time_indx)
                pos_str = '(x = %0.1f [mm], y = %0.1f [mm], time = %0.1f = [micro-sec]' % (pos['x'], pos['y'], t_pos)
        self.main_docview.set_status(pos_str)
