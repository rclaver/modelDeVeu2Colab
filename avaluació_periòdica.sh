#!/bin/bash

p /home/rafael/bin/entorns/tts/lib/python3.11/site-packages/TTS/bin/synthesize.py \
  --text "Això és una prova de síntesi de veu en català." \
  --model_path ./proces/tts_output/best_model.pth \
  --config_path ./config_mix.json \
  --out_path prova.wav