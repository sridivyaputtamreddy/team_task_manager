# 📊 Team Task Manager

A full-stack web application for managing team projects and tasks with role-based access control.

## 🎯 Features

- **User Authentication** - Secure login and signup with JWT tokens
- **Project Management** - Create and manage multiple projects
- **Task Assignment** - Assign tasks to team members with priorities
- **Dashboard** - Real-time task statistics and overview
- **Role-Based Access Control** - Admin and Member roles with different permissions
- **Task Status Tracking** - Pending, In Progress, and Completed statuses
- **User Management** - Add team members to projects
- **Priority Levels** - Low, Medium, High priority tasks
- **mobile ui responsive**

## 🛠 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | React + Vite | Latest |
| **Backend** | FastAPI | 0.10+ |
| **Database** | PostgreSQL | 12+ |
| **Deployment** | Railway | - |
| **Auth** | JWT Tokens | - |

## 📁 Project Structure

```
team_task_manager/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth_routes.py      # Authentication endpoints
│   │   │   ├── dashboard_routes.py # Dashboard statistics
│   │   │   ├── project_routes.py   # Project management
│   │   │   └── task_routes.py      # Task operations
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── database.py             # Database configuration
│   │   ├── dependencies.py         # Dependency injection
│   │   ├── main.py                 # FastAPI app entry
│   │   └── requirements.txt        # Python dependencies
│   ├── Dockerfile                  # Docker configuration
│   └── Procfile                    # Railway deployment config
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.jsx          # Navigation component
│   │   ├── pages/
│   │   │   ├── Login.jsx           # Login page
│   │   │   ├── Signup.jsx          # Registration page
│   │   │   ├── Dashboard.jsx       # Dashboard page
│   │   │   ├── Projects.jsx        # Projects page
│   │   │   └── Tasks.jsx           # Tasks page
│   │   ├── api.js                  # API client
│   │   ├── App.jsx                 # Main app component
│   │   └── main.jsx                # React entry point
│   ├── package.json                # Node dependencies
│   └── vite.config.mjs             # Vite configuration
└── README.md                       # This file
```

## 📋 Prerequisites

- **Node.js** 16+ (for frontend)
- **Python** 3.8+ (for backend)
- **PostgreSQL** 12+ (or use Railway database)
- **Git**

## 🚀 Installation & Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend/app
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create `.env` file):
```
DATABASE_URL=postgresql://postgres:GTYQZLaSQYwpDqdGuRJTItbLyFZfWYqU@postgres.railway.internal:5432/railway
SECRET_KEY=my_super_secret_key_123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Backend will be available at `http://localhost:8080`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables (create `.env` file):
```
VITE_API_URL=http://localhost:8080
```

4. Start the development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 📖 API Endpoints Overview

### Authentication
- `POST /login` - User login
- `POST /signup` - User registration

### Dashboard
- `GET /dashboard/` - Get dashboard statistics
- `GET /dashboard/?project_id={id}` - Get project-specific stats
- `GET /dashboard/projects` - Get user's projects

### Projects
- `GET /projects/` - List all projects
- `POST /projects/` - Create new project
- `GET /projects/users` - Get available users

### Tasks
- `GET /tasks/?project_id={id}` - Get tasks for a project
- `POST /tasks/` - Create new task
- `PUT /tasks/{id}` - Update task status
- `PUT /tasks/{id}/assign` - Assign task to user

## 🔐 User Roles & Permissions

| Action | Admin | Member |
|--------|-------|--------|
| Create Task | ✅ | ❌ |
| Assign Task | ✅ | ❌ |
| View Own Tasks | ✅ | ✅ |
| View Project Tasks | ✅ | ❌ |
| Update Task Status | ✅ | ✅* |
| Add Members | ✅ | ❌ |

*Members can only update their own tasks

## 🐳 Docker Deployment

Build and run with Docker:
```bash
docker build -t team-task-manager ./backend
docker run -p 8080:8080 team-task-manager
```

## 🚢 Railway Deployment

1. Push to GitHub
2. Connect repository to Railway
3. Set environment variables in Railway dashboard
4. Deploy automatically

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection error | Verify `DATABASE_URL` in `.env` |
| CORS errors | Check backend is running on correct port |
| 422 Validation errors | Ensure request data matches schema (lowercase status values) |
| Frontend not connecting | Verify `VITE_API_URL` matches backend URL |

## 📝 Status Values

- `pending` - Task not started
- `in_progress` - Task being worked on
- `completed` - Task finished

## 💡 Priority Levels

- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add your feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📧 Support

For issues and questions, please open an issue on GitHub.