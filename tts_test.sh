#!/bin/bash

# Test
#  provar cuando haya checkpoints

tts \
  --text "Hola, això és una prova de síntesi de veu en català" \
  --model_path tts_output/best_model.pth \
  --config_path config.json \
  --vocoder_name vocoder_models/en/ljspeech/hifigan_v2 \
  --out_path test/test.wav
