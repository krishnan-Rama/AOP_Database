import React from 'react';
import './App.css';
import SpeciesSelector from './SpeciesSelector'; // Assuming SpeciesSelector.js is directly under src/

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>TRACE: Toxicity Response & AOPs Comprehensive Explorer</h1>
        <SpeciesSelector />
      </header>
    </div>
  );
}

export default App;

