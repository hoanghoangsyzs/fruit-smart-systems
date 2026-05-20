import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { DashboardSummary, Orchard, api } from "../api";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [orchards, setOrchards] = useState<Orchard[]>([]);
  const [orchardId, setOrchardId] = useState<number | "">("");
  const [error, setError] = useState("");

  function load() {
    api
      .dashboard(orchardId === "" ? undefined : Number(orchardId))
      .then(setData)
      .catch((e) => setError(e instanceof Error ? e.message : "Lỗi"));
  }

  useEffect(() => {
    api.orchards().then(setOrchards).catch(() => {});
  }, []);

  useEffect(() => {
    load();
  }, [orchardId]);

  return (
    <>
      <div className="card">
        <h2>Dashboard giám sát vườn</h2>
        <label>Lọc theo vườn</label>
        <select
          value={orchardId}
          onChange={(e) => setOrchardId(e.target.value ? Number(e.target.value) : "")}
        >
          <option value="">Tất cả</option>
          {orchards.map((o) => (
            <option key={o.id} value={o.id}>
              {o.name}
            </option>
          ))}
        </select>
        <button type="button" onClick={load}>
          Làm mới
        </button>
        {error && <p className="error">{error}</p>}
        {data && <p>Tổng lượt quét: <strong>{data.total_scans}</strong></p>}
      </div>

      {data && data.disease_distribution.length > 0 && (
        <div className="card">
          <h3>Phân bố sâu bệnh</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data.disease_distribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="label" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#2e7d32" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {data && data.timeline.length > 0 && (
        <div className="card">
          <h3>Chất lượng theo ngày</h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={data.timeline}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="avg_quality" stroke="#558b2f" name="Điểm TB" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {data && data.total_scans === 0 && (
        <p>Chưa có dữ liệu. Hãy phân tích vài ảnh tại trang Upload hoặc Scan.</p>
      )}
    </>
  );
}
