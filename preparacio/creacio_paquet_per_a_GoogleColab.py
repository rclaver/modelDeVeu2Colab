#!/usr/bin/python
# -*- coding: utf-8 -*-

# Creació d'un paquet reduit per pujar-lo a GoogleColab

import random
import shutil
import os

original_dir = "../dades/dataset"
input_meta = f"{original_dir}/metadata.csv"
output_dir = "../dades/dataset_small"

os.makedirs(f"{output_dir}/wavs", exist_ok=True)

with open(input_meta, encoding="utf-8") as f:
   lines = f.readlines()

subset = random.sample(lines, 8000)

with open(f"{output_dir}/metadata.csv", "w", encoding="utf-8") as f:
   for line in subset:
      f.write(line)
      wav = line.split("|")[0] + ".wav"
      shutil.copy(f"{original_dir}/wavs/{wav}", f"{output_dir}/wavs/{wav}")
