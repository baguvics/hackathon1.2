import React, { useState } from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Home from './components/Home';
import ArticleForm from './components/ArticlForm';
import './css/App.css'
import logo from './img/logo.png';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginError, setLoginError] = useState('');
  const navigate = useNavigate();
  const [userId, setUserId] = useState(null);

  const handleLogin = id => {
    setUserId(id)
    setIsLoggedIn(true);
    setLoginError('');
    navigate('');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  const handleRegister = () => {
    setIsLoggedIn(true);
    setLoginError('');
    navigate('');
  };

  return (
    <>
      <div className='app'>
        <header className='header'>
          <div className='header-left'>
            <div className='logo'>
              <img src = {logo} width='170px' className='logo'></img>
              {/* <svg width="200px" height="100px" viewBox="0 0 100 100">
                <image xlinkHref={logo} width="100" height="100" />
              </svg> */}
            </div>
          </div>
          <div className='header-right'>
            <div className='register-container'>
              <Link to="/register" className='register-link'>Регистрация</Link>
            </div>
            <div className='login-container'>
              <Link to="/login" className='register-link'>Авторизация</Link>
            </div>
          </div>
        </header>

        <div className='container'>
            <Routes>
              <Route
                path="/register"
                element={<Register onRegister={handleRegister} />}
              />
              <Route
                path="/login"
                element={<Login onLogin={handleLogin} setError={setLoginError} />}
              />
              <Route 
              path=''
              element ={<ArticleForm/>}
              />
            </Routes>
        </div>
      </div>


    </>
  );
}

export default App;
