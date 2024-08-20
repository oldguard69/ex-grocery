// src/DiscountList.js
import React, { useEffect, useState } from "react";
import CONSTANTS from "../Constants";
import AddDiscount from "./AddDiscount";

const DiscountList = () => {
  const [discounts, setDiscounts] = useState([]);

  const fetchDiscounts = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      console.error("No access token found");
      return;
    }

    try {
      const response = await fetch(`${CONSTANTS.BASE_URL}/discounts/`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch discounts");
      }

      const data = await response.json();
      setDiscounts(data);
    } catch (error) {
      console.error("Error fetching discounts:", error);
    }
  };

  useEffect(() => {
    fetchDiscounts();
  }, []);

  return (
    <div>
      <h2>Discount List</h2>
      <ul>
        {discounts.map((discount) => (
          <li key={discount.discount_id}>
            <p>Percentage: {discount.percentage}%</p>
            <p>Active: {discount.is_active ? "Yes" : "No"}</p>
            <p>Product Category: {discount.product_category.name}</p>
            <p>Customer Category: {discount.customer_category.name}</p>
          </li>
        ))}
      </ul>
      <AddDiscount onAddDiscount={fetchDiscounts} />
    </div>
  );
};

export default DiscountList;
