# Verklegt2_Group10
#  Art Vault

**Art Vault** is a web-based auction platform for buying and selling artwork. Users can participate both as buyers and sellers, with support for individual sellers and galleries.

---

##  Features

###  User System
- User registration and login
- Editable user profile
- View active bids and bidding history
- Logout functionality

###  Artwork & Listings
- Create artwork listings with:
  - Images
  - Descriptions
  - Pricing
- Browse all artwork with filtering options
- Homepage sections:
  -  New Listings
  -  Active Bids
  -  Recently Sold

###  Seller System
- Two seller types:
  - Individual
  - Gallery
- Seller profiles showing:
  - Sold artwork
  - Seller type

###  Bidding System (Core Feature)
- Users can bid on listed artwork
- Once the first bid is placed:
  - A **24-hour auction timer** starts
- Sellers can:
  - Accept a bid early
  - Reject bids
  - Let auction expire
- After acceptance:
  - Highest bidder proceeds to payment

###  Localization
- Language toggle between:
  - English 🇬🇧
  - Icelandic 🇮🇸

###  Additional Pages
- About section describing the platform

---

##  Tech Stack

- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Deployment/Cloud:** Azure

---

##  Installation

1. Clone the repository:
```bash
git clone <https://github.com/PDAYSig/Verklegt2_Group10.git>
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Enviorment variables
```bash
DB_PASSWORD=your_password
DB_ENGINE=your_db_engine
DB_NAME=your_db_name
DB_USER=your_db_user
DB_HOST=your_host
DB_PORT=your_port
```

### Database setup
```bash
python manage.py migrate
```

### Run the project 
```bash
python manage.py runserver
```
and then open
```bash
http://127.0.0.1:8000/
```

### Known issues
setja hér ef það er eitthvað


### Group members
#### Daníel Darri Ragnarsson
#### Patrik Dagur Sigurðsson
#### Nanna Katrín Snorradóttir

