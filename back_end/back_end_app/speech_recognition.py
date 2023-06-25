# -*- coding: utf-8 -*-
import os
from moviepy.editor import VideoFileClip
import cv2
import re
import whisper
import ssl
from pytube import YouTube
from time import gmtime, strftime
import openai


# Генерация кадров для статьи
def frame_extrude(video_path, frame_time, output_folder, chunk_timings: list):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)

    frame_skip = int(fps * int(frame_time))  # Количество кадров, после которых будет извлекаться важный кадр
    prev_frame = None
    unchanged_frames = 0
    frame_count = 0
    saved_frames = set()
    print(fps)
    frames_array = [[] for i in range(len(chunk_timings))]

    while True:
        ret, frame = video.read()

        if not ret:
            break

        if prev_frame is None:
            prev_frame = frame
            continue

        frame_diff = cv2.absdiff(frame, prev_frame)  # Вычисляем разницу между текущим и предыдущим кадром
        diff_mean = frame_diff.mean()  # Среднее значение разницы

        if diff_mean == 0:
            unchanged_frames += 1
        else:
            unchanged_frames = 0

        if unchanged_frames >= frame_skip and frame.tostring() not in saved_frames:
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")  # Путь к файлу кадра
            cv2.imwrite(frame_filename, frame)  # Сохраняем кадр в файл
            saved_frames.add(frame.tostring())
            for chunk in range(len(chunk_timings)):
                if frame_count / fps < chunk_timings[chunk] and f"frame_{frame_count}.jpg" not in frames_array:
                    if chunk != 0 and frame_count / fps > chunk_timings[chunk - 1]:
                        frames_array[chunk].append(f"frame_{frame_count}.jpg")
                        print(frames_array)
                    elif chunk == 0:
                        frames_array[chunk].append(f"frame_{frame_count}.jpg")
                        print(frames_array)

        prev_frame = frame
        frame_count += 1

    # Проверка и заполненение пустых массивов с картинками
    for i in range(len(frames_array)):
        if len(frames_array[i]) == 0:
            frame_position = int(chunk_timings[i] * fps)
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
            ret, frame = video.read()
            if ret:
                frame_filename = os.path.join(output_folder, f"frame_{frame_position}.jpg")
                cv2.imwrite(frame_filename, frame)
                frames_array[i].append(f'frame_{frame_position}.jpg')

    video.release()
    print(frames_array)
    return frames_array


# Генерация статьи
def create_article(video_url, power, start_time, end_time, add_time, video_file, article_size):
    ssl._create_default_https_context = ssl._create_unverified_context
    file_dir = ''
    video_title = ''
    video_duration = 0
    if video_file is None:
        youtube_video_content = YouTube(video_url)
        video_title = youtube_video_content.title
        youtube_video_content.title = str(strftime("%a%d%b%Y%H%M%S", gmtime()))
        file_dir = "back_end/youtube/{}.mp4".format(youtube_video_content.title)
        high_res_streams = youtube_video_content.streams.filter(progressive=True,
                                                                file_extension='mp4')  # progressive=True filters streams with audio and video
        sorted_streams = high_res_streams.order_by('resolution').desc()  # sorting by best quality
        best_stream = sorted_streams.first()
        print(best_stream)
        best_stream.download("back_end/youtube")
        video_duration = youtube_video_content.length

    else:
        video_title = video_file.name
        print("title ", video_title)
        file_dir = f'back_end_app/back_end/user/{video_title}'
        video_clip = VideoFileClip(file_dir)
        video_duration = video_clip.duration
        print("Video Title:", video_title)
        print("File Directory:", file_dir)
        print("Video Duration:", video_duration)

    model_size = {
        0: "tiny",
        1: "small",
        2: "medium",
    }

    model = whisper.load_model(model_size.get(power))

    result = model.transcribe(file_dir, verbose=True, fp16=False, language="Russian")
    print(result["text"])

    for segment in result["segments"]:
        print(str(strftime('%H:%M:%S', gmtime(int(segment["start"])))) + segment["text"])

    text_from_video = result["text"]
    text_from_video_length = len(result["text"])
    print(f"длина текста из видева {text_from_video_length}")
    chunk_size = 700

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

    # Находим тайминги для каждого чанка
    chunks_timings = []
    chunk_timings = []
    print(f"все чанки!!! *{chunks}*")
    for chunk in chunks:
        for segment in result["segments"]:

            if segment["text"][:7] == chunk[:7]:
                timing = str(strftime('%H:%M:%S', gmtime(int(segment["start"]))))
                chunks_timings.append(timing)
                if int(segment["start"]) != 0:
                    chunk_timings.append(int(segment["start"]))
                print("chunk number ", len(chunks_timings), " timing: ", timing)
                break

    chunk_timings.append(int(video_duration))

    chunks_quantity = len(chunks_timings)
    print(f"колво абзацев: {chunks_quantity}")

    if article_size == 0 or article_size > text_from_video_length:
        article_size = text_from_video_length
    ai_chunk_size = int((article_size / chunks_quantity) / 2)
    titles_of_summaries = []
    summary_text = []
    openai.api_key = "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"
    prompt = "перепиши текст в стилистике статьи чтобы получилось {} символов и до конца осмысленного предложения и в начале придумай заголок в кавычках для текста в 1 предложение."
    chunk_id = 0
    for paragraph in chunks:  # openai requests in cycle for every chunk
        chunk_id += 1
        text = prompt.format(ai_chunk_size) + paragraph
        summary = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            max_tokens=ai_chunk_size,
            temperature=0.1
        )
        # splitting titles and body
        ai_output = summary['choices'][0]['text']
        text_utf8 = ai_output.encode('utf-8')
        text_without_newline = re.sub(b'\n', b'', text_utf8)

        text_decoded = text_without_newline.decode('utf-8')
        match = re.search(r'"(.*?)"', text_decoded)
        title_of_chunk = ""
        if match:
            title_of_chunk = match.group(1)
            print("заголовок " + title_of_chunk)
        else:
            print("No match found.")

        body = text_decoded[len(title_of_chunk) + 2:]
        titles_of_summaries.append(title_of_chunk)
        summary_text.append(body)
        print(summary['choices'][0]['text'])

    messages = [{"role": "user", "content": f"Напиши аннотацию в 3-4 предложения из следующего текста {summary_text}"}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    )
    annotation = response["choices"][0]["message"]["content"]

    frame_time = 3
    output_folder = r"hackathon1.2/back_end/frames/"
    for timing_id in range(len(chunks_timings)):
        if chunks_timings[timing_id] != chunks_timings[-1]:
            chunks_timings[timing_id] = f"{chunks_timings[timing_id]}-{chunks_timings[timing_id+1]}"
        else:
            chunks_timings[timing_id] = f"{chunks_timings[timing_id]}-{str(strftime('%H:%M:%S', gmtime(int(video_duration))))}"

    frames = frame_extrude(file_dir, frame_time, output_folder, chunk_timings)
    print(f"Статья по видео - {video_title}", annotation,
          summary_text, titles_of_summaries, chunks_timings, frames)

    return {
        'title_of_article': f"Статья по видео - {video_title}",
        'annotation': annotation,
        'summary': summary_text,
        'titles': titles_of_summaries,
        'timings': chunks_timings,
        'frames': frames
    }

