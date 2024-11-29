import React, { useState, useEffect } from 'react';
import apiService from '../api/apiservice'; // Ensure the path is correct to your apiService
import RestaurantCard from './RestaurantCard';
import RestaurantModal from './SlotsModal'; // Import the modal component
import '../assets/manageslots.css'; // Add the restaurant card styles


const ManageSlots = () => {
  const [restaurants, setRestaurants] = useState([]); // For storing restaurant data
  const [loading, setLoading] = useState(true); // For loading state
  const [error, setError] = useState(''); // For error handling
  const [selectedRestaurant, setSelectedRestaurant] = useState(null); // State for the selected restaurant

  // Fetch the restaurants from the API on component mount
  useEffect(() => {
    const fetchRestaurants = async () => {
      try {
        const data = await apiService.getEntities();
        setRestaurants(data.entities);
      } catch (err) {
        setError('Failed to fetch restaurants');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchRestaurants();
  }, []);

  const handleCardClick = (restaurant) => {
    setSelectedRestaurant(restaurant); // Set the clicked restaurant for the modal
  };

  const handleCloseModal = () => {
    setSelectedRestaurant(null); // Close the modal by resetting the selected restaurant
  };



  return (
    <div className="manage-slots">
      <h2>Manage Restaurant Slots</h2>
      {/* Displaying restaurant list */}
      <h2>Restaurant List</h2>
      {loading ? (
        <p>Loading restaurants...</p>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : restaurants.length > 0 ? (
        <div className="restaurant-list">
          {restaurants.map((restaurant) => (
            <RestaurantCard
              key={restaurant.id}
              restaurant={restaurant}
              onClick={() => handleCardClick(restaurant)}
            />
          ))}
        </div>
      ) : (
        <div className="no-results">No results found</div>
      )}

      {/* Modal for displaying restaurant details */}
      {selectedRestaurant && (
        <RestaurantModal
          restaurant={selectedRestaurant}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
};

export default ManageSlots;
