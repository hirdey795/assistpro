import React, { useState, useEffect, useRef } from 'react';
import './SearchComponent.css';
import data from '../dataset/uni_and_classes.json'; // Import the JSON data

const SearchComponent = () => {
  const [selectedUni, setSelectedUni] = useState('');
  const [selectedMajor, setSelectedMajor] = useState('');
  const [selectedClass, setSelectedClass] = useState('');
  const [showUniDropdown, setShowUniDropdown] = useState(false);
  const [showMajorDropdown, setShowMajorDropdown] = useState(false);
  const [showClassDropdown, setShowClassDropdown] = useState(false);
  const [filteredUnis, setFilteredUnis] = useState(Object.keys(data));
  const [filteredMajors, setFilteredMajors] = useState([]);
  const [filteredClasses, setFilteredClasses] = useState([]);

  const uniDropdownRef = useRef();
  const majorDropdownRef = useRef();
  const classDropdownRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (uniDropdownRef.current && !uniDropdownRef.current.contains(event.target)) {
        setShowUniDropdown(false);
      }
      if (majorDropdownRef.current && !majorDropdownRef.current.contains(event.target)) {
        setShowMajorDropdown(false);
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
    const query = { selectedUni, selectedMajor, selectedClass };

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
    setShowMajorDropdown(false);
    setShowClassDropdown(false);
  };

  const handleMajorClick = () => {
    if (selectedUni) {
      setShowMajorDropdown(!showMajorDropdown);
      setShowUniDropdown(false);
      setShowClassDropdown(false);
    }
  };

  const handleClassClick = () => {
    if (selectedMajor) {
      setShowClassDropdown(!showClassDropdown);
      setShowUniDropdown(false);
      setShowMajorDropdown(false);
    }
  };

  const handleUniChange = (e) => {
    const input = e.target.value;
    setSelectedUni(input);
    setFilteredUnis(Object.keys(data).filter(uni => uni.toLowerCase().includes(input.toLowerCase())));
    setFilteredMajors([]);  // Clear majors if the university selection changes
    setFilteredClasses([]); // Clear classes if the university selection changes
    setSelectedMajor('');   // Clear selected major
    setSelectedClass('');   // Clear selected class
  };

  const handleMajorChange = (e) => {
    const input = e.target.value;
    setSelectedMajor(input);
    if (selectedUni) {
      setFilteredMajors(Object.keys(data[selectedUni]).filter(major => major.toLowerCase().includes(input.toLowerCase())));
      setFilteredClasses([]); // Clear classes if the major selection changes
      setSelectedClass('');   // Clear selected class
    }
  };

  const handleClassChange = (e) => {
    const input = e.target.value;
    setSelectedClass(input);
    if (selectedMajor) {
      setFilteredClasses(data[selectedUni][selectedMajor].filter(cls => cls.toLowerCase().includes(input.toLowerCase())));
    }
  };

  const handleUniSelect = (uni) => {
    setSelectedUni(uni);
    setShowUniDropdown(false);
    setFilteredMajors(Object.keys(data[uni]));
    setSelectedMajor('');
    setFilteredClasses([]);
  };

  const handleMajorSelect = (major) => {
    setSelectedMajor(major);
    setShowMajorDropdown(false);
    setFilteredClasses(data[selectedUni][major]);
    setSelectedClass('');
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
          onClick={selectedUni ? handleMajorClick : null}
          className="selector"
          style={{ cursor: selectedUni ? 'pointer' : 'not-allowed', opacity: selectedUni ? 1 : 0.5 }}
        >
          {selectedMajor || (selectedUni ? 'Select Major...' : 'Select Uni first...')}
        </div>
        {selectedUni && showMajorDropdown && (
          <div ref={majorDropdownRef} className="dropdown">
            <input
              type="text"
              placeholder="Search Major..."
              value={selectedMajor}
              onChange={handleMajorChange}
              className="dropdown-input"
            />
            <ul className="list">
              {filteredMajors.map((major) => (
                <li key={major} onClick={() => handleMajorSelect(major)} className="list-item">
                  {major}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <div className="select-container">
        <div
          onClick={selectedMajor ? handleClassClick : null}
          className="selector"
          style={{ cursor: selectedMajor ? 'pointer' : 'not-allowed', opacity: selectedMajor ? 1 : 0.5 }}
        >
          {selectedClass || (selectedMajor ? 'Select Class...' : 'Select Major first...')}
        </div>
        {selectedMajor && showClassDropdown && (
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
