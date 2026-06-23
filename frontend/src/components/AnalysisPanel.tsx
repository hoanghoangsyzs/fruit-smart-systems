import type { AnalyzeResult } from "../api";
import HotspotImage from "./HotspotImage";

const SEVERITY_LABEL: Record<string, string> = {
  none: "Không có vùng bệnh",
  low: "Mức độ nhẹ",
  medium: "Mức độ trung bình",
  high: "Mức độ nặng",
};

const PRIORITY_CLASS: Record<string, string> = {
  low: "rec-low",
  medium: "rec-medium",
  high: "rec-high",
};

function pct(value: number) {
  return `${Math.round(Math.max(0, Math.min(1, value)) * 100)}%`;
}

export default function AnalysisPanel({
  result,
  fallbackSrc,
}: {
  result: AnalyzeResult;
  fallbackSrc?: string | null;
}) {
  return (
    <div className="analysis-grid">
      <section className="card analysis-visual">
        <div className="card-head">
          <h3>Kết quả AI - vùng ảnh hưởng</h3>
          <span className={`severity-pill sev-${result.severity}`}>
            {SEVERITY_LABEL[result.severity] ?? result.severity}
          </span>
        </div>
        <HotspotImage
          imageUrl={result.image_url}
          hotspots={result.hotspots}
          severity={result.severity}
          fallbackSrc={fallbackSrc}
        />
      </section>

      <section className="card analysis-metrics">
        <h3>3 mức đánh giá chính</h3>
        <div className="metric-cards">
          <div className="metric">
            <div className="metric-row">
              <span className="metric-label">Tên trái:</span>
              <strong>{result.fruit.label_vi}</strong>
            </div>
          </div>

          <div className="metric">
            <div className="metric-row">
              <span className="metric-label">Sâu bệnh:</span>
              <strong>{result.disease.label_vi}</strong>
            </div>
            <div className="progress-bar">
              <div className="progress-fill disease" style={{ width: pct(result.disease.confidence) }} />
            </div>
            <small>{pct(result.disease.confidence)} tin cậy</small>
          </div>

          <div className="metric">
            <div className="metric-row">
              <span className="metric-label">Độ chín:</span>
              <strong>{result.ripeness.label_vi}</strong>
            </div>
            <div className="progress-bar">
              <div className="progress-fill ripeness" style={{ width: pct(result.ripeness.confidence) }} />
            </div>
            <small>{pct(result.ripeness.confidence)} tin cậy</small>
          </div>

          <div className="metric">
            <div className="metric-row">
              <span className="metric-label">Chất lượng:</span>
              <strong>
                {result.quality_score}/100{" "}
                <span className={`badge grade-${result.quality_grade}`}>Hạng {result.quality_grade}</span>
              </strong>
            </div>
          </div>
        </div>
      </section>

      <section className="card analysis-recs">
        <h3>Khuyến nghị khắc phục</h3>
        {result.recommendations.length === 0 ? (
          <p className="muted">Chưa có khuyến nghị phù hợp cho kết quả này.</p>
        ) : (
          <ul className="rec-list">
            {result.recommendations.map((r, i) => (
              <li key={i} className={PRIORITY_CLASS[r.priority] ?? ""}>
                <span className="rec-priority">{r.priority.toUpperCase()}</span>
                <div>
                  <strong>{r.title}</strong>
                  <p>{r.detail}</p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
