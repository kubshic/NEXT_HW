import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import React from 'react';
import Main from './pages/Main';
import Footer from './components/Footer/Footer';
import './App.css';

function App() {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Main />} />
                </Routes>
                <Footer />
            </div>
        </Router>
    );
}

export default App;
