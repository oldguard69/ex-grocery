# API Service

## Features
### User
- Register
- Login
- Send email for verification
- Verify email

### Product
- List products
- View product details
- Create product
- Update product


### Product Category
- List product categories
- Create product category

### Order
- List orders
- Create order
- View order details

### Discount
- List discount
- Create discount
- Update discount


## Technologies use
- Python 3.12
- Postgres 16


## Environment variables
- `DB_HOST`: the host address of the Postgres database. Used for local development only.
- `DB_USER`: the root account in the Postgres database.
- `DB_PASSWORD`: the password of the root account.
- `DB_NAME`: the name of the main database.
- `SECRET_KEY`: the secret key use to sign the JWT.

## Run instruction
Run the following command to start both API and database service:  
`docker compose up -d`
