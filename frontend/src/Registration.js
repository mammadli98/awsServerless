import React, { useState } from 'react';
import axios from 'axios';
import './Registration.css';

function Registration() {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [vorname, setVorname] = useState('');
  const [geburtstag, setGeburtstag] = useState('');
  const [plz, setPlz] = useState('');
  const [geschlecht, setGeschlecht] = useState('');
  const [systemrelevanz, setSystemrelevanz] = useState('');
  const [vorerkrankungen, setVorerkrankungen] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Convert the date format before sending it to the backend
    const formattedGeburtstag = formatDate(geburtstag);
    const item = {
      "Name": name,
      "Vorname": vorname,
      "Mail": email,
      "Geburtstag": formattedGeburtstag,
      "PLZ": plz,
      "Geschlecht": geschlecht,
      "secret": password,
      "Systemrelevanz": systemrelevanz,
      "Vorerkrankungen": vorerkrankungen
    };
    try {
      // You can replace this with your API endpoint
      const response = await axios.post('https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/writeitem', {
        "items": [item]
      });
      setMessage('Registration successful!');
      console.log(response.data); // Optional: Log response from server
    } catch (error) {
      setMessage('Registration failed. Please try again.');
      console.error('Error:', error); // Log any errors
    }
  };

  // Function to format date as dd-mm-yyyy
  const formatDate = (dateString) => {
    const dateObject = new Date(dateString);
    const day = String(dateObject.getDate()).padStart(2, '0');
    const month = String(dateObject.getMonth() + 1).padStart(2, '0');
    const year = dateObject.getFullYear();
    return `${day}-${month}-${year}`;
  };

  return (
    <div className="App">
      <h1>User Registration</h1>
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
        <div className="form-group">
          <label>Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Vorname:</label>
          <input
            type="text"
            value={vorname}
            onChange={(e) => setVorname(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Geburtstag:</label>
          <input
            type="date"
            value={geburtstag}
            onChange={(e) => setGeburtstag(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>PLZ:</label>
          <input
            type="text"
            value={plz}
            onChange={(e) => setPlz(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Geschlecht:</label>
          <select
            value={geschlecht}
            onChange={(e) => setGeschlecht(e.target.value)}
            required
          >
            <option value="">Select</option>
            <option value="Mann">Mann</option>
            <option value="Frau">Frau</option>
          </select>
        </div>
        <div className="form-group">
          <label>Systemrelevanz:</label>
          <input
            type="number"
            value={systemrelevanz}
            onChange={(e) => setSystemrelevanz(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Vorerkrankungen:</label>
          <input
            type="number"
            value={vorerkrankungen}
            onChange={(e) => setVorerkrankungen(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default Registration;
