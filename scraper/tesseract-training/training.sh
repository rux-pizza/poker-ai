#!/bin/bash

## first learning on small example (exp0)

# crate first box file
tesseract pokerai.pokerstar.exp0.tif pokerai.pokerstar.exp0 batch.nochop makebox
# correct mistakes with predefined one
mv box0 pokerai.pokerstar.exp0
# create train files (.tr)
tesseract pokerai.pokerstar.exp0.tif pokerai.pokerstar.exp0 nobatch box.train
# extract charset
unicharset_extractor pokerai.pokerstar.exp0.box
# learn
shapeclustering -F font_properties -U unicharset pokerai.pokerstar.exp0.tr
mftraining -F font_properties -U unicharset -O pokerai.unicharset pokerai.pokerstar.exp0.tr
cntraining pokerai.pokerstar.exp0.tr
# create DAWG files from lists
wordlist2dawg frequent_words_list pokerai.freq-dawg pokerai.unicharset
wordlist2dawg words_list pokerai.word-dawg pokerai.unicharset
# rename created files
mv inttemp pokerai.inttemp
mv normproto pokerai.normproto
mv pffmtable pokerai.pffmtable
mv shapetable pokerai.shapetable
# combine into pokerai.traineddata
combine_tessdata pokerai.


## copy trained data into folder tessdata
sudo cp pokerai.traineddata /usr/local/share/tessdata

## second training : uses previous learning to create a larger box file (exp1)

# box file with -l pokerai option
tesseract pokerai.pokerstar.exp1.tif pokerai.pokerstar.exp1 -l pokerai makebox
# TODO correct mistakes on the newly created pokerai.pokerstar.exp1.box
# and then retrain tesseract as before
