import { useEffect, useState } from "react";
import API from "../api";
import Navbar from "../components/Navbar";

export default function Tasks() {
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedProject, setSelectedProject] = useState("");
  const [form, setForm] = useState({
    title: "",
    description: "",
    due_date: "",
    priority: "MEDIUM",
    assigned_to: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProjects();
    fetchUsers();
  }, []);

  useEffect(() => {
    if (selectedProject) {
      fetchTasks(selectedProject);
    } else {
      setTasks([]);
    }
  }, [selectedProject]);

  const fetchProjects = async () => {
    try {
      const res = await API.get("/projects/");
      setProjects(res.data || []);
      if (res.data?.length) {
        setSelectedProject(res.data[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchUsers = async () => {
    try {
      const res = await API.get("/projects/users");
      setUsers(res.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchTasks = async (projectId) => {
    try {
      const res = await API.get(`/tasks/?project_id=${projectId}`);
      setTasks(res.data || []);
    } catch (err) {
      console.error(err);
      setTasks([]);
    }
  };

  const createTask = async () => {
    if (!selectedProject) {
      setError("Select a project first.");
      return;
    }

    if (!form.title.trim()) {
      setError("Title is required.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      await API.post("/tasks/", {
        project_id: selectedProject,
        title: form.title,
        description: form.description,
        due_date: form.due_date || null,
        priority: form.priority,
        assigned_to: form.assigned_to || null,
      });
      setForm({ title: "", description: "", due_date: "", priority: "MEDIUM", assigned_to: "" });
      await fetchTasks(selectedProject);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create task");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (taskId, status) => {
    try {
      await API.put(`/tasks/${taskId}`, { status });
      await fetchTasks(selectedProject);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Unable to update status");
    }
  };

  return (
    <div>
      <Navbar />
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h1>Tasks</h1>
        </div>

        {error && <div style={{ color: 'red', marginBottom: '15px', padding: '10px', backgroundColor: '#ffe6e6', borderRadius: '6px' }}>{error}</div>}

        <div style={{ display: 'grid', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            <label>
              Project
              <select
                className="input"
                value={selectedProject || ""}
                onChange={(e) => setSelectedProject(e.target.value)}
                style={{ minWidth: '220px' }}
              >
                <option value="">Select a project</option>
                {projects.map((project) => (
                  <option key={project.id} value={project.id}>{project.name}</option>
                ))}
              </select>
            </label>
          </div>

          <div className="card" style={{ padding: '20px' }}>
            <h2>Create New Task</h2>
            <div style={{ display: 'grid', gap: '12px' }}>
              <input
                className="input"
                placeholder="Title"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
              <textarea
                className="input"
                placeholder="Description"
                rows={4}
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
              />
              <div style={{ display: 'grid', gap: '12px', gridTemplateColumns: '1fr 1fr' }}>
                <input
                  className="input"
                  type="date"
                  value={form.due_date}
                  onChange={(e) => setForm({ ...form, due_date: e.target.value })}
                />
                <select
                  className="input"
                  value={form.priority}
                  onChange={(e) => setForm({ ...form, priority: e.target.value })}
                >
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                </select>
              </div>
              <select
                className="input"
                value={form.assigned_to}
                onChange={(e) => setForm({ ...form, assigned_to: e.target.value })}
              >
                <option value="">Assign to user</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>{user.name} ({user.email})</option>
                ))}
              </select>
              <button className="btn" onClick={createTask} disabled={loading}>
                {loading ? "Saving..." : "Create Task"}
              </button>
            </div>
          </div>

          <div>
            <h2>Task List</h2>
            {tasks.length === 0 ? (
              <p style={{ color: '#999' }}>No tasks available for this project.</p>
            ) : (
              tasks.map((task) => (
                <div key={task.id} className="card" style={{ padding: '18px', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
                    <div>
                      <h3>{task.title}</h3>
                      <p style={{ margin: '8px 0 4px', color: '#555' }}>{task.description}</p>
                      <div style={{ fontSize: '13px', color: '#666' }}>
                        Assigned to: {task.assigned_user_name || 'Unassigned'} • {task.priority}
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                      <span style={{ fontWeight: 'bold' }}>{task.status}</span>
                      <button className="btn" onClick={() => updateStatus(task.id, 'TODO')}>TODO</button>
                      <button className="btn" onClick={() => updateStatus(task.id, 'IN_PROGRESS')}>In Progress</button>
                      <button className="btn" onClick={() => updateStatus(task.id, 'DONE')}>Done</button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
