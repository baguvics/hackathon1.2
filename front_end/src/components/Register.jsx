import axios from 'axios';
import React, { useState } from 'react';
import validator from 'validator';

const Register = ({ onRegister }) => {

  const APIRegister = 'http://127.0.0.1:8000/api/v1/register/';

  // Состояния полей формы
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [first_name, setFirstname] = useState('');
  const [email, setEmail] = useState('');

  // Состояние для отображения ошибки валидации email
  const [emailError, setEmailError] = useState('');

  // Состояние для отображения сообщения об успешной регистрации
  const [registrationSuccess, setRegistrationSuccess] = useState('');

  // Состояние для отображения сообщения об ошибке регистрации
  const [registrationError, setRegistrationError] = useState('');

  const handleRegister = () => {
    // Проверка валидности email
    if (!validator.isEmail(email)) {
      setRegistrationError('');
      setEmailError('Некорректный email');
      return;
    } else {
      setEmailError('');
    }

    // Отправка запроса на регистрацию
    axios
      .post(APIRegister, { username, password, first_name, email })
      .then(response => {
        console.log(response.data);
        if (response.data.success) {
          setRegistrationSuccess('Регистрация прошла успешно!');
          setRegistrationError('');
          
          const userId = response.data.id; // Получение ID пользователя из ответа сервера
          onRegister(userId); // Вызов функции onRegister после успешной регистрации
        } else if (response.data.error == 'User with this email already exists.') {
          setRegistrationSuccess('');
          setRegistrationError('Пользователь с такой почтой уже существует');
        }
        else{
          setRegistrationSuccess('');
          setRegistrationError('Произошла ошибка при регистрации. Попробуйте еще раз.');
        }
      })
      .catch(error => {
        console.error(error);
        setRegistrationSuccess('');
        setRegistrationError('Произошла ошибка при регистрации. Попробуйте еще раз.');
      });
  };

  return (
    <div>
      <h1>Registration Form</h1>
      <input type="text" placeholder="Логин" value={username} onChange={e => setUsername(e.target.value)} />
      <br />
      <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} />
      <br />
      <input type="text" placeholder="Имя" value={first_name} onChange={e => setFirstname(e.target.value)} />
      <br />
      <input type="text" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      {emailError && <span className="error">{emailError}</span>}
      {registrationSuccess && <span className="success">{registrationSuccess}</span>}
      {registrationError && <span className="error">{registrationError}</span>}
      <br />
      <button onClick={handleRegister}>Register</button>
    </div>
  );
};

export default Register;
