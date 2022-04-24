#!/bin/bash
#Convertir en ejecutable: chmod u+x justdoit.sh

echo -e "\n\n######  Inicia programa mama  ######"
for ((i=19; i<20; i++)); do
  echo -e "\n*** Ejecutando la paciente numero $i"
  python3.7 main.py $i $PWD
done
echo -e "\n\n######  Finaliza programa mama  ######\n\n"
