from typing import List
import pydicom
import numpy as np
import os


class DicomAnalyzer:
    def __init__(self, study_directory_path: str) -> None:
        self._file_paths = self._get_first_dicom_files(study_directory_path)

    def _get_first_dicom_files(self, study_directory_path: str) -> List[str]:
        """
        Finds and returns the paths of the first DICOM files in each subfolder of the study directory.

        Args:
            study_directory_path (str): The path of the study directory.

        Returns:
            List[str]: A list of paths of the first DICOM files found in each subfolder.
        """
        if not os.path.isdir(study_directory_path):
            raise ValueError("Invalid directory path")

        file_paths = []
        for root, dirs, files in os.walk(study_directory_path):
            if files:
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if self._is_dicom_file(file_path):
                        file_paths.append(file_path)
                        break

        return file_paths

    def _is_dicom_file(self, file_path: str) -> bool:
        """
        Checks if a file is a DICOM file.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file is a DICOM file, False otherwise.
        """
        try:
            pydicom.dcmread(file_path)
            return True
        except pydicom.errors.InvalidDicomError:
            return False

    def _read_files(self, file_paths: List[str]) -> List[pydicom.Dataset]:
        """
        Reads DICOM files from a list of file paths.

        Args:
            file_paths (List[str]): A list of file paths.

        Returns:
            List[pydicom.Dataset]: A list of DICOM datasets.
        """
        datasets = []
        for file_path in file_paths:
            datasets.append(pydicom.dcmread(file_path, stop_before_pixels=True))

        return datasets


if __name__ == "__main__":
    study_dir = "/home/ralcala/Documents/AID4ID/testPatients/23342540/20231102/columna_lumbar_2_bl"
    analyzer = DicomAnalyzer(study_dir)
    for i in analyzer._file_paths:
        print(i)
    for k in analyzer._read_files(analyzer._file_paths):
        print(k)
