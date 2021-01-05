import numpy as np
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
from Event import Event


class GateDocView(pTypes.GroupParameter):
    I_POS_STR = 'Row'
    J_POS_STR = 'Col'
    T_MIN_STR = 'Low Cursor'
    T_MAX_STR = 'High Cursor'


    def __init__(self, name, hdf_doc : HdfDoc, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc

        (num_wave, num_row, num_col, wave_len) = hdf_doc.get_data_dim()
        self.AddChildWithSlot({'name': GateDocView.I_POS_STR, 'type': 'int', 'value': np.round(num_row/2), 'siPrefix': True,
                            'suffix': 'pix', 'readonly': False}, self.set_row_value)
        self.AddChildWithSlot({'name': GateDocView.J_POS_STR, 'type': 'int', 'value': np.round(num_col/2), 'siPrefix': True,
                            'suffix': 'pix', 'readonly': False}, self.set_col_value)
        self.AddChildWithSlot({'name': GateDocView.T_MIN_STR, 'type': 'int', 'value': 0, 'siPrefix': True,
                            'suffix': 'sample', 'readonly': False}, self.set_tmin_value)
        self.AddChildWithSlot({'name': GateDocView.T_MAX_STR, 'type': 'int', 'value': wave_len - 1, 'siPrefix': True,
                            'suffix': 'sample', 'readonly': False}, self.set_tmax_value)

        self.ij_change_event = Event()
        self.t_range_event = Event()

    def find_child(self, child_name):
        ret_child = None
        for child in self.childs:
            if (child.name() == child_name):
                ret_child = child
                break

        return ret_child

    def get_ipos_param(self):
        return self.find_child(GateDocView.I_POS_STR)

    def get_jpos_param(self):
        return self.find_child(GateDocView.J_POS_STR)

    def get_tmin_param(self):
        return self.find_child(GateDocView.T_MIN_STR)

    def get_tmax_param(self):
        return self.find_child(GateDocView.T_MAX_STR)

    def AddChildWithSlot(self, dict, slot):
        child = self.addChild(dict)
        child.sigValueChanged.connect(slot)

    def update_ij_pos(self, i_indx = None, j_indx=None):
        ipos_param: pTypes.Parameter = self.get_ipos_param()
        if i_indx is not None:
            ipos_param.setValue(i_indx)

        jpos_param: pTypes.Parameter = self.get_jpos_param()
        if j_indx is not None:
            jpos_param.setValue(j_indx)

        self.ij_change_event(ipos_param.value(), jpos_param.value())

    def set_row_value(self, changeDesc, row):
        jpos_param: pTypes.Parameter = self.get_jpos_param()
        col = jpos_param.value()
        self.ij_change_event(row, col)

    def set_col_value(self, changeDesc, col):
        ipos_param: pTypes.Parameter = self.get_ipos_param()
        row = ipos_param.value()
        self.ij_change_event(row, col)

    def set_tmin_value(self, changeDesc, tmin):
        tmax_param: pTypes.Parameter = self.get_tmax_param()
        tmax = tmax_param.value()
        self.t_range_event(tmin, tmax)

    def set_tmax_value(self, changeDesc, tmax):
        tmin_param: pTypes.Parameter = self.get_tmin_param()
        tmin = tmin_param.value()
        self.t_range_event(tmin, tmax)
