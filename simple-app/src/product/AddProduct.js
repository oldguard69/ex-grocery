// src/AddProduct.js
import React, { useState } from 'react';
import CONSTANTS from '../Constants';

const AddProduct = ({ onAddProduct }) => {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [productCategoryIds, setProductCategoryIds] = useState([]);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('access_token');
    if (!token) {
      console.error('No access token found');
      return;
    }

    const newProduct = {
      name,
      price: parseFloat(price),
      description,
      product_category_ids: productCategoryIds.split(',').map(Number),
    };

    try {
      const response = await fetch(`${CONSTANTS.BASE_URL}/products`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(newProduct),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to add product');
      }

      onAddProduct();
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div>
      <h3>Add Product</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input 
            type="text" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Price:</label>
          <input 
            type="number" 
            value={price} 
            onChange={(e) => setPrice(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Description:</label>
          <input 
            type="text" 
            value={description} 
            onChange={(e) => setDescription(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Product Category IDs (comma separated):</label>
          <input 
            type="text" 
            value={productCategoryIds} 
            onChange={(e) => setProductCategoryIds(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Add Product</button>
      </form>
    </div>
  );
};

export default AddProduct;