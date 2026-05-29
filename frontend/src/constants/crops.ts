export const CROP_TYPES = [
  { value: "jackfruit", label: "Mít" },
  { value: "mango", label: "Xoài" },
  { value: "durian", label: "Sầu riêng" },
  { value: "banana", label: "Chuối" },
  { value: "citrus", label: "Cam / quýt" },
  { value: "dragonfruit", label: "Thanh long" },
  { value: "other", label: "Loại khác" },
] as const;

export function cropLabel(value: string): string {
  return CROP_TYPES.find((c) => c.value === value)?.label ?? value;
}

export const SEVERITY_LEGEND = [
  { key: "low", label: "Nhẹ", color: "#43a047" },
  { key: "medium", label: "Trung bình", color: "#fb8c00" },
  { key: "high", label: "Nặng", color: "#e53935" },
] as const;
