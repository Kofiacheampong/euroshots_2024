import os
import sys



import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch


st.title("Euros 2024 Shot Map")
st.subheader("Check out where players took their shots Euros 2024?")

df = pd.read_csv("euros_2024_shot_map.csv")
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df ['location'] = df['location'].apply(json.loads)

team = st.selectbox("Select a team", df['team'].sort_values().unique(), index= None)
player = st.selectbox("Select a player", df[df['team'] == team]['player'].sort_values().unique(), index= None)

def filter_data(df,team, player):
  if team is not None:
    df = df[df['team'] == team]
  if player is not None:
    df = df[df['player'] == player]
  return df

filtered_df = filter_data(df,team, player)

pitch = VerticalPitch(pitch_type='statsbomb', pitch_length=105, pitch_width=68, half=True)

fig, ax = pitch.draw(figsize=(16, 12))


def plot_shot_map(df, ax,pitch):
  for x in df.to_dict(orient='records'):
    pitch.scatter(
      x= float(x['location'][0]),
      y= float(x['location'][1]),
      ax=ax,
      s=1000 * x['shot_statsbomb_xg'],
      color = 'green' if x['shot_outcome'] == 'Goal' else 'white',
      edgecolors='black',
      alpha=1 if x['type'] == 'goal' else 0.5,
      zorder = 2 if x['type'] == 'goal' else 1
    )
  

plot_shot_map(filtered_df, ax, pitch)
st.pyplot(fig)

