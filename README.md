# Audify Music Streaming Application

## Introduction

Audify is an intuitive music streaming application that leverages modern web technologies and a robust back-end architecture. This document outlines the project’s objectives, technical framework, and features. Built with Flask and supported by HTML, CSS, and an SQLite database, Audify offers a comprehensive platform for users to discover and enjoy a diverse music library.

## Project Setup

### Prerequisites

- Python installed on your system.
- Virtualenv package installed.

### Installation Steps

1. **Extract the Project**:
  Unzip the project into the desired directory: `[project dir]`.

3. **Navigate to Project Directory**:

   ```bash
   cd [project dir]
   ```

4. **Create a Virtual Environment**:

   ```bash
   virtualenv .env
   ```

5. **Activate Virtual Environment**:

   - On Windows:
     ```bash
     .env\Scripts\activate
     ```

6. **Install Dependencies**:
   ```bash
   python -m pip install -r requirements\requirements.txt
   ```

7. **Create a Superuser**:

   ```bash
   python -m flask create_superuser <username> <password>
   ```

    **Note:** Username and password must be a minimum of 6 characters. Passwords should include uppercase letters, special characters, and numbers.

1. **Download and Set Up Media**:

   - Download initial media data (tracks, album art, etc.) from [Google Drive Media Link](https://drive.google.com/file/d/1VYX7TTlG2D8swIrHA0ujgplGFPtoPrRQ/view).
   - Unzip and place the `media` dir in a sibling directory of the project: `/media/`.
   - Ensure the directory is named `media` for compatibility.

2.  **Run the Application**:

   ```bash
   python app.py
   ```

   - Visit `http://localhost:5000` in your browser.
   - Log in with your superuser credentials to access the platform.

### Final Steps

Once you've completed these steps, you should be able to access the login page and explore the application with your superuser account.
