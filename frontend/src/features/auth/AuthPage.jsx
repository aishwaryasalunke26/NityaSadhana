
import { useState } from "react";
import { authAPI } from "../../services/api";

export default function AuthPage({ onAuthenticated }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (mode === "register") {
        await authAPI.register(email, password);
      }

      await authAPI.login(email, password);
      const user = await authAPI.me();
      onAuthenticated(user);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <form onSubmit={handleSubmit} style={styles.card}>
        <div style={styles.icon}>🪷</div>
        <h1 style={styles.title}>NityaSadhana</h1>
        <p style={styles.subtitle}>
          Your daily devotional practice companion
        </p>

        <h2 style={styles.heading}>
          {mode === "login" ? "Welcome Back" : "Create Your Account"}
        </h2>

        <label style={styles.label}>Email Address</label>
        <input
          style={styles.input}
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          required
        />

        <label style={styles.label}>Password</label>
        <input
          style={styles.input}
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Minimum 8 characters"
          minLength={8}
          maxLength={128}
          required
        />

        {error && <p style={styles.error}>{error}</p>}

        <button style={styles.button} type="submit" disabled={loading}>
          {loading
            ? "Please wait..."
            : mode === "login"
              ? "Login"
              : "Create Account"}
        </button>

        <p style={styles.switchText}>
          {mode === "login"
            ? "Don't have an account?"
            : "Already have an account?"}
          {" "}
          <button
            type="button"
            style={styles.link}
            onClick={() => {
              setMode(mode === "login" ? "register" : "login");
              setError("");
            }}
          >
            {mode === "login" ? "Register" : "Login"}
          </button>
        </p>
      </form>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f7f3eb",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
  card: {
    width: "100%",
    maxWidth: "420px",
    padding: "35px",
    background: "#ffffff",
    borderRadius: "16px",
    boxShadow: "0 8px 30px rgba(0,0,0,0.08)",
  },
  icon: { fontSize: "38px", textAlign: "center" },
  title: {
    textAlign: "center",
    color: "#76532b",
    marginBottom: "8px",
  },
  subtitle: {
    textAlign: "center",
    color: "#777",
    fontSize: "14px",
    marginBottom: "30px",
  },
  heading: { color: "#333", fontSize: "22px" },
  label: {
    display: "block",
    marginTop: "18px",
    marginBottom: "8px",
    fontSize: "14px",
    fontWeight: "bold",
  },
  input: {
    width: "100%",
    boxSizing: "border-box",
    padding: "12px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    fontSize: "15px",
  },
  button: {
    width: "100%",
    marginTop: "24px",
    padding: "13px",
    background: "#8b6336",
    color: "white",
    border: "none",
    borderRadius: "8px",
    fontSize: "16px",
    cursor: "pointer",
  },
  error: { color: "#c0392b", fontSize: "14px" },
  switchText: {
    textAlign: "center",
    marginTop: "22px",
    fontSize: "14px",
    color: "#666",
  },
  link: {
    border: "none",
    background: "none",
    color: "#8b6336",
    fontWeight: "bold",
    cursor: "pointer",
  },
};
