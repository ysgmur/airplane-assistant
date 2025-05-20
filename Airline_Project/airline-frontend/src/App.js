import React, { useState } from 'react';
import LoginPage from './components/LoginPage';
import ChatBot from './components/ChatBot';

function App() {
  const [user, setUser] = useState(localStorage.getItem("username"));

  return (
    <div>
      {user ? <ChatBot username={user} /> : <LoginPage onLogin={setUser} />}
    </div>
  );
}

export default App;
