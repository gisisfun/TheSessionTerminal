#! /bin/bash

for i in pdf/*.abc
do
    if test -f "$i" 
    then
        y=${i%.abc}
        pdf="pdf/${y##*/}.pdf"
        if [ ! -f "$pdf" ];
        then
          # works
          bash abc2pdf.sh "${y##*/}"
          # works
        fi
    fi
done