import { useState } from "react";
import type { HotspotRegion } from "../api";
import { SEVERITY_LEGEND } from "../constants/crops";
import { resolveImageUrl } from "../utils/media";

type Props = {
  imageUrl: string;
  hotspots: HotspotRegion[];
  severity: string;
  fallbackSrc?: string | null;
};

export default function HotspotImage({ imageUrl, hotspots, severity, fallbackSrc }: Props) {
  const [src, setSrc] = useState(() => resolveImageUrl(imageUrl));
  const [failed, setFailed] = useState(false);

  function onError() {
    if (fallbackSrc && src !== fallbackSrc) {
      setSrc(fallbackSrc);
      setFailed(false);
      return;
    }
    if (src !== resolveImageUrl(imageUrl)) {
      setSrc(resolveImageUrl(imageUrl));
      return;
    }
    setFailed(true);
  }

  return (
    <div className="hotspot-panel">
      <div className="hotspot-canvas">
        {!failed ? (
          <>
            <img src={src} alt="Ảnh phân tích" className="hotspot-img" onError={onError} />
            <div className="hotspot-overlay" aria-hidden>
              {hotspots.map((h, i) => (
                <div
                  key={i}
                  className="hotspot-region"
                  style={{
                    left: `${h.x * 100}%`,
                    top: `${h.y * 100}%`,
                    width: `${h.width * 100}%`,
                    height: `${h.height * 100}%`,
                    borderColor: h.color,
                    backgroundColor: `${h.color}40`,
                    boxShadow: `0 0 14px ${h.color}80`,
                  }}
                  title={`${h.label_vi} (${Math.round(h.confidence * 100)}%)`}
                >
                  <span className="hotspot-tag" style={{ background: h.color }}>
                    {h.label_vi}
                  </span>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="hotspot-fallback">
            <p className="error">Không tải được ảnh từ máy chủ.</p>
            <p className="muted">Kiểm tra backend đang chạy tại http://127.0.0.1:8000</p>
            {fallbackSrc && <img src={fallbackSrc} alt="Ảnh local" className="hotspot-img" />}
          </div>
        )}
      </div>
      <div className="legend-row">
        {SEVERITY_LEGEND.map((s) => (
          <span key={s.key} className="legend-chip">
            <i style={{ background: s.color }} />
            {s.label}
          </span>
        ))}
      </div>
      {severity === "none" && hotspots.length === 0 && !failed && (
        <p className="muted">AI không phát hiện vùng bệnh đáng lo — cây/trái ở trạng thái ổn định.</p>
      )}
    </div>
  );
}
