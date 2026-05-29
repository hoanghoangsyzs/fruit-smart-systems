import { Navigate, Route, Routes } from "react-router-dom";
import AppShell from "./components/AppShell";
import { getToken } from "./api";
import AnalyzePage from "./pages/Analyze";
import DashboardPage from "./pages/Dashboard";
import LoginPage from "./pages/Login";
import OrchardsPage from "./pages/Orchards";
import ScanPage from "./pages/Scan";

function PrivateRoute({ children }: { children: React.ReactNode }) {
  if (!getToken()) return <Navigate to="/login" replace />;
  return <AppShell>{children}</AppShell>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/analyze"
        element={
          <PrivateRoute>
            <AnalyzePage />
          </PrivateRoute>
        }
      />
      <Route
        path="/upload"
        element={<Navigate to="/analyze" replace />}
      />
      <Route
        path="/orchards"
        element={
          <PrivateRoute>
            <OrchardsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/scan"
        element={
          <PrivateRoute>
            <ScanPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <DashboardPage />
          </PrivateRoute>
        }
      />
      <Route path="*" element={<Navigate to="/analyze" replace />} />
    </Routes>
  );
}
