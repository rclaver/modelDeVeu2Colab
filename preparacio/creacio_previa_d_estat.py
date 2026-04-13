#!/usr/bin/python
# -*- coding: utf-8 -*-

#creació prèvia de l'arxiu d'estat '../proces/cache/f0/pitch_stats.npy'

import numpy as np
import os

# Crear directorios si no existen
os.makedirs("../proces/cache/f0", exist_ok=True)
os.makedirs("../proces/cache/energy", exist_ok=True)

stats = {
   "mean": np.array([0.0], dtype=np.float32),
   "std": np.array([1.0], dtype=np.float32)
}

np.save("../proces/cache/f0/pitch_stats.npy", stats)
np.save("../proces/cache/energy/energy_stats.npy", stats)
