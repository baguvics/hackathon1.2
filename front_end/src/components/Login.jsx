import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ onLogin }) => {

  const APILogin = 'http://127.0.0.1:8000/api/v1/login/'

  // Состояния полей формы
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Состояние для отображения сообщения об ошибке авторизации
  const [loginError, setLoginError] = useState('');

  const handleLogin = () => {
    axios
      .post(APILogin, { username, password })
      .then(response => {
        console.log(response.data);
        if (response.data.success) {
          setLoginError('');
          
          const userId = response.data.id;  // Получение ID пользователя из ответа сервера
          onLogin(userId); // Вызов функции onLogin после успешной авторизации
        } else {
          setLoginError('Неправильное имя пользователя или пароль');
        }
      })
      .catch(error => {
        console.error(error);
        setLoginError('Произошла ошибка при авторизации. Попробуйте еще раз.');
      });
  };

  return (
    <div>
      <h1>Login Form</h1>
      <input type="text" placeholder="Логин" value={username} onChange={e => setUsername(e.target.value)} />
      <br />
      <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} />
      <br />
      <button onClick={handleLogin}>Login</button>
      {loginError && <span className="error">{loginError}</span>}
    </div>
  );
};

export default Login;
