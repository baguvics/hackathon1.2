import whisper
import ssl
from pytube import YouTube
from time import gmtime, strftime
import os
import openai


def create_article(url, timing):
    ssl._create_default_https_context = ssl._create_unverified_context

    youtube_video_url = "https://www.youtube.com/watch?v=FX0s2tK-KU8"
    youtube_video_content = YouTube(youtube_video_url)
    youtube_video_content.title = str(strftime("%a%d%b%Y%H%M%S", gmtime()))
    title = youtube_video_content.title

    audio_streams = youtube_video_content.streams.filter(only_audio=True)
    audio_stream = audio_streams[1]
    audio_stream.download("youtube")

    # ffmpeg -ss 1924 -i "/content/earnings_call_microsoft_q4_2022.mp4/Microsoft (MSFT) Q4 2022 Earnings Call.mp4" -t 2515 "earnings_call_microsoft_q4_2022_filtered.mp4"

    model = whisper.load_model("small")

    result = model.transcribe("youtube/{}.mp4".format(title), verbose=True, fp16=True)
    print(result["text"])

    api_key = "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"
    openai.api_key = api_key

    text = "summarize next text from video." + result['text']

    summary = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        max_tokens=2000,
        temperature=0.3
    )

    print(summary['choices'][0]['text'])

# # load audio and pad/trim it to fit 30 seconds
# audio = whisper.load_audio("ya-pomnyu-chudnoe-mgnovenie.mp3")
# audio = whisper.pad_or_trim(audio)

# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)

# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")

# # decode the audio
# options = whisper.DecodingOptions(fp16 = False)
# result = whisper.decode(model, mel, options)

# # print the recognized text
# print(result.text)
