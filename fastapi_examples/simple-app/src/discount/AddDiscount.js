// src/AddDiscount.js
import React, { useState } from "react";
import CONSTANTS from "../Constants";

const AddDiscount = ({ onAddDiscount }) => {
  const [customerCategoryId, setCustomerCategoryId] = useState(1);
  const [productCategoryId, setProductCategoryId] = useState(1);
  const [percentage, setPercentage] = useState(0);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("access_token");
    if (!token) {
      console.error("No access token found");
      return;
    }

    const newDiscount = {
      customer_category_id: customerCategoryId,
      product_category_id: productCategoryId,
      percentage,
    };

    try {
      const response = await fetch(`${CONSTANTS.BASE_URL}/discounts`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newDiscount),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to add discount");
      }

      onAddDiscount();
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div>
      <h3>Add Discount</h3>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Customer Category ID:</label>
          <input
            type="number"
            value={customerCategoryId}
            onChange={(e) => setCustomerCategoryId(Number(e.target.value))}
            required
          />
        </div>
        <div>
          <label>Product Category ID:</label>
          <input
            type="number"
            value={productCategoryId}
            onChange={(e) => setProductCategoryId(Number(e.target.value))}
            required
          />
        </div>
        <div>
          <label>Percentage:</label>
          <input
            value={percentage}
            onChange={(e) => setPercentage(Number(e.target.value))}
            required
          />
        </div>
        <button type="submit">Add Discount</button>
      </form>
    </div>
  );
};

export default AddDiscount;
