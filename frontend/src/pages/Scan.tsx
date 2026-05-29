import { useEffect, useRef, useState } from "react";
import AnalysisPanel from "../components/AnalysisPanel";
import { AnalyzeResult, Orchard, api } from "../api";
import { cropLabel } from "../constants/crops";
import { readFileAsDataUrl } from "../utils/media";

export default function ScanPage() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [orchards, setOrchards] = useState<Orchard[]>([]);
  const [orchardId, setOrchardId] = useState<number | "">("");
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.orchards().then(setOrchards).catch(() => {});
  }, []);

  async function onCapture(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    setResult(null);
    setError("");
    setLoading(true);
    try {
      setPreview(await readFileAsDataUrl(f));
      const res = await api.analyze(f, orchardId === "" ? undefined : Number(orchardId));
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Lỗi");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="card">
        <h2>Chụp tại vườn (PWA)</h2>
        <p className="muted">Dùng camera điện thoại — kết quả có tô vùng bệnh giống Phytelix.</p>
        <div className="field">
          <label>Vườn</label>
          <select
            value={orchardId}
            onChange={(e) => setOrchardId(e.target.value ? Number(e.target.value) : "")}
          >
            <option value="">— Không chọn —</option>
            {orchards.map((o) => (
              <option key={o.id} value={o.id}>
                {o.name} ({cropLabel(o.crop_type)})
              </option>
            ))}
          </select>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          capture="environment"
          style={{ display: "none" }}
          onChange={onCapture}
        />
        <button type="button" className="btn-primary" onClick={() => inputRef.current?.click()} disabled={loading}>
          {loading ? "AI đang phân tích..." : "Mở camera / chọn ảnh"}
        </button>
        {error && <p className="error">{error}</p>}
      </div>
      {result && <AnalysisPanel result={result} fallbackSrc={preview} />}
      {preview && !result && !loading && (
        <div className="card">
          <img src={preview} alt="preview" style={{ maxWidth: "100%", borderRadius: 8 }} />
        </div>
      )}
    </>
  );
}
