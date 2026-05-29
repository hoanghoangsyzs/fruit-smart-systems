import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, setToken } from "../api";

export default function LoginPage() {
  const nav = useNavigate();
  const [email, setEmail] = useState("demo@mit.local");
  const [password, setPassword] = useState("demo1234");
  const [fullName, setFullName] = useState("Demo User");
  const [mode, setMode] = useState<"login" | "register">("login");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "register") {
        await api.register(email, password, fullName);
      }
      const { access_token } = await api.login(email, password);
      setToken(access_token);
      nav("/analyze");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Lỗi đăng nhập");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="layout">
      <div className="card" style={{ maxWidth: 400, margin: "2rem auto" }}>
        <h2>{mode === "login" ? "Đăng nhập" : "Đăng ký"}</h2>
        <form onSubmit={submit}>
          {mode === "register" && (
            <>
              <label>Họ tên</label>
              <input value={fullName} onChange={(e) => setFullName(e.target.value)} />
            </>
          )}
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <label>Mật khẩu</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
          />
          {error && <p className="error">{error}</p>}
          <button type="submit" disabled={loading}>
            {loading ? "Đang xử lý..." : mode === "login" ? "Đăng nhập" : "Đăng ký"}
          </button>
        </form>
        <p style={{ marginTop: "1rem" }}>
          <button
            type="button"
            style={{ background: "#558b2f" }}
            onClick={() => setMode(mode === "login" ? "register" : "login")}
          >
            {mode === "login" ? "Tạo tài khoản mới" : "Đã có tài khoản? Đăng nhập"}
          </button>
        </p>
      </div>
    </div>
  );
}
