# API service


## User
### Register
Let customer user to create new account.  
If the email is already exist, an error will be raised.

Example request
```
POST /register

{
    "email": "",
    "password": ""
}
```

Example success response
```
{"message": ""}
```

### Login
Let user, both staff and customer to login into the system.  
Raise error when:
- Email is not exist in the database.
- Wrong password.

Example request
```
POST /login

{
    "email": "",
    "password": ""
}
```

Example success response
```
{"access_token": "", "token_type": "bearer"}
```


### Send verification email
Send an email contains an OTP code for user to verify their account.  
Raise error when:
- User already verified their email.

Example request
```
GET /email-verification
Authorization: Bearer access-token

```

Example success response
```
{"message": ""}
```

### Verify email
Verify the account using the otp contains in the email sent to customer.  
Raise error when:
- The OTP is invalid (based on the HOTP algorithm)
- The OTP is expired (based on the `users.otp_expired_at` column)

Example request
```
GET /email-verification
Authorization: Bearer access-token

{
    "otp": ""
}
```

Example success response
```
{"message": ""}
```


## Product
### List product
Return all the products in the system.

Example request
```
GET /products
```


Example success response
```
[
    {
        "product_id": 1,
        "name": "Coffee",
        "description": "",
        "price": 68.79,
        "created_at": "2024-07-29T16:58:09.400986",
        "product_categories": [
            {
                "category_id": 1,
                "name": "Fast Food"
            },
            {
                "category_id": 2,
                "name": "Frozen Food"
            }
        ]
    }
]
```

### Create product
For staff to create product.  
Raise error when:
- The user who call the API is not staff.
- There are `product_category_id` that not exist in the `product_categories` table.
- There are `product_category_id` belong to department that the user who call the API don't linked to.



Example request
```
POST /products/
Authorization: Bearer access-token

{
    "name": "Noddle",
    "price": "68.79",
    "description": "Instant Noddle",
    "product_category_ids": [1]
}
```

Example success response
```
{
        "product_id": 1,
        "name": "Noddle",
        "description": "Instant Noddle",
        "price": 68.79,
        "created_at": "2024-07-29T16:58:09.400986",
        "product_categories": [
            {
                "category_id": 1,
                "name": "Fast Food"
            },
            {
                "category_id": 2,
                "name": "Frozen Food"
            }
        ]
    }
```


### Update product
For staff to update the product.  
Raise error when:
- The user who call the API is not staff.
- The department of the product categories the product is linked to, is not the department of the user.
- There is no product with the `product_id` path param.
- There are `product_category_id` that not exist in the `product_categories` table.
- There are `product_category_id` belong to department that the user who call the API don't linked to.


Example request
```
PUT /products/:product_id
Authorization: Bearer access-token

{
    "name": "Noddle",
    "price": "68.79",
    "description": "Instant Noddle",
    "product_category_ids": [1]
}
```

Example success response
```
{
        "product_id": 1,
        "name": "Noddle",
        "description": "Instant Noddle",
        "price": 68.79,
        "created_at": "2024-07-29T16:58:09.400986",
        "product_categories": [
            {
                "category_id": 1,
                "name": "Fast Food"
            },
            {
                "category_id": 2,
                "name": "Frozen Food"
            }
        ]
    }
```


## Product Category
### List product categories
Return the product category list

Example request
```
GET /product-categories
```

Example success response
```
[
    {
        "category_id": 1,
        "name": "Fast Food"
    },
    {
        "category_id": 2,
        "name": "Frozen Food"
    }
]
```

### Create product category
For staff to create new product category.  
Raise error when:
- User is not staff

Example request
```
POST /product-categories
Authorization Bearer access-token

{
    "name": "Traditional dish",
    "department_id": 1
}
```

Example success response
```

```


## Order
### List orders
For user to list their created orders.

Example request
```
GET /orders
Authorization Bearer access-token

```

Example success response
```
[
    {
        "order_id": 1,
        "note": "this is my third order",
        "discount": null,
        "total_items": 2,
        "total_price": 4587.9,
        "discount_price": 0.0,
        "price": 4587.9
    }
]
```

### Create orders
For customer to create order.  
Increase the `user.success_order_count` to 1.  
Update the `usr.customer_category_id` base on the `user.success_order_count`.  
Raise error when:
- User is not customer
- The `items` is empty.
- There are `product_id` that not exist in the database.
- The `discount_id` is not exist in the database.

Example request
```
POST /orders
Authorization Bearer access-token

{
    "note": "this is my third order",
    "items": [
        {
            "product_id": 1,
            "quantity": 10
        },
        {
            "product_id": 2,
            "quantity": 100
        }
    ]
}
```

Example success response
```
{
    "order_id": 1,
    "note": "this is my third order",
    "discount": null,
    "total_items": 0,
    "total_price": 0.0,
    "items": [
        {
            "product": {
                "product_id": 1,
                "name": "Coffee",
                "description": "",
                "price": 68.79,
                "created_at": "2024-07-29T16:58:09.400986",
                "product_categories": [
                    {
                        "category_id": 1,
                        "name": "Fast Food"
                    },
                    {
                        "category_id": 2,
                        "name": "Frozen Food"
                    }
                ]
            },
            "quantity": 10,
            "price": 68.79
        },
        {
            "product": {
                "product_id": 2,
                "name": "Noddle",
                "description": "",
                "price": 39.0,
                "created_at": "2024-07-29T16:58:09.400986",
                "product_categories": [
                    {
                        "category_id": 4,
                        "name": "Cake and Candy"
                    }
                ]
            },
            "quantity": 100,
            "price": 39.0
        }
    ],
    "discount_price": 0.0,
    "price": 0.0
}
```

### Get order details
Get the order details.  
Raise error when:
- User is not customer
- The `order_id` is not exist in the database.

Example request
```
GET /orders/order_id
Authorization Bearer access-token

```

Example success response
```
{
    "order_id": 1,
    "note": "this is my third order",
    "discount": null,
    "total_items": 0,
    "total_price": 0.0,
    "items": [
        {
            "product": {
                "product_id": 1,
                "name": "Coffee",
                "description": "",
                "price": 68.79,
                "created_at": "2024-07-29T16:58:09.400986",
                "product_categories": [
                    {
                        "category_id": 1,
                        "name": "Fast Food"
                    },
                    {
                        "category_id": 2,
                        "name": "Frozen Food"
                    }
                ]
            },
            "quantity": 10,
            "price": 68.79
        },
        {
            "product": {
                "product_id": 2,
                "name": "Noddle",
                "description": "",
                "price": 39.0,
                "created_at": "2024-07-29T16:58:09.400986",
                "product_categories": [
                    {
                        "category_id": 4,
                        "name": "Cake and Candy"
                    }
                ]
            },
            "quantity": 100,
            "price": 39.0
        }
    ],
    "discount_price": 0.0,
    "price": 0.0
}
```


## Discount
### List discounts
For staff to list the discounts.  
Raise error when:
- User is not staff

Example request
```
GET /discounts
Authorization Bearer access-token
```

Example success response
```
[
    {
        "discount_id": 1,
        "percentage": 30.0,
        "is_active": true,
        "product_category": {
            "category_id": 1,
            "name": "Fast Food"
        },
        "customer_category": {
            "category_id": 1,
            "name": "Bronze"
        }
    },
    {
        "discount_id": 2,
        "percentage": 40.0,
        "is_active": true,
        "product_category": {
            "category_id": 1,
            "name": "Fast Food"
        },
        "customer_category": {
            "category_id": 2,
            "name": "Silver"
        }
    }
]
```


### Create discount
For staff to create a discount.  
Raise error when:
- The `customer_category_id` is not exist in the database.
- The `product_category-id` is not exist in the database.
- The department of the product category is not linked to the user.
- `percentage` is less than or equal 0, or greater than 100.

Example request
```
POST /discounts
Authorization Bearer access-token

{

    "customer_category_id": 1,
    "product_category_id": 1,
    "percentage": 0
}
```

Example success response
```
{
    "discount_id": 5,
    "percentage": 39.0,
    "is_active": true,
    "product_category": {
        "category_id": 1,
        "name": "Fast Food"
    },
    "customer_category": {
        "category_id": 1,
        "name": "Bronze"
    }
}
```


### Update discount
For staff to update a discount.  
Raise error when:
- The `customer_category_id` is not exist in the database.
- The `product_category-id` is not exist in the database.
- The department of the product category is not linked to the user.
- `percentage` is less than or equal 0, or greater than 100.
- There are not discount with the `discount_id`.
- The discount belongs to product category that have department not linked with the user.

Example request
```
POST /discounts/discount_id
Authorization Bearer access-token

{

    "customer_category_id": 1,
    "product_category_id": 1,
    "percentage": 0
}
```

Example success response
```
{
    "discount_id": 5,
    "percentage": 39.0,
    "is_active": true,
    "product_category": {
        "category_id": 1,
        "name": "Fast Food"
    },
    "customer_category": {
        "category_id": 1,
        "name": "Bronze"
    }
}
```