import { useEffect, useState } from "react";
import API from "../api";
import Navbar from "../components/Navbar";

export default function Dashboard() {
  const [data, setData] = useState({});
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchProjects();
    fetchDashboard();
  }, []);

  useEffect(() => {
    if (selectedProject !== null) {
      fetchDashboard();
    }
  }, [selectedProject]);

  const fetchProjects = async () => {
    try {
      const res = await API.get("/dashboard/projects");
      setProjects(res.data || []);
    } catch (err) {
      console.error("Failed to fetch projects:", err);
    }
  };

  const fetchDashboard = async () => {
    setLoading(true);
    setError("");
    try {
      const url = selectedProject 
        ? `/dashboard/?project_id=${selectedProject}` 
        : "/dashboard/";
      const res = await API.get(url);
      setData(res.data);
    } catch (err) {
      setError("Failed to fetch dashboard data");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectChange = (e) => {
    const value = e.target.value === "" ? null : parseInt(e.target.value);
    setSelectedProject(value);
  };

  return (
    <>
      <Navbar />

      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h1>Dashboard</h1>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <select 
              id="project-select"
              value={selectedProject || ""} 
              onChange={handleProjectChange}
              style={{
                padding: '8px 12px',
                borderRadius: '6px',
                border: '1px solid #ddd',
                fontSize: '14px',
                cursor: 'pointer'
              }}
            >
              <option value="">All Tasks</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
            <button 
              onClick={fetchDashboard}
              className="btn"
              style={{ padding: '8px 16px' }}
              disabled={loading}
            >
              {loading ? "Refreshing..." : "Refresh"}
            </button>
          </div>
        </div>

        {error && <div style={{color: 'red', marginBottom: '15px', padding: '10px', backgroundColor: '#ffe6e6', borderRadius: '6px'}}>{error}</div>}

        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>Loading dashboard data...</div>
        ) : (
          <>
            <div className="card-grid">
              <div className="card">
                <h3>Total Tasks</h3>
                <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#2563eb' }}>{data.total || 0}</p>
              </div>

              <div className="card">
                <h3>📝 Todo</h3>
                <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#f59e0b' }}>{data.todo || 0}</p>
              </div>

              <div className="card">
                <h3>⚙️ In Progress</h3>
                <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#8b5cf6' }}>{data.in_progress || 0}</p>
              </div>

              <div className="card">
                <h3>✅ Done</h3>
                <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#10b981' }}>{data.done || 0}</p>
              </div>

              <div className="card">
                <h3>⏰ Overdue</h3>
                <p style={{ fontSize: '32px', fontWeight: 'bold', color: '#ef4444' }}>{data.overdue || 0}</p>
              </div>
            </div>

            {data.tasks_per_user?.length > 0 && (
              <div style={{ marginTop: '25px' }}>
                <h2>Tasks per User</h2>
                <div className="card" style={{ padding: '20px', maxWidth: '420px' }}>
                  <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                    {data.tasks_per_user.map((item) => (
                      <li key={item.user_name} style={{ padding: '10px 0', borderBottom: '1px solid #ececec' }}>
                        <strong>{item.user_name}</strong>: {item.task_count} task{item.task_count !== 1 ? 's' : ''}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </>
  );
}