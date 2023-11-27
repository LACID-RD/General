# Descomprime imagenes
#unzip 2.16.840.1.114584.4142594449.29072.20143.46613.238949137071360.zip -d /home/daniel/Documents/FAuto/ImgID/Images
#for i in $PWD/Images/*
#do
#	mv "$i" DICOM_Fol
#done
#rm -r Images
var_t13D=$(python3 main.py DICOM_Fol)
echo "Hola mundo"
echo "$var_t13D"
mv $var_t13D DICOM_Fol/T1_3D
echo "terminooo se las mande a guardar"
#dcm2niix -f T1 -p y -z y -o 'DICOM_Fol/T1_3D' 'DICOM_Fol/T1_3D'
#mkdir NIFTI_Fol
#mv DICOM_Fol/T1_3D/T1* NIFTI_Fol/
#bet2 NIFTI_Fol/T1.nii.gz NIFTI_Fol/Bet -o -m -s -e
