import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/articlForm.css'

const ArticleForm = () => {
    const APIGetTimeVideo = 'http://127.0.0.1:8000/api/v1/get_video_duration/'; // API для получения длительности видео
    const APIGetArticle = 'http://127.0.0.1:8000/api/v1/article/';              // API для получения статьи

    const [videoUrl, setVideoUrl] = useState('');               // URL видоса
    const [videoDuration, setVideoDuration] = useState('s');    // Полученная длительнотсь видео
    const [power, setPower] = useState(0);                      // Выбор мощности
    const [addTime, setAddTime] = useState(false);              // Выбор времени если нужно
    const [startTime, setStartTime] = useState(0);              // Начало видео
    const [endTime, setEndTime] = useState(0);                  // Конец видео

    const handleSubmit = async (e) => {
        if (endTime == 0){
            setEndTime(videoDuration);
        }
        e.preventDefault();
        // POST-запрос для получения статьи
        const response = await axios.post(APIGetArticle, {
        videoUrl,
        videoDuration,
        power,
        addTime,
        startTime,
        endTime,
        });
        console.log(response.data)
    };

    const fetchVideoDuration = async () => {
        // POST-запрос для получения длительности видео
        try {
          const response = await axios.post(`${APIGetTimeVideo}${encodeURIComponent(videoUrl)}/`);
          setVideoDuration(response.data.duration);
          console.log(response.data.duration);
        } catch (error) {
          console.error(error);
        }
      };
          

    useEffect(() => {
        if (addTime) {
        if (startTime > endTime) {
            setEndTime(startTime);
        }
        }
    }, [addTime, startTime, endTime]);

    return (
        <div className='content_articlForm'>
            <br />
            {/* URL видео */}
            <label htmlFor="videoUrl" className='videoUrl'>Ссылка на видео из YouTube:</label>
            <input
            type="text"
            id="videoUrl"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            />
            <button type="button" onClick={fetchVideoDuration}>
            Отправить
            </button>

            <br />
            {/* Выбор мощности */}
            <label htmlFor="power" className='power'>Мощность:</label>
            <select id="power" onChange={(e) => setPower(parseInt(e.target.value))}>
                <option value={0}>Мощно</option>
                <option value={1}>Среднее</option>
                <option value={2}>Быстро</option>
            </select>

            <br />
            {/* Добавления времени  */}
            <label className='addTime'>
            Исправить начало и конец видео?
            <input
                type="checkbox"
                checked={addTime}
                onChange={(e) => setAddTime(e.target.checked)}
            />
            </label>

            {/* Появление ползунков для выбора времени видео */}
            {addTime && (
            <div>
                <label htmlFor="startTime" className='startTime'>Начальное время (в секундах):</label>
                <input
                type="range"
                id="startTime"
                min={0}
                max={videoDuration}
                value={startTime}
                onChange={(e) => setStartTime(parseInt(e.target.value))}
                />

                <label htmlFor="endTime" className='endTime'>Конечное время:</label>
                <input
                type="range"
                id="endTime"
                min={0}
                max={videoDuration}
                value={endTime}
                onChange={(e) => setEndTime(parseInt(e.target.value))}
                />
            </div>
            )}

            <br />
            <button onClick={handleSubmit}>Отправить</button>
        </div>
    );
};

export default ArticleForm;
