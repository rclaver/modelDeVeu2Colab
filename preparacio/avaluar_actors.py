#!/usr/bin/python
# -*- coding: utf-8 -*-

# 1. Preparar el dataset català correctament

import pandas as pd

df = None
tsv_path = "../dades/cv-corpus/train_full.tsv"
clips_dir = "../dades/cv-corpus/clips"

# 1.1 Analitza i agrupa els actors
def avalua_actors():
   global df
   print("1.1 Analitza i agrupa els actors")
   # Agrupar por speaker
   grouped = df.groupby("client_id").agg({
       "sentence": "count",
       "duration": "sum",
       "sentence_len": "mean"
   }).rename(columns={
       "sentence": "num_samples",
       "duration": "total_duration",
       "sentence_len": "avg_len"
   })

   # filtrat inicial
   candidates = grouped[
       (grouped["num_samples"] > 200) &
       (grouped["total_duration"] > 1800)  # >30 min
   ]
   # ordenar per durada
   candidates = candidates.sort_values(by="total_duration", ascending=False)
   print("Llista de candidats per durada")
   print(candidates.head(20))

   # ranking automátic: puntuar actors
   grouped["score"] = (
       grouped["total_duration"] * 0.6 +
       grouped["num_samples"] * 0.3 +
       grouped["avg_len"] * 0.1
   )
   top_speakers = grouped.sort_values(by="score", ascending=False)
   print("\nLlista dels millors candidats")
   print(top_speakers.head(20))

def reduir_dataset(millor_veu):
   global df
   df_speaker = df[df["client_id"] == best_speaker]
   df_speaker = df_speaker[
       (df_speaker["duration"] > 1.0) &
       (df_speaker["duration"] < 8.0)
   ]

   df_speaker = df_speaker[
       (df_speaker["sentence_len"] > 20) &
       (df_speaker["sentence_len"] < 200)
   ]


if __name__ == "__main__":
   print("1.0 Obtenir els registres del dataset")
   # columnes: "client_id", "audio_file", "transcription"
   df = pd.read_csv(tsv_path, sep="\t")

   # 1.1 Analitza i agrupa els actors
   avalua_actors()
