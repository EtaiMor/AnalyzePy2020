import numpy as np
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
from Event import Event


class MyGroupParameter(pTypes.GroupParameter):
    def __init__(self, name):
        super().__init__(name=name)

    def find_child(self, child_name):
        ret_child = None
        for child in self.childs:
            if (child.name() == child_name):
                ret_child = child
                break

        return ret_child

    def get_value_by_name(self, name):
        return self.find_child(name).value()



class GateDocView(MyGroupParameter):
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

        self.fwf_arr = None
        self.ij_change_event = Event()
        self.t_range_event = Event()
        self.fwf_changed_event = Event()

    def set_fwf_arr(self, fwf_left, fwf_bottom, fwf_width, fwf_height):
        cur_i = self.get_ipos_param().value()
        cur_j = self.get_jpos_param().value()
        self.fwf_arr = self.hdf_doc.get_fwf(fwf_left, fwf_bottom, fwf_width, fwf_height, cur_i, cur_j)
        self.fwf_changed_event()

    def get_fwf_arr(self):
        return self.fwf_arr

    def get_cur_fwf_pos(self):
        if (self.fwf_arr is not None):
            cur_i = self.get_ipos_param().value()
            cur_j = self.get_jpos_param().value()
            index = self.hdf_doc.wave_indx_mat[cur_i, cur_j]
            return self.fwf_arr[index]
        else:
            return 0

    def get_dn_min_max(self):
        (_, _, _, wave_len) = self.hdf_doc.get_data_dim()

        t_min = self.get_tmin_param().value()
        t_max = self.get_tmax_param().value()
        cur_fwf_pos = self.get_cur_fwf_pos()

        dn0 = int(max(t_min - cur_fwf_pos, 0))
        dn1 = int(min(t_max - cur_fwf_pos, wave_len-1))

        return dn0, dn1

    def get_ipos_param(self):
        ret: pTypes.Parameter = self.find_child(GateDocView.I_POS_STR)
        return ret

    def get_jpos_param(self):
        ret: pTypes.Parameter = self.find_child(GateDocView.J_POS_STR)
        return ret

    def get_tmin_param(self):
        ret: pTypes.Parameter = self.find_child(GateDocView.T_MIN_STR)
        return ret

    def get_tmax_param(self):
        ret: pTypes.Parameter = self.find_child(GateDocView.T_MAX_STR)
        return ret

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
        self.t_range_event()

    def set_tmax_value(self, changeDesc, tmax):
        tmin_param: pTypes.Parameter = self.get_tmin_param()
        tmin = tmin_param.value()
        self.t_range_event()
