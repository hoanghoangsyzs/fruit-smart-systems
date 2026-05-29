import { FormEvent, useEffect, useState } from "react";
import { Orchard, api } from "../api";
import { CROP_TYPES, cropLabel } from "../constants/crops";

export default function OrchardsPage() {
  const [orchards, setOrchards] = useState<Orchard[]>([]);
  const [name, setName] = useState("");
  const [cropType, setCropType] = useState("jackfruit");
  const [location, setLocation] = useState("");
  const [areaHa, setAreaHa] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  function load() {
    api.orchards().then(setOrchards).catch((e) => setError(e instanceof Error ? e.message : "Lỗi"));
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      await api.createOrchard({
        name,
        crop_type: cropType,
        location: location || undefined,
        area_ha: areaHa ? Number(areaHa) : undefined,
      });
      setName("");
      setLocation("");
      setAreaHa("");
      setSuccess("Đã thêm vườn mới.");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không thêm được vườn");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-grid">
      <section className="card form-card">
        <h2>Thêm vườn / lô trồng</h2>
        <p className="muted">Gắn loại cây trồng để theo dõi và phân tích chính xác hơn (theo mô hình Phytelix).</p>
        <form onSubmit={submit} className="form-grid">
          <div className="field">
            <label>Tên vườn *</label>
            <input value={name} onChange={(e) => setName(e.target.value)} required placeholder="VD: Vườn mít Bến Tre A" />
          </div>
          <div className="field">
            <label>Loại cây trồng *</label>
            <select value={cropType} onChange={(e) => setCropType(e.target.value)}>
              {CROP_TYPES.map((c) => (
                <option key={c.value} value={c.value}>
                  {c.label}
                </option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>Địa điểm</label>
            <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Xã, huyện, tỉnh" />
          </div>
          <div className="field">
            <label>Diện tích (ha)</label>
            <input
              type="number"
              min="0"
              step="0.1"
              value={areaHa}
              onChange={(e) => setAreaHa(e.target.value)}
              placeholder="VD: 2.5"
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Đang lưu..." : "+ Thêm vườn"}
          </button>
        </form>
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
      </section>

      <section className="card">
        <h2>Danh sách vườn ({orchards.length})</h2>
        {orchards.length === 0 ? (
          <p className="muted">Chưa có vườn. Thêm vườn bên trái để chọn khi phân tích ảnh.</p>
        ) : (
          <div className="orchard-table-wrap">
            <table className="orchard-table">
              <thead>
                <tr>
                  <th>Tên</th>
                  <th>Loại cây</th>
                  <th>Địa điểm</th>
                  <th>Diện tích</th>
                </tr>
              </thead>
              <tbody>
                {orchards.map((o) => (
                  <tr key={o.id}>
                    <td>
                      <strong>{o.name}</strong>
                    </td>
                    <td>
                      <span className="crop-badge">{cropLabel(o.crop_type)}</span>
                    </td>
                    <td>{o.location ?? "—"}</td>
                    <td>{o.area_ha != null ? `${o.area_ha} ha` : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
