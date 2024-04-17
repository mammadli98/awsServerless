import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'; // Import Routes
import Login from './Login';
import Registration from './Registration'; 
import UserPage from './UserPage'; // Import UserPage component
import Admin from './Admin'; // Import Admin component
import './App.css'; // Import CSS file

function App() {
  return (
    <Router>
      <div>
        <nav className="navbar"> {/* Add navbar class */}
          <ul>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/registration">Registration</Link>
            </li>
            <li>
              <Link to="/user">User</Link> {/* Add link to User Page */}
            </li>
            <li>
              <Link to="/admin">Admin</Link> {/* Add link to Admin Page */}
            </li>
          </ul>
        </nav>

        <hr />

        <Routes> {/* Wrap your routes with <Routes> */}
          <Route path="/login" element={<Login />} /> {/* Use 'element' prop */}
          <Route path="/registration" element={<Registration />} />
          <Route path="/user" element={<UserPage />} /> {/* Route for User Page */}
          <Route path="/admin" element={<Admin />} /> {/* Route for Admin Page */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
