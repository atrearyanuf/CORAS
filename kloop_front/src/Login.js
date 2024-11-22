// src/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate(); // Use useNavigate instead of useHistory

    // Default credentials
    const defaultUsername = 'admin';
    const defaultPassword = 'password123';

    const handleSubmit = (e) => {
        e.preventDefault();

        // Check if the entered credentials match the default credentials
        if (username === defaultUsername && password === defaultPassword) {
            // alert('Login successful!');
            onLogin(); // Set isAuthenticated to true in App.js
            navigate('/'); // Redirect to the main page (Home component in App.js)
        } else {
            alert('Invalid username or password');
        }
    };

    return (
        <div className="login">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;
