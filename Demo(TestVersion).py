## Use the MoviePy package to extract the audio from the video into a required format.
from moviepy.editor import *

fps=44100;  # Set the audio bit rate, 44100Hz is a common high-fidelity MP3 standard.
# If you need to reduce the bandwidth usage, you can reduce this value, but it may affect the accuracy.

# ac = AudioFileClip('S.mp4')
# ac.write_audiofile('Audio.wav',fps=fps, ffmpeg_params=["-ac", "1"])


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
files=os.listdir(path)
lenN=len(files)

for i in range (0,lenN):
    print(files[i])
    ac = AudioFileClip(os.path.join(path,files[i]))
    ac.write_audiofile(files[i]+'Audio.wav', fps=fps, ffmpeg_params=["-ac", "1"])
    trans = transcribe_model_selection(files[i]+'Audio.wav', "default")
    print("Name: "+files[i])
    print("Trans: "+trans)



#
# trans=transcribe_model_selection('Audio.wav',"default")  # Call the above function and get the result.
#
# print(trans)


# # Call Amazon API
# import boto3
#
# #Amazon Key config
# comprehend = boto3.client('comprehend',
#                               region_name = "us-east-2",
#                               aws_access_key_id="AKIA4LSCBOB7257IG4F3",
#                               aws_secret_access_key="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")
# phrases = comprehend.detect_pii_entities(Text=trans, LanguageCode="en")
#
# entities = phrases['Entities']
#
#
# #Save result in 'RstInfo.csv'
# with open('RstInfo.csv', 'w') as f:
#     for entity in entities:
#         f.write(str(entity['Type']))
#         f.write(" : ")
#         f.write(trans[entity['BeginOffset']:entity['EndOffset']])
#         f.write("\n")


path_intro=r"D:\2021 s2\8715\introduction"
files_intro=os.listdir(path_intro)
lenN_intro=len(files_intro)

for i in range (0,lenN_intro):
    print(files_intro[i])
    ac = AudioFileClip(os.path.join(path_intro,files_intro[i]))
    ac.write_audiofile(files_intro[i]+'Audio.wav', fps=fps, ffmpeg_params=["-ac", "1"])
    trans_intro = transcribe_model_selection(files_intro[i]+'Audio.wav', "default")
    print("Name_intro: "+files_intro[i])
    print("Trans_intro: "+trans_intro)