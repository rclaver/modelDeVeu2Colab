#!/bin/bash

p TTS/bin/synthesize.py \
  --text "Això és una prova de síntesi de veu en català." \
  --model_path ./proces/tts_output/best_model.pth \
  --config_path ./config.json \
  --out_path prova.wav