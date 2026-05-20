import { useEffect, useState } from "react";
import { AnalyzeResult, Orchard, api } from "../api";

export default function UploadPage() {
  const [orchards, setOrchards] = useState<Orchard[]>([]);
  const [orchardId, setOrchardId] = useState<number | "">("");
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.orchards().then(setOrchards).catch(() => {});
  }, []);

  async function analyze() {
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await api.analyze(file, orchardId === "" ? undefined : Number(orchardId));
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Lỗi phân tích");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="card">
        <h2>Phân tích ảnh mít</h2>
        <label>Chọn vườn (tuỳ chọn)</label>
        <select
          value={orchardId}
          onChange={(e) => setOrchardId(e.target.value ? Number(e.target.value) : "")}
        >
          <option value="">— Không chọn —</option>
          {orchards.map((o) => (
            <option key={o.id} value={o.id}>
              {o.name}
            </option>
          ))}
        </select>
        <label>Ảnh (JPG/PNG)</label>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        <button onClick={analyze} disabled={!file || loading}>
          {loading ? "Đang phân tích..." : "Phân tích"}
        </button>
        {error && <p className="error">{error}</p>}
      </div>

      {result && (
        <div className="card">
          <h3>Kết quả</h3>
          {result.image_url && (
            <img src={result.image_url} alt="uploaded" style={{ maxWidth: "100%", borderRadius: 8 }} />
          )}
          <p>
            <strong>Sâu bệnh:</strong> {result.disease.label_vi} ({(result.disease.confidence * 100).toFixed(0)}%)
          </p>
          <p>
            <strong>Độ chín:</strong> {result.ripeness.label_vi} ({(result.ripeness.confidence * 100).toFixed(0)}%)
          </p>
          <p>
            <strong>Chất lượng:</strong> {result.quality_score}/100{" "}
            <span className={`badge grade-${result.quality_grade}`}>Hạng {result.quality_grade}</span>
          </p>
          <h4>Khuyến nghị</h4>
          <ul>
            {result.recommendations.map((r, i) => (
              <li key={i}>
                <strong>[{r.priority}]</strong> {r.title} — {r.detail}
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}
