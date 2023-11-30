import logging
import os
from typing import List
import pydicom
import numpy as np


class DicomVolumeMRI:
    """
    This class takes a directory and returns a list of sorted file paths
    and a volumetric array of the entire directory files.
    """

    def __init__(self, directory_path: str) -> None:
        if not os.path.isdir(directory_path):
            raise ValueError("Invalid directory path")
        self.directory_path = directory_path
        self.sorted_files = self._sort_dicom_files()
        self.volumetric_array = self._generate_volumetric_array()

    def _sort_dicom_files(self) -> List[str]:
        """
        Sorts the DICOM files in the directory based on their acquisition time.

        Returns:
            List[str]: A list of sorted file paths of the DICOM files in the directory.
        """
        logging.info("Sorting DICOM files...")
        dicom_files = [
            file for file in os.listdir(self.directory_path) if file.endswith(".dcm")
        ]
        sorted_files = sorted(
            dicom_files,
            key=lambda file: pydicom.dcmread(
                os.path.join(self.directory_path, file)
            ).AcquisitionTime,
        )
        return [os.path.join(self.directory_path, file) for file in sorted_files]

    def _generate_volumetric_array(self) -> np.ndarray:
        """
        Generate a 3D stacked array of the volume.

        Returns:
            np.ndarray: 3D numpy array representing the volume.
        """
        logging.info("Generating volumetric array...")
        dcm_matrices = [pydicom.dcmread(path).pixel_array for path in self.sorted_files]
        stacked_volume = np.dstack(dcm_matrices)
        return stacked_volume


if __name__ == "__main__":
    try:
        directory = "/path/to/directory"
    except IsADirectoryError:
        pass
    # Replace with your directory path

    dicom_sorter = DicomVolumeMRI(directory)
    dicom_files_sorted = dicom_sorter.sorted_files

    for i, file_path in enumerate(dicom_files_sorted, start=1):
        print(f"Image {i}: {file_path}")

    print(np.shape(dicom_sorter.volumetric_array))
