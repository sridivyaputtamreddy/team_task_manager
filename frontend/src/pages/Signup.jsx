import { useState } from "react";
import API from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function Signup() {
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: ""
  });

  const signup = async () => {
    setError("");
    
    if (!form.name || !form.email || !form.password) {
      setError("Please fill in all fields");
      return;
    }

    if (form.name.length < 2 || form.name.length > 50) {
      setError("Name must be between 2 and 50 characters");
      return;
    }

    if (form.password.length < 6 || form.password.length > 128) {
      setError("Password must be between 6 and 128 characters");
      return;
    }

    try {
      await API.post("/signup", form);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Signup failed. Please try again.");
    }
  };
  return (
    <div className="auth-box">
      <h1>Signup</h1>
      
      {error && <div style={{color: 'red', marginBottom: '10px'}}>{error}</div>}

      <input
        className="input"
        placeholder="Name"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
      />

      <input
        className="input"
        placeholder="Email"
        type="email"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />

      <input
        className="input"
        type="password"
        placeholder="Password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />
      <button className="btn" style={{width: '100%'}} onClick={signup}>Signup</button>
      
      <p style={{marginTop: '15px', textAlign: 'center'}}>
        Already have an account? <Link to="/" style={{color: '#2563eb', fontWeight: 'bold'}}>Log in</Link>
      </p>
    </div>
  );
}