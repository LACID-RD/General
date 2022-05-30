#! /bin/sh
#echo "Este script sirve para obtener modelo de ball and stick (bedpostx-fsl) y posterior matriz de conectividad (probtrackx) para imagenes DWI corregidas por eddy current. Funciona en fsl version 6, y debe estar ubicado en una carpeta con los volúmenes de cada dirección de DTI, junto con los archivos .bval y .bvec y el T1 (asegurarse que el nombre del archivo que contiene el T1 sea wT1.nii, y que los nombres de los archivos de las direcciones comiencen con '2'.). Además debe estar en esa carpeta el archivo aal2.nii.gz. Modificar el directorio del probtrackx2 (último paso) con la carpeta del paciente que corresponda."

echo "Este script sirve para obtener modelo ball and stick y posterior matriz de conectividad para imágenes DWI corregidas por eddy current. Funciona en FSL versión 6 con GPU. Debe encontrarse en la carpeta del paciente, junto con el archivo de la difusión (llamado DWIwc.nii), los archivos .bval y .bvec, el T1 (denominado wT1.nii) y el archivo aal2.nii.gz. Asegurarse de modificar el directorio del probtrackx2_gpu (último paso) con la carpeta del paciente que corresponda antes de correr."
#read -p "Una vez comprobado esto presione ENTER."

echo "\n INICIA EDDY (Este script tiene eddy_cuda, PROBAR)"
mkdir eddy
mv DWIwc.nii eddy
cd eddy
eddy_correct DWIwc.nii DWIeddy.nii 1
#eddy_cuda DWIwc.nii DWIeddy.nii 1
mv DWIwc.nii ../
mv DWIeddy.nii.gz ../
cd ..

echo "\n TERMINO EDDY - INICIA BET"
bet2 DWIeddy.nii.gz nodif_data_brain.nii -m -f 0.5

echo "\n TERMINO BET - INICIA BEDPOSTX (sin gpu)"
mkdir DWIBed
cp DWIeddy.nii.gz DWIBed/data.nii.gz
cp *mask* DWIBed/nodif_brain_mask.nii.gz
mv *.bvec DWIBed/bvecs
mv *.bval DWIBed/bvals

bedpostx_gpu DWIBed -n 2 
echo "\n FIN BEDPOSTX"

#Transformaciones
mkdir T1
mv wT1.nii T1
bet2 T1/wT1.nii T1/wT1_brain -f 0.4

echo "\n INICIA FLIRT (MATRIZ DE TRANSFORMACION MNI-->T1)"

flirt -in /usr/local/fsl/data/standard/MNI152_T1_2mm_brain -ref T1/wT1_brain.nii.gz -out T1/MNItoT1 -omat T1/MNItoT1mat
echo "FIN MNItoT1"

echo "\n INICIA FLIRT (MATRIZ DE TRANSFORMACION DWI-->T1)"
flirt -in nodif_data_brain.nii.gz -ref T1/wT1_brain.nii.gz -out T1/DWItoT1 -omat T1/DWItoT1mat
echo "FIN DWItoT1"

echo "\n INICIA LA INVERSION DE LA MATRIZ DWI-->T1"
convert_xfm -omat DWIBed/INVDWItoT1mat -inverse T1/DWItoT1mat
echo "FIN INVDWItoT1"

echo "\n CONCATENACION DE MATRICES"
convert_xfm -omat DWIBed/concat -concat DWIBed/INVDWItoT1mat T1/MNItoT1mat
echo "FIN CONCAT MNItoDWI"

echo "Comienza la concatenación de aal2 y nodif_data_brain."
flirt -in aal2.nii.gz -ref nodif_data_brain.nii.gz -applyxfm -init DWIBed/concat -out aal2toDWI_concat_nn.nii.gz -interp nearestneighbour 

mkdir SEMILLAS
for i in {1..120}
do
echo $i;

fslmaths aal2toDWI_concat_nn.nii.gz -thr $i -uthr $i -bin SEMILLAS/concat_NN_$i.nii.gz;
echo "SEMILLAS/concat_NN_$i.nii.gz" >> SEMILLAS/120SEMILLAS.txt

done;

#read -p "Correr script split para dividir las 120 semillas. Luego aprete ENTER"
#pause 'Correr script split para dividir las 120 semillas. Aprete ENTER'

echo "\n INICIA PROBTRACKX. Verificar que el directorio en que se encuentra el archivo 120SEMILLAS.txt corresponda con el del script."
$FSLDIR/bin/probtrackx2_gpu --network -x /home/clisazo/Documents/HConnectome/111716/111716_tracto/SEMILLAS/120SEMILLAS.txt -l --onewaycondition --xfm=DWIBed/concat --forcedir --opd -s DWIBed.bedpostX/merged -m DWIBed.bedpostX/nodif_brain_mask.nii.gz --dir=track2
echo "\n FIN PROBTRACKX"
