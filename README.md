# Trader Go API

Trader Go API is a Django-based backend application designed to provide user authentication, stock trading information, news, and WebSocket-based real-time updates. This project is built with Django REST Framework and integrates third-party APIs for stock and news data.

## Features

- **User Management**:

  - User registration, login, and email verification.
  - JWT-based authentication.
  - User profile management.

- **Stock Trading**:

  - Fetch stock details and ticker information.
  - Manage a wishlist of stocks.
  - Real-time stock price updates via WebSocket.

- **News Integration**:

  - Fetch stock-related news articles using the NewsAPI.

- **WebSocket Support**:
  - Real-time communication for stock updates using Django Channels.

## Installation

### Prerequisites

- Python 3.12 or higher
- Django 5.0 or higher
- A virtual environment tool (e.g., `venv` or `pipenv`)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/UmangSachdeva/Trader-Go-Backend
   cd trader-go-api
   ```
