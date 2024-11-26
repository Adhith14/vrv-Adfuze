# AdFuze - Flask Application Setup Guide

The project Influencer Engagement and Sponsorship Coordination Platform is built using Python Flask. This guide provides a detailed process to set up and run a Flask application.

---

## Prerequisites

Before you begin, ensure you have **Python 3.6 or higher** and **pip** installed on your system.

---

## Instructions

1. Open your terminal or command prompt and clone the repository:
   ```bash
   git clone https://github.com/Adhith14/vrv-Adfuze.git
   cd <project-directory>

2. Create virtual Environment

   For Windows:
   ```bash
   python -m venv venv
   source venv\Scripts\activate

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the application
   ```bash
   flask run

# Influencer Engagement and Sponsorship Coordination Platform

A platform designed to connect **Sponsors** and **Influencers** for seamless collaboration. Sponsors can advertise their products/services, and influencers can earn monetary benefits.

---

## Frameworks Used

The platform will be built using:
- **Flask**: For application logic.
- **Jinja2 + Bootstrap**: For HTML generation and styling.
- **SQLite**: For data storage.

> **Note**: All demos will run on a local machine.

---

## Roles and Features

### 1. Admin  
- Monitor users and campaigns.
- View platform statistics.
- Flag inappropriate users or campaigns.
> **Note**: Default admin credentials are - username: admin, password: admin.

### 2. Sponsors  
- Create and manage multiple campaigns.  
- Search for influencers and send ad requests.  

**Sponsor Profile:**
- Company/Individual Name.  
- Industry.  
- Budget.

### 3. Influencers  
- Receive, accept/reject, or negotiate ad requests.  
- Search for and join public campaigns based on category, budget, etc.  

**Influencer Profile:**
- Name.  
- Category and Niche.  
- Reach (followers/activity).  

--- 

This platform ensures efficient collaboration and transparent management for both Sponsors and Influencers.


