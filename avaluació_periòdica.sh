#!/bin/bash

source /home/rafael/bin/entorns/tts/bin/activate

p /home/rafael/bin/entorns/tts/lib/python3.10/site-packages/TTS/bin/synthesize.py \
  --text "Això és una prova de síntesi de veu en català." \
  --model_path ./proces/tts_output/best_model.pth \
  --config_path ./proces/tts_output/config.json \
  --out_path ./test/prova.wav
