#!/bin/bash

# Test de inferencia
#  provar cuando haya checkpoints

tts \
  --text "Hola, això és una prova de síntesi de veu en català" \
  --model_path tts_output/best_model.pth \
  --config_path config.json \
  --out_path test/test.wav
