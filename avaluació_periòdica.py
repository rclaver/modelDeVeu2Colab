import os
from TTS.api import TTS

run_path = "./proces/tts_output"
latest_model = os.path.join(run_path, "best_model.pth")
output_wav = os.path.join("test", "test.wav")
text = "Aquesta és una prova automàtica de la veu entrenada."

print("Usando modelo:", latest_model)

tts = TTS(model_path=latest_model, config_path=os.path.join(run_path, "config.json"))
tts.tts_to_file(text=text, file_path=output_wav)

print("Audio generado en:", output_wav)
