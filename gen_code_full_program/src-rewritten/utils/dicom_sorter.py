import pathlib
from typing import List
import pydicom


class DicomSorterMRI:
    """This class generates a loader object that takes a directory and returns
    a sorted list of each .dcm file inside that directory
    """

    def __init__(self, directory_path: str) -> None:
        self.directory_path = directory_path
        self.sorted_files = None

    def get_sorted_files(self) -> List[str]:
        """
        This method returns a sorted list of the paths of each file in the directory

        Returns:
            List[str]: a sorted list of file paths
        """
        dicom_files = []
        try:
            for file in sorted(pathlib.Path(self.directory_path).rglob("*.dcm")):
                try:
                    dicom_files.append(str(file))
                except (IOError, pydicom.errors.InvalidDicomError) as e:
                    raise Exception(f"Error reading file: {file}. {str(e)}")
        except IOError as e:
            raise Exception(
                f"Error accessing directory: {self.directory_path}. {str(e)}"
            )

        return dicom_files

    def process_sorted_files(self, dicom_files: List[str]) -> None:
        self.sorted_files = self.get_sorted_files()
        dicom_files.sort(
            key=lambda file: pydicom.dcmread(
                file, stop_before_pixels=True
            ).InstanceNumber
        )

        return dicom_files


if __name__ == "__main__":
    # Replace with your directory path
    try:
        directory = "/path/to/directory"
    except IsADirectoryError:
        pass

    dicom_sorter = DicomSorterMRI(directory)
    dicom_files_sorted = dicom_sorter.get_sorted_files()
    dicom_files_sorted = dicom_sorter.process_sorted_files(dicom_files_sorted)

    for i, file_path in enumerate(dicom_files_sorted, start=1):
        print(f"Image {i}: {file_path}")
