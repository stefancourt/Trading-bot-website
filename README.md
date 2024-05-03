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
### On Mac
To configure the virtual environment for the TradeIT application on macOS, follow these steps:

1. Make sure that [Python 3.11.x](https://www.python.org/downloads/macos/) is installed on the device
1. Navigate to the **Technical Documents/Source/tradingsite directory**.
2. Run the following commands to activate the virtual environment:

```bash
chmod +x commands.sh
./commands.sh
```

This will create a virtual environment, install all packages and the redis server needed for the application. Please ensure that you have python 3.11.x installed on the device.

### On Windows
To configure the virtual environment for the TradeIT application on Windows, follow these steps:

1. Make sure that [Python 3.11.x](https://www.python.org/downloads/windows/) is installed on the device
2. download the developer version of [Memurai](https://www.memurai.com/get-memurai)
3. Navigate to the **Technical Documents/Source/tradingsite directory**.
4. Run the following commands to activate the virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

This will create a virtual environment, install all packages and the memurai server needed for the application.

## 🚀 Launching the Application

To launch the TradeIT application, follow the steps below:

1. Execute the following command:

```bash
# For MacOS
redis-server
```

```bash
# For Windows
memurai-server
```

2. In a seperate terminal navigate to the **Technical Documents/Source/tradingsite** directory.
3. In a seperate terminal execute the following commands:

```bash
# For MacOS
source venv/bin/activate
python3 manage.py runserver 0.0.0.0:8000
```

```bash
# For Windows
venv\Scripts\activate
python3 manage.py runserver 0.0.0.0:8000
```

4. If the when running the previous command, a migration warning appears, execute

```bash
# Should only occur on first time running the application
python3 manage.py makemigrations
python3 manage.py migrate
```

### 💻 On PC
1. Put http://127.0.0.1:8000/ into the url to run the application.

### 📱 on Phone
1. Add your local IP address of your computer to your ALLOWED_HOSTS in the **Technical Documents/Source/tradingsite/tradingsite/settings.py** file.
2. Change
```bash
socket = new WebSocket('ws://localhost:8000/ws/trade/');
```
to
```bash
socket = new WebSocket('ws://{your_ip}:8000/ws/trade/');
```
in both **Technical Documents/Source/tradingsite/tradingsite/trade/trade.js** and **Technical Documents/Source/tradingsite/tradingsite/aitrade/ai-trade.js** files

3. Put http://{your_ip}:8000/ into the url to run the application
Important: If these changes have completed to run on computer you will need to revert the changes.
## 🧪 Executing Test Suites

To execute the test suites for the TradeIT application, follow these steps:

1. Ensure you are within the application's virtual environment.
2. Run all the tests by entering the following command in the terminal:

```bash
python3 manage.py test
```

3. If wanting to run tests for a specific app run

```bash
python3 manage.py test '<app>'
```
Replace `<app>` with the name of the app whose tests you want to run. For example:

```bash
python3 manage.py test trade
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
└── README.md
```
