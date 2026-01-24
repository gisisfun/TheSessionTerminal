#!/bin/bash
abc="'pdf/$1.abc'"
ps="'pdf/$1.ps'"
pdf="'pdf/$1.pdf'"
echo "processing $abc to $pdf"
#echo "abcm2ps $abc -O $ps"
eval "abcm2ps $abc -O $ps"
#echo "ps2pdf $ps $pdf"
eval "ps2pdf $ps $pdf"