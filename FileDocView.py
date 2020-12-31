from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes
from HdfDoc import HdfDoc
from GateDocView import GateDocView

class FileDocView(pTypes.GroupParameter):
    def __init__(self, file_name, hdf_doc : HdfDoc, **opts):
        super().__init__(name=file_name)
        self.hdf_doc = hdf_doc
        print('init')

    def open_gate(self):
        num_gates = len(self.childs)
        gate_docview = GateDocView('Data View - {0}'.format(num_gates), self.hdf_doc)
        gate_docview.setParent(self)
        self.addChild(gate_docview)
        return gate_docview
