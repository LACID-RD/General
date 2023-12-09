import numpy as np
import pydicom
import SimpleITK as sitk
import matplotlib.pyplot as plt

from dicom_loader import DicomLoaderMRI


class DicomPlotter:
    def __init__(self, directory_path: str) -> None:
        self.path = directory_path
        self.dicom_loader = DicomLoaderMRI(directory_path)
        self.dicom_files = self.dicom_loader.sorted_files

    def _show_image(self, arr: np.ndarray, show: bool = True):
        """
        Plot a 2D or 3D array using SimpleITK.

        Args:
            arr (np.ndarray): A 2D or 3D array.

        Returns:
            matplotlib.image.AxesImage: The plot object representing the image.
        """
        plt_images = []
        itk_image = sitk.GetImageFromArray(arr)
        plt_images.append(plt.imshow(sitk.GetArrayViewFromImage(itk_image), cmap="gray"))
        print(plt_images)
        if show:
            plt.show()
        return plt_images

    @property
    def _plot_all_files(self):
        def load_and_plot_images():
            for dicom in self.dicom_files:
                ds = pydicom.dcmread(dicom)
                yield ds.pixel_array

        for pixel_array in load_and_plot_images():
            self._show_image(pixel_array)

    def _plot_single_file(self, img_num_input: int):
        ds = pydicom.dcmread(self.dicom_files[img_num_input])
        self._show_image(ds.pixel_array)


if __name__ == "__main__":
    directory = "/your/directory/path"
    plotter = DicomPlotter(directory)
    plotter._plot_all_files
    plotter._plot_single_file(img_num_input=0)
    # arr = plotter.dicom_loader.volumetric_array
    # plotter._show_image(arr)
