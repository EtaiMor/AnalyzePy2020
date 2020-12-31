import sys
from PyQt5.QtWidgets import QApplication
from MainDocView import MainDocView
from MainView import MainView

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g_app = QApplication(sys.argv)
    g_main_doc_view = MainDocView()
    g_main_view = MainView(g_main_doc_view)
    g_app.setApplicationName("Analyze - 2020");
    g_app.setOrganizationName("Soreq");
    g_app.setOrganizationDomain("NDT");
    # file_name = 'G:/My Drive/doctorat/Experiments/Sample1-  5MHz Focus N01 Glue Interface.hdf';

    # hdf_data = HdfData(file_name)
    # cur_c_scan = hdf_data.get_c_scan(DispType.ENVELOP_TIME_PEAK, 0, 200)
    # cur_a_scan = hdf_data.get_a_scan(100, 100)
    # plt.figure('c-scan')
    # plt.imshow(cur_c_scan)
    # plt.figure('a-scan')
    # plt.plot(cur_a_scan)
    # plt.show()

    sys.exit(g_app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
