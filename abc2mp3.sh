#!/bin/bash
echo $PWD
abc="'$1.abc'"
mid="'$1.mid'"
wav="'$1.wav'"
mp3="'$1.mp3'"
echo "processing $abc to $mid"
echo $abc
eval "abc2midi $abc -o $mid"
eval "timidity $mid -Ow -o $wav"
eval "sox $wav $mp3 speed 1.33"
eval "rm $wav"
eval "rm $mid"
