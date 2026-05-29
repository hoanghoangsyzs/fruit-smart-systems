import { NavLink, useNavigate } from "react-router-dom";
import { clearToken } from "../api";

const NAV = [
  { to: "/analyze", label: "Phân tích AI"  },
  { to: "/orchards", label: "Quản lý vườn" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/scan", label: "Chụp tại vườn", icon: "" },
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const nav = useNavigate();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">🍈</span>
          <div>
            <strong>Mit Smart</strong>
            <small>Giám sát &amp; AI nhận diện</small>
          </div>
        </div>
        <nav className="sidebar-nav">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}
            >
              <span aria-hidden>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <button type="button" className="btn-ghost" onClick={() => { clearToken(); nav("/login"); }}>
          Đăng xuất
        </button>
      </aside>
      <div className="main-area">
        <header className="topbar">
          <h1>Hệ thống thông minh nhận diện trái cây</h1>
          <p>Phát hiện sâu bệnh · Đánh giá độ chín · Khuyến nghị xử lý</p>
        </header>
        <main className="page-content">{children}</main>
      </div>
    </div>
  );
}
