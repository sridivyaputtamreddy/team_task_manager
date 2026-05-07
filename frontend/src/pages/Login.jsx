import { useState } from "react";
import API from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    email: "",
    password: ""
  });

  const login = async () => {
    setError("");
    
    if (!form.email || !form.password) {
      setError("Please fill in all fields");
      return;
    }

    try {
      const res = await API.post("/login", form);
      localStorage.setItem("token", res.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Please try again.");
    }
   };

  return (
    <div className="auth-box">
      <h1>Login</h1>
      
      {error && <div style={{color: 'red', marginBottom: '10px'}}>{error}</div>}

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

      <button className="btn" style={{width: '100%'}} onClick={login}>Login</button>
      
      <p style={{marginTop: '15px', textAlign: 'center'}}>
        Don't have an account? <Link to="/signup" style={{color: '#2563eb', fontWeight: 'bold'}}>Sign up</Link>
      </p>
    </div>
  );
}