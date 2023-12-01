import numpy as np
import matplotlib.pyplot as plt

from dicom_loader import DicomLoaderMRI


class HistogramGenerator:
    def __init__(self, array_2D=None, array_3D=None):
        """
        Initializes the HistogramGenerator class with optional 2D and 3D arrays.

        Args:
            array_2D (np.ndarray, optional): 2D array used for generating 2D histograms. Defaults to None.
            array_3D (np.ndarray, optional): 3D array used for generating 3D histograms. Defaults to None.
        """
        self.array_2D = array_2D
        self.array_3D = array_3D

    def create_histogram_2D(self, offset: int = 0, show: bool = True):
        """
        Generates a 2D histogram from the provided 2D array and returns the bins and frequencies.

        Args:
            offset (int, optional): The offset to apply to the histogram bins and frequencies. Defaults to 0.
            show (bool, optional): Whether to display the histogram using matplotlib. Defaults to True.

        Returns:
            tuple: bins and frequencies of the histogram
        """
        if self.array_2D is None:
            return None, None

        arr_max = int(np.max(self.array_2D))
        hist, bins = np.histogram(self.array_2D.flatten(), bins=arr_max, density=False)

        if offset < len(bins):
            bins = bins[offset + 1 :]
            hist = hist[offset:]
        else:
            bins = []
            hist = []

        if show:
            try:
                plt.plot(bins, hist)
                plt.xlabel("Pixel Value")
                plt.ylabel("Frequency")
                plt.title("2D Histogram")
                plt.grid()
                plt.show()
            except Exception as e:
                print("Error plotting histogram:", str(e))

        return hist, bins

    def create_histogram_3D(self, offset: int = 0, show: bool = True):
        """
        Generates a 3D histogram from the provided 3D array and returns the bins and frequencies.

        Args:
            offset (int, optional): The offset to apply to the histogram bins and frequencies. Defaults to 0.
            show (bool, optional): Whether to display the histogram using matplotlib. Defaults to True.

        Returns:
            tuple: bins and frequencies of the histogram
        """
        if self.array_3D is None:
            return None, None

        histograms = []
        arr_max = int(np.max(self.array_3D))
        for i in range(self.array_3D.shape[2]):
            arr = self.array_3D[:, :, i]
            hist, bins = np.histogram(arr.flatten(), bins=arr_max, density=False)

            if offset < len(bins):
                bins = bins[offset + 1 :]
                hist = hist[offset:]
            else:
                bins = []
                hist = []

            histograms.append(hist)
        average_hist = np.mean(histograms, axis=0)

        if show:
            try:
                plt.plot(bins, average_hist)
                plt.xlabel("Pixel Value")
                plt.ylabel("Frequency")
                plt.title("3D Histogram")
                plt.grid()
                plt.show()
            except Exception as e:
                print("Error plotting histogram:", str(e))

        return average_hist, bins


if __name__ == "__main__":
    directory = "/your/dicom/directory"
    loader = DicomLoaderMRI(directory)
    dicom_files = loader.dicom_loader(loader.sorted_files)
    arr_2D = dicom_files[7].pixel_array

    arr_3D = loader.volumetric_array

    hist_generator = HistogramGenerator(array_2D=arr_2D, array_3D=arr_3D)
    hist_generator.create_histogram_2D(offset=5, show=True)
    hist_generator.create_histogram_3D(offset=5, show=True)
    pass
