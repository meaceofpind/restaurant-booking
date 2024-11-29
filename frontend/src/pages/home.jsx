import { useNavigate } from 'react-router-dom';
import '../assets/homepage.css';  // Import the CSS file

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1 className="home-heading">Welcome to the Restaurant Booking System</h1>
      <div className="button-container">
        <button className="home-button" onClick={() => navigate('/customer')}>
          Customer Page
        </button>
        <button className="home-button" onClick={() => navigate('/owner')}>
          Owner Page
        </button>
      </div>
    </div>
  );
};

export default Home;
