import torch
import torchaudio
from pydub import AudioSegment
import moviepy.editor as mp
import speech_recognition as sr
import subprocess
import os
import sys



class GreedyCTCDecoder(torch.nn.Module):
  def __init__(self, labels, ignore):
    super().__init__()
    self.labels = labels
    self.ignore = ignore

  def forward(self, emission: torch.Tensor) -> str:
    indices = torch.argmax(emission, dim=-1) 
    indices = torch.unique_consecutive(indices, dim=-1)
    indices = [i for i in indices if i not in self.ignore]
    return ''.join([self.labels[i] for i in indices])

def get_transcript_sr(speech_file):
  r = sr.Recognizer()
  text = 0
  with sr.AudioFile(speech_file) as source:
    audio_data = r.record(source)
    try:
      text = r.recognize_google(audio_data)
    except sr.UnknownValueError:
      text=""
    return text

def get_transcript_model(speech_file):
  torch.random.manual_seed(0)
  device = torch.device('cpu')
  bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
  model = bundle.get_model().to(device)
  waveform, sample_rate = torchaudio.load(speech_file)
  waveform = waveform.to(device)
  if sample_rate != bundle.sample_rate:
    waveform = torchaudio.functional.resample(waveform, sample_rate, bundle.sample_rate)
  with torch.inference_mode():
    emission, _ = model(waveform)

  decoder = GreedyCTCDecoder(
      labels=bundle.get_labels(),
      ignore=(0, 1, 2, 3),
  )
  transcript = decoder(emission[0])
  a=[]

  for i in range (0, len(transcript)):
      if transcript[i] == '|':
          a.append(' ')
      else:
          a.append(transcript[i])
  
  return transcript



def compute_break(src):
  SPEECH_FILE = "test1.wav"
  song = AudioSegment.from_wav(src)
  len_song = len(song)
  intervals = (len_song - len_song % 5000)/5000

  print(intervals)
  if os.path.exists("out_model.srt"):
    os.remove("out_model.srt")
  if os.path.exists("out_library.srt"):
    os.remove("out_library.srt")
  f1 = open("out_model.srt", "w")
  f2 = open("out_library.srt", "w")
  for i in range(0, int(intervals)):
    beg = i * 5000
    end = (i+1) * 5000
    print(beg)
    print(end)
    the_5_seconds = song[beg: end]

    the_5_seconds.export(SPEECH_FILE, format="wav")
    a = get_transcript_model(SPEECH_FILE)
    b= get_transcript_sr(SPEECH_FILE)
    print(a)
    print(b)
    print(" ")
    f1.write(a+" "+str(beg)+" "+str(end)+"\n")
    f2.write(b+" "+str(beg)+" "+str(end)+"\n")
    os.remove(SPEECH_FILE)


  #last_part
  beg = intervals * 5000
  end = len_song
  the_5_seconds = song[beg: end]

  the_5_seconds.export(SPEECH_FILE, format="wav")
  a = get_transcript_model(SPEECH_FILE)
  b= get_transcript_sr(SPEECH_FILE)
  print(a)
  print(b)
  print(" ")
  f1.write(a+" "+str(beg)+" "+str(end)+"\n")
  f2.write(b+" "+str(beg)+" "+str(end)+"\n")
  f1.close()
  f2.close()
  os.remove(SPEECH_FILE)

def break_video(src):
  my_clip = mp.VideoFileClip(src)
  my_clip.audio.write_audiofile("my_result.wav")
  compute_break("my_result.wav")





#compute_break("test111.wav")
  


