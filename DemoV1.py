## Use the MoviePy package to extract the audio from the video intro a required format.
from moviepy.editor import *

fps=44100;  # Set the audio bit rate, 44100Hz is a common high-fidelity MP3 standard.
# If you need to reduce the bandwidth usage, you can reduce this value, but it may affect the accuracy.

ac = AudioFileClip('S.mp4')
ac.write_audiofile('Audio.wav',fps=fps, ffmpeg_params=["-ac", "1"])


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


trans=transcribe_model_selection('Audio.wav',"default")  # Call the above function and get the result.

print(trans)


# Call Amazon API
import boto3

#Amazon Key config
comprehend = boto3.client('comprehend',
                              region_name = "us-east-2",
                              aws_access_key_id="AKIA4LSCBOB7257IG4F3",
                              aws_secret_access_key="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")
phrases = comprehend.detect_pii_entities(Text=trans, LanguageCode="en")
# for i in range(0,len(phrases['Entities'])):
#     print((phrases['KeyPhrases'][i]['Text']))
# print(phrases)

entities = phrases['Entities']
# print(entities)

#Save result in 'RstInfo.csv'
with open('RstInfo.csv', 'w') as f:
    for entity in entities:
        f.write(str(entity['Type']))
        f.write(" : ")
        f.write(trans[entity['BeginOffset']:entity['EndOffset']])
        f.write("\n")
