import React, { useState, useEffect, useCallback } from 'react';
import '../assets/modal.css';
import apiService from '../api/apiservice';

const Modal = ({ restaurant, closeModal }) => {
  const [availability, setAvailability] = useState([]);
  const [selectedTime, setSelectedTime] = useState(null);
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);
  const [slotsInfo, setSlotsInfo] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const [numberOfPeople, setNumberOfPeople] = useState('');
  const [contactName, setContactName] = useState('');
  const [contactNumber, setContactNumber] = useState('');
  const [formError, setFormError] = useState('');

  // Fetch slot information based on restaurant entity_id
  const fetchSlotsInfo = useCallback(async (entityId) => {
    try {
      const data = await apiService.getSlots(entityId);
      if (data && data.length > 0) {
        setSlotsInfo(data[0]);
      }
    } catch (error) {
      console.error('Error fetching slot information:', error);
    }
  }, []);

  useEffect(() => {
    if (restaurant) {
      fetchSlotsInfo(restaurant.id); // Using entity_id to fetch slot data
    }
  }, [restaurant, fetchSlotsInfo]);

  const handleDateChange = async (e) => {
    const date = e.target.value;
    setSelectedDate(date);
    setSelectedTime(null); // Reset time selection on date change
    setIsButtonDisabled(true);
    const currentYear = new Date().getFullYear();
    const dateString = `${date} ${currentYear}`; 
    const parsedDate = new Date(dateString);
    // Convert the selected date to the YYYY-MM-DD format
    const formattedDate = new Date(parsedDate).toLocaleDateString('en-CA'); // 'en-CA' returns YYYY-MM-DD format
  
    try {
      const data = await apiService.getAvailability(restaurant.id, formattedDate);
      setAvailability(data);
    } catch (error) {
      console.error('Error fetching availability:', error);
    }
  };

  const handleButtonClick = (time) => {
    setSelectedTime(time);
    const selectedPeriod = availability.find((period) => period.time === time);
    setIsButtonDisabled(!selectedPeriod || selectedPeriod.available_tables === 0);
  };

  // Generate array of next available dates
  const generateDateOptions = () => {
    const dates = [];
    if (slotsInfo && slotsInfo.number_of_days) {
      const today = new Date();
      for (let i = 0; i < slotsInfo.number_of_days; i++) {
        const nextDate = new Date(today);
        nextDate.setDate(today.getDate() + i);
        const formattedDate = `${nextDate.getDate().toString().padStart(2, '0')} ${nextDate.toLocaleString('default', { month: 'short' })}`;
        dates.push(formattedDate);
      }
    }
    return dates;
  };

  const handleSubmit = async () => {
    if (parseInt(numberOfPeople) > restaurant.max_people_per_table) {
      setFormError(`Number of people cannot exceed ${restaurant.max_people_per_table}`);
      return;
    }

    const phonePattern = /^\d{10}$/;
    if (!phonePattern.test(contactNumber)) {
      setFormError('Contact number must be a 10-digit number');
      return;
    }

    if (!contactName || !contactNumber || !numberOfPeople || !selectedTime || !selectedDate) {
      setFormError('All fields are required');
      return;
    }

    const currentYear = new Date().getFullYear();
    const dateString = `${selectedDate} ${currentYear}`; 
    const parsedDate = new Date(dateString);
    parsedDate.setMinutes(parsedDate.getMinutes()-parsedDate.getTimezoneOffset())
    console.log(parsedDate)
    const formattedBookingDate = new Date(parsedDate).toISOString().split('T')[0];
    console.log(formattedBookingDate)

    // Prepare the booking data
    const bookingData = {
      entity_id: restaurant.id,
      slot_id: slotsInfo.id,
      people_count: numberOfPeople,
      booking_name: contactName,
      booking_contact: contactNumber,
      booking_time: selectedTime,
      booking_date: formattedBookingDate,
    };

    // Call the API to book the table
    const result = await apiService.bookTable(bookingData);

    if (result.success) {
      // If the booking is successful, show an alert
      alert('Booking successful: ' + result.message);
      setFormError('');
      closeModal(); // Close the modal
    } else {
      // If the booking failed, close the modal and show the error message in the alert
      alert('Booking failed: ' + result.message);
      closeModal(); // Close the modal
    }
  };

  // Disable "Book Table" button based on field completion
  useEffect(() => {
    if (
      selectedTime &&
      contactName &&
      contactNumber &&
      numberOfPeople &&
      parseInt(numberOfPeople) <= restaurant.max_people_per_table
    ) {
      setIsButtonDisabled(false); // Enable button if all fields are filled and valid
    } else {
      setIsButtonDisabled(true); // Disable button if any field is empty or invalid
    }
  }, [selectedTime, numberOfPeople, contactName, contactNumber, restaurant.max_people_per_table]);

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <div className="modal-header">
          <h2>{restaurant.name}</h2>
          <button className="close-btn" onClick={closeModal}>X</button>
        </div>
        <div className="modal-body">
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

          <div className="availability-section">
            <h3>Select Date</h3>
            <select onChange={handleDateChange} value={selectedDate}>
              <option value="">Select a date</option>
              {generateDateOptions().map((date, index) => (
                <option key={index} value={date}>
                  {date}
                </option>
              ))}
            </select>

            <div className="availability-heading">
              <h3>Availability</h3>
            </div>

            <div className="availability-buttons">
              {Array.from({ length: 24 }, (_, hour) => {
                const formattedTime = `${hour.toString().padStart(2, '0')}:00`;
                const period = availability.find((p) => p.time === formattedTime);
                const isDisabled = !period || period.available_tables === 0;

                return (
                  <button
                    key={hour}
                    className={`availability-button ${selectedTime === formattedTime ? 'selected' : ''}`}
                    onClick={() => handleButtonClick(formattedTime)}
                    disabled={isDisabled}
                  >
                    {formattedTime}
                  </button>
                );
              })}
            </div>

            {selectedTime && (
              <p>
                Selected Time: {selectedTime} —{' '}{availability.find((p) => p.time === selectedTime)?.available_tables || 0} tables available
              </p>
            )}

            {selectedDate && (
              <div className="booking-form">
                <div className="input-field">
                  <label htmlFor="numberOfPeople">Number of People</label>
                  <input
                    id="numberOfPeople"
                    type="number"
                    value={numberOfPeople}
                    onChange={(e) => setNumberOfPeople(e.target.value)}
                    min="1"
                    max={restaurant.max_people_per_table}
                  />
                </div>
                <div className="input-field">
                  <label htmlFor="contactName">Contact Name</label>
                  <input
                    id="contactName"
                    type="text"
                    value={contactName}
                    onChange={(e) => setContactName(e.target.value)}
                  />
                </div>
                <div className="input-field">
                  <label htmlFor="contactNumber">Contact Number</label>
                  <input
                    id="contactNumber"
                    type="tel"
                    value={contactNumber}
                    onChange={(e) => setContactNumber(e.target.value)}
                    pattern="^\d{10}$"
                    maxLength="10"
                  />
                </div>

                {formError && <p className="form-error">{formError}</p>}

                <button className="add-btn" onClick={handleSubmit} disabled={isButtonDisabled}>
                  Book Table
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
