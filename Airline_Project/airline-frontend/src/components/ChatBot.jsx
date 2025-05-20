// src/components/ChatBot.jsx
import React, { useState, useEffect } from 'react';
import { collection, addDoc, onSnapshot, query, orderBy } from 'firebase/firestore';
import { db } from '../firebase/firebase'; // 🔥 sadece bu import yeterli

function ChatBot({ username }) {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);

  useEffect(() => {
    const q = query(collection(db, 'chat'), orderBy('timestamp'));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const messages = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setChat(messages);
    });
    return () => unsubscribe();
  }, []);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const token = localStorage.getItem('token');
    await addDoc(collection(db, 'chat'), {
      message,
      token,
      processed: false,
      timestamp: new Date()
    });

    setMessage('');
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>✈️ Airline Chat Assistant</h2>
      <div style={{ height: 300, overflowY: 'scroll', border: '1px solid #ccc', marginBottom: 10 }}>
        {chat.map((msg, idx) => (
          <div key={idx}>
            <p><b>💬 {msg.message}</b></p>
            {msg.response && (
              <pre style={{ color: 'green' }}>{JSON.stringify(msg.response, null, 2)}</pre>
            )}
            <hr />
          </div>
        ))}
      </div>
      <input
        placeholder="Type a message..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ width: '70%' }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default ChatBot;
