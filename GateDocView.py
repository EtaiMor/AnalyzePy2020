import numpy as np
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes

from HdfDoc import HdfDoc
from Pkgs.Ascan.AscanDocView import AscanDocView
from BscanDocView import BscanDocView
from CscanDocView import CscanDocView


class GateDocView(pTypes.GroupParameter):
    I_POS_STR = 'Row'
    J_POS_STR = 'Col'
    T_MIN_STR = 'Low Cursor'
    T_MAX_STR = 'High Cursor'


    def __init__(self, name, hdf_doc : HdfDoc, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.ascan_docview : AscanDocView = None
        self.cscan_docview: CscanDocView = None
        (num_wave, num_row, num_col, wave_len) = hdf_doc.get_data_dim()
        # self.sigTreeStateChanged.connect(self.param_changed)
        # self.sigValueChanged.connect(self.value_changed)
        self.AddChildWithSlot({'name': GateDocView.I_POS_STR, 'type': 'int', 'value': np.round(num_row/2), 'siPrefix': True,
                            'suffix': 'pix', 'readonly': False}, self.row_value_changed)
        self.AddChildWithSlot({'name': GateDocView.J_POS_STR, 'type': 'int', 'value': np.round(num_col/2), 'siPrefix': True,
                            'suffix': 'pix', 'readonly': False}, self.col_value_changed)
        self.AddChildWithSlot({'name': GateDocView.T_MIN_STR, 'type': 'int', 'value': 0, 'siPrefix': True,
                            'suffix': 'sample', 'readonly': False}, self.tmin_value_changed)
        self.AddChildWithSlot({'name': GateDocView.T_MAX_STR, 'type': 'int', 'value': wave_len - 1, 'siPrefix': True,
                            'suffix': 'sample', 'readonly': False}, self.tmax_value_changed)

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

    def open_ascan(self):
        i_pos = int(self.getValues()[GateDocView.I_POS_STR][0])
        j_pos = int(self.getValues()[GateDocView.J_POS_STR][0])
        a_scan = self.hdf_doc.get_a_scan(i_pos, j_pos)
        self.ascan_docview = AscanDocView(self, 'A-Scan', self.hdf_doc, a_scan)
        return self.ascan_docview

    def open_cscan(self):
        t_min = int(self.getValues()[GateDocView.T_MIN_STR][0])
        t_max = int(self.getValues()[GateDocView.T_MAX_STR][0])
        c_scan = self.hdf_doc.get_c_scan(dn0=t_min, dn1=t_max)
        self.cscan_docview = CscanDocView(self, 'C-Scan', self.hdf_doc, c_scan)
        return self.cscan_docview

    def update_ij_pos(self, i_indx, j_indx):
        ipos_param: pTypes.Parameter = self.get_ipos_param()
        ipos_param.setValue(i_indx, self.row_value_changed)
        jpos_param: pTypes.Parameter = self.get_jpos_param()
        jpos_param.setValue(j_indx)
        # self.ascan_docview.update_ascan(i_indx, j_indx)

    def row_value_changed(self, changeDesc, row):
        print(changeDesc)
        print(row)
        jpos_param: pTypes.Parameter = self.get_jpos_param()
        self.ascan_docview.update_ascan(row, jpos_param.value())

    def col_value_changed(self, changeDesc, col):
        print(changeDesc)
        print(col)
        ipos_param: pTypes.Parameter = self.get_ipos_param()
        self.ascan_docview.update_ascan(ipos_param.value(), col)

    def tmin_value_changed(self, changeDesc, data):
        print(changeDesc)
        print(data)

    def tmax_value_changed(self, changeDesc, data):
        print(changeDesc)
        print(data)

