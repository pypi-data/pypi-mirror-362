# Graph representation
import os
import pickle
import numpy as np
from pathlib import Path
import mne

from numpy import mean, ones, expand_dims, sum, \
    linalg, array, floor, corrcoef, zeros, \
    where, angle

from multiprocessing import Process, Pool
from scipy.signal import csd, butter, lfilter

from typing import Tuple

def _compute_correlation(x):
    return corrcoef(x)

def calculate_coherence_signal_trace(signal_trace, fs):
    electrode_no = len(signal_trace)
    # Initialize output matrices for coherence and phase values, and freq_indices:
    coherence_dict = {}
    phase_dict = {}
    freq_bands = _compute_frequency_bands(fs)
    # Fill-in initialized matrices
    for band in freq_bands.keys():
        coherence_dict[band] = zeros((electrode_no, electrode_no))
        phase_dict[band] = zeros((electrode_no, electrode_no))

    # get initialized 3D arrays (matrices) of the coherence, phase, and ij_pairs
    ij_pairs = get_ij_pairs(electrode_no)

    # initialize Cxy_dict and phase dictionaries, and list of frequencies
    # Cxy_dict is a dictionary in the form of: (0, 1): [coh-freq1, coh-freq2, ..., coh-freqNyq]
    # for all pairs of electrodes
    # Cxy_phase_dict is also a dictionary in the form of: (0, 1): [time1, time2, ..., timeN] for all electrodes
    # fqs is a list of frequencies
    Cxy_dict = {}
    Cxy_phase_dict = {}
    freqs = []
    # check every electrode pair only once
    for electrode_pair in ij_pairs:
        # initialization of dictionaries to electrode_pair key
        Cxy_dict.setdefault(electrode_pair, {})
        Cxy_phase_dict.setdefault(electrode_pair, {})
        # get signals by index
        x = signal_trace[electrode_pair[0]]
        y = signal_trace[electrode_pair[1]]
        # compute coherence
        nperseg = _nperseg(fs)
        freqs, Cxy, ph, Pxx, Pyy, Pxy = coherence(x, y, fs=fs, nperseg=nperseg, noverlap=16)
        # x and y are the first and second signal we compare against
        # freqs = frequencies that are returned by the coherence function
        # in coherence function computing cross spectral density which gives us this evaluation
        # cross spectral density is a function that looks at what are the frequencies that compose the signal in x

        Cxy_dict[electrode_pair] = Cxy
        Cxy_phase_dict[electrode_pair] = ph

    # Create numpy array of keys and values:
    Cxy_keys = array(list(Cxy_dict.keys()))
    Cxy_values = array(list(Cxy_dict.values()))
    phase_keys = array(list(Cxy_phase_dict.keys()))
    phase_values = array(list(Cxy_phase_dict.values()))

    # Create dictionary with freq-band as keys and list of frequency indices from freqs as values, i.e.
    # freq_indices = {'delta': [1, 2]}
    freq_indices = {}
    for band in freq_bands.keys():
        freq_indices[band] = list(where((freqs >= freq_bands[band][0]) & (freqs <= freq_bands[band][1]))[0])

    # filter for signals that are present that correspond to different bands
    # For each freq band (delta...) is a range, here we are filtering using freqs, which contains frequencies found
    # in signal when converted to frequency domain

    # average over the frequency bands; row averaging
    coh_mean = {}
    phase_mean = {}
    for band in freq_bands.keys():
        coh_mean[band] = mean(Cxy_values[:, freq_indices[band]], axis=1)
        phase_mean[band] = mean(phase_values[:, freq_indices[band]], axis=1)

    for band in freq_bands.keys():
        # Fill coherence_dict matrices:
        # Set diagonals = 1
        coherence_dict[band][range(electrode_no), range(electrode_no)] = 1
        # Fill in rest of the matrices
        for pp, pair in enumerate(Cxy_keys):
            coherence_dict[band][pair[0], pair[1]] = coh_mean[band][pp]
            coherence_dict[band][pair[1], pair[0]] = coh_mean[band][pp]

        # Fill phase matrices:
        # Set diagonals = 1
        phase_dict[band][range(electrode_no), range(electrode_no)] = 1
        # Fill in rest of the matrices
        for pp, pair in enumerate(phase_keys):
            phase_dict[band][pair[0], pair[1]] = phase_mean[band][pp]
            phase_dict[band][pair[1], pair[0]] = phase_mean[band][pp]

    return {'coherence': coherence_dict, 'phase_dict': phase_dict, 'freq_dicts': freq_indices, 'freqs': freqs}

def _compute_energy(x):
    nf = zeros(x.shape[0], dtype=x.dtype)
    for i in range(x.shape[0]):
        nf[i] = sum([j ** 2 for j in x[i]])
    nf /= linalg.norm(nf)
    nf = expand_dims(nf, -1)
    return nf

def butter_bandpass(lowcut: float, highcut: float, fs: float, order: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Design a Butterworth bandpass filter and return its filter coefficients.

    Parameters:
        lowcut (float): The lower cutoff frequency.
        highcut (float): The upper cutoff frequency.
        fs (float): The sampling frequency of the signal.
        order (int, optional): The order of the filter. Defaults to 5.

    Returns:
        Tuple[np.ndarray, np.ndarray]: The numerator (b) and denominator (a) filter coefficients.
    """
    nyquist: float = 0.5 * fs
    # Validate cutoff frequencies
    if lowcut <= 0:
        raise ValueError("lowcut frequency must be greater than 0.")
    if highcut >= nyquist:
        raise ValueError("highcut frequency must be less than Nyquist frequency (0.5 * fs).")
    
    normalized_low: float = lowcut / nyquist
    normalized_high: float = highcut / nyquist
    b, a = butter(order, [normalized_low, normalized_high], btype='band')
    return b, a

def butter_bandpass_filter(data: np.ndarray, lowcut: float, highcut: float, fs: float, order: int = 5) -> np.ndarray:
    """
    Apply a Butterworth bandpass filter to the input data.

    Parameters:
        data (np.ndarray): The input signal array.
        lowcut (float): The lower cutoff frequency.
        highcut (float): The upper cutoff frequency.
        fs (float): The sampling frequency of the signal.
        order (int, optional): The order of the filter. Defaults to 5.

    Returns:
        np.ndarray: The filtered signal.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    filtered_signal = lfilter(b, a, data)
    return filtered_signal

def _compute_frequency_bands(fs):
    """
    Pass segments of frequency bands constrained to the sampling frequency 'fs'
    :param fs: int, sampling frequency
    :return: dictionary with frequency bands
    """
    if fs < 499:
        return {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30), 'gamma': (30, 70),
                'gammaHi': (70, 100)}
    elif fs < 999:
        return {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30), 'gamma': (30, 70),
                'gammaHi': (70, 100), 'ripples': (100, 250)}
    # Define frequency oscillation bands, range in Hz:
    return {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30), 'gamma': (30, 70),
            'gammaHi': (70, 100), 'ripples': (100, 250), 'fastRipples': (250, 500)}


    # return {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'b1': (13, 20), 'b2': (20,30), 'g1': (30, 40),
    #         'g2': (40,50), 'g3': (50,60), 'g4': (60,70),
    #         'gh1': (70, 80), 'gh2': (80, 90), 'gh3': (90, 100),
    #         'r1': (100, 130), 'r2': (130, 160), 'r3': (160, 190), 'r4': (190, 220), 'r5': (220, 250),
    #         'fr1': (250, 300), 'fr2': (300, 350), 'fr3': (350, 400), 'fr4': (400, 450), 'fr5': (450, 500)
    #         }

def get_ij_pairs(electrode_no):
    """
    Get list of tuples with i, j pairs of electrodes;
        i, j are indices
    :param electrode_no: int, number of electrodes
    :return: ij_pairs (list of tuples(ints))
    """
    # Define electrode pairs over which to calculate
    # the coherence and save it as list of tuples
    ij_pairs = []
    for i in range(electrode_no):
        for j in range(i + 1, electrode_no):
            ij_pairs.append((i, j))

    return ij_pairs

def _nperseg(fs):
    if fs <= 250:
        return 128
    return 256

def coherence(x, y, fs=1.0, window='hann', nperseg=None, noverlap=None,
              nfft=None, detrend='constant', axis=-1):
    """
    Overriding scipy.signal.spectral.coherence method
    to calculate phase lag from CSD
    :return: freqs (ndarray), Cxy (ndarray), phase (ndarray), Pxx (ndarray), Pyy (ndarray), Pxy (ndarray)
    """


    # power spectral density = signal in frequency domain
    # pxx and pyy are the PSD lines
    freqs, Pxx = csd(x, x, fs=fs, window=window, nperseg=nperseg,
                     noverlap=noverlap, nfft=nfft, detrend=detrend, axis=axis)
    _, Pyy = csd(y, y, fs=fs, window=window, nperseg=nperseg, noverlap=noverlap,
                 nfft=nfft, detrend=detrend, axis=axis)
    _, Pxy = csd(x, y, fs=fs, window=window, nperseg=nperseg,
                 noverlap=noverlap, nfft=nfft, detrend=detrend, axis=axis)

    ph = angle(Pxy, deg=False)

    # formula for coherence
    Cxy = abs(Pxy) ** 2 / (Pxx * Pyy)

    return freqs, Cxy, ph, Pxx, Pyy, Pxy

########################################################

# save preprocessed data for patient sub with all combinations
def graph_representation_elements(sub, w_sz=None, a_sz=None, w_st=0.125):
    """
    Compute and save graph representation elements
    Creates three subprocesses, one for each signal trace

    After getting the preprocessed signal traces (see projects.gnn_to_soz.preprocess), the function
    creates 3 subprocesses that call the function save_gres() for the preictal, ictal, and postictal traces.
    save_gres() will compute all co-activity measurements (currently correlation, coherence, and phase-lock value),
    to then create the graph, node and edge features. These metrics are then stored in pickle files at the directory
    graph_representation_elements_dir/{patientID} (see native.datapaths).

    Preprocessed signal traces are stored in the preprocessed_data_dir directory declared in native.datapaths.
    This function will save gres for every subject run. For instance, if there are 2 subject runs in
    datarecord_path/{subject}, then there will be 2 gres for every signal trace.

    :param sub: string, patient ID (i.e., pt2).
    :param w_sz: float, window size to analyze signal
    :param w_st: float, percentage of window size to be used as
                window step to analyze signal. 0 < w_st <= 1
    :return: nothing, it saves the signal traces into pickle files.
    """
    # load data (pickle file)
    with open("pp_preictal_1.pickle", "rb") as f:
        pp_preictal = pickle.load(f)

    with open("pp_ictal_1.pickle", "rb") as f:
        pp_ictal = pickle.load(f)

    with open("pp_postictal_1.pickle", "rb") as f:
        pp_postictal = pickle.load(f)

    preictal_trace = pp_preictal.get_data()
    ictal_trace = pp_ictal.get_data()
    postictal_trace = pp_postictal.get_data()

    # default to sampling frequency
    if w_sz is None:
        window_size = int(pp_ictal.info["sfreq"])
    else:
        window_size = w_sz

    # default to sampling frequency, floor
    window_step = int(floor(window_size * w_st))

    # create directory to store data
    data_dir = Path.cwd() / "graph_representation"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # save channel names
    ch_names = pp_ictal.ch_names
    data_file = Path(data_dir, "ch_names.pickle")
    print('creating ch_names')
    pickle.dump(ch_names, open(data_file, 'wb'))

    p_save_preictal_trace = Process(target=save_gres,
                                    args=(preictal_trace, pp_preictal.info["sfreq"], window_size,
                                            window_step, data_dir, "preictal", a_sz))
    p_save_preictal_trace.daemon = False
    p_save_ictal_trace = Process(target=save_gres,
                                    args=(ictal_trace, pp_ictal.info["sfreq"], window_size,
                                        window_step, data_dir, "ictal", a_sz))
    p_save_ictal_trace.daemon = False
    p_save_postictal_trace = Process(target=save_gres,
                                        args=(postictal_trace, pp_postictal.info["sfreq"], window_size,
                                            window_step, data_dir, "postictal", a_sz))
    p_save_postictal_trace.daemon = False

    p_save_preictal_trace.start()
    p_save_ictal_trace.start()
    p_save_postictal_trace.start()

    p_save_preictal_trace.join()
    p_save_ictal_trace.join()
    p_save_postictal_trace.join()

def save_gres(signal_trace, sfreq, window_size, window_step, data_dir, trace_type, adj_window_size=20*1000):
    """
    Create sequences of graph representations of the signal traces by considering
    windows of size 'window_size'

    :param signal_trace: ndarray, EEG signal trace
    :param run: int, run number
    :param sfreq: float, sampling frequency
    :param window_size: int, size of window
    :param window_step: int, step that window takes when iterating through signal trace
    :param data_dir: string, directory where to dump serialized (pickle) graph representations
    :param trace_type: string, preictal, ictal, postictal
    :return:
    """
    last_step = signal_trace.shape[1] - window_size
    # pool = Pool(3) FIXME: changed
    pool = Pool()
    """
    # Regular processes - Adj matrix computed from the same window_size as features
    processes = [pool.apply_async(get_all, args=(signal_trace[:, i:i + window_size], sfreq))
                 for i in range(0, last_step, window_step)]
    """


    # Custom processes - Adj matrix computed from adj_window_size while features are computed from window_size
    # processes = [pool.apply_async(custom_adj_get_all, args=(signal_trace[:, i:i + window_size],
    #                                                         # [int(i - min(max(i - adj_window_size / 2, 0), last_step - adj_window_size)), int(i + window_size - min(max(i - adj_window_size / 2, 0), last_step - adj_window_size))],
    #                                                           signal_trace[:, int (min(max(i - adj_window_size / 2, 0), last_step - adj_window_size)): int( min( max(adj_window_size, i + adj_window_size / 2), last_step ))],
    #                                                           sfreq, i, last_step))
    #              for i in range(0, last_step, window_step)]

    # Custom processes - Adj matrix computed from adj_window_size while features are computed from window_size - this version is the most consistent
    processes = [pool.apply_async(custom_adj_get_all, args=(signal_trace[:, i:i + window_size],
                                                            signal_trace[:, int(i - adj_window_size / 2):
                                                                            int(i + adj_window_size / 2)],
                                                            sfreq, i, last_step))
                 for i in range(int(adj_window_size / 2), int(last_step - adj_window_size / 2), window_step)]



    result = [p.get() for p in processes]
    pool.close()
    pool.join()
    file_name = trace_type + ".pickle"
    data_file = Path(data_dir, file_name)
    with open(data_file, 'wb') as save_file:
        print('dumping some file')
        pickle.dump(result, save_file)

def custom_adj_get_all(x_features, x_adj, sfreq, i, last_step):
    """
        Compute adjacency matrix (from the window x_adj), node and edge features (both from the window x_features)
        :param x_features: ndarray, EEG signal trace
        :param x_adj: ndarray, EEG signal trace
        :param sfreq: float, sampling frequency of signal
        :param i: float, step index for tracking progress
        :param last_step: float, last step for tracking progress
        :return: ndarrays of adj_matrices
    """

    print(f'On step {i} / {last_step}')

    # get adj_matrices
    adj_matrices = generate_adjacency_matrices(x_adj, sfreq)

    # get all other features
    node_features, edge_features = generate_node_and_edge_features(x_features, sfreq)

    return adj_matrices, node_features, edge_features

def generate_adjacency_matrices(x, sfreq):
    """
        Compute adjacency matrix
        :param x: ndarray, EEG signal trace
        :param sfreq: float, sampling frequency of signal
        :return: ndarrays of adj_matrices
    """

    # "corr"
    corr_x = _compute_correlation(x)

    # "coh"
    coherence_result = calculate_coherence_signal_trace(x, sfreq)
    coherences_dict = coherence_result['coherence']
    coherences = []
    for key in coherences_dict.keys():
        coherences.append(coherences_dict[key])
    coherences = mean(coherences, axis=0)

    # "phase"
    phases_dict = coherence_result['phase_dict']
    phases = []
    for key in phases_dict.keys():
        phases.append(phases_dict[key])
    phases = mean(phases, axis=0)

    adj_matrices = [ones((x.shape[0], x.shape[0]), dtype=x.dtype),  # "ones"
                    corr_x,  # "corr"
                    coherences,  # "coh"
                    phases]  # "phase"

    return adj_matrices

# Function to compute node and edge features
def generate_node_and_edge_features(x, sfreq):
    """
    Get all combinations of node and edge features, WITHOUT adjacency matrices
    :param x: ndarray, EEG signal trace
    :param sfreq: float, sampling frequency of signal
    :return: ndarrays of node_features, edge_features
    """
    # ---------- edge features ----------
    # "ones"
    edge_features = [ones((x.shape[0], x.shape[0], 1), dtype=x.dtype)]

    # "corr"
    corr_x = _compute_correlation(x)
    edge_features.append(expand_dims(corr_x, -1))

    # "coh"
    coherence_result = calculate_coherence_signal_trace(x, sfreq)
    coherences_dict = coherence_result['coherence']
    coherences = []
    for key in coherences_dict.keys():
        coherences.append(coherences_dict[key])
    coherences = mean(coherences, axis=0)
    edge_features.append(expand_dims(coherences, -1))

    # "coh+" expanded with extra features for each band
    coherence_result = calculate_coherence_signal_trace(x, sfreq)
    coherences_dict = coherence_result['coherence']
    coherences = []
    for key in coherences_dict.keys():
        coherences.append(coherences_dict[key])
    coherences.insert(0,mean(coherences, axis=0))
    combined_coherences = [
        [[sublists[i][j] for sublists in coherences] for j in range(len(coherences[0][0]))]
        for i in range(len(coherences[0]))
    ]
    combined_coherences = np.array(combined_coherences)
    edge_features.append(combined_coherences)

    # "phase"
    phases_dict = coherence_result['phase_dict']
    phases = []
    for key in phases_dict.keys():
        phases.append(phases_dict[key])
    phases = mean(phases, axis=0)
    edge_features.append(expand_dims(phases, -1))

    # ---------- node features ----------
    # "ones"
    node_features = [ones((x.shape[0], 1), dtype=x.dtype)]

    # "energy"
    nf = _compute_energy(x)
    node_features.append(nf)

    # "band_energy"
    freq_dicts = coherence_result['freq_dicts']
    freqs = coherence_result['freqs']
    nf = [[] for _i in range(x.shape[0])]
    for i in range(x.shape[0]):
        for band in freq_dicts.keys():
            lowcut = freqs[min(freq_dicts[band])]
            highcut = freqs[max(freq_dicts[band])]
            if lowcut == highcut:
                lowcut = freqs[min(freq_dicts[band])-1]
            # lowcut frequencies must be greater than 0, so currently set to 0.1
            if lowcut == 0:
                lowcut += 0.1
            # highcut frequencies must be less than sfreq / 2, so subtract 1 from max
            if highcut == sfreq / 2:
                highcut -= 0.1
            freq_sig = butter_bandpass_filter(x[i], lowcut, highcut, sfreq)
            nf[i].append(sum([j ** 2 for j in freq_sig]))
        nf[i] = nf[i]
    nf /= linalg.norm(nf, axis=0, keepdims=True)
    node_features.append(nf)

    return node_features, edge_features

import os
import pickle
import numpy as np
from pathlib import Path
from multiprocessing import Pool

class EEGGraphProcessor:
    def __init__(self, eeg_pickle_path=None, edf_loader=None, output_dir=None, window_size=None, adj_window_size=20000, window_step_ratio=0.125):
        if eeg_pickle_path is None and edf_loader is None:
            raise ValueError("Either eeg_pickle_path or edf_loader must be provided")
        if eeg_pickle_path is not None and edf_loader is not None:
            raise ValueError("Provide either eeg_pickle_path or edf_loader, not both")
        
        if edf_loader is not None:
            # Use EDFLoader - create MNE pickle without modifying the loader
            self.edf_loader = edf_loader
            pickle_path = self._convert_edf_to_mne_pickle()
            self.eeg_pickle_path = pickle_path
            self.filename = edf_loader.name
        else:
            # Use provided pickle path
            self.edf_loader = None
            self.eeg_pickle_path = eeg_pickle_path
            self.filename = Path(self.eeg_pickle_path).stem
        
        self.output_dir = Path.cwd() / "graph_representation" if output_dir is None else Path(output_dir)
        self.adj_window_size = adj_window_size
        self.window_step_ratio = window_step_ratio
        self.window_size = window_size  # Will be updated dynamically if None
        self.eeg_data = None
        self.sfreq = None
        self.ch_names = None

    def load_eeg(self):
        """
        Load EEG data from a pickle file and extract metadata.
        Assumes the object has .get_data(), .info["sfreq"], and .ch_names attributes.
        """
        with open(self.eeg_pickle_path, "rb") as f:
            eeg_obj = pickle.load(f)
        
        self.eeg_data = eeg_obj.get_data()
        self.sfreq = eeg_obj.info["sfreq"]
        self.ch_names = eeg_obj.ch_names

        if self.window_size is None:
            self.window_size = int(self.sfreq)

        self.window_step = int(self.window_size * self.window_step_ratio)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.output_dir / "ch_names.pickle", 'wb') as f:
            pickle.dump(self.ch_names, f)

    def _convert_edf_to_mne_pickle(self, output_filename=None):
        """
        Converts the EDF file to MNE Raw format and saves as pickle file.
        
        :param output_filename: str, optional filename for the pickle file (defaults to {name}_mne.pickle)
        :return: str, path to the saved pickle file
        """
        if output_filename is None:
            output_filename = f"{self.edf_loader.name}_mne.pickle"
        
        output_path = os.path.join(self.edf_loader.folder_path, self.edf_loader.name, output_filename)
        
        # Load EDF using MNE
        raw = mne.io.read_raw_edf(self.edf_loader.edf_file_path, preload=True, verbose=False)
        
        # Save as pickle
        with open(output_path, 'wb') as f:
            pickle.dump(raw, f)
        
        print(f"MNE Raw object saved to: {output_path}")
        return output_path

    def generate_graphs(self):
        """
        Generate graph representation features in parallel and save to pickle.
        """
        last_step = self.eeg_data.shape[1] - self.window_size
        processes = []

        for i in range(int(self.adj_window_size / 2), int(last_step - self.adj_window_size / 2), self.window_step):
            x_feat = self.eeg_data[:, i:i + self.window_size]
            x_adj = self.eeg_data[:, int(i - self.adj_window_size / 2): int(i + self.adj_window_size / 2)]
            processes.append((x_feat, x_adj, self.sfreq, i, last_step))

        with Pool() as pool:
            results = pool.starmap(self._compute_graph_components, processes)

        output_file = self.output_dir / f"{self.filename}.pickle"
        with open(output_file, 'wb') as f:
            pickle.dump(results, f)

    def _compute_graph_components(self, x_features, x_adj, sfreq, i, last_step):
        """
        Compute adjacency matrices, node features, and edge features for one window.
        """
        print(f'Processing window {i}/{last_step}')
        adj_matrices = generate_adjacency_matrices(x_adj, sfreq)
        node_features, edge_features = generate_node_and_edge_features(x_features, sfreq)
        return adj_matrices, node_features, edge_features

########################################################

# if __name__ == '__main__':
#     eeg_file = "pp_ictal_1.pickle"

#     # Set window size, optional
#     w_sz = 1000  # Optional, defaults to sampling frequency

#     print(f"Processing {eeg_file} ####################")
#     processor = EEGGraphProcessor(
#         eeg_pickle_path=eeg_file,
#         window_size=w_sz,
#         adj_window_size=20000  # optional, defaults to sampling frequency
#     )
#     processor.load_eeg()
#     processor.generate_graphs()
