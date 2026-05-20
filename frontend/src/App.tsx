import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import { getToken } from "./api";
import DashboardPage from "./pages/Dashboard";
import LoginPage from "./pages/Login";
import ScanPage from "./pages/Scan";
import UploadPage from "./pages/Upload";

function PrivateLayout({ children }: { children: React.ReactNode }) {
  if (!getToken()) return <Navigate to="/login" replace />;
  return (
    <div className="layout">
      <header>
        <h1>Mit Smart System</h1>
        <p style={{ margin: 0, opacity: 0.8 }}>Hệ thống thông minh nhận diện trái mít — SDC</p>
        <nav>
          <NavLink to="/upload" className={({ isActive }) => (isActive ? "active" : "")}>
            Phân tích ảnh
          </NavLink>
          <NavLink to="/scan" className={({ isActive }) => (isActive ? "active" : "")}>
            Chụp tại vườn (PWA)
          </NavLink>
          <NavLink to="/dashboard" className={({ isActive }) => (isActive ? "active" : "")}>
            Dashboard
          </NavLink>
        </nav>
      </header>
      {children}
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/upload"
        element={
          <PrivateLayout>
            <UploadPage />
          </PrivateLayout>
        }
      />
      <Route
        path="/scan"
        element={
          <PrivateLayout>
            <ScanPage />
          </PrivateLayout>
        }
      />
      <Route
        path="/dashboard"
        element={
          <PrivateLayout>
            <DashboardPage />
          </PrivateLayout>
        }
      />
      <Route path="*" element={<Navigate to="/upload" replace />} />
    </Routes>
  );
}
