# Alex Weston
# Digital Innovation Lab, Mayo Clinic

import os
import pydicom  # pydicom is using the gdcm package for decompression


def clean_text(
    string,
    forbidden_symbols=["*", ".", ",", '"', "\\", "/", "|", "[", "]", ":", ";", " "],
):
    """
    Clean and standardize text descriptions.

    Parameters:
    - string: a string representing the text to be cleaned.
    - forbidden_symbols: a list of symbols to be replaced with an underscore.

    Returns:
    - a string with cleaned and standardized text.

    Raises:
    - None
    """
    if string is None or not isinstance(string, str):
        return ""

    string = string.lower()  # convert the string to lowercase
    translation_table = str.maketrans(
        "".join(forbidden_symbols), "_" * len(forbidden_symbols)
    )
    return string.translate(translation_table)


def main():
    # user specified parameters
    src = os.getcwd()
    dst = src

    print("reading file list...")
    unsortedList = []
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith(".dcm"):  # exclude non-dicoms, good for messy folders
                unsortedList.append(os.path.join(root, file))

    print("%s files found." % len(unsortedList))

    for dicom_loc in unsortedList:
        # read the file
        ds = pydicom.read_file(dicom_loc, force=True)

        # get patient, study, and series information
        patientID = clean_text(ds.get("PatientID", "NA"))
        studyDate = clean_text(ds.get("StudyDate", "NA"))
        studyDescription = clean_text(ds.get("StudyDescription", "NA"))
        seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))

        # generate new, standardized file name
        modality = ds.get("Modality", "NA")
        studyInstanceUID = ds.get("StudyInstanceUID", "NA")
        seriesInstanceUID = ds.get("SeriesInstanceUID", "NA")
        instanceNumber = str(ds.get("InstanceNumber", "0"))
        fileName = modality + "." + seriesInstanceUID + "." + instanceNumber + ".dcm"

        # uncompress files (using the gdcm package)
        try:
            ds.decompress()
        except Exception as e:
            print(
                f'an instance in file {patientID} - {studyDate} - {studyDescription} - {seriesDescription}" could not be decompressed. Exiting. Error: {str(e)}'
            )

        # save files to a 4-tier nested folder structure
        patient_path = os.path.join(dst, patientID)
        study_path = os.path.join(patient_path, studyDate)
        study_desc_path = os.path.join(study_path, studyDescription)
        series_desc_path = os.path.join(study_desc_path, seriesDescription)

        os.makedirs(patient_path, exist_ok=True)
        os.makedirs(study_path, exist_ok=True)
        os.makedirs(study_desc_path, exist_ok=True)
        os.makedirs(series_desc_path, exist_ok=True)

        print(
            "Saving out file: %s - %s - %s - %s."
            % (patientID, studyDate, studyDescription, seriesDescription)
        )

        ds.save_as(os.path.join(series_desc_path, fileName))
    print("done.")


main()
