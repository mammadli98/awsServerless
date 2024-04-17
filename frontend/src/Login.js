import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); // Initialize useNavigate hook

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // You can replace this with your API endpoint
      const authToken = `${email}|${password}`;

      const authResponse = await axios.post(
        'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/getAuth',
        {
            "authorizationToken": authToken 
        }
      );

      const response = await axios.post(
        'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/readitem',
        {
            "IDs": [authResponse.data.ID] // eslint-disable-line no-loss-of-precision
        },
        {
            headers: {
                'Authorization': authToken
            }
        }
      );
      setMessage('Login successful!');
      console.log(response.data); // Optional: Log response from server

      // Set cookies for email and password
      document.cookie = `email=${email}; path=/`;
      document.cookie = `password=${password}; path=/`;

      // Redirect to user page after successful login
      navigate('/user');
    } catch (error) {
      setMessage('Login failed. Please try again.');
      console.error('Error:', error); // Log any errors
    }
  };

  return (
    <div className="Login">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default Login;
