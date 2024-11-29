import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from '../pages/home';
import Customer from '../pages/Customer';
import Owner from '../pages/Owner';

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/customer" element={<Customer />} />
        <Route path="/owner" element={<Owner />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
