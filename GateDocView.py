import numpy as np
from pyqtgraph.parametertree import types as pTypes

from HdfDoc import HdfDoc
from Pkgs.GateViewPkgs.Ascan.AscanDocView import AscanDocView
from Pkgs.GateViewPkgs.Cscan.CscanDocView import CscanDocView


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
                            'suffix': 'pix', 'readonly': False}, self.row_value_changed)
        self.AddChildWithSlot({'name': GateDocView.J_POS_STR, 'type': 'int', 'value': np.round(num_col/2), 'siPrefix': True,
                            'suffix': 'pix', 'readonly': False}, self.col_value_changed)
        self.AddChildWithSlot({'name': GateDocView.T_MIN_STR, 'type': 'int', 'value': 0, 'siPrefix': True,
                            'suffix': 'sample', 'readonly': False}, self.tmin_value_changed)
        self.AddChildWithSlot({'name': GateDocView.T_MAX_STR, 'type': 'int', 'value': wave_len - 1, 'siPrefix': True,
                            'suffix': 'sample', 'readonly': False}, self.tmax_value_changed)

        self.ij_change_event_slots = list()
        self.t_range_event_slots = list()


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


    def update_ij_pos(self, i_indx, j_indx):
        ipos_param: pTypes.Parameter = self.get_ipos_param()
        ipos_param.setValue(i_indx)
        jpos_param: pTypes.Parameter = self.get_jpos_param()
        jpos_param.setValue(j_indx)
        for fun in self.ij_change_event_slots:
            fun(i_indx, j_indx)



    def row_value_changed(self, changeDesc, row):
        jpos_param: pTypes.Parameter = self.get_jpos_param()
        col = jpos_param.value()
        for fun in self.ij_change_event_slots:
            fun(row, col)

    def col_value_changed(self, changeDesc, col):
        jpos_param: pTypes.Parameter = self.get_ipos_param()
        row = jpos_param.value()
        for fun in self.ij_change_event_slots:
            fun(row, col)

    def update_time_range(self, time_range):
        tmin_param: pTypes.Parameter = self.get_tmin_param()
        tmin_param.setValue(time_range[0])
        tmax_param: pTypes.Parameter = self.get_tmax_param()
        tmax_param.setValue(time_range[1])

        for fun in self.t_range_event_slots:
            fun(time_range)

    def tmin_value_changed(self, changeDesc, tmin):
        tmax_param: pTypes.Parameter = self.get_tmax_param()
        tmax = tmax_param.value()
        for fun in self.t_range_event_slots:
            fun((tmin, tmax))

    def tmax_value_changed(self, changeDesc, tmax):
        tmin_param: pTypes.Parameter = self.get_tmin_param()
        tmin = tmin_param.value()
        for fun in self.t_range_event_slots:
            fun((tmin, tmax))
