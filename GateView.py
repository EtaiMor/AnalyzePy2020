from pyqtgraph.dockarea import Dock
from GateDocView import GateDocView
# from Pkgs.Ascan.AscanView import AScanView
import os
import importlib

class GateView(Dock):
    def __init__(self, parent, gate_docview :GateDocView):
        super().__init__(gate_docview.name())
        self.parent = parent
        self.gate_docview = gate_docview
        self.ascan_view = None
        self.cscan_view = None
        self.child_views = list()

        self.load_gateview_pkgs()
        # self.open_ascanview()
        # self.open_cscanview()
        # self.cscan_dock = None
        # self.bscan_dock = None
        # self.ascan_dock = None
        # self.open_cscan()
        # self.open_bscan()
        # self.open_ascanview()

        # self.data_view.sigTreeStateChanged.connect(self.data_view_changed)
    def load_gateview_pkgs(self):
        for pkg_dir in os.listdir('./Pkgs/GateViewPkgs/'):
            module_name = 'Pkgs.GateViewPkgs.{0}.{1}View'.format(pkg_dir, pkg_dir)
            class_name = '{0}View'.format(pkg_dir)
            module = importlib.import_module(module_name)
            klass = getattr(module, class_name)
            self.child_views.append(klass.init_instance(self, self.gate_docview))



    # def export_to_text(self):
    #     my_settings = QSettings()
    #     last_open_file = my_settings.value('LAST_OPEN_FILE')
    #     last_open_dir = os.path.dirname(os.path.abspath(last_open_file))
    #     file_name, _ = QFileDialog.getSaveFileName(self.parent, "Save to Text File", last_open_dir, "(*.sig)")
    #     my_settings.setValue('LAST_OPEN_FILE', file_name)
    #
    #     t_min = int(DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.T_MIN_STR).value())
    #     t_max = int(DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.T_MAX_STR).value())
    #     a_scan = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.ASCAN_STR)
    #     signal = a_scan.opts['signal']
    #     np.savetxt(file_name, signal[t_min:t_max])
    #
    # def data_view_changed(self, param, changes):
    #     print("data_view_changed:")
    #     for param, change, data in changes:
    #         path = self.data_view.childPath(param)
    #         if path is not None:
    #             childName = '.'.join(path)
    #         else:
    #             childName = param.name()
    #         if (childName == DatasetArr.I_POS_STR) or (childName == DatasetArr.J_POS_STR):
    #             a_scan = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.ASCAN_STR)
    #             signal_view = self.ascan_dock.widgets[0]
    #             signal_view.plotItem.dataItems[0].setData(a_scan.opts['signal'])
    #             if (childName == DatasetArr.I_POS_STR):
    #                 image_view = self.bscan_dock.widgets[0]
    #                 image_view.setCurrentIndex(int(param.value()))
    #
    #             fwf = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.FWF_STR)
    #             left = fwf.opts['fwf_left']
    #             bottom = fwf.opts['fwf_bottom']
    #             self.fwf_roi.setPos((left, bottom))
    #
    #
    #
    #         if (childName == DatasetArr.T_MAX_STR) or (childName == DatasetArr.T_MIN_STR):
    #             tmin = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.T_MIN_STR)
    #             tmax = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.T_MAX_STR)
    #             self.time_region.setRegion((tmin.value(), tmax.value()))
    #             # image_view = self.bscan_dock.widgets[0]
    #             # image_view.setCurrentIndex(int(param.value()))
    #
    #         if (childName == DatasetArr.CSCAN_STR):
    #             if (param.value() is True):
    #                 self.cscan_dock.show()
    #             else:
    #                 self.cscan_dock.hide()
    #
    #         if (childName == DatasetArr.BSCAN_STR):
    #             if (param.value() is not 'None'):
    #                 self.bscan_dock.show()
    #             else:
    #                 self.bscan_dock.hide()
    #
    #         if (childName == DatasetArr.ASCAN_STR):
    #             if (param.value() is True):
    #                 self.ascan_dock.show()
    #             else:
    #                 self.ascan_dock.hide()
    #
    #         if (childName == DatasetArr.FWF_STR):
    #             if (param.value() is True):
    #                 self.fwf_roi.show()
    #             else:
    #                 self.fwf_roi.hide()
    #
    #         if (childName == DatasetArr.UPDATE_VIEWS_STR):
    #             c_scan = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.CSCAN_STR)
    #             image_view = self.cscan_dock.widgets[0]
    #             image_view.imageItem.setImage(c_scan.opts['image'])
    #
    #             b_scan = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.BSCAN_STR)
    #             image_view = self.bscan_dock.widgets[0]
    #             image_view.setImage(b_scan.opts['image'], axes={'t': 0, 'x': 0 + 1, 'y': 1 + 1, 'c': None})
    #
    #             a_scan = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.ASCAN_STR)
    #             signal_view = self.ascan_dock.widgets[0]
    #             signal_view.plotItem.dataItems[0].setData(a_scan.opts['signal'])
    #
    # def time_region_changed_finished(self, event):
    #     t_min_val, t_max_val = event.getRegion()
    #     t_min = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.T_MIN_STR)
    #     t_min.setValue(t_min_val)
    #     t_max = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.T_MAX_STR)
    #     t_max.setValue(t_max_val)
    #
    #     # c_scan = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.CSCAN_STR)
    #     # image_view = self.cscan_dock.widgets[0]
    #     # image_view.imageItem.setImage(c_scan.opts['image'])
    #     #
    #     # b_scan = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.BSCAN_STR)
    #     # image_view = self.bscan_dock.widgets[0]
    #     # image_view.setImage(b_scan.opts['image'], axes={'t': 0, 'x': 0+1, 'y': 1+1, 'c': None})
    #     #
    #     # ipos = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.I_POS_STR)
    #     # image_view.setCurrentIndex(ipos.value())
    #
    #
    # def bscan_row_changed(self, event):
    #     i_pos = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.I_POS_STR)
    #     image_view = self.bscan_dock.widgets[0]
    #     # i_pos.setValue(image_view.currentIndex)
    #
    # def fwf_region_changed_finished(self, event):
    #     left, bottom = self.fwf_roi.pos()
    #     width, height = self.fwf_roi.size()
    #     fwf = DatasetArr.find_child_in_dataview(self.data_view, DatasetArr.FWF_STR)
    #     fwf.setOpts(fwf_left = left, fwf_bottom=bottom, fwf_width=width, fwf_height=height)
    #     print(event)
