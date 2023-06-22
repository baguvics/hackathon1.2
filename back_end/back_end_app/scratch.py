import re

import whisper
import ssl
from pytube import YouTube
from time import gmtime, strftime
import openai


paragraph_quantity = 7

ssl._create_default_https_context = ssl._create_unverified_context

youtube_video_content = YouTube("https://www.youtube.com/watch?v=gfUlCnMrZbw")
youtube_video_content.title = str(strftime("%a%d%b%Y%H%M%S", gmtime()))
title = youtube_video_content.title

high_res_streams = youtube_video_content.streams
print(high_res_streams)
high_res_stream = high_res_streams[1]
high_res_stream.download("youtube")
YOUR_FILE = "youtube/{}.mp4".format(title)

# probe = ffmpeg.probe(YOUR_FILE)
# time = float(probe['streams'][0]['duration']) // 2
# width = probe['streams'][0]['width']


model = whisper.load_model("small")

result = model.transcribe("youtube/{}.mp4".format(title), verbose=True, fp16=False, language="russian")
print(result["text"])

for segment in result["segments"]:
    print("{}:{}".format(segment["start"]//60, int(segment["start"]) & 60) + "  " + segment["text"])

text_from_video = result["text"]
chunk_size = 1500

sentences = re.findall(r'[^.!?]+[.!?]', text_from_video)
chunks = []

current_chunk = ''
for sentence in sentences:
    if len(current_chunk) + len(sentence) <= chunk_size:
        current_chunk += sentence
    else:
        chunks.append(current_chunk)
        current_chunk = sentence

# Добавляем последний кусок текста
if current_chunk:
    chunks.append(current_chunk)

chunks_timings = []
# Находим тайминги для каждого чанка

i=0
for chunk in chunks:
    i+=1
    for segment in result["segments"]:
        if segment["text"][:7] == chunk[:7]:
            chunks_timings.append(segment["start"])
            print("chunk number ", i, " timing: ", segment["start"])



summary_text = []
openai.api_key = "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"
prompt = "напиши абзац {} по следующему тексту из видео."
chunk_id = 0
for paragraph in chunks:
    chunk_id += 1
    text = prompt.format(chunk_id) + paragraph
    summary = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        max_tokens=2000,
        temperature=0.3
    )
    summary_text.append({"paragraph {}".format(chunk_id): summary['choices'][0]['text']})
    print(summary['choices'][0]['text'])
print(summary_text)




# text = "summarize next text in 5 paragraphs for the article in 1500 words." + result['text']
# summary = openai.Completion.create(
#     model="text-davinci-003",
#     prompt=text,
#     max_tokens=2000,
#     temperature=0.3
# )
#
# print(summary['choices'][0]['text'])

# # Set how many spots you want to extract a video from.
# parts = 7
#
# intervals = time // parts
# intervals = int(intervals)
# interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
# i = 0
#
# for item in interval_list:
#     (
#         ffmpeg
#         .input(YOUR_FILE, ss=item[1])
#         .filter('scale', width, -1)
#         .output('Image' + str(i) + '.jpg', vframes=1)
#         .run()
#     )
#     i += 1
#
#
