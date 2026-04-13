#!/usr/bin/python
# -*- coding: utf-8 -*-

# 1. Preparar el dataset català correctament

import pandas as pd
import re, os
from pydub import AudioSegment

df = None
tsv_path = "../dades/cv-corpus/train_manel.tsv"
clips_dir = "../dades/cv-corpus/clips"
wav_dir = "../dades/dataset/wavs"
metadata_path = "../dades/dataset/metadata.csv"
tsv_wav_path = "../dades/cv-corpus/train_wavs.tsv"

#1.0: Eliminar columnes
def eliminar_columnes(columna):
   global df
   print(f"0.1: Eliminar la columna: {columna}")
   df = df.drop(columns=[columna], axis=1)

#1.0: Afegir columnes
def afegir_columnes(columna, valor):
   global df
   print(f"1.0: Afegir columna: {columna}")
   df[columna] = valor

#1.1 Netejar sentències
def neteja_sentencies():
   global df
   print("1.1 Netejar sentències")
   # Filtrar frases buides o molt curtes
   df = df[df["transcription"].notnull()]
   df = df[df["transcription"].str.len() > 5]

   # Opcional: limitar la duració si existeix la columna
   #if "duration" in df.columns:
   #   df = df[df["duration"] < 10]

   print(" "*4 + f"- registres després de la neteja: {len(df)}")

#1.2. Normalització de text
def normalize_text(text):
   text = text.lower()
   text = text.strip()

   # eliminar caracters extranys i espais múltiples
   text = re.sub(r"’", "'", text)
   text = re.sub(r"[^a-zà-ÿ0-9'·\s]", "", text)
   text = re.sub(r"\s+", " ", text)

   return text

#1.3: Conversió MP3 → WAV
def convert_audio(row, idx):
   os.makedirs(wav_dir, exist_ok=True)

   mp3_path = os.path.join(clips_dir, row["audio_file"])
   wav_name = f"{idx:06d}.wav"
   wav_path = os.path.join(wav_dir, wav_name)

   try:
      audio = AudioSegment.from_mp3(mp3_path)
      audio = audio.set_frame_rate(22050).set_channels(1)
      audio.export(wav_path, format="wav")
      return wav_name
   except:
      return None

#1.4: Afegir durada
def afegir_duration(row):
   global df
   file_path = os.path.join(wav_dir, row["audio_file"])
   duration = _get_duration(file_path)
   if duration < 1.0 or duration > 10.0:
      print(f"   {duration}")
   return duration

def _get_duration(wav_path):
   sound = AudioSegment.from_file(wav_path, format="wav")
   return float(sound.duration_seconds)

#1.5: Filtrat per durada (clau per a estabilitat)
def filtra_per_durada():
   global df
   print("1.5: Filtrat per durada")
   filtered_rows = []

   for _, row in df.iterrows():
      file_path = os.path.join(wav_dir, row["audio_file"])
      duration = _get_duration(file_path)

      if 1.0 < duration < 10.0:
         filtered_rows.append(row)

   df = pd.DataFrame(filtered_rows)
   print(" "*4 + f"- registres després de filtrar: {len(df)}")

#1.6: Crear metadata.csv
def genera_metadata():
   global df
   print("1.6: Crear metadata.csv")
   # el formatter ljspeech que utilitzarem necessita 3 columnes: afegim columna 2 amb valor 'o'
   # i necessita el nom de l'arxiu sesne extensió
   with open(metadata_path, "w", encoding="utf-8") as f:
      for _, row in df.iterrows():
         wav = row['audio_file'].replace(".wav", "")
         f.write(f"{wav}|o|{row['transcription']}\n")


if __name__ == "__main__":
   print("1.0 Obtenir els registres del dataset")
   # columnes originals: "client_id","path","sentence_id","sentence","sentence_domain","up_votes","down_votes","age","gender","accents","variant","locale","segment"
   # columnes actuals: "audio_file", "transcription", "duration"
   df = pd.read_csv(tsv_path, sep="\t")

   #1.0: Eliminar i afegir columnes
   eliminar_columnes("client_id")
   afegir_columnes("duration", 5.0)

   #1.1 Netejar sentències
   neteja_sentencies()

   print("1.2. Normalització de text")
   df["transcription"] = df["transcription"].apply(normalize_text)

   print("1.3: Conversió MP3 → WAV")
   df["audio_file"] = [convert_audio(row, i) for i, row in df.iterrows()]
   df = df[df["audio_file"].notnull()]

   print("1.4: Afegir durada")
   df["duration"] = [afegir_duration(row) for i, row in df.iterrows()]

   #1.5: Filtrat per durada
   filtra_per_durada()

   #1.6: Crear metadata.csv
   genera_metadata()

   print("1.7: Desar")
   df.to_csv(tsv_wav_path, sep="\t", index=False)
