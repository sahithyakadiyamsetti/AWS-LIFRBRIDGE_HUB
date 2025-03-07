### Blood Bridge: Optimizing Lifesaving Resources using AWS

## Project Overview
Blood Bridge is a web-based blood bank management system designed to optimize blood donation and distribution processes.
The platform leverages AWS services, including Amazon RDS for secure and scalable data storage and Amazon EC2 for efficient web hosting, ensuring high availability and security.

## Features
- **User Registration & Authentication**: Secure login and registration system for donors, hospitals, and blood banks.
- **Blood Request Management**: Users can request and donate blood based on availability.
- **Real-Time Blood Availability**: Live inventory tracking for blood banks.
- **Donor Scheduling**: Automated notifications for eligibility and donation reminders.
- **Secure & Scalable**: Built on AWS with secure authentication protocols.
- **Community Engagement**: Connects volunteers with blood donation opportunities.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: MySQL (AWS RDS)
- **Cloud Hosting**: AWS EC2
- **Version Control**: Git & GitHub
- 
## Project Architecture
1. **AWS EC2 Instance**: Hosts the web application.
2. **AWS RDS (MySQL Database)**: Stores user, donor, and request data.
3. **Flask Framework**: Manages backend logic and database integration.
4. **HTML/CSS/JS**: Frontend UI development.

## Installation & Setup
### Prerequisites
- AWS Account
- Python 3 Installed
- Git Installed
- MySQL Installed

### Steps to Run Locally
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/blood-bridge.git
   cd blood-bridge
   ```
2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Database**
   - Update `db_config` in `app.py` with your MySQL credentials.
5. **Run the Application**
   ```bash
   python app.py
   ```
6. **Access the Application**
   Open `http://127.0.0.1:5000/` in your browser.

## AWS Deployment Steps
1. **Launch an AWS EC2 Instance**
2. **SSH into the Instance**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   ```
3. **Install Required Packages**
   ```bash
   sudo yum update -y
   sudo yum install python3 -y
   sudo pip3 install virtualenv
   ```
4. **Clone Repository & Run Application**
   ```bash
   git clone https://github.com/your-repo/blood-bridge.git
   cd blood-bridge
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
5. **Configure Security Groups**
   - Allow inbound traffic on ports 22 (SSH), 80 (HTTP), 443 (HTTPS), and 3306 (MySQL RDS).

## Future Enhancements
- **AI-Powered Donor Matching**: Predictive analytics for better blood supply-demand forecasting.
- **Blockchain-Based Security**: Secure, tamper-proof donor-recipient records.
- **Automated Blood Drive Coordination**: Machine learning-driven recommendations for donor outreach.

## Contributors
- Team Leader - Sahithya Kadiyamsetti
- Team Members - Hema Latha Kollipara
                 Sunil Joshi Kancharla 
                 Kadhar basha Rompicherla

## Contact
For any queries or contributions, feel free to reach out via GitHub Issues.

