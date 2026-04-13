#!/usr/bin/python
# -*- coding: utf-8 -*-

# 0.0 Neteja arxiu gran

import pandas as pd
import re, os
from pydub import AudioSegment

df = None
tsv_path = "../dades/cv-corpus/train_full.tsv"
clips_dir = "../dades/cv-corpus/clips_full"
wav_dir = "../dades/dataset/z-wavs"
sortida = "../dades/cv-corpus/train_wav_full.tsv"

def mostrar_dataset(mostra_files=False):
   global df
   print("="*22+"\nDescripció del dataset\n"+"="*22)
   print(df.info())

   if mostra_files:
      print("\nLas primeras 20 filas 'up_votes'")
      print(df.nlargest(20, "up_votes"))
      print("\nLas primeras 20 filas 'down_votes'")
      print(df.nlargest(20, "down_votes"))
      print("\nLas primeras 20 filas 'age'")
      print(df.sort_values(by="age", ascending=False).head(20))
      print("\nLas primeras 20 filas 'gender'")
      print(df.sort_values(by="gender", ascending=False).head(20))
      print("\nLas primeras 20 filas 'variant'")
      print(df.sort_values(by="variant", ascending=False).head(20))

#0.1: Eliminar columnes
def eliminar_columnes(columna):
   global df
   print(f"0.1: Eliminar la columna: {columna}")
   df = df.drop(columns=[columna], axis=1)

#0.2: Afegir columnes
def afegir_columnes(columna, valor):
   global df
   print(f"0.2: Afegir columna: {columna}")
   df[columna] = valor

#0.3: Conversió MP3 → WAV
def convert_audio(row, idx):
   os.makedirs(wav_dir, exist_ok=True)

   mp3_path = os.path.join(clips_dir, row["path"])
   wav_name = f"{idx:08d}.wav"
   wav_path = os.path.join(wav_dir, wav_name)

   try:
      audio = AudioSegment.from_mp3(mp3_path)
      audio = audio.set_frame_rate(22050).set_channels(1)
      audio.export(wav_path, format="wav")
      return wav_name
   except:
      return None

#0.4: Afegir duration
def afegir_duration():
   global df
   print("0.4: Afegir duration")

   for _, row in df.iterrows():
      file_path = os.path.join(wav_dir, row["path"])
      duration = _get_duration(file_path)
      df['duration'] = duration

def _get_duration(wav_path):
   sound = AudioSegment.from_file(wav_path, format="wav")
   return float(sound.duration_seconds)


if __name__ == "__main__":
   # columnes originals: "client_id","path","sentence_id","sentence","sentence_domain","up_votes","down_votes","age","gender","accents","variant","locale","segment"
   # columnes finals: "client_id", "path", "sentence","age","gender","variant","wav","duration"
   pd.set_option('display.max_columns', None)
   df = pd.read_csv(tsv_path, sep="\t", dtype={"sentence_domain":"object", "up_votes":int, "down_votes":int, "age":"string", "gender":"string", "accents":"object"})


   #0.1: Eliminar columnes
   eliminar_columnes("sentence_id")
   eliminar_columnes("sentence_domain")
   eliminar_columnes("up_votes")
   eliminar_columnes("down_votes")
   eliminar_columnes("accents")
   eliminar_columnes("locale")
   eliminar_columnes("segment")

   #0.2: Afegir columnes
   afegir_columnes("duration", 0.0)
   afegir_columnes("wav", "")

   mostrar_dataset()

   print("0.3: Conversió MP3 → WAV")
   df["wav"] = [convert_audio(row, i) for i, row in df.iterrows()]

   #0.4: Afegir duration
   afegir_duration()

   #0.5: Desar
   df.to_csv(sortida, sep="\t", index=False)
