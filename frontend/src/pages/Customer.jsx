import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import '../assets/customer.css';
import RestaurantCard from '../components/RestaurantCard';
import Modal from '../components/BookingModal';  
import apiService from '../api/apiservice';
import PropTypes from 'prop-types';

const Customer = () => {
  const [search, setSearch] = useState('');
  const [filtersVisible, setFiltersVisible] = useState(false);
  const [filteredRestaurants, setFilteredRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [area, setArea] = useState('');
  const [cuisine, setCuisine] = useState('');
  const [ratingMin, setRatingMin] = useState('');
  const [ratingMax, setRatingMax] = useState('');
  const [costMin, setCostMin] = useState('');
  const [costMax, setCostMax] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const restaurantShape = PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    city: PropTypes.string.isRequired,
    area: PropTypes.string.isRequired,
    cuisine: PropTypes.string.isRequired,
    rating: PropTypes.number.isRequired,
    cost_for_two: PropTypes.number.isRequired,
    is_veg_friendly: PropTypes.bool.isRequired,
    number_of_tables: PropTypes.number.isRequired,
    max_people_per_table: PropTypes.number.isRequired
  });
  
  filteredRestaurants.propTypes = {
    filteredRestaurants: PropTypes.arrayOf(restaurantShape)
  };

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
  };

  // Function to fetch data
  const fetchRestaurants = async () => {
    try {
      const filters = {};
      if (search.trim()) filters.plainText = search.trim();
      if (name.trim()) filters.name = name.trim();
      if (city.trim()) filters.city = city.trim();
      if (area.trim()) filters.area = area.trim();
      if (cuisine.trim()) filters.cuisine = cuisine.trim();
      if (ratingMin.trim()) filters.rating_min = parseFloat(ratingMin);
      if (ratingMax.trim()) filters.rating_max = parseFloat(ratingMax);
      if (costMin.trim()) filters.cost_for_two_min = parseInt(costMin, 10);
      if (costMax.trim()) filters.cost_for_two_max = parseInt(costMax, 10);
      
      const data = await apiService.searchRestaurants(filters);
      setFilteredRestaurants(data);
    } catch (error) {
      setErrorMessage(error.message);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      fetchRestaurants();
    }
  };

  // useEffect to fetch when 'search' changes
  useEffect(() => {
    if (search.length >= 3) {
      fetchRestaurants();
    }
  }, [search]);

  const toggleFilters = () => setFiltersVisible(!filtersVisible);

  const handleRatingMinChange = (e) => {
    const value = e.target.value;
    setRatingMin(value);
    if (ratingMax && parseFloat(value) >= parseFloat(ratingMax)) {
      setErrorMessage('Min Rating should be less than Max Rating');
    } else {
      setErrorMessage('');
    }
  };

  const handleRatingMaxChange = (e) => {
    const value = e.target.value;
    setRatingMax(value);
    if (ratingMin && parseFloat(value) <= parseFloat(ratingMin)) {
      setErrorMessage('Max Rating should be greater than Min Rating');
    } else {
      setErrorMessage('');
    }
  };

  const handleCostMinChange = (e) => {
    const value = e.target.value;
    setCostMin(value);
    if (costMax && parseInt(value) >= parseInt(costMax, 10)) {
      setErrorMessage('Min Cost should be less than Max Cost');
    } else {
      setErrorMessage('');
    }
  };

  const handleCostMaxChange = (e) => {
    const value = e.target.value;
    setCostMax(value);
    if (costMin && parseInt(value) <= parseInt(costMin, 10)) {
      setErrorMessage('Max Cost should be greater than Min Cost');
    } else {
      setErrorMessage('');
    }
  };

  const handleCardClick = (restaurant) => {
    setSelectedRestaurant(restaurant);
  };

  const closeModal = () => {
    setSelectedRestaurant(null);
  };

  return (
    <div className="customer-page">
      <Navbar />
      <div className="search-container">
        <div className="search-box">
          <input
            className="search-input"
            type="text"
            placeholder="Search for restaurants..."
            value={search}
            onChange={handleSearchChange}
            onKeyUp={handleKeyPress}
          />
          <button className="search-btn" onClick={fetchRestaurants}>Search</button>
          <button className="filter-btn" onClick={toggleFilters}>Filters</button>
        </div>
      </div>

      {/* Filter Section */}
      <div className={`filters-container ${filtersVisible ? 'active' : ''}`}>
        <div className="filter-fields">
          <div className="form-field">
            <label>Name</label>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div className="form-field">
            <label>City</label>
            <input type="text" value={city} onChange={(e) => setCity(e.target.value)} />
          </div>
          <div className="form-field">
            <label>Area</label>
            <input type="text" value={area} onChange={(e) => setArea(e.target.value)} />
          </div>
          <div className="form-field">
            <label>Cuisine</label>
            <input type="text" value={cuisine} onChange={(e) => setCuisine(e.target.value)} />
          </div>
          <div className="form-field">
            <label>Min Rating</label>
            <input
              type="number"
              min="1.0"
              max="5.0"
              step="0.1"
              value={ratingMin}
              onChange={handleRatingMinChange}
            />
          </div>
          <div className="form-field">
            <label>Max Rating</label>
            <input
              type="number"
              min="1.0"
              max="5.0"
              step="0.1"
              value={ratingMax}
              onChange={handleRatingMaxChange}
            />
          </div>
          <div className="form-field">
            <label>Min Cost for Two</label>
            <input
              type="number"
              min="10"
              max="500"
              value={costMin}
              onChange={handleCostMinChange}
            />
          </div>
          <div className="form-field">
            <label>Max Cost for Two</label>
            <input
              type="number"
              min="10"
              max="500"
              value={costMax}
              onChange={handleCostMaxChange}
            />
          </div>
        </div>
      </div>

      {/* Restaurant List */}
      <div className="restaurant-list">
        {filteredRestaurants.length > 0 ? (
          filteredRestaurants.map((restaurant) => (
            <RestaurantCard
              key={restaurant.id}
              restaurant={restaurant}
              onClick={() => handleCardClick(restaurant)}
            />
          ))
        ) : (
          <div className="no-results">No results found</div>
        )}
      </div>

      {/* Modal for displaying restaurant details */}
      {selectedRestaurant && (
        <Modal restaurant={selectedRestaurant} closeModal={closeModal} />
      )}
    </div>
  );
};

export default Customer;
