// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./Login";
import Home from "./Home";
import ProductList from "./product/ProductList";
import DiscountList from "./discount/DiscountList";

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home/*" element={<Home />} />
      <Route path="/products/" element={<ProductList />} />
      <Route path="/discounts/" element={<DiscountList />} />
    </Routes>
  </Router>
);

export default App;
