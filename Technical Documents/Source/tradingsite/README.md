# 📈 TradeIT

## 📋 Table of Contents

- [🌐 Overview](#overview)
- [⚙️ Features](#features)
- [🌱 Configuring the Virtual Environment](#running-the-virtual-environment)
- [🚀 Launching the Application](#running-the-program)
- [🧪 Executing Test Suites](#running-the-tests) 
- [📦 Requirements](#requirements)
- [🌲 Project Structure](#project-structure) 

## 🌐 Overview

## ⚙️ Features

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

## 🌲 Project Structure

```plaintext
TradeIT/
├── Product-Documents/
│   ├── Literature Review
│   ├── Final Report
├── Technical-Documents/
│   ├── Source/
│   │   └── tradingsite/
│           ├──
│           ├── 
│           ├── 
│           ├── 
│           ├── 
│           ├── 
│           ├── 
│           ├── 
│           ├── 
│           ├── 
│   └── Jupyter/
│       └── Notebooks
├── LICENSE
└── README.md
```
