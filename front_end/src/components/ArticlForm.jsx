import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/articlForm.css'


const ArticleForm = () => {
    const APIGetTimeVideo = 'http://127.0.0.1:8000/api/v1/get_video_duration/'; // API для получения длительности видео
    const APIGetArticle = 'http://127.0.0.1:8000/api/v1/article/';              // API для получения статьи

    const [videoUrl, setVideoUrl] = useState('');               // URL видоса
    const [videoDuration, setVideoDuration] = useState('');     // Полученная длительнотсь видео
    const [power, setPower] = useState(2);                      // Выбор мощности
    const [addTime, setAddTime] = useState(false);              // Выбор времени если нужно
    const [startTime, setStartTime] = useState(0);              // Начало видео
    const [endTime, setEndTime] = useState(0);                  // Конец видео
    const [settings, setSettings] = useState(false);            // Дополнительные настройки
    const [article, setArticle] = useState(null);               // Статья
    const [timings, setTimings] = useState('');                 // Тайминги
    const [isLoading, setIsLoading] = useState(false);          // Состояние загрузки статьи
    const [frames, setFrames] = useState(null)                  // Кадры статьи
    const [videoFile, setVideoFile] = useState(null);           // Видео файл
    const [titleOfArticle, setTitleOfArticle] = useState(null); // Название статьи
    const [annotation, setAnnotation] = useState(null);         // Аннотация статьи
    const [titles, setTitles] = useState(null);                 // Заголовки абзацев
    const [symbol, setSymbol] = useState(0);                   // Количество символов для статьи



    const handleSubmit = async (e, videoFile) => {
        e.preventDefault();
        setIsLoading(true);
        console.log(videoFile)
        if (endTime === 0) {
          setEndTime(videoDuration);
        }
        console.log('Файл загружен:', videoFile);
        
        // Создание экземпляра FormData
        const formData = new FormData();
        
        // Добавление данных в FormData
        formData.append('videoUrl', videoUrl);
        formData.append('videoFile', videoFile);
        formData.append('videoDuration', videoDuration);
        formData.append('power', power);
        formData.append('addTime', addTime);
        formData.append('startTime', startTime);
        formData.append('endTime', endTime);
        formData.append('article_size', symbol);
        
        // POST-запрос для получения статьи
        try {
          const response = await axios.post(APIGetArticle, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          
          setArticle(response.data.summary);
          setTimings(response.data.timings);
          setFrames(response.data.frames);
          setTitleOfArticle(response.data.title_of_article);
          setTitles(response.data.titles);
          setAnnotation(response.data.annotation);
          console.log(response.data);
          console.log(response.data.frames);

        } catch (error) {
          console.error(error);
          setIsLoading(false);
        }
      };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setVideoFile(file);
        
      };

    const fetchVideoDuration = async () => {
        // POST-запрос для получения длительности видео
        try {
          const response = await axios.post(`${APIGetTimeVideo}${encodeURIComponent(videoUrl)}/`);
          setVideoDuration(response.data.duration);
          setSettings(true)
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
            <section className='first-section'>
                <div className='welcome'>
                    <h2>КОНВЕРТЕР ВИДЕО</h2>
                    <h3>создает_статью_из_видео</h3>
                    <button className='glowing-btn' >
                        <a href='#second-section' className='link'><span className='glowing-txt'>C<span className='faulty-letter'>L</span>ICK</span></a>
                    </button>
                </div>
            </section>
            <br />
            {/* URL видео */}
            <section className='second-section' id='second-section'>
                {isLoading == false && article == null && (
                    <div>
                        <div htmlFor="videoUrl" className='videoUrl'>Ссылка на видео из YouTube:</div>
                        <input className='input_videoUrl'
                        type="text"
                        id="videoUrl"
                        value={videoUrl}
                        onChange={(e) => setVideoUrl(e.target.value)}
                        />

                        <div className='imputVideo'>
                            <input type="file" id='uploadBtn' name="videoFile" accept="video/*" onChange={handleFileChange} />
                            <label htmlFor='uploadBtn'>Загрузить свой файл</label>
                        </div>

                        <div className='settings'>
                        Дополнительные настройки
                        <input
                            type="checkbox"
                            className='checkbox'
                            onClick={fetchVideoDuration}
                        />
                        </div>

                        {settings && (
                            <div>
                            {/* Выбор мощности */}
                            <div htmlFor="power" className='power'>Скорость обработки голоса:</div>
                                <select id="power" className="power-select" onChange={(e) => setPower(parseInt(e.target.value))}>
                                    <option value={0}>Быстрро, возможны потери в качестве</option>
                                    <option value={1}>Среднее значение</option>
                                    <option value={2}>Полная обработка голоса(рекомендуется)</option>
                                </select>
                            
                            <div className='symbol'>
                                <div className='text_symbol'>
                                    Введите желаемое количество символов для статьи
                                </div>
                                <input className='input_symbol'
                                type="text"
                                id="input_symbol"
                                value={symbol}
                                onChange={(e) => setSymbol(e.target.value)}
                            />
                            </div>

                            {/* Добавления времени  */}
                            <div className='addTime'>
                            Исправить начало и конец видео?
                            <input
                            className='checkbox'
                                type="checkbox"
                                checked={addTime}
                                onChange={(e) => setAddTime(e.target.checked)}
                            />
                            </div>

                            {/* Появление ползунков для выбора времени видео */}
                            {addTime && (
                                <div>
                                    <div htmlFor="startTime" className='startTime'>Начальное время (в секундах):</div>
                                    <input
                                    type="range"
                                    id="startTime"
                                    min={0}
                                    max={videoDuration}
                                    value={startTime}
                                    onChange={(e) => setStartTime(parseInt(e.target.value))}
                                    />
                                    <span className="slider-value">{startTime}</span>

                                    <div htmlFor="endTime" className='endTime'>Конечное время:</div>
                                    <input
                                    type="range"
                                    id="endTime"
                                    min={0}
                                    max={videoDuration}
                                    value={endTime}
                                    onChange={(e) => setEndTime(parseInt(e.target.value))}
                                    />
                                    <span className="slider-value">{endTime}</span>
                                </div>
                            )}

                            </div>
                        )}
                        <button className='btn_articl' onClick={(e) => {handleSubmit(e, videoFile)}}>Получить статью</button>
                    </div>
                )}

                {/*Демонстрация ползунка загрузки*/ }
                {isLoading && article === null && (
                    <div>
                        Ползунок загрузки
                    </div>
                )}

                {/*Демонстрация статьи*/ }
                {article != null && (
                    
                    <div className='article'>
                        
                    <div className='titleArticle'>{titleOfArticle}</div>
                    <div className='annotation'>
                        <p className='p_annotation'>Аннотация:</p>
                        {annotation}
                    </div>

                    {titles.map((title, index) => (
                    <div key={index}>
                        <div className='articleText' contentEditable>
                        <div className='articleTitle' contentEditable>{title}</div>
                        <div className='articleTiming' contentEditable>Timing: {timings[index]}</div>
                        <div className='articleSumary' contentEditable>{article[index]}</div>
                        </div>

                        <div className='articleFrames'>
                        {frames[index].map((frame, frameIndex) => (
                            <img key={frameIndex} src={'/frames/' + frame} className='articleImage' />
                        ))}
                        </div>

                    </div>
                    ))}
                </div>
                )}

            </section>
        </div>
    );
};

export default ArticleForm;
