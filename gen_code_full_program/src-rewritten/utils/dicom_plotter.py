import numpy as np
import pydicom
import SimpleITK as sitk

from dicom_loader import DicomLoaderMRI


class DicomPlotter:
    def __init__(self, directory_path: str) -> None:
        self.path = directory_path
        self.dicom_loader = DicomLoaderMRI(directory_path)
        self.dicom_files = self.dicom_loader._sorted_files

    def _show_image(self, arr: np.ndarray):
        """
        Plot a 2D or 3D array using SimpleITK.
        Requires Fiji or some other external viewer.

        Args:
            arr (np.ndarray): A 2D or 3D array.

        Returns:
            None
        """
        itk_image = sitk.GetImageFromArray(arr)
        return sitk.Show(itk_image)

    def _plot_all_files(self):
        for dicom_file in self.dicom_files:
            ds = pydicom.dcmread(dicom_file)
            self._show_image(ds.pixel_array)

    def _plot_sigle_file(self):
        img_num_input: int = input("Enter img number to plot: ")
        ds = pydicom.dcmread(self.dicom_files[img_num_input])
        self._show_image(ds.pixel_array)


if __name__ == "__main__":
    directory = "/home/ralcala/Documents/AID4ID/testPatients/23342540/20231102/columna_lumbar_2_bl/t2w_tse_sag"
    plotter = DicomPlotter(directory)
    plotter._plot_all_files()
    pass
