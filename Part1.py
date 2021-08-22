from moviepy.editor import *

video = VideoFileClip('1.mov')
audio = video.audio
audio.write_audiofile('a.mp3')

def transcribe_model_selection(speech_file, model):
    """Transcribe the given audio file synchronously with
    the selected model."""
    import google.cloud.speech as speech

    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model=model,
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        print(u"Transcript: {}".format(alternative.transcript))

transcribe_model_selection('a.mp3',"default")
