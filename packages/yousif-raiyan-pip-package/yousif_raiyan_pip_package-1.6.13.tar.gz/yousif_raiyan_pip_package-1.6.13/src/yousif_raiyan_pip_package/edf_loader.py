import os
import pyedflib
import matplotlib.pyplot as plt

class EDFLoader:
    def __init__(self, folder_path, name):
        """
        Initializes the EDFLoader with a folder path where the EDF file is stored.

        :param folder_path: str, the base directory where the EDF file is stored
        :param name: str, the name of the subject or experiment (the EDF file should match this name)
        """
        self.folder_path = folder_path
        self.name = name
        self.edf_file_path = f"{folder_path}/{name}/{name}.edf"
        self.signals_dict = None
        # Check for the existence of the EDF file
        if not os.path.exists(self.edf_file_path):
            raise FileNotFoundError(f"EDF file not found: {self.edf_file_path}")

    def inspect_data(self):
        """
        Inspects the EDF file for the specified subject, printing out various signal information.
        """
        try:
            with pyedflib.EdfReader(self.edf_file_path) as edf:
                print("File header:")
                print(edf.getHeader())
                n = edf.signals_in_file
                print("\nNumber of signals:", n)

                for i in range(n):
                    print(f"\nSignal {i} information:")
                    print("Label:", edf.getLabel(i))
                    print("Sample rate:", edf.getSampleFrequency(i))
                    print("Duration:", edf.getFileDuration())
                    print("Physical maximum:", edf.getPhysicalMaximum(i))
                    print("Physical minimum:", edf.getPhysicalMinimum(i))
                    print("Digital maximum:", edf.getDigitalMaximum(i))
                    print("Digital minimum:", edf.getDigitalMinimum(i))
                    print("First 10 samples:", edf.readSignal(i)[:10])
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_and_plot_signals(self):
        """
        Loads and plots the signals from the EDF file, storing them along with their sample rates in a dictionary.
        """
        signals_dict = {}

        try:
            with pyedflib.EdfReader(self.edf_file_path) as edf:
                self.signals_dict = signals_dict
                n = edf.signals_in_file
                signal_data = [edf.readSignal(i) for i in range(n)]
                sample_rates = [edf.getSampleFrequency(i) for i in range(n)]

                fig, axes = plt.subplots(nrows=n, ncols=1, figsize=(10, 2 * n))
                if n == 1:
                    axes = [axes]  # Make it iterable if there's only one signal

                for i, (data, rate, ax) in enumerate(zip(signal_data, sample_rates, axes)):
                    signal_label = edf.getLabel(i)
                    signals_dict[signal_label] = {'data': data, 'sample_rate': rate}
                    ax.plot(data)
                    ax.set_title(f'Signal {i + 1}: {signal_label}')
                    ax.set_xlabel('Samples')
                    ax.set_ylabel('Amplitude')

                plt.tight_layout()
                plt.show()

        except FileNotFoundError:
            print(f"File not found: {self.edf_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

