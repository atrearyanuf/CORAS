// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './Login';
import Home from './Home'; // Assume Home is the main component you want to land on after login

function App() {
    // State to track whether the user is authenticated
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    return (
        <Router>
            <Routes>
                {/* If not authenticated, show Login page; otherwise, redirect to Home */}
                <Route
                    path="/Login"
                    element={
                        isAuthenticated ? <Navigate to="/" /> : <Login onLogin={() => setIsAuthenticated(true)} />
                    }
                />
                 <Route
                    path="/"
                    element={
                        isAuthenticated ? (
                            <Home onLogout={() => setIsAuthenticated(false)} />
                        ) : (
                            <Navigate to="/login" />
                        )
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
