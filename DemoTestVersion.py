## Use the MoviePy package to extract the audio from the video into a required format.
from moviepy.editor import *

fps=44100;  # Set the audio bit rate, 44100Hz is a common high-fidelity MP3 standard.
# If you need to reduce the bandwidth usage, you can reduce this value, but it may affect the accuracy.

# ac = AudioFileClip('S.mp4')
# ac.write_audiofile('Audio.wav',fps=fps, ffmpeg_params=["-ac", "1"])
from age_gender_detect import age_gender_detect

# Call Amazon API
import boto3


## Call Google API
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GCKey.json" # Recall the Google key stored locally



def transcribe_model_selection(speech_file, model):
    """Transcribe the given audio file synchronously with
    the selected model."""

    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=fps,
        language_code="en-US",
        enable_automatic_punctuation=True,
        model=model,

    )

    response = client.recognize(config=config, audio=audio)

    strALl=''

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        strALl+=u"Transcript: {}".format(alternative.transcript);

    return strALl;

path=r"D:\2021 s2\8715\voiceover"
path_intro=r"D:\2021 s2\8715\introduction"

def run_demo_2(path,path_intro):
    fileName_List = []
    vText_List = []
    gender_List = []
    age_List = []
    amazonDir_List = []

    files=os.listdir(path)
    intro_list=os.listdir(path_intro)
    lenN=len(files)

    for i in range (0,lenN):

        fileName_List.append(files[i])
        ac = AudioFileClip(os.path.join(path,files[i]))
        ac.write_audiofile(files[i]+'Audio.wav', fps=fps, ffmpeg_params=["-ac", "1"])
        trans = transcribe_model_selection(files[i]+'Audio.wav', "default")
        vText_List.append(trans)
        intro_Name=files[i].replace("shot7.voiceover", "shot1.introductions",1)
        if intro_Name in intro_list:
            age, gender = age_gender_detect(os.path.join(path_intro, intro_Name), False)
            ac = AudioFileClip(os.path.join(path_intro, intro_Name))
            ac.write_audiofile(intro_Name + 'Audio.wav', fps=fps, ffmpeg_params=["-ac", "1"])
            trans_intro = transcribe_model_selection(intro_Name + 'Audio.wav', "default")
            age_List.append(age)
            gender_List.append(gender)

            comprehend = boto3.client('comprehend',
                                      region_name="us-east-2",
                                      aws_access_key_id="AKIA4LSCBOB7257IG4F3",
                                      aws_secret_access_key="JI4aKwp9CqZpVWGC86zmlFACV6M7E29o3CAolimr")

            if trans_intro=="":
                trans_intro="dummy"
            phrases = comprehend.detect_pii_entities(Text=trans_intro, LanguageCode="en")

            entities = phrases['Entities']
            amazonDir_List.append(entities)
        else:
            age_List.append("No intro clip to detect")
            gender_List.append("No intro clip to detect")
            amazonDir_List.append("No intro clip to detect")
        print("\n\n\n")

    return fileName_List,vText_List,gender_List,age_List,amazonDir_List





