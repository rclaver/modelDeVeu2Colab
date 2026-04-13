#!/bin/bash

# 1
# Entrenamiento con FastSpeech2
#  FastSpeech2 → modelo acústico (texto → espectrograma)

#tts --train --config_path ./config.json
p -m TTS.bin.train_tts --config_path config.json
