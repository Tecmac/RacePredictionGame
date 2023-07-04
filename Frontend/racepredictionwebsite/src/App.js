import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./components/Login"
import { useState, useEffect } from "react";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login">
          <Login />
        </Route>
        {/* Weitere Routen */}
      </Routes>
    </Router>
  );
}

export default App;
