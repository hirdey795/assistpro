import React, { useState, useEffect, useRef } from 'react';
import './SearchComponent.css'; // Import the CSS file

// Sample data for demonstration
const data = {
  'University 1': ['Class 1.1', 'Class 1.2', 'Class 1.3'],
  'University 2': ['Class 2.1', 'Class 2.2', 'Class 2.3'],
  'University 3': ['Class 3.1', 'Class 3.2', 'Class 3.3'],
  'University 4': ['Class 4.1', 'Class 4.2', 'Class 4.3'],
};

const SearchComponent = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedUni, setSelectedUni] = useState('');
  const [selectedClass, setSelectedClass] = useState('');
  const [showUniDropdown, setShowUniDropdown] = useState(false);
  const [showClassDropdown, setShowClassDropdown] = useState(false);
  const [filteredUnis, setFilteredUnis] = useState(Object.keys(data));
  const [filteredClasses, setFilteredClasses] = useState([]);

  const uniDropdownRef = useRef();
  const classDropdownRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (uniDropdownRef.current && !uniDropdownRef.current.contains(event.target)) {
        setShowUniDropdown(false);
      }
      if (classDropdownRef.current && !classDropdownRef.current.contains(event.target)) {
        setShowClassDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    const query = { searchTerm, selectedUni, selectedClass };

    try {
      const response = await fetch('http://your-django-server-endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(query),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Search results:', data);
      } else {
        console.error('Search failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error during search:', error);
    }
  };

  const handleUniClick = () => {
    setShowUniDropdown(!showUniDropdown);
    setShowClassDropdown(false);
  };

  const handleClassClick = () => {
    setShowClassDropdown(!showClassDropdown);
    setShowUniDropdown(false);
  };

  const handleUniChange = (e) => {
    const input = e.target.value;
    setSelectedUni(input);
    setFilteredUnis(Object.keys(data).filter(uni => uni.toLowerCase().includes(input.toLowerCase())));
    setFilteredClasses([]);  // Clear classes if the university selection changes
    setSelectedClass('');    // Clear selected class
  };

  const handleClassChange = (e) => {
    const input = e.target.value;
    setSelectedClass(input);
    if (selectedUni) {
      setFilteredClasses(data[selectedUni].filter(cls => cls.toLowerCase().includes(input.toLowerCase())));
    }
  };

  const handleUniSelect = (uni) => {
    setSelectedUni(uni);
    setShowUniDropdown(false);
    setFilteredClasses(data[uni]);
  };

  const handleClassSelect = (cls) => {
    setSelectedClass(cls);
    setShowClassDropdown(false);
  };

  return (
    <form onSubmit={handleSearch} className="form-container">
      <div className="select-container">
        <div onClick={handleUniClick} className="selector">
          {selectedUni || 'Select Uni...'}
        </div>
        {showUniDropdown && (
          <div ref={uniDropdownRef} className="dropdown">
            <input
              type="text"
              placeholder="Search Uni..."
              value={selectedUni}
              onChange={handleUniChange}
              className="dropdown-input"
            />
            <ul className="list">
              {filteredUnis.map((uni) => (
                <li key={uni} onClick={() => handleUniSelect(uni)} className="list-item">
                  {uni}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <div className="select-container">
        <div
          onClick={selectedUni ? handleClassClick : null}
          className="selector"
          style={{ cursor: selectedUni ? 'pointer' : 'not-allowed', opacity: selectedUni ? 1 : 0.5 }}
        >
          {selectedClass || (selectedUni ? 'Select Class...' : 'Select Uni first...')}
        </div>
        {selectedUni && showClassDropdown && (
          <div ref={classDropdownRef} className="dropdown">
            <input
              type="text"
              placeholder="Search Class..."
              value={selectedClass}
              onChange={handleClassChange}
              className="dropdown-input"
            />
            <ul className="list">
              {filteredClasses.map((cls) => (
                <li key={cls} onClick={() => handleClassSelect(cls)} className="list-item">
                  {cls}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <button type="submit" className="search-button">Search</button>
    </form>
  );
};

export default SearchComponent;
