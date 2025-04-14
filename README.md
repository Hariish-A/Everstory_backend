# Everstory – A Social Media Platform (FastAPI + React)

A modern social media web app where users can share encrypted memories, connect with friends, and control privacy, all built using *FastAPI microservices* for the backend and *React + TypeScript* for the frontend.

---

## 🔗 Links

- 🎥 *Demo Video*: [Watch here](https://drive.google.com/drive/folders/1Oj3dRa5sHZ9uytnbCeMMKUm1MPyUjLzI?usp=drive_link)
- 🎨 *Figma Design*: [View Design](https://www.figma.com/design/NDSEALzxd4shreHpoTtKfB/Everstory?node-id=0-1&p=f&t=B5y4GXFslDH2XB9E-0)
- 🧑‍💼 *Frontend Repo*: [everstory-frontend](https://github.com/Hariish-A/Everstory-frontend)
- ⚙️ *Backend Repo*: [everstory-backend](https://github.com/Hariish-A/Everstory_backend)

---
## Tech Stack

### Frontend
- *React + TypeScript*
- *React Router DOM* for routing
- *React Query* for API state management
- *Tailwind CSS* for styling
- *Axios* for HTTP requests
- *Cloudinary Widget* for media uploads

### Backend
- *FastAPI* (Python) with modular microservices
- *PostgreSQL* for persistent data
- *Redis* for inter-service messaging & token storage
- *Docker + Docker Compose*
- *Swagger* docs
- *Cloudinary* for secure media storage

---

## Folder Structure

### Frontend (everstory-frontend)


everstory-frontend/
├── public/
│   └── everstory-bg.png
├── src/
│   ├── assets/
│   ├── components/
│   ├── config/
│   ├── contexts/
│   ├── hooks/
│   ├── pages/
│   │   ├── auth/         # Login, Signup, ResetPassword, UpdatePassword
│   │   ├── home/         # UserForYou page
│   │   ├── friend/       # FriendPage, FriendList
│   │   ├── profile/      # ProfilePage, OtherUserPage
│   ├── services/         # Axios service handlers
│   ├── types/            # Global TypeScript types
│   └── App.tsx
├── tailwind.config.js
└── package.json


### Backend (everstory-backend)


everstory-backend/
├── auth/
│   └── app/
├── posts/
│   └── app/
├── friendship/
│   └── app/
├── gateway/
│   └── app/
├── shared/ (optional core/redis/logger utils)
├── docker-compose.yml
└── README.md


---

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js + npm (Frontend)
- Python 3.11+
- Cloudinary account

#### Sample .env
- Backend (for each service)
env
POSTGRES_DB=auth_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
JWT_SECRET_KEY=supersecret
REDIS_HOST=redis
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret

- Frontend 
env
VITE_API_BASE_URL=http://localhost:5173
VITE_CLOUDINARY_CLOUD_NAME=your_cloud

---

### Step 1: Clone Repositories
bash
git clone https://github.com/Hariish-A/Everstory-frontend.git
git clone https://github.com/Hariish-A/Everstory_backend.git


### Step 2: Backend
bash
cd everstory-backend
docker-compose up --build

##### Python Dependencies
Each service has a requirements.txt. Install dependencies (if running manually):
bash
pip install -r requirements.txt

### Step 3: Frontend
bash
cd ../everstory-frontend
npm install
npm run dev


##### Frontend Dependencies (installed with npm install)
- react
- react-dom
- react-router-dom
- axios
- @tanstack/react-query
- tailwindcss
- postcss
- autoprefixer
- dotenv

### Step 4: Finished Setup 
Now the backend is running on ports 8001(Gateway), 8011, 8021, and 8031, and the frontend on http://localhost:5173.

---

## Features

### Frontend (React + TypeScript)
- Structured using a *feature-based architecture* for scalability
- Implemented *JWT-based authentication* with protected routes
- *API handling* optimized using *React Query*
- *Image uploads* integrated with *Cloudinary*, including secure delivery
- Virtualized post feed using *infinite scroll* 
- Role-based access control for *Public/Private posts*

### Backend (Microservices)
- Built using *FastAPI microservices architecture, fully **Dockerized*
- *Auth Service*: Handles user signup/login, JWT, Redis sessions, and role-based access
- *Posts Service*: Uploads media to Cloudinary, manages public/private posts
- *Friendship Service*: Sends/accepts friend requests, retrieves friends list
- Each service is integrated with its own *PostgreSQL* database
- Central *Gateway* handles routing and JWT token verification

---

## 📮 Contact

Made with 💛 by [Hariish A](https://github.com/Hariish-A)  
📬 Email: hariishero@gmail.com
📬 Email: 22pw15@psgtech.ac.in