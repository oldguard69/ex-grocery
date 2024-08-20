// src/ProductList.js
import React, { useEffect, useState } from "react";
import CONSTANTS from "../Constants";
import AddProduct from "./AddProduct";

const ProductList = () => {
  const [products, setProducts] = useState([]);

  const fetchProducts = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      console.error("No access token found");
      return;
    }

    try {
      const response = await fetch(`${CONSTANTS.BASE_URL}/products`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch products");
      }

      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div>
      <h2>Product List</h2>
      <ul>
        {products.map((product) => (
          <li key={product.product_id}>
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <p>Price: ${product.price}</p>
            <p>
              Categories:{" "}
              {product.product_categories
                .map((category) => category.name)
                .join(", ")}
            </p>
          </li>
        ))}
      </ul>
      <AddProduct onAddProduct={fetchProducts} />
    </div>
  );
};

export default ProductList;
