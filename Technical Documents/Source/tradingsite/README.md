# 📈 TradeIT

## 🌐 Overview
Introducing TradeIt your all in one software for managining finance, completing trades and viewing the news. Whether your a seasoned investor or just starting out, this app can help elevate your trading experience. With the option of placing trades quickly over a long time frame without the risk of losing capital, this software is perfect for those wanting to learn about long term trades in the market.

## 📋 Table of Contents

- [🌐 Overview](#overview)
- [⚙️ Features](#features)
- [🌱 Configuring the Virtual Environment](#running-the-virtual-environment)
- [🚀 Launching the Application](#running-the-program)
- [🧪 Executing Test Suites](#running-the-tests) 
- [📦 Requirements](#requirements)
- [🌲 Project Structure](#project-structure) 

## ⚙️ Features

- Stats page where you can view portfolio for different stocks
- User trading page where you can place your own trades
- AI trading page where you can have an AI place trades for you
- Finance page where you can manage your funds
- News page where you can view the news for all stocks
- Features a robust AI that has been tested with backtesting


## 🌱 Configuring the Virtual Environment

To configure the virtual environment for the TradeIT application on macOS, follow these steps:

1. Navigate to the **Technical Documents/Source/tradingsite directory**.
2. Run the following commands to activate the virtual environment:

```bash
chmod +x commands.sh
./commands.sh
```

This will create a virtual environment, install all packages and the redis server needed for the application. Please ensure that you have python 3.11.x installed on the device.

## 🚀 Launching the Application

To launch the TradeIT application, follow the steps below:

1. Execute the following command:

```bash
redis-server
```

2. In a seperate terminal navigate to the **Technical Documents/Source/tradingsite** directory.
3. In a seperate terminal execute the following commands:

```bash
source venv/bin/activate
python3 manage.py runserver 0.0.0.0:8000
```

## 🧪 Executing Test Suites

To execute the test suites for the TradeIT application, follow these steps:

1. Ensure you are within the application's virtual environment.
2. Locate the tests using the **pytest** framework within each separate app, including backend, frontend, and database tests.
3. Run the tests for a specific app by entering the following command in the terminal:

```bash
pytest <app>
```

Replace `<app>` with the name of the app whose tests you want to run. For example:

```bash
pytest trade
```

## 📦 Requirements
The following libraries and packages are required to run the TradeIT application. Ensure that you have the correct versions installed in your development environment.
- [Django](https://www.djangoproject.com/) 4.2.6
- [pandas](https://pandas.pydata.org/docs/) 2.1.3
- [django-extensions](https://django-extensions.readthedocs.io) 3.2.3
- [plotly](https://plotly.com/python/) 5.18.0
- [channels](https://channels.readthedocs.io/en/latest/) 4.0.0
- [daphne](https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/daphne/) 4.1.0
- [channels-redis](https://channels.readthedocs.io/en/stable/topics/channel_layers.html) 4.2.0
- [asgiref](https://asgi.readthedocs.io/en/latest/) 3.7.1
- [yfinance](https://pypi.org/project/yfinance/) 0.2.36

## 🌲 Project Structure
Any (item) means multiple files of type *item*

```plaintext
TradeIT/
├── Product-Documents/
│   ├── Literature Review
│   ├── Final Report
│   └── Project Slides
├── Technical-Documents/
│   ├── Source/
│   │   └── tradingsite/
│   │       ├── aitrade/
│   │       │   └── (ai-trade-app)
│   │       ├── trade/
│   │       │   └── (trade-app)
│   │       ├── finance/
│   │       │   └── (finance-app)
│   │       ├── main/
│   │       │   └── (stats-app)
│   │       ├── news/
│   │       │   └── (news-app)
│   │       ├── logins/
│   │       │   └── (logins-app)
│   │       ├── stock_data/
│   │       │   └── (all-stock-data)
│   │       ├── tradingsite/
│   │       │   └── (settings)
│   │       ├── manage.py
│   │       ├── commands.sh
│   │       ├── requirements.txt
│   │       └── db.sqlite3
│   └── Jupyter/
│       ├── (stock)_hist.csv
│       └── AI-Backtesting.ipynb
├── LICENSE
└── README.md
```
