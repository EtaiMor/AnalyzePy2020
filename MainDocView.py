from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree import types as pTypes

from HdfDoc import HdfDoc
from FileDocView import FileDocView

class MainDocView(pTypes.GroupParameter):
    def __init__(self):
        super().__init__(name='MainDocView')
        print('init')

    def find_file_docview(self, file_name):
        for file_docview in self.childs:
            if (file_docview.name == file_name):
                return file_docview

        return None

    def open_file(self, file_name):
        file_docview = self.find_file_docview(file_name)
        if (file_docview is not None):
            return (file_docview, False)
        else:
            hdf_doc = HdfDoc(file_name)
            file_docview = FileDocView(file_name, hdf_doc)
            file_docview.setParent(self)
            self.addChild(file_docview)

            return (file_docview, True)
