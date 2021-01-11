import os
import PyQt5.QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFileDialog

import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
from Pkgs.GateViewPkgs.Ascan.AscanDocView import AscanDocView
from GateDocView import GateDocView
from MainView import MainView


class AscanView(Dock):
    @staticmethod
    def init_instance(gate_docview: GateDocView):
        i_pos = int(gate_docview.getValues()[GateDocView.I_POS_STR][0])
        j_pos = int(gate_docview.getValues()[GateDocView.J_POS_STR][0])
        a_scan = gate_docview.hdf_doc.get_a_scan(i_pos, j_pos)
        ascan_docview = AscanDocView(gate_docview, 'A-Scan', gate_docview.hdf_doc, a_scan)
        view = AscanView(ascan_docview)
        return view

    def __init__(self, ascan_docview: AscanDocView):
        super().__init__(ascan_docview.name(), closable=True)
        self.ascan_docview = ascan_docview
        self.gate_docview: GateDocView = ascan_docview.gate_docview

        self.signal_view = pg.PlotWidget(self)
        self.signal_view.plot(ascan_docview.a_scan)
        self.addWidget(self.signal_view)

        t_min = self.gate_docview.get_tmin_param().value()
        t_max = self.gate_docview.get_tmax_param().value()
        self.time_region = pg.LinearRegionItem(values=[t_min, t_max])
        self.signal_view.addItem(self.time_region)
        self.time_region.sigRegionChangeFinished.connect(self.time_region_changed_finished)

        fwf_roi = self.ascan_docview.get_fwf_roi()
        self.fwf_roi = pg.RectROI([fwf_roi['left'], fwf_roi['bottom']],
                                  [fwf_roi['width'], fwf_roi['height']], True)
        self.fwf_roi.sigRegionChangeFinished.connect(self.fwf_region_changed_finished)
        self.signal_view.addItem(self.fwf_roi)

        export_action = PyQt5.QtGui.QAction('Export Signal to text')
        self.signal_view.sceneObj.contextMenu.append(export_action)
        export_action.triggered.connect(self.export_to_text)


        ascan_docview.ascan_changed_event += self.set_ascan


    def set_ascan(self, ascan):
        self.signal_view.plotItem.dataItems[0].setData(ascan)

    def time_region_changed_finished(self, event):
        t_min_val, t_max_val = event.getRegion()
        self.gate_docview.get_tmin_param().setValue(t_min_val)
        self.gate_docview.get_tmax_param().setValue(t_max_val)

    def fwf_region_changed_finished(self, event):
        left, bottom = self.fwf_roi.pos()
        width, height = self.fwf_roi.size()
        self.ascan_docview.set_fwf_roi(left, bottom, width, height)

    def export_to_text(self):
        my_settings = QSettings()
        last_open_file = my_settings.value('LAST_OPEN_FILE')
        last_open_dir = os.path.dirname(os.path.abspath(last_open_file))
        file_name, _ = QFileDialog.getSaveFileName(self, "Save to Text File", last_open_dir, "(*.sig)")
        my_settings.setValue('LAST_OPEN_FILE', file_name)
        self.ascan_docview.save_ascan_to_txt_file(file_name)
