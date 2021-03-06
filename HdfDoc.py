import numpy as np
from scipy.signal import hilbert
import h5py
from enum import Enum
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from Event import Event


class DispType(Enum):
    PEAK_TO_PEAK = 1
    MAX = 2
    MIN = 3
    MIN_MAX = 4
    ENVELOP_PEAK = 5
    ENVELOP_PEAK_DB = 6
    ENVELOP_TIME_PEAK = 7


class HdfDoc:
    def __init__(self, hdf_file_name, on_progress_fun=None, percent_to_progress=100):
        self.a_scan_mat = None
        self.hdf_filename = hdf_file_name
        self.progressEvent = Event()
        if on_progress_fun is not None:
            self.progressEvent += on_progress_fun
            self.percent_to_progress = percent_to_progress
        self.load_file()

    def _load_ascans_with_event(self, file: h5py.File):
        a_scans_dataset = file['A-Scans']
        num_wave, wave_len = a_scans_dataset.shape
        step = int(num_wave * self.percent_to_progress / 100)
        self.a_scan_mat = np.zeros(a_scans_dataset.shape)

        for index in range(0, num_wave, step):
            end_index = min(index + step, num_wave)
            self.a_scan_mat[index:end_index, :] = np.float64(a_scans_dataset[index:end_index, :])
            self.progressEvent(index * 100 / num_wave, 'loading file...')

        if a_scans_dataset.dtype is np.dtype('uint8'):
            self.a_scan_mat /= np.power(2., 8)
        elif a_scans_dataset.dtype is np.dtype('uint16'):
            self.a_scan_mat /= np.power(2., 16)
        else:
            raise NotImplementedError
        self.progressEvent(100, '')

    def load_file(self):
        with h5py.File(self.hdf_filename, 'r') as file:
            self.phi_arr = file['Phi Array'][:]
            self.radius_arr = file['Radius Array'][:]
            self.z_arr = file['Z Array'][:]
            # a_scans_dataset = file['A-Scans'][:, :]
            # self.a_scan_mat = np.float64(a_scans_dataset)
            self._load_ascans_with_event(file)

            self.a_scan_mat = self.a_scan_mat - np.mean(self.a_scan_mat, 1, keepdims=True)
            self.sample_rate = file['A-Scans'].attrs['Sample Rate'] / 1e6
            self.is_3D = np.bool(file.attrs['Is 3D'])
            self.x_arr = self.radius_arr * np.cos(self.phi_arr)
            self.y_arr = self.radius_arr * np.sin(self.phi_arr)
            self.reso = self.get_scan_reso()

            if self.is_3D:
                raise NotImplementedError
                # curvDistArr =  self.phi_arr * self.radius_arr
                # midDist = (np.max(curvDistArr) - np.min(curvDistArr))/2
                # curvDistArr -= midDist
            else:
                self.j_arr = np.uint64(np.floor((self.x_arr - np.min(self.x_arr)) / self.reso))
                self.i_arr = np.uint64(np.floor((self.y_arr - np.min(self.y_arr)) / self.reso))

            self.num_col = np.uint64(np.max(self.j_arr) + 1)
            self.num_row = np.uint64(np.max(self.i_arr) + 1)
            self.wave_indx_mat = np.zeros((self.num_row, self.num_col), dtype='uint64')
            for indx, i_indx in enumerate(self.i_arr):
                j_indx = self.j_arr[indx]
                self.wave_indx_mat[i_indx, j_indx] = indx

    def get_s_pos_arr(self):
        raise NotImplementedError

    def get_scan_reso(self):
        if self.is_3D:
            if abs(self.phi_arr[0] - self.phi_arr[1]) > 1e-16:
                arc0 = self.phi_arr[0] * self.radius_arr[0]
                arc1 = self.phi_arr[1] * self.radius_arr[1]
                return abs(arc0 - arc1)
            else:
                # This is for the rotor which scans first the Z axis and then phi
                return abs(self.z_arr[0] - self.z_arr[1])
        else:
            delta_x = self.x_arr[1:] - self.x_arr[:-1]
            delta_y = self.y_arr[1:] - self.y_arr[:-1]
            dist_arr = np.sqrt(np.power(delta_x, 2) + np.power(delta_y, 2.0))
            first_change_indx = (dist_arr > 1e-6).nonzero()[0][0]
            dist = dist_arr[first_change_indx]
            return dist

    def arrange_a_scans_in_mat(self):
        raise NotImplementedError

    @staticmethod
    def get_disp_val(vals_arr, disp_type):
        if disp_type is DispType.PEAK_TO_PEAK:
            val = np.max(vals_arr) - np.min(vals_arr)
        elif disp_type is DispType.MAX:
            val = np.max(vals_arr)
        elif disp_type is DispType.MIN:
            val = np.min(vals_arr)
        elif disp_type is DispType.MIN_MAX:
            min_val = np.abs(np.min(vals_arr))
            max_val = np.abs(np.max(vals_arr))
            val = max(min_val, max_val)
        elif disp_type is DispType.ENVELOP_PEAK:
            envelop = np.abs(hilbert(vals_arr))
            val = np.max(envelop)
        elif disp_type is DispType.ENVELOP_PEAK_DB:
            envelop = np.abs(hilbert(vals_arr))
            envelop = 20 * np.log10(envelop)
            val = np.max(envelop)
        elif disp_type is DispType.ENVELOP_TIME_PEAK:
            envelop = np.abs(hilbert(vals_arr))
            val = np.argmax(envelop)
        else:
            val = 0

        return val

    def get_n0_n1(self, dn0, dn1, fwf_n):
        (num_wave, wave_len) = self.a_scan_mat.shape
        cur_n0 = dn0 + fwf_n
        cur_n1 = dn1 + fwf_n
        cur_n0 = int(min(cur_n0, wave_len))
        cur_n0 = int(max(cur_n0, 0))
        cur_n1 = int(min(cur_n1, wave_len))
        cur_n1 = int(max(cur_n1, 0))
        return cur_n0, cur_n1

    def get_c_scan(self, val_type=DispType.PEAK_TO_PEAK, dn0=0, dn1=None, fwf_arr=None):
        (num_wave, wave_len) = self.a_scan_mat.shape
        c_scan = np.zeros_like(self.wave_indx_mat, dtype='float64')
        fwf_n = 0
        num_to_progress = int(num_wave * self.percent_to_progress / 100)
        for indx, i_indx in enumerate(self.i_arr):
            j_indx = self.j_arr[indx]
            if fwf_arr is not None:
                fwf_n = fwf_arr[indx]
            cur_n0, cur_n1 = self.get_n0_n1(dn0, dn1, fwf_n)
            if (cur_n1 > cur_n0):
                a_scan = self.a_scan_mat[indx][cur_n0:cur_n1]
                c_scan[i_indx, j_indx] = HdfDoc.get_disp_val(a_scan, val_type)


            if (indx %  num_to_progress) == 0:
                self.progressEvent(100 * indx / num_wave, 'calculating c-scan...')
        self.progressEvent(100, '')

        return c_scan

    def get_a_scan(self, i_indx, j_indx):
        index = self.wave_indx_mat[i_indx, j_indx]
        return self.a_scan_mat[index, :]

    def get_data_dim(self):
        (num_wave, wave_len) = self.a_scan_mat.shape
        return (num_wave, self.num_row, self.num_col, wave_len)

    def get_b_scan(self, row, col=None, dn0=0, dn1=0, fwf_arr=None):
        if (row is not None and col is not None) or (row is None and col is None):
            raise ValueError

        (num_wave, num_row, num_col, max_len) = self.get_data_dim()
        bscan_len = np.abs(dn1 - dn0) + 1
        fwf_n = 0
        if (row is not None):
            b_scan = np.zeros((num_col, bscan_len))
            num_to_progress = int(num_col * self.percent_to_progress / 100)
            for cur_col in range(num_col):
                index = self.wave_indx_mat[row, cur_col]
                if fwf_arr is not None:
                    fwf_n = fwf_arr[index]

                cur_n0, cur_n1 = self.get_n0_n1(dn0, dn1, fwf_n)
                b_scan[cur_col, 0:cur_n1 - cur_n0] = self.a_scan_mat[index, cur_n0:cur_n1]
                if (cur_col % num_to_progress) == 0:
                    self.progressEvent(100 * cur_col / num_col, 'calculating b-scan...')
        elif (col is not None):
            b_scan = np.zeros((num_row, bscan_len))
            num_to_progress = int(num_row * self.percent_to_progress / 100)
            for cur_row in range(num_row):
                index = self.wave_indx_mat[cur_row, col]
                if fwf_arr is not None:
                    fwf_n = fwf_arr[index]
                cur_n0, cur_n1 = self.get_n0_n1(dn0, dn1, fwf_n)
                b_scan[cur_row, 0:cur_n1 - cur_n0] = self.a_scan_mat[index, cur_n0:cur_n1]
                if (cur_row % num_to_progress) == 0:
                    self.progressEvent(100 * cur_row / num_row, 'calculating b-scan...')

        self.progressEvent(100, '')
        return b_scan

    def get_volume_ascans(self, ascan_mat=None, dn0=0, dn1=None, fwf_arr=None):
        if (ascan_mat is None):
            ascan_mat = self.a_scan_mat

        (num_wave, wave_len) = self.a_scan_mat.shape
        # wave_len = dn1 - dn0

        ascan_vol = np.zeros((self.num_row, self.num_col, wave_len))

        max_n = 0
        fwf_pos = 0.0
        for indx, i_indx in enumerate(self.i_arr):
            if (fwf_arr is not None):
                fwf_pos = fwf_arr[indx]

            j_indx = self.j_arr[indx]
            cur_n0 = fwf_pos + dn0
            cur_n1 = fwf_pos + dn1
            cur_n0 = int(min(cur_n0, wave_len))
            cur_n0 = int(max(cur_n0, 0))
            cur_n1 = int(min(cur_n1, wave_len))
            cur_n1 = int(max(cur_n1, 0))

            max_n = max(max_n, cur_n1)
            if (cur_n1 > cur_n0):
                ascan_vol[i_indx, j_indx, 0:cur_n1 - cur_n0] = ascan_mat[indx, cur_n0:cur_n1]
        ascan_vol = ascan_vol[:, :, 0:max_n]
        return ascan_vol

    def update_fwf_roi(self, signal_indx, fwf_left, fwf_bottom, fwf_width, fwf_height):
        signal = self.a_scan_mat[signal_indx, :]
        wave_len = signal.shape[0]
        fwf_top = fwf_bottom + fwf_height
        fwf_right = fwf_left + fwf_width

        left = max(int(fwf_left), 0)
        right = min(int(fwf_right), wave_len)
        k_max = np.argmax(signal[left:right])
        k_min = np.argmin(signal[left:right])

        max_val = 0
        k_choose = (left + right) / 2 - left
        if (signal[k_max + left] > fwf_top):
            k_choose = k_max
            max_val = signal[k_max + left]

        if (signal[k_min + left] < fwf_bottom):
            if (-signal[k_min + left] > max_val):
                k_choose = k_min
                max_val = -signal[k_min + left]

        max_pos = left + k_choose

        if (max_val > 0):
            fwf_left_upd = max_pos - fwf_width / 2
        else:
            fwf_left_upd = fwf_left

        return max_pos, fwf_left_upd

    def get_fwf(self, fwf_left, fwf_bottom, fwf_width, fwf_height, cur_i, cur_j):
        fwf_arr = np.zeros_like(self.phi_arr)
        fwf_left_upd = fwf_left
        for row in range(cur_i, 0, -1):
            signal_indx = self.wave_indx_mat[row, cur_j]
            max_pos, fwf_left_upd = self.update_fwf_roi(signal_indx, fwf_left_upd, fwf_bottom, fwf_width, fwf_height)
            fwf_arr[signal_indx] = max_pos

        for col in range(cur_j, 0, -1):
            signal_indx = self.wave_indx_mat[0, col]
            max_pos, fwf_left_upd = self.update_fwf_roi(signal_indx, fwf_left_upd, fwf_bottom, fwf_width, fwf_height)
            fwf_arr[signal_indx] = max_pos

        num_to_progress = int(self.num_row * self.percent_to_progress / 100)
        for row in range(self.num_row):
            for col in range(self.num_col):
                if ((row % 2) > 0):
                    col = int(self.num_col - col - 1)
                signal_indx = self.wave_indx_mat[row, col]
                max_pos, fwf_left_upd = self.update_fwf_roi(signal_indx, fwf_left_upd, fwf_bottom, fwf_width,
                                                            fwf_height)
                fwf_arr[signal_indx] = max_pos

            if (row % num_to_progress) == 0:
                self.progressEvent(100 * row / self.num_row, 'calculating FWF...')

            self.progressEvent(100, '')
        return fwf_arr

    # def get_fwf_pos(self, row, col):
    #     signal_indx = self.wave_indx_mat[row, col]
    #     return self.fwf_arr[signal_indx]

    def band_pass_filter(self, low_freq, high_freq, order):
        nyq = 0.5 * self.sample_rate * 1e6
        low = low_freq / nyq
        high = high_freq / nyq
        b, a = butter(order, [low, high], btype='band')
        self.a_scan_mat = lfilter(b, a, self.a_scan_mat, 1)

    def get_pos(self, row, col):
        index = self.wave_indx_mat[row, col]

        if (self.is_3D):
            raise NotImplementedError
        else:
            pos = {'is_3d': False, 'x': self.x_arr[index], 'y': self.y_arr[index]}

        return pos

    def get_time(self, time_index):
        time_val = time_index / self.sample_rate
        return time_val


if __name__ == '__main__':
    # file_name = 'D:/US_Scans/adhessive_scans/Sample1-  5MHz Focus N01 Glue Interface.hdf'
    file_name = 'G:/My Drive/doctorat/Experiments/Sample1-  5MHz Focus N01 Glue Interface.hdf'

    hdf_data = HdfDoc(file_name)
    cur_a_scan = hdf_data.get_a_scan(100, 100)
    plt.figure('a-scan')
    plt.plot(cur_a_scan)
    plt.show()
