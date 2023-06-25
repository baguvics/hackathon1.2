import os
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
  
    frame_skip = int(fps * int(frame_time))                # Количество кадров, после которых будет извлекаться важный кадр
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

        frame_diff = cv2.absdiff(frame, prev_frame)     # Вычисляем разницу между текущим и предыдущим кадром
        diff_mean = frame_diff.mean()                   # Среднее значение разницы

        if diff_mean == 0:
            unchanged_frames += 1
        else:
            unchanged_frames = 0

        if unchanged_frames >= frame_skip and frame.tostring() not in saved_frames:
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")  # Путь к файлу кадра
            cv2.imwrite(frame_filename, frame)                                        # Сохраняем кадр в файл
            saved_frames.add(frame.tostring())
            for chunk in range(len(chunk_timings)):
                if frame_count/fps < chunk_timings[chunk] and f"frame_{frame_count}.jpg" not in frames_array:
                    if chunk != 0 and frame_count/fps > chunk_timings[chunk-1]:
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

    title = str(strftime("%a%d%b%Y%H%M%S", gmtime()))
    file_dir = "hackathon1.2/back_end/youtube/{}.mp4".format(title)
    print(file_dir)
    if video_file is None:
        youtube_video_content = YouTube(video_url)
        youtube_video_content.title = str(strftime("%a%d%b%Y%H%M%S", gmtime()))
        high_res_streams = youtube_video_content.streams.filter(progressive=True, file_extension='mp4')
        sorted_streams = high_res_streams.order_by('resolution').desc()
        best_stream = sorted_streams.first()
        print(best_stream)
        best_stream.download("hackathon1.2/back_end/youtube")
        video_duration = youtube_video_content.length
        

    else:
        pass
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
    text_from_video_lenght = len(result["text"])
    print(f"длина текста из видева {text_from_video_lenght}")
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

    if article_size == 0 or article_size > text_from_video_lenght:
        article_size = text_from_video_lenght
    ai_chunk_size = int((article_size/chunks_quantity)/2)
    titles_of_summaries = []
    summary_text = []
    openai.api_key = "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"
    prompt = "перепиши текст чтобы получилось {} символов и в начале придумай заголок в кавычках для текста в 1 предложение."
    chunk_id = 0
    for paragraph in chunks:
        chunk_id += 1
        text = prompt.format(ai_chunk_size) + paragraph
        summary = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            max_tokens=ai_chunk_size,
            temperature=0.1
        )
        # Извлечение заголовка
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
    
    
    frame_time = 3
    output_folder = r"hackathon1.2/back_end/frames/"
    
    frames = frame_extrude(file_dir, frame_time, output_folder, chunk_timings)
    print(summary_text, titles_of_summaries, chunks_timings, frames)

    return summary_text, titles_of_summaries, chunks_timings, frames


create_article(video_url="https://www.youtube.com/watch?v=TpIrJmVwfBo", video_file=None, start_time=0, power=2, end_time=0, add_time=0, article_size=0)





