import { useRef, useState } from "react";
import { AnalyzeResult, api } from "../api";

/** PWA-friendly: camera capture on mobile */
export default function ScanPage() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function onCapture(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setError("");
    setLoading(true);
    api
      .analyze(f)
      .then(setResult)
      .catch((err) => setError(err instanceof Error ? err.message : "Lỗi"))
      .finally(() => setLoading(false));
  }

  return (
    <div className="card">
      <h2>Chụp tại vườn</h2>
      <p>Dùng camera điện thoại (PWA). Cài app: Add to Home Screen trên trình duyệt.</p>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        capture="environment"
        style={{ display: "none" }}
        onChange={onCapture}
      />
      <button type="button" onClick={() => inputRef.current?.click()} disabled={loading}>
        {loading ? "Đang phân tích..." : "Mở camera / chọn ảnh"}
      </button>
      {preview && (
        <img src={preview} alt="preview" style={{ maxWidth: "100%", marginTop: "1rem", borderRadius: 8 }} />
      )}
      {error && <p className="error">{error}</p>}
      {result && (
        <div style={{ marginTop: "1rem" }}>
          <p>
            {result.disease.label_vi} · {result.ripeness.label_vi} · Điểm {result.quality_score}
          </p>
        </div>
      )}
    </div>
  );
}
