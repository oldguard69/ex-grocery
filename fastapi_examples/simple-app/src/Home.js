// src/Home.js
import React from "react";
import { Link, Route, Routes, useLocation } from "react-router-dom";
import ProductList from "./product/ProductList";
import DiscountList from "./discount/DiscountList";

const Home = () => {
  const location = useLocation();

  return (
    <div>
      <h2>Home Page</h2>
      <nav>
        <ul>
          <li>
            <Link
              to="/products"
              className={location.pathname === "/products" ? "active" : ""}
            >
              Products
            </Link>
          </li>
          <li>
            <Link
              to="/discounts"
              className={location.pathname === "/discounts" ? "active" : ""}
            >
              Discounts
            </Link>
          </li>
        </ul>
      </nav>
      <Routes>
        <Route path="/products" element={<ProductList />} />
        <Route path="/discounts" element={<DiscountList />} />
      </Routes>
    </div>
  );
};

export default Home;
