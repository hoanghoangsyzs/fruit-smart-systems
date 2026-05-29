import { useEffect, useState } from "react";
import AnalysisPanel from "../components/AnalysisPanel";
import { AnalyzeResult, Orchard, api } from "../api";
import { cropLabel } from "../constants/crops";
import { readFileAsDataUrl } from "../utils/media";

export default function AnalyzePage() {
  const [orchards, setOrchards] = useState<Orchard[]>([]);
  const [orchardId, setOrchardId] = useState<number | "">("");
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.orchards().then(setOrchards).catch(() => {});
  }, []);

  async function onFileChange(f: File | null) {
    setFile(f);
    setResult(null);
    setError("");
    if (!f) {
      setPreview(null);
      return;
    }
    try {
      setPreview(await readFileAsDataUrl(f));
    } catch {
      setError("Không hiển thị được ảnh. Thử file JPG hoặc PNG.");
      setPreview(null);
    }
  }

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

  const selectedOrchard = orchards.find((o) => o.id === orchardId);

  return (
    <>
      <div className="card upload-card">
        <div className="card-head">
          <h2>Phân tích AI — nhận diện sâu bệnh &amp; độ chín</h2>
          <span className="ai-badge">Powered by AI</span>
        </div>
        <p className="muted">
          Tải ảnh trái/lá — hệ thống tô màu vùng bệnh (xanh / cam / đỏ) và đưa ra khuyến nghị xử lý.
        </p>

        <div className="form-grid two-col">
          <div className="field">
            <label>Vườn (tuỳ chọn)</label>
            <select
              value={orchardId}
              onChange={(e) => setOrchardId(e.target.value ? Number(e.target.value) : "")}
            >
              <option value="">— Không chọn vườn —</option>
              {orchards.map((o) => (
                <option key={o.id} value={o.id}>
                  {o.name} ({cropLabel(o.crop_type)})
                </option>
              ))}
            </select>
            {orchards.length === 0 && (
              <small className="muted">
                Chưa có vườn — vào <a href="/orchards">Quản lý vườn</a> để thêm.
              </small>
            )}
          </div>
          {selectedOrchard && (
            <div className="field orchard-hint">
              <label>Loại cây đang theo dõi</label>
              <p>
                <span className="crop-badge">{cropLabel(selectedOrchard.crop_type)}</span>
                {selectedOrchard.location && ` · ${selectedOrchard.location}`}
              </p>
            </div>
          )}
        </div>

        <div className="upload-zone">
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            id="analyze-file"
            className="file-input"
            onChange={(e) => void onFileChange(e.target.files?.[0] ?? null)}
          />
          {preview ? (
            <div className="upload-preview-wrap">
              <img src={preview} alt="Xem trước" className="upload-preview" />
              <label htmlFor="analyze-file" className="upload-change-btn">
                Chọn ảnh khác
              </label>
            </div>
          ) : (
            <label htmlFor="analyze-file" className="upload-label">
              <span>
                <strong>Nhấn để chọn ảnh</strong>
                <br />
                JPG, PNG, WebP — tối đa 10MB
              </span>
            </label>
          )}
        </div>

        <button type="button" className="btn-primary" onClick={analyze} disabled={!file || loading}>
          {loading ? "AI đang phân tích..." : "Chạy phân tích AI"}
        </button>
        {error && <p className="error">{error}</p>}
      </div>

      {result && <AnalysisPanel result={result} fallbackSrc={preview} />}
    </>
  );
}
