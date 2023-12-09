from typing import List
import pydicom
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
            try:
                datasets.append(pydicom.dcmread(file_path, stop_before_pixels=True))
            except pydicom.errors.InvalidDicomError:
                print(f"Failed to read DICOM file: {file_path}")
                continue
            
        return datasets

    def _determine_sequence(self, datasets: List[pydicom.Dataset]):
        sequences = []
        for i in datasets:
            if "SeriesDescription" in i:
                sequences.append(i.SeriesDescription)
            else:
                raise ValueError("No series description found")
        
        return sequences
    
    def _determine_institution(self, datasets: List[pydicom.Dataset]):
        institutions = []
        for i in datasets:
            if hasattr(i, "InstitutionName"):
                try:
                    institutions.append(i.InstitutionName)
                except:
                    raise ValueError("No institution name found")
            
        return institutions


if __name__ == "__main__":
    study_dir = "/your/directory/path"
    analyzer = DicomAnalyzer(study_dir)
    paths = analyzer._file_paths
    reader = analyzer._read_files(paths)
    print(analyzer._determine_sequence(analyzer._read_files(analyzer._file_paths)))
    print(analyzer._determine_institution(analyzer._read_files(analyzer._file_paths)))
