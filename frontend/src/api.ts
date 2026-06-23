const TOKEN_KEY = "mit_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(path, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(typeof err.detail === "string" ? err.detail : JSON.stringify(err));
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  login: (email: string, password: string) =>
    request<{ access_token: string }>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  register: (email: string, password: string, full_name: string) =>
    request("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, full_name }),
    }),
  orchards: () => request<Orchard[]>("/api/v1/orchards"),
  createOrchard: (body: { name: string; crop_type?: string; location?: string; area_ha?: number }) =>
    request<Orchard>("/api/v1/orchards", { method: "POST", body: JSON.stringify(body) }),
  analyze: (file: File, orchard_id?: number) => {
    const fd = new FormData();
    fd.append("file", file);
    if (orchard_id) fd.append("orchard_id", String(orchard_id));
    return request<AnalyzeResult>("/api/v1/analyze", { method: "POST", body: fd });
  },
  dashboard: (orchard_id?: number) => {
    const q = orchard_id ? `?orchard_id=${orchard_id}` : "";
    return request<DashboardSummary>(`/api/v1/dashboard/summary${q}`);
  },
  predictions: () => request<PredictionRow[]>("/api/v1/predictions?limit=20"),
  chat: (message: string, history: ChatMessage[]) =>
    request<ChatResponse>("/api/v1/chat", {
      method: "POST",
      body: JSON.stringify({ message, history }),
    }),
};

export interface Orchard {
  id: number;
  name: string;
  crop_type: string;
  location: string | null;
  area_ha: number | null;
}

export interface HotspotRegion {
  x: number;
  y: number;
  width: number;
  height: number;
  severity: string;
  color: string;
  label: string;
  label_vi: string;
  confidence: number;
}

export interface AnalyzeResult {
  prediction_id: number;
  fruit: { label: string; label_vi: string; confidence: number };
  disease: { label: string; label_vi: string; confidence: number };
  ripeness: { label: string; label_vi: string; confidence: number };
  quality_score: number;
  quality_grade: string;
  severity: string;
  hotspots: HotspotRegion[];
  recommendations: { priority: string; title: string; detail: string }[];
  image_url: string;
}

export interface DashboardSummary {
  total_scans: number;
  disease_distribution: { label: string; count: number }[];
  ripeness_distribution: { label: string; count: number }[];
  timeline: { date: string; scans: number; avg_quality: number }[];
}

export interface PredictionRow {
  id: number;
  disease_label: string;
  ripeness_label: string;
  quality_score: number;
  quality_grade: string;
  created_at: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponse {
  reply: string;
  suggestions: string[];
}
