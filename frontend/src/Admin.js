import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Admin.css';

function Admin() {
  const navigate = useNavigate();
  const [plz, setPlz] = useState('');
  const [authorization, setAuthorization] = useState('');
  const [prio, setPrio] = useState('');
  const [datum, setDatum] = useState('');
  const [selectedTimes, setSelectedTimes] = useState([]);
  const [responseDataPlz, setResponseDataPlz] = useState([]);
  const [responseDataPrio, setResponseDataPrio] = useState([]);
  const [responseDataDate, setResponseDataDate] = useState([]);

  const handleAdminClick = () => {
    navigate('/admin');
  };

  // Function to format date as dd-mm-yyyy
  const formatDate = (dateString) => {
    const dateObject = new Date(dateString);
    const day = String(dateObject.getDate()).padStart(2, '0');
    const month = String(dateObject.getMonth() + 1).padStart(2, '0');
    const year = dateObject.getFullYear();
    return `${day}-${month}-${year}`;
  };

  const handleFetchByPlz = async () => {
    try {
      const response = await axios.post(
        'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/admin/getuserbyzipcode',
        {
          "PLZ": plz
        },
        {
          headers: {
            'Authorization': authorization
          }
        }
      );
      setResponseDataPlz(response.data);
    } catch (error) {
      console.error('Error fetching data by PLZ:', error);
    }
  };

  const handleFetchByPrio = async () => {
    try {
      const response = await axios.post(
        'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/admin/getuserbyprio',
        {
          "prio": parseInt(prio)
        },
        {
          headers: {
            'Authorization': authorization
          }
        }
      );
      setResponseDataPrio(response.data);
    } catch (error) {
      console.error('Error fetching data by priority:', error);
    }
  };

  const handleFetchByDate = async () => {
    try {
      const response = await axios.post(
        'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/admin/addfreedates',
        {
          "PLZ": plz,
          "Datum": formatDate(datum),
          "Termine": selectedTimes
        },
        {
          headers: {
            'Authorization': authorization
          }
        }
      );
      setResponseDataDate(response.data);
    } catch (error) {
      console.error('Error fetching data by date:', error);
    }
  };

  // Generate time options from 8:00 to 18:00 with 30-minute intervals
  const generateTimeOptions = () => {
    const options = [];
    for (let hour = 8; hour <= 18; hour++) {
      for (let minute = 0; minute < 60; minute += 30) {
        const time = `${hour < 10 ? '0' + hour : hour}:${minute === 0 ? '00' : minute}`;
        options.push(time);
      }
    }
    return options;
  };

  return (
    <div className="Admin">
      <h1>Welcome to the Admin Page</h1>
      <button onClick={handleAdminClick}>Go to Admin Page</button>
      <div className="input-container">
        <div>
          <input
            type="text"
            placeholder="Auth Token"
            value={authorization}
            onChange={(e) => setAuthorization(e.target.value)}
          />
          <input
            type="text"
            placeholder="PLZ"
            value={plz}
            onChange={(e) => setPlz(e.target.value)}
          />
          <button onClick={handleFetchByPlz}>Fetch Data by PLZ</button>
        </div>
        <div>
          <input
            type="number"
            placeholder="Priority"
            value={prio}
            onChange={(e) => setPrio(e.target.value)}
          />
          <button onClick={handleFetchByPrio}>Fetch Data by Priority</button>
        </div>
        <div>
          <input
            type="date"
            placeholder="Date"
            value={datum}
            onChange={(e) => setDatum(e.target.value)}
          />
          <select
            multiple
            value={selectedTimes}
            onChange={(e) => setSelectedTimes(Array.from(e.target.selectedOptions, option => option.value))}
          >
            {generateTimeOptions().map((time, index) => (
              <option key={index} value={time}>{time}</option>
            ))}
          </select>
          <button onClick={handleFetchByDate}>Add termin to users</button>
        </div>
      </div>
      <h2>Data by PLZ:</h2>
      <table className="data-table">
        <thead>
          <tr>
            {Object.keys(responseDataPlz[0] || {}).map((key) => (
              <th key={key} scope="col">{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {responseDataPlz.map((item, index) => (
            <tr key={index}>
              {Object.values(item).map((value, index) => (
                <td key={index}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <h2>Data by Priority:</h2>
      <table className="data-table">
        <thead>
          <tr>
            {Object.keys(responseDataPrio[0] || {}).map((key) => (
              <th key={key} scope="col">{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {responseDataPrio.map((item, index) => (
            <tr key={index}>
              {Object.values(item).map((value, index) => (
                <td key={index}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <h2>Termin added to these users:</h2>
      <table className="data-table">
        <thead>
          <tr>
            {Object.keys(responseDataDate[0] || {}).map((key) => (
              <th key={key} scope="col">{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {responseDataDate.map((item, index) => (
            <tr key={index}>
              {Object.values(item).map((value, index) => (
                <td key={index}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Admin;
