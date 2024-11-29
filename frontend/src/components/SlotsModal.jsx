import React, { useState, useEffect, useCallback } from 'react';
import apiService from '../api/apiservice';
import '../assets/slotsModal.css';

const RestaurantModal = ({ restaurant, onClose, onAddSlot }) => {
  const [newSlot, setNewSlot] = useState('');
  const [slotsInfo, setSlotsInfo] = useState(null);
  const [slotDetails, setSlotDetails] = useState({
    startTime: '',
    endTime: '',
    maxDays: 0,
  });
  const [successMessage, setSuccessMessage] = useState('');

  // Memoize fetchSlotsInfo to avoid recreating it on every render
  const fetchSlotsInfo = useCallback(async (entityId) => {
    try {
      const data = await apiService.getSlots(entityId);
      if (data && data.length > 0) {
        setSlotsInfo(data[0]);}
      console.log(slotsInfo)
    } catch (error) {
      console.error('Error fetching slot information:', error);
    }
  }, []);

  useEffect(() => {
    if (restaurant && restaurant.id) {
      fetchSlotsInfo(restaurant.id);
    }
  }, [restaurant, fetchSlotsInfo]);

  // Memoize handleAddSlot
  const handleAddSlot = useCallback(async () => {
    const { startTime, endTime, maxDays } = slotDetails;
  
    if (startTime >= 0 && startTime <= 23 && endTime >= 0 && endTime <= 23 && startTime < endTime) {
      try {
        const response = await apiService.addOrUpdateSlot(
          restaurant.id,
          startTime,
          endTime,
          maxDays
        );
  
        if (response.success) {
          setSuccessMessage(response.message);
          alert('Slot added successfully!');
          fetchSlotsInfo(restaurant.id);  // Always show alert on success
        } else {
          alert('Failed to add slot: ' + response.message);
        }
      } catch (error) {
        console.error('Error while adding/updating slot:', error);
        alert('An error occurred while adding the slot.');
      }
    } else {
      alert('Invalid slot details. Ensure start time is less than end time, and values are within the range of 0-23.');
    }
  }, [slotDetails, restaurant.id]);

  // Memoize handleSlotDetailsChange
  const handleSlotDetailsChange = useCallback((e) => {
    const { name, value } = e.target;
    setSlotDetails((prevDetails) => ({
      ...prevDetails,
      [name]: parseInt(value, 10) || 0,  // Convert to number, default to 0 if NaN
    }));
  }, []);

  const isSlotInputValid = () => {
    const { startTime, endTime, maxDays } = slotDetails;
    return (
      startTime >= 0 &&
      startTime <= 23 &&
      endTime >= 0 &&
      endTime <= 23 &&
      endTime > startTime &&
      maxDays >= 0
    );
  };

  return (
    <div className="slot-modal-overlay">
      <div className="slot-modal-container">
        <div className="slot-modal-header">
          <button onClick={onClose}>Close</button>
        </div>
        <div className="slot-modal-body">
          <div className="restaurant-details">
            <h3>{restaurant.name}</h3>
            <p>City: {restaurant.city}</p>
            <p>Area: {restaurant.area}</p>
            <p>Cuisine: {restaurant.cuisine}</p>
            <p>Rating: {restaurant.rating}</p>
            <p>Cost for Two: ${restaurant.cost_for_two}</p>
            <p>Veg Friendly: {restaurant.is_veg_friendly ? 'Yes' : 'No'}</p>
            <p>Number of Tables: {restaurant.number_of_tables}</p>
            <p>Max People Per Table: {restaurant.max_people_per_table}</p>
          </div>
          <div className="divider"></div>
          <div className="available-slots">
            <h4>Available Slots</h4>
            <div>
              {slotsInfo?.number_of_days > 0 ? (
                <p>
                  Slot booking is allowed for a maximum number of{' '}
                  {slotsInfo.number_of_days} days in the future. <br /> Start time for slots is{' '}
                  {slotsInfo.start_time} and last slot of the day is at{' '}
                  {slotsInfo.end_time}.
                </p>
              ) : (
                <p>No available slots.</p>
              )}
            </div>
            <div>
              <h5>Add a New Slot</h5>
              <label>Day Slot Start Time (0-23):</label>
              <input
                type="number"
                name="startTime"
                value={slotDetails.startTime}
                onChange={handleSlotDetailsChange}
                min="0"
                max="23"
              />
              <label>Day Slot End Time (0-23):</label>
              <input
                type="number"
                name="endTime"
                value={slotDetails.endTime}
                onChange={handleSlotDetailsChange}
                min="0"
                max="23"
              />
              <label>Max Number of Days for Future Booking:</label>
              <input
                type="number"
                name="maxDays"
                value={slotDetails.maxDays}
                onChange={handleSlotDetailsChange}
                min="0"
              />
              <button
                onClick={handleAddSlot}
                disabled={!isSlotInputValid()} // Disable if input is invalid
              >
                Update Slot
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RestaurantModal;
