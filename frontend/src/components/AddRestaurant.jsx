import React, { useState } from 'react';
import '../assets/addrestaurant.css';
import apiService from '../api/apiservice';

const AddRestaurant = () => {
  const [restaurantName, setRestaurantName] = useState('');
  const [city, setCity] = useState('');
  const [area, setArea] = useState('');
  const [cuisine, setCuisine] = useState('');
  const [rating, setRating] = useState('');
  const [costForTwo, setCostForTwo] = useState('');
  const [isVegFriendly, setIsVegFriendly] = useState(false);
  const [numberOfTables, setNumberOfTables] = useState('');
  const [maxPeoplePerTable, setMaxPeoplePerTable] = useState('');
  const [formErrors, setFormErrors] = useState({});
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate the form fields
    const errors = {};
    if (!restaurantName) errors.restaurantName = 'Restaurant name is required';
    if (!city) errors.city = 'City is required';
    if (!area) errors.area = 'Area is required';
    if (!cuisine) errors.cuisine = 'Cuisine type is required';
    if (!rating || rating <= 0) errors.rating = 'Rating is required and must be positive';
    if (!costForTwo || costForTwo <= 0) errors.costForTwo = 'Cost for two must be a positive value';
    if (!numberOfTables || numberOfTables <= 0) errors.numberOfTables = 'Number of tables must be a positive value';
    if (!maxPeoplePerTable || maxPeoplePerTable <= 0) errors.maxPeoplePerTable = 'Max people per table must be a positive value';

    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    // Prepare restaurant data
    const restaurantData = {
      name: restaurantName,
      city,
      area,
      cuisine,
      rating: parseFloat(rating),
      cost_for_two: parseFloat(costForTwo),
      is_veg_friendly: isVegFriendly,
      number_of_tables: parseInt(numberOfTables, 10),
      max_people_per_table: parseInt(maxPeoplePerTable, 10),
    };

    try {
      const response = await apiService.registerRestaurant(restaurantData);
      setMessage(response.message || 'Restaurant registered successfully!');
      setIsError(false);
      setRestaurantName('');
      setCity('');
      setArea('');
      setCuisine('');
      setRating('');
      setCostForTwo('');
      setIsVegFriendly(false);
      setNumberOfTables('');
      setMaxPeoplePerTable('');
      setFormErrors({});
    } catch (error) {
      setMessage(error.message || 'Something went wrong!');
      setIsError(true);
    }
  };

  return (
    <div className="add-restaurant-form">
      <h2>Add a New Restaurant</h2>
      {message && <p className={isError ? 'error-message' : 'success-message'}>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-field">
          <label>Restaurant Name:</label>
          <input
            type="text"
            value={restaurantName}
            onChange={(e) => setRestaurantName(e.target.value)}
            required
          />
          {formErrors.restaurantName && <p className="error">{formErrors.restaurantName}</p>}
        </div>
        <div className="form-field">
          <label>City:</label>
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            required
          />
          {formErrors.city && <p className="error">{formErrors.city}</p>}
        </div>
        <div className="form-field">
          <label>Area:</label>
          <input
            type="text"
            value={area}
            onChange={(e) => setArea(e.target.value)}
            required
          />
          {formErrors.area && <p className="error">{formErrors.area}</p>}
        </div>
        <div className="form-field">
          <label>Cuisine Type:</label>
          <input
            type="text"
            value={cuisine}
            onChange={(e) => setCuisine(e.target.value)}
            required
          />
          {formErrors.cuisine && <p className="error">{formErrors.cuisine}</p>}
        </div>
        <div className="form-field">
          <label>Rating (1-5):</label>
          <input
            type="number"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            min="1"
            max="5"
            step="0.1"
            required
          />
          {formErrors.rating && <p className="error">{formErrors.rating}</p>}
        </div>
        <div className="form-field">
          <label>Cost for Two:</label>
          <input
            type="number"
            min="10"
            max="500"
            value={costForTwo}
            onChange={(e) => setCostForTwo(e.target.value)}
            required
          />
          {formErrors.costForTwo && <p className="error">{formErrors.costForTwo}</p>}
        </div>
        <div className="form-field">
          <label>Vegetarian Friendly:</label>
          <div className="slider-container">
            <input
              type="checkbox"
              checked={isVegFriendly}
              onChange={() => setIsVegFriendly(!isVegFriendly)}
              className="slider-checkbox"
            />
            <label className="slider-label">{isVegFriendly ? 'Yes' : 'No'}</label>
          </div>
        </div>
        <div className="form-field">
          <label>Number of Tables:</label>
          <input
            type="number"
            value={numberOfTables}
            onChange={(e) => setNumberOfTables(e.target.value)}
            required
          />
          {formErrors.numberOfTables && <p className="error">{formErrors.numberOfTables}</p>}
        </div>
        <div className="form-field">
          <label>Max People Per Table:</label>
          <input
            type="number"
            value={maxPeoplePerTable}
            onChange={(e) => setMaxPeoplePerTable(e.target.value)}
            required
          />
          {formErrors.maxPeoplePerTable && <p className="error">{formErrors.maxPeoplePerTable}</p>}
        </div>
        <button type="submit" className="submitForm">Add Restaurant</button>
      </form>
    </div>
  );
};

export default AddRestaurant;
