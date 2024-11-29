import React from 'react';
import '../assets/restaurantcard.css';

const RestaurantCard = ({ restaurant, onClick }) => {
  return (
    <div className="restaurant-card" onClick={onClick}>
      <h3>{restaurant.name}</h3>
      <p>{restaurant.city}</p>
      <p>{restaurant.cuisine}</p>
      <p>Rating: {restaurant.rating}</p>
      <p>Cost for Two: ${restaurant.cost_for_two}</p>
    </div>
  );
};

export default RestaurantCard;
