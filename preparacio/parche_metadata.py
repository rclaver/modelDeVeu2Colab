#!/usr/bin/python
# -*- coding: utf-8 -*-

#parche para añadir columna a metadata.csv i eliminar extensió .wav

import os

original = "../dades/dataset/metadata.csv"
temporal = "../dades/dataset/metadata_temp.csv"

os.rename(original, temporal)

with open(temporal, "r", encoding="utf-8") as f_in, \
     open(original, "w", encoding="utf-8") as f_out:

   for line in f_in:
      parts = line.strip().split("|")
      if len(parts) == 2:
         wav, text = parts
         wav = wav.replace(".wav", "")
         f_out.write(f"{wav}|o|{text}\n")
      if len(parts) == 3:
         wav, o, text = parts
         wav = wav.replace(".wav", "")
         f_out.write(f"{wav}|{o}|{text}\n")
