from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

class BscanDocView(Parameter):
    def __init__(self, **opts):
        super().__init__(opts)
        print('init')

