import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';
import './UserPage.css';

function UserPage() {
  const [userData, setUserData] = useState(null);
  const [cookies, removeCookie] = useCookies(['email', 'password']);
  const navigate = useNavigate();
  const [updatedValue, setUpdatedValue] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      if (!cookies.email || !cookies.password) {
        navigate('/login');
      } else {
        try {
          // Fetch user authentication data
          const authToken = `${cookies.email}|${cookies.password}`;
          const authResponse = await axios.post(
            'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/getAuth',
            {
              "authorizationToken": authToken 
            }
          );

          // Fetch user data
          const response = await axios.post(
            'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/readitem',
            {
              "IDs": [authResponse.data.ID]
            },
            {
              headers: {
                'Authorization': authToken
              }
            }
          );
          setUserData(response.data[0]); // Take the first element from the response array
        } catch (error) {
          console.error('Error:', error);
        }
      }
    };

    fetchData();
  }, []);

  const handleLogout = () => {
    removeCookie('email');
    removeCookie('password');
    navigate('/login');
  };

  const handleUpdate = async (fieldName) => {
    try {
      const updatedField = updatedValue[fieldName];
      if (updatedField !== undefined) {
        const authToken = `${cookies.email}|${cookies.password}`;
        const authResponse = await axios.post(
          'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/getAuth',
          {
              "authorizationToken": authToken 
          }
        );
        console.log(fieldName);
        if(fieldName == "Mail"){
          await axios.post(
            'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/updatemail',
            {
              "ID": authResponse.data.ID,
              "Mail": updatedField
            },
            {
              headers: {
                'Authorization': authToken
              }
            }
          );
          document.cookie = `email=${updatedField}; path=/`;
        }else if(fieldName == "Name"){
          await axios.post(
            'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/updatelastname',
            {
              "ID": authResponse.data.ID,
              "Name": updatedField
            },
            {
              headers: {
                'Authorization': authToken
              }
            }
          );
        }
        // Refresh user data after update
        const response = await axios.post(
          'https://9xna35s7vi.execute-api.eu-central-1.amazonaws.com/dev/user/readitem',
          {
            "IDs": [authResponse.data.ID]
          },
          {
            headers: {
              'Authorization': `${cookies.email}|${cookies.password}`
            }
          }
        );
        setUserData(response.data[0]);
        setUpdatedValue({});
        window.location.reload();
      }
    } catch (error) {
      console.error('Error updating data:', error);
    }
  };

  const handleChange = (fieldName, value) => {
    setUpdatedValue({ ...updatedValue, [fieldName]: value });
  };

  return (
    <div className="UserPage">
      {userData ? (
        <>
          <h1>Welcome {userData.Vorname}!</h1>
          <button onClick={handleLogout}>Logout</button>
          <table className="userTable">
            <tbody>
              {Object.entries(userData).map(([fieldName, value]) => (
                <tr key={fieldName}>
                  <td className="label">{fieldName}</td>
                  <td className="value">{value}</td>
                  <td>
                    <input
                      type="text"
                      value={updatedValue[fieldName] || ''}
                      onChange={(e) => handleChange(fieldName, e.target.value)}
                    />
                    <button onClick={() => handleUpdate(fieldName)}>Update</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <p>Please log in</p>
      )}
    </div>
  );
}

export default UserPage;
