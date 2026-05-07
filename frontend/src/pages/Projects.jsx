import { useEffect, useState } from "react";
import API from "../api";
import Navbar from "../components/Navbar";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [members, setMembers] = useState([]);
  const [users, setUsers] = useState([]);
  const [newProjectName, setNewProjectName] = useState("");
  const [selectedMember, setSelectedMember] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProjects();
    fetchUsers();
  }, []);

  useEffect(() => {
    if (selectedProject) {
      fetchProjectMembers(selectedProject);
    } else {
      setMembers([]);
    }
  }, [selectedProject]);

  const fetchProjects = async () => {
    try {
      const res = await API.get("/projects/");
      setProjects(res.data || []);
    } catch (err) {
      setError("Failed to fetch projects");
      console.error(err);
    }
  };

  const fetchUsers = async () => {
    try {
      const res = await API.get("/projects/users");
      setUsers(res.data || []);
    } catch (err) {
      console.error("Failed to fetch users:", err);
    }
  };

  const fetchProjectMembers = async (projectId) => {
    try {
      const res = await API.get(`/projects/${projectId}/members`);
      setMembers(res.data || []);
    } catch (err) {
      console.error("Failed to fetch members:", err);
      setMembers([]);
    }
  };

  const createProject = async () => {
    if (!newProjectName.trim()) {
      setError("Please enter a project name");
      return;
    }

    setError("");
    setLoading(true);

    try {
      await API.post("/projects/", { name: newProjectName });
      setNewProjectName("");
      await fetchProjects();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create project");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addMember = async () => {
    if (!selectedProject || !selectedMember) {
      setError("Select a project and a user before adding a member.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      await API.post(`/projects/${selectedProject}/members`, {
        user_id: Number(selectedMember)
      });
      setSelectedMember("");
      await fetchProjectMembers(selectedProject);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add member");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const removeMember = async (userId) => {
    if (!selectedProject) return;

    setError("");
    setLoading(true);

    try {
      await API.delete(`/projects/${selectedProject}/members/${userId}`);
      await fetchProjectMembers(selectedProject);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to remove member");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Navbar />
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h1>Projects</h1>
        </div>

        {error && <div style={{ color: 'red', marginBottom: '15px', padding: '10px', backgroundColor: '#ffe6e6', borderRadius: '6px' }}>{error}</div>}

        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' }}>
          <input
            className="input"
            placeholder="Project Name"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            disabled={loading}
            style={{ flex: 1, minWidth: '240px' }}
            onKeyPress={(e) => e.key === 'Enter' && createProject()}
          />
          <button className="btn" onClick={createProject} disabled={loading} style={{ opacity: loading ? 0.6 : 1 }}>
            {loading ? "Creating..." : "Create"}
          </button>
        </div>

        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '280px' }}>
            <h2>Your Projects</h2>
            {projects.length === 0 ? (
              <p style={{ color: '#999' }}>No projects yet.</p>
            ) : (
              <div style={{ display: 'grid', gap: '12px' }}>
                {projects.map((p) => (
                  <button
                    key={p.id}
                    className="project-item"
                    style={{ textAlign: 'left', width: '100%' }}
                    onClick={() => setSelectedProject(p.id)}
                  >
                    {p.name}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div style={{ flex: 1, minWidth: '320px' }}>
            <h2>Project Members</h2>
            {selectedProject ? (
              <>
                <div style={{ display: 'flex', gap: '10px', marginBottom: '15px', flexWrap: 'wrap' }}>
                  <select
                    value={selectedMember}
                    onChange={(e) => setSelectedMember(e.target.value)}
                    className="input"
                    style={{ flex: 1, minWidth: '180px' }}
                  >
                    <option value="">Select a user</option>
                    {users.map((user) => (
                      <option key={user.id} value={user.id}>{user.name} ({user.email})</option>
                    ))}
                  </select>
                  <button className="btn" onClick={addMember} disabled={loading || !selectedMember}>
                    Add Member
                  </button>
                </div>

                {members.length === 0 ? (
                  <p style={{ color: '#999' }}>No members in this project yet.</p>
                ) : (
                  <div style={{ display: 'grid', gap: '10px' }}>
                    {members.map((member) => (
                      <div key={member.user_id} className="project-item" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                          <strong>{member.name}</strong>
                          <div style={{ fontSize: '13px', color: '#555' }}>{member.email} • {member.role}</div>
                        </div>
                        {member.role !== 'Admin' && (
                          <button className="btn" style={{ padding: '6px 10px' }} onClick={() => removeMember(member.user_id)} disabled={loading}>
                            Remove
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <p style={{ color: '#999' }}>Select a project to manage members.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}