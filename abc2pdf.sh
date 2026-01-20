#!/bin/bash
abc="'pdf/$1.abc'"
ps="'pdf/$1.ps'"
pdf="'pdf/$1.pdf'"
echo "processing $abc to $pdf"
eval "abcm2ps $abc  -O  $ps"
eval "ps2pdf $ps $pdf"