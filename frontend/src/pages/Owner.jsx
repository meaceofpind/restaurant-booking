import React, { useState } from 'react';
import AddRestaurant from '../components/AddRestaurant';
import ManageSlots from '../components/ManageSlots';
import Navbar from '../components/Navbar';
import '../assets/owner.css'; // Make sure your CSS file is correctly linked

const OwnerPage = () => {
  const [activeTab, setActiveTab] = useState('addRestaurant');

  return (
    <div className="owner-page">
      {/* Navbar component */}
      <Navbar />

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'addRestaurant' ? 'active' : ''}`}
          onClick={() => setActiveTab('addRestaurant')}
        >
          Add Restaurant
        </button>
        <button
          className={`tab ${activeTab === 'manageSlots' ? 'active' : ''}`}
          onClick={() => setActiveTab('manageSlots')}
        >
          Manage Slots
        </button>
        <div className="slider" style={{ left: activeTab === 'addRestaurant' ? '0%' : '50%' }}></div>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'addRestaurant' && <AddRestaurant />}
        {activeTab === 'manageSlots' && <ManageSlots />}
      </div>
    </div>
  );
};

export default OwnerPage;
