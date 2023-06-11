import React, { useState } from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Home from './components/Home';

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
    <div className='container'>
      <header className='header'>
        <Link to="/register" className='register'>Register</Link>
          <br />
        <Link to="/login" className='login'>Login</Link>
      </header>


      <Routes>
        <Route
          path="/register"
          element={<Register onRegister={handleRegister} />}
        />
        <Route
          path="/login"
          element={<Login onLogin={handleLogin} setError={setLoginError} />}
        />
        <Route path="" element={<Home />} />
      </Routes>
      {isLoggedIn && (
        <div>
          <h2>Добро пожаловать! Вы успешно авторизованы.</h2>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </div>
    </>
  );
}

export default App;
