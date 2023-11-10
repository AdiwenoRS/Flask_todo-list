# Flask To-Do List Application

A simple To-Do list web application built with Flask in Python.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)

## Introduction

This Flask-based To-Do list application allows users to create, manage, and organize their tasks easily. It provides a simple web interface for managing your tasks.

## Features

- User authentication (register, login, logout) with cookies
- Create, read, update, and delete tasks
- Search tasks
- Mark tasks as completed
- User-friendly interface

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have the following installed on your system:

- Python 3 (Python 3.10 is recommended)
- PIP (Python Package Installer)
- MYSQL (for database)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Arhta/to-do_list_Flask
   cd to-do_list_Flask

2. Create virtual environment (optional)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows, use
   source venv\Scripts\activate

3. Install the project dependecies
   ```bash
   pip install -r requirements.txt

4. Import MYSQL database
   ```bash
   mysql -u <user> -p -e "create database to-do_list";
   mysql -u <user> -p to-do_list < to-do_list.sql

5. Set your MYSQL username and password in `app.py` file at:
   - `app.config['MYSQL_DATABASE_USER'] = '<username>'`
   - `app.config['MYSQL_DATABASE_PASSWORD'] = '<password>'`

## Usage

1. Run app
   ```bash
   python3 app.py
3. Open your web browser and navigate to http://localhost:8989.
4. Register for an account and login.
5. You can start adding, editing, and completing tasks.
