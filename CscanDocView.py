from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from HdfDoc import HdfDoc

class CscanDocView(Parameter):
    def __init__(self, gate_docview, name, hdf_doc: HdfDoc, c_scan, **opts):
        super().__init__(name=name)
        self.hdf_doc = hdf_doc
        self.c_scan = c_scan
        self.gate_docview = gate_docview
