import React, { useState, useEffect } from 'react';

function SpeciesSelector() {
  const [speciesList, setSpeciesList] = useState([]);
  const [selectedSpecies, setSelectedSpecies] = useState('');
  const [aopEventData, setAopEventData] = useState([]);

  // Load the initial list of species from species.json
  useEffect(() => {
    fetch('/species.json')
      .then(response => response.json())
      .then(data => setSpeciesList(data.species));
  }, []);

  // Fetch species-specific AOP and Event data when a new species is selected
  useEffect(() => {
    if (selectedSpecies) {
      const speciesFileName = selectedSpecies.replace(/ /g, '_'); // Adjust if your file naming uses a different convention
      fetch(`/species_data/${speciesFileName}.json`)
        .then(response => response.json())
        .then(data => setAopEventData(data))
        .catch(error => console.error("Failed to fetch data for species:", selectedSpecies, error));
    }
  }, [selectedSpecies]);

  const handleSelectionChange = (event) => {
    setSelectedSpecies(event.target.value);
  };

  return (
    <div>
      <h5>Select Species</h5>
      <select onChange={handleSelectionChange} value={selectedSpecies}>
        {speciesList.map((species, index) => (
          <option key={index} value={species.name}>
            {species.name}
          </option>
        ))}
      </select>

      <div>
        {aopEventData.length > 0 && (
          <ul>
            {aopEventData.map((item, index) => (
              <li key={index}>
                GO Term: {item.goTerm}, AOP ID: {item.aopId}, Event ID: {item.eventId}
                {/* Customize based on your data structure */}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default SpeciesSelector;

