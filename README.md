# SupplyChainTracker

A web-based blockchain solution to bring **transparency**, **traceability**, and **accountability** to supply chains involving multiple entities such as manufacturers, distributors, and retailers. This project demonstrates how blockchain technology can be applied to solve real-world supply chain problems including counterfeit prevention, immutable product history, and audit logging.

---

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Demo

[Optional: Insert a link to a live demo or demo video]

---

## Features

- **Immutable Product Ledger:** Each product event (manufacture, shipment, receipt) is recorded as a tamper-proof blockchain block.
- **Multi-Role Support:** Distinct user roles: Manufacturer, Distributor, Retailer with role-based UI and permissions.
- **QR Code Generation:** Generate scannable QR codes linking to product tracking pages.
- **Product Tracking:** View full chronological history of each product with timestamps.
- **Public Product Catalog:** Browse latest statuses of all registered products without login.
- **User Activity Audit Log:** Immutable, chronological user action logs for accountability.
- **Automated Product Recall System:** Manufacturers can issue recalls permanently recorded on-chain, with prominent alerts.
- **Dark/Light Mode:** Modern responsive UI with Tailwind CSS and theme toggle.
- **Glassmorphism Design:** Modern glass-effect cards for clarity and aesthetics.
- **Toast Notifications:** Smooth, dismissible confirmation popups on actions.
- **Responsive & Mobile Friendly:** UI adapts perfectly to different screen sizes.

---

## Technologies Used

- **Python 3 & Flask:** Backend web framework
- **Tailwind CSS:** Utility-first CSS framework for styling
- **JavaScript:** For UI interactivity (theme toggle, animated timeline, toasts)
- **QR Code (qrcode Python library):** Generate scannable codes
- **Other Python Libraries:** datetime, collections, etc.

---

## Project Structure

SupplyChainTracker/
├── app.py # Main flask app with routes and logic
├── blockchain.py # Blockchain and block classes
├── roles.py # Role definitions and credentials
├── utils.py # QR code generation and utility functions
├── templates/ # HTML template files with Jinja2
│ ├── base.html
│ ├── dashboard.html
│ ├── login.html
│ ├── product_form.html
│ ├── recall_form.html
│ ├── track_product.html
│ ├── view_history.html
│ ├── catalog.html
│ └── audit.html
├── static/
│ ├── css/style.css # Tailwind and custom styles including glassmorphism
│ └── js/timeline.js # JS for timeline animations and IntersectionObserver
└── README.md # This file


---

## Installation

### Prerequisites

- Python 3.x installed
- pip package manager

### Setup steps

-Clone the repo:

git clone https://github.com/yourusername/SupplyChainTracker.git
cd SupplyChainTracker

1. Run the Flask application:

python app.py


2. Open your browser and go to:

http://localhost:5000/


3. Log in using one of the predefined roles and credentials:

- Manufacturer: `manu` / `manu123`
- Distributor: `dist` / `dist123`
- Retailer: `retail` / `retail123`

4. Use the dashboard to add/update products, track products by ID, view catalog, audit logs, and issue recalls (Manufacturer role).

---

## How It Works

- Each product event (manufacture, shipment, receipt) creates a new block on an in-memory blockchain.
- Blocks contain product ID, description, role (by whom updated), and timestamp.
- Product history is retrievable by product ID, displayed as a timeline with QR code.
- Audit logs track every user action and are displayed chronologically.
- Recalls are special blocks flagged on the chain, with visual alerts to users and blocked updates.
- The public catalog shows the latest block per product.
- Dark/light theme toggling is persisted using localStorage.
- UI is powered by Tailwind CSS with modern design patterns including glassmorphism.

---

## Future Enhancements

- Persistent blockchain storage with a database
- Peer-to-peer distributed blockchain with consensus
- Cryptographic signatures for blocks and digital verification
- Integration with IoT devices for real-time sensor data tracking
- Automated alerts and notifications (email/SMS/WebSockets)
- Analytics dashboard with supply chain KPIs
- Consumer-facing verification portal accessible via QR codes
- Role expansion and more granular permissions
- CSRF protection and improved security hardening

---

## License

MIT License © Nikhil Kumar

---

## Contributing

Contributions are welcome! Please fork the repo and open a pull request with your enhancements or bug fixes.

---

## Contact

Created by Nikhil Kumar - https://www.linkedin.com/in/nikhil-kumar-328a99250/

Feel free to reach out for questions or collaborations!

---

*Thank you for checking out SupplyChainTracker! This project aims to demonstrate practical blockchain applications to improve supply chain trust and safety.*
