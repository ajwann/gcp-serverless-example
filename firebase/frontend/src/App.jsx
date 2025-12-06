import { useState } from 'react';
import { auth } from './firebase';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';

// The variable is now retrieved from the environment injected by Vite
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL; 

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState(null);

  const [taskMsg, setTaskMsg] = useState('');
  const [delay, setDelay] = useState(5);

  const handleAuth = async (isSignup) => {
    try {
      const userCred = isSignup 
        ? await createUserWithEmailAndPassword(auth, email, password)
        : await signInWithEmailAndPassword(auth, email, password);
      setUser(userCred.user);
      alert(`Welcome ${userCred.user.email}`);
    } catch (error) {
      alert(error.message);
    }
  };

  const scheduleTask = async () => {
    if (!user) return;
    // Check to ensure the URL is available before fetching
    if (!BACKEND_URL) {
        alert("Configuration Error: BACKEND_URL is missing.");
        return;
    }
    try {
      const res = await fetch(`${BACKEND_URL}/schedule-task`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: taskMsg, delay_minutes: parseInt(delay) })
      });
      const data = await res.json();
      if (res.ok) alert(`Task Scheduled! Job Name: ${data.job_name}`);
      else alert(`Error: ${data.detail}`);
    } catch (err) {
      alert("Network Error");
    }
  };

  if (user) {
    return (
      <div style={{padding: '2rem'}}>
        <h2>Create a Task</h2>
        <p>User: {user.email}</p>
        <input 
          placeholder="Message to log" 
          value={taskMsg} 
          onChange={e => setTaskMsg(e.target.value)} 
        />
        <br /><br />
        <input 
          type="number" 
          placeholder="Minutes from now" 
          value={delay} 
          onChange={e => setDelay(e.target.value)} 
        />
        <br /><br />
        <button onClick={scheduleTask}>Schedule Task</button>
      </div>
    );
  }

  return (
    <div style={{padding: '2rem'}}>
      <h2>Login / Signup</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <br /><br />
      <button onClick={() => handleAuth(false)}>Login</button>
      <button onClick={() => handleAuth(true)}>Sign Up</button>
    </div>
  );
}

export default App;
