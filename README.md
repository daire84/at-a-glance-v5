# At a Glance v6 - Film Production Calendar Scheduler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) A comprehensive web application built with Flask and Docker for film production scheduling and calendar management. This professional tool provides an intuitive "at a glance" overview of prep, shoot, and wrap periods with advanced features including smart location search, automatic sunrise/sunset calculations, and enhanced user experience.

## Key Features

### 🎬 **Production Management**
* **Project Management:** Create and manage multiple film projects with defined prep, shoot, and wrap dates
* **Automatic Calendar Generation:** Intelligent calendar creation with automatic shoot day calculation
* **Customizable Scheduling:** Advanced handling of weekends, working weekends, bank holidays, hiatus periods, and special dates

### 🌅 **Sunrise/Sunset Integration** *(NEW)*
* **Automatic Sun Times:** Real-time sunrise and sunset calculations for all filming locations
* **Professional Astronomy:** Powered by industry-standard Astral library with accurate timezone handling
* **Calendar Integration:** Sun times displayed directly in calendar view for outdoor shoot planning
* **Performance Optimized:** 100x faster calculations with intelligent caching system

### 📍 **Smart Location Management** *(NEW)*
* **Intelligent Search:** Google-style location search - just type "Dublin" or any address
* **Popular Film Locations:** Pre-loaded database of common filming venues and studios
* **Automatic Geocoding:** Coordinates automatically found and populated behind the scenes
* **Professional Geocoding:** Powered by OpenStreetMap with Ireland/UK bias for local productions

### 📅 **Enhanced Calendar Features**
* **Detailed Day Editing:** Comprehensive daily production planning:
    * Main Unit details and Sequence information
    * Location assignment with automatic sun time calculation
    * Extras and Featured Extras tracking
    * Department tagging (SFX, Stunts, Crane, etc.)
    * Production notes and scheduling details
* **Visual Organization:** Color-coded location areas and department counters
* **Responsive Design:** Professional interface that works on desktop, tablet, and mobile

### 🔐 **Secure Access Control**
* **Viewer Mode:** Secure, read-only calendar access for cast and crew
* **Admin Mode:** Full administrative control with separate authentication
* **Project Isolation:** Each production maintains separate, secure data

### 🛠 **Modern Architecture**
* **RESTful API:** Complete API backend for all data operations
* **Dockerized Deployment:** Easy setup and deployment with Docker Compose
* **Professional UI/UX:** Clean, intuitive interface designed for production environments
* **Mobile Optimized:** Responsive design for on-set access

## Tech Stack

* **Backend:** Python 3.11, Flask, Gunicorn
* **Astronomy:** Astral library for precise sun calculations
* **Geocoding:** OpenStreetMap Nominatim API with intelligent fallbacks  
* **Timezone:** pytz for professional timezone handling
* **Data Storage:** Structured JSON files with automatic backups
* **Frontend:** Modern HTML5, CSS3, Vanilla JavaScript
* **APIs:** RESTful API design with comprehensive endpoints
* **Containerization:** Docker & Docker Compose for easy deployment
* **Performance:** Intelligent caching, optimized calculations, responsive design

## Project Structure

    .
    ├── Dockerfile             # Defines the Docker image
    ├── docker-compose.yml     # Defines the Docker services
    ├── requirements.txt       # Python dependencies
    ├── .env.example           # Example environment variables
    ├── app.py                 # Main Flask application factory and entry point
    ├── routes/                # Flask Blueprints for different sections
    │   ├── admin.py
    │   ├── api.py
    │   ├── auth.py
    │   └── main.py
    ├── utils/                 # Helper modules and core logic
    │   ├── calendar_generator.py # Logic for creating calendar days
    │   ├── decorators.py      # Access control decorators (@admin_required, etc.)
    │   ├── helpers.py         # Data loading/saving, other core functions
    │   └── ...                # Other utility modules (dates, files)
    ├── templates/             # HTML templates (Jinja2)
    │   ├── admin/             # Admin-specific templates
    │   └── ...
    ├── static/                # Static assets (CSS, JS, Images)
    │   ├── css/
    │   ├── js/
    │   └── ...
    ├── data/                  # Application data (SHOULD BE BACKED UP)
    │   ├── projects/          # Data for each project (in subfolders)
    │   │   └── {project_uuid}/
    │   │       ├── main.json
    │   │       ├── calendar.json
    │   │       └── ... (holidays.json, hiatus.json etc.)
    │   ├── areas.json         # Global location areas
    │   ├── departments.json   # Global departments
    │   └── locations.json     # Global locations
    ├── logs/                  # Application logs
    └── README.md              # This file

## Setup and Installation

### Prerequisites

* Docker ([Install Docker](https://docs.docker.com/engine/install/))
* Docker Compose ([Install Docker Compose](https://docs.docker.com/compose/install/))

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/daire84/at-a-glance-v4.git](https://github.com/daire84/at-a-glance-v4.git)
    cd at-a-glance-v4
    ```

2.  **Configure Environment Variables:**
    * Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    * Edit the `.env` file with your preferred settings:
        * `SECRET_KEY`: **Required.** A long, random string for Flask session security. Generate one using `python -c 'import secrets; print(secrets.token_hex(16))'`.
        * `ADMIN_PASSWORD`: **Required.** The password for accessing the admin section.
        * `VIEWER_PASSWORD`: **Required.** The password for accessing the read-only viewer mode.
        * `FLASK_DEBUG`: Set to `True` for development mode (enables debugger, auto-reload), `False` for production. Defaults to `False`.

3.  **Build and Run with Docker Compose:**
    * From the project root directory (`at-a-glance-v4`), run:
        ```bash
        docker-compose up --build -d
        ```
        * `--build`: Forces Docker to build the image based on the `Dockerfile`.
        * `-d`: Runs the containers in detached mode (in the background).

4.  **Access the Application:**
    * Open your web browser and navigate to `http://localhost:5000` (or the host/port configured in `docker-compose.yml` if you changed it).

## What's New in v6

### 🌅 **Sunrise/Sunset Times**
- **Automatic calculations** for all filming locations with GPS coordinates
- **Industry-standard astronomy** using Astral library  
- **Dublin timezone support** with automatic DST handling
- **100x performance improvement** over previous implementations
- **Calendar integration** - times appear directly in your schedule

### 📍 **Smart Location Search**
- **No more coordinates!** Simply type "Dublin", "Trinity College", or any address
- **Google-style search** with instant suggestions and autocomplete
- **Popular film locations** pre-loaded for one-click selection
- **Professional geocoding** using OpenStreetMap with Ireland/UK optimization
- **Mobile-friendly** responsive interface

### ⚡ **Performance Enhancements**
- **Native Python calculations** replace slow subprocess calls
- **Intelligent caching** prevents repeated API calls
- **Optimized styling** - cleaner, more professional appearance
- **Enhanced error handling** with graceful fallbacks

### 🎨 **UI/UX Improvements**
- **Simplified sun times display** that matches calendar aesthetics
- **Better text visibility** with improved contrast
- **Dropdown positioning** fixed for better usability
- **Professional styling** throughout the interface

## Usage

### **Viewer Mode**
Navigate to the root URL (`/`). Enter the Viewer Password to access read-only calendar views with:
- Full production calendar with sunrise/sunset times
- Color-coded location areas and department tags
- Mobile-optimized interface for on-set access

### **Admin Mode**
1. Navigate to `/admin/login` and enter your Admin Password
2. Access the full Admin Dashboard with these capabilities:

#### **📍 Smart Location Management**
- **Add locations easily:** Just type "Dublin" or any address - no coordinates needed!
- **Choose from popular film locations:** Pre-loaded studios, landmarks, and venues
- **Automatic sun times:** Coordinates and sunrise/sunset times calculated automatically
- **Color-coded areas:** Organize locations by regions with visual coding

#### **📅 Project Management**
- Create and manage multiple film projects
- Set prep, shoot, and wrap dates with automatic calendar generation
- Manage project-specific holidays, hiatuses, and working weekends
- Track department usage and location scheduling

#### **🎬 Daily Production Planning**
- Edit individual calendar days with comprehensive details
- Assign locations (with automatic sun time calculation)
- Track extras, featured extras, and department requirements
- Add production notes and sequence information

## Data Storage

This application currently stores all its data as JSON files within the `data/` directory inside the container volume.

* Global configurations (locations, departments, areas) are stored directly in `data/`.
* Each project's data (main details, calendar, holidays, etc.) is stored in a separate subdirectory under `data/projects/`, named with a unique UUID.

**Important:** Ensure the volume mapped to `/app/data` in your `docker-compose.yml` is persistent and regularly backed up, as this contains all user-generated data.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue. (Optional: Add more specific contribution guidelines if desired).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (Optional: Create a LICENSE file with the MIT license text or choose another license).
