import os
import time
os.environ['ETS_TOOLKIT'] = 'qt4'

import numpy as np
import sip
sip.setapi('QString', 2)

from PyQt5 import QtGui
from pyqtgraph.dockarea import Dock
from Pkgs.GateViewPkgs.Vscan.VscanDocView import VscanDocView
from GateDocView import GateDocView
from traits.api import HasTraits, Instance, on_trait_change
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene
from traitsui.api import View, Item
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.modules.image_plane_widget import ImagePlaneWidget
from mayavi.sources.api import ArraySource
from mayavi.modules.api import IsoSurface, ImagePlaneWidget

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    source = Instance(ArraySource, ())
    x_plane = Instance(ImagePlaneWidget, ())
    y_plane = Instance(ImagePlaneWidget, ())
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=25, width=300, show_label=False),
                resizable=True)  # We need this to resize with the parent widget

    @on_trait_change('scene.activated')
    def update_plot(self):
        self.scene.engine.add_source(self.source)
        self.source.add_module(self.x_plane)
        self.x_plane.name = 'x cut'
        self.x_plane.ipw.plane_orientation = 'x_axes'
        self.source.add_module(self.y_plane)
        self.y_plane.name = 'y cut'
        self.y_plane.ipw.plane_orientation = 'y_axes'

    def update_scalar_data(self, scalar_data):
        self.source.scalar_data = scalar_data

class MayaviQWidget(QtGui.QWidget):
    def __init__(self, data, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization(source = ArraySource(scalar_data = data))
        self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        time.sleep(1)
        self.ui.setParent(self)
        layout.addWidget(self.ui)



class VscanView(Dock):
    @staticmethod
    def init_instance(gate_docview: GateDocView):
        fwf_arr = gate_docview.get_fwf_arr()
        dn0, dn1 = gate_docview.get_dn_min_max()
        v_scan = gate_docview.hdf_doc.get_volume_ascans(ascan_mat=None, dn0=dn0, dn1 = dn1, fwf_arr=fwf_arr)
        vscan_docview = VscanDocView(gate_docview, 'V-Scan', gate_docview.hdf_doc, v_scan)
        view = VscanView(vscan_docview)
        return view

    def __init__(self, vscan_docview: VscanDocView):
        super().__init__(vscan_docview.name(), closable=True, autoOrientation = False)
        self.vscan_docview = vscan_docview
        self.gate_docview: GateDocView = vscan_docview.gate_docview
        container = QtGui.QWidget()
        self.maya_widget = MayaviQWidget(self.vscan_docview.v_scan, container)
        self.addWidget(self.maya_widget)
        container.show()
        vscan_docview.vscan_changed_event += self.on_vscan_changed

    def on_vscan_changed(self, v_scan: np.ndarray):
        print('on_vscan_changed')
        # self.maya_widget.visualization.source.scalar_data = v_scan
        self.maya_widget.visualization.update_scalar_data(v_scan)



