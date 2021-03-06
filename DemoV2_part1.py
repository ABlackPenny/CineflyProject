## Use the MoviePy package to extract the audio from the video intro a required format.
from moviepy.editor import *

fps = 44100;  # Set the audio bit rate, 44100Hz is a common high-fidelity MP3 standard.
# If you need to reduce the bandwidth usage, you can reduce this value, but it may affect the accuracy.

# ac = AudioFileClip('S.mp4')
# ac.write_audiofile('Audio.wav',fps=fps, ffmpeg_params=["-ac", "1"])
from age_gender_detect import age_gender_detect

# Call Amazon API
import boto3

## Call Google API
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GCKey.json"  # Recall the Google key stored locally


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

    strALl = ''

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        strALl += u"Transcript: {}".format(alternative.transcript);

    return strALl;


def run_demo_2(path, path_intro):
    fileName_List = []
    vText_List = []
    gender_List = []
    age_List = []
    amazonDir_List = []

    files = os.listdir(path)

    for filename in files:
        portion = os.path.splitext(filename)
        if portion[1] != ".mp4":
            newname = portion[0] + ".mp4"
            filename = os.path.join(path, filename)
            newname = os.path.join(path, newname)
            os.rename(filename, newname)

    intro_list = os.listdir(path_intro)

    for filename in intro_list:
        portion = os.path.splitext(filename)
        if portion[1] != ".mp4":
            newname = portion[0] + ".mp4"
            filename = os.path.join(path_intro, filename)
            newname = os.path.join(path_intro, newname)
            os.rename(filename, newname)

    lenN = len(files)

    for i in range(0, lenN):
        try:
            fileName_List.append(files[i])
            ac = AudioFileClip(os.path.join(path, files[i]))
            ac.write_audiofile(files[i] + 'Audio.wav', fps=fps, ffmpeg_params=["-ac", "1"])
            trans = transcribe_model_selection(files[i] + 'Audio.wav', "default")
            vText_List.append(trans)
            intro_Name = files[i].replace("shot7.voiceover", "shot1.introductions", 1)
            if intro_Name in intro_list:
                age, gender = age_gender_detect(os.path.join(path_intro, intro_Name), False)
                ac = AudioFileClip(os.path.join(path_intro, intro_Name))
                ac.write_audiofile(intro_Name + 'Audio.wav', fps=fps, ffmpeg_params=["-ac", "1"])
                trans_intro = transcribe_model_selection(intro_Name + 'Audio.wav', "default")
                age_List.append(age)
                gender_List.append(gender)

                comprehend = boto3.client('comprehend',
                                          region_name="",
                                          aws_access_key_id="",
                                          aws_secret_access_key="")

                if trans_intro == "":
                    trans_intro = "Empty"
                phrases = comprehend.detect_pii_entities(Text=trans_intro, LanguageCode="en")

                entities = phrases['Entities']
                entities.append(trans_intro)

                amazonDir_List.append(entities)
            else:
                age_List.append("No intro clip to detect")
                gender_List.append("No intro clip to detect")
                amazonDir_List.append("No intro clip to detect")
            print("\n\n\n")
        except:
            age_List.append("Video file is damaged or format is not supported")
            gender_List.append("Video file is damaged or format is not supported")
            amazonDir_List.append("Video file is damaged or format is not supported")
            vText_List.append("Video file is damaged or format is not supported")
            entities = [{"dummy": "dummy"}]
            amazonDir_List.append(entities)
            continue

    return fileName_List, vText_List, gender_List, age_List, amazonDir_List
