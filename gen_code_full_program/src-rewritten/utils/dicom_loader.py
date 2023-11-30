import logging
import os
import numpy as np
from typing import List
import pydicom
from dicom_sorter import DicomSorterMRI
from dicom_volume import DicomVolumeMRI


class DicomLoaderMRI:
    """
    A class for loading and processing DICOM files from a given directory path.

    Attributes:
        directory_path (str): The directory path where the DICOM files are located.
        _sorted_files (List[str]): A private field to store the sorted file paths of the DICOM files.
        _volumetric_array (np.ndarray): A private field to store the volumetric array of the DICOM files.
    """

    def __init__(self, directory_path: str) -> None:
        """
        Initializes the DicomLoaderMRI instance with the given directory path.

        Args:
            directory_path (str): The directory path where the DICOM files are located.
        
        Raises:
            ValueError: If the directory path is invalid.
        """
        self.validate_directory(directory_path)
        self.directory_path = directory_path
        self._sorted_files = None
        self._volumetric_array = None

    def validate_directory(self, directory_path: str) -> None:
        """
        Validates the directory path to ensure it is a valid directory.

        Args:
            directory_path (str): The directory path to validate.
        
        Raises:
            ValueError: If the directory path is invalid.
        """
        if not os.path.isdir(directory_path):
            raise ValueError("Invalid directory path")

    def dicom_loader(self, sorted_files: List[str]) -> List[pydicom.Dataset]:
        """
        Load DICOM files from a given list of sorted file paths.

        Args:
            sorted_files (List[str]): A list of sorted file paths of DICOM files.

        Returns:
            List[pydicom.Dataset]: A list of DICOM files read from the sorted file paths.
        """
        dicom_files = []
        for file in sorted_files:
            try:
                dicom_files.append(pydicom.dcmread(file))
            except Exception as e:
                logging.error(f"Error loading DICOM file: {file}. Error: {str(e)}")
        return dicom_files

    @property
    def sorted_files(self) -> List[str]:
        """
        Retrieves the sorted file paths of the DICOM files.

        Returns:
            List[str]: A list of sorted file paths of the DICOM files.
        """
        if self._sorted_files is None:
            sorter = DicomSorterMRI(self.directory_path)
            self._sorted_files = sorter.process_sorted_files(sorter.get_sorted_files())
        return self._sorted_files

    @property
    def volumetric_array(self) -> np.ndarray:
        """
        Retrieves the volumetric array of the DICOM files.

        Returns:
            np.ndarray: The volumetric array of the DICOM files.
        """
        if not hasattr(self, "_volumetric_array"):
            self._volumetric_array = DicomVolumeMRI(
                self.directory_path
            ).volumetric_array
        return self._volumetric_array


if __name__ == "__main__":
    try:
        directory = "/path/to/directory"
    except IsADirectoryError:
        pass
    loader = DicomLoaderMRI(directory)
    dcm_list = loader.dicom_loader(loader.sorted_files)
    print(len(dcm_list))

    for i in dcm_list:
        print(i.InstanceNumber)
    pass
