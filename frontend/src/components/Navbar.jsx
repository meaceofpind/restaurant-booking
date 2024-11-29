import React from 'react';
import { Link } from 'react-router-dom'; 
import '../assets/navbar.css'

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/customer">Customer</Link></li>
        <li><Link to="/owner">Owner</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
