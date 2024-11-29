
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const handleResponse = async (response) => {
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Something went wrong');
    }

    return response.json();
  };
  
  // Function to filter out empty values from input filters
  const cleanFilters = (filters) => {
    const cleanedFilters = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '' && value !== null) {
        cleanedFilters[key] = value;
      }
    });
    return cleanedFilters;
  };
  
  const apiService = {
    searchRestaurants: async (filters, page = 1, pageSize = 10) => {
      const cleanedFilters = cleanFilters({
        name: filters.name,
        city: filters.city,
        area: filters.area,
        cuisine: filters.cuisine,
        rating_min: filters.ratingMin,
        rating_max: filters.ratingMax,
        cost_for_two_max: filters.costMax,
        cost_for_two_min: filters.costMin,
        plain_text: filters.plainText,
      });
  
      console.log('Requesting filters:', JSON.stringify(cleanedFilters));
  
      // Construct query parameters for pagination
      const queryParams = new URLSearchParams({
        page,
        page_size: pageSize,
      }).toString();
  
      // Send cleaned filters in the request body, and pagination as query parameters
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/search?${queryParams}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(cleanedFilters),
        });
  
        return handleResponse(response);
      } catch (error) {
        console.error('Fetch failed:', error);
        throw error; // Re-throw the error to handle it in the caller
      } // Returns array of restaurants
    },registerRestaurant: async (restaurantData) => {
      try {
        const response = await fetch('${API_BASE_URL}/api/v1/entities', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(restaurantData),
        });
  
        const result = await handleResponse(response);
        return { success: true, message: result.message, entity: result.entity };
      } catch (error) {
        console.error('Registration failed:', error);
        return { success: false, message: error.message };
      }
    },
    getEntities: async () => {
      try {
        const response = await fetch('${API_BASE_URL}/api/v1/entities', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        return handleResponse(response);
      } catch (error) {
        console.error('Fetching entities failed:', error);
        throw error; // Re-throw the error to handle it in the caller
      }
    },

    getSlots: async (entityId) => {
  
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/entities/${entityId}/slots`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
  
        return handleResponse(response);
      } catch (error) {
        console.error('Fetching slots failed:', error);
        throw error; // Re-throw the error to handle it in the caller
      }
    },
    addOrUpdateSlot: async (entityId, startTime, endTime, numberOfDays) => {
      try {
        // Construct query parameters to send in the URL
        const queryParams = new URLSearchParams({
          start: startTime,
          end: endTime,
          number_of_days: numberOfDays,
        }).toString();
  
        // Send the request with query parameters in the URL
        const response = await fetch(`${API_BASE_URL}/api/v1/entities/${entityId}/slots?${queryParams}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
  
        // Handle the response
        const result = await handleResponse(response);
        return { success: true, message: result.message, start_time: result.start_time, end_time: result.end_time };
      } catch (error) {
        console.error('Slot update failed:', error);
        return { success: false, message: error.message };
      }
    },

    getAvailability: async (entityId, date) => {
      try {
        // Make a GET request to the /availability/{entity_id} endpoint with the entityId and date parameters.
        const response = await fetch(`${API_BASE_URL}/api/v1/availability/${entityId}?date=${date}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
  
        // Handle and return the response data
        return handleResponse(response); // This will return the list of availability objects.
      } catch (error) {
        console.error('Fetching availability failed:', error);
        throw error; // Re-throw the error to handle it in the caller
      }
    },
    bookTable: async (bookingData) => {
      try {
        // Prepare the booking data to send to the backend
        const response = await fetch('${API_BASE_URL}/api/v1/book_table', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(bookingData),
        });
  
        // Handle the response
        const result = await handleResponse(response);
        return { success: true, message: result.message, booking_id: result.booking_id };
      } catch (error) {
        console.error('Booking failed:', error);
        return { success: false, message: error.message };
      }
    },
  };
  
  export default apiService;
  