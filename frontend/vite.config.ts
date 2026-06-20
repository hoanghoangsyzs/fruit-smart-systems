import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const apiTarget = env.VITE_API_TARGET || env.VITE_API_BASE_URL || "http://127.0.0.1:8001";

  return {
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "Mit Smart — Giám sát vườn mít",
        short_name: "MitSmart",
        description: "Nhận diện sâu bệnh và độ chín trái mít",
        theme_color: "#1b5e20",
        background_color: "#f1f8e9",
        display: "standalone",
        start_url: "/",
        icons: [
          { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
        ],
      },
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg}"],
        navigateFallbackDenylist: [/^\/api/, /^\/uploads/],
      },
    }),
  ],
  server: {
    port: 5173,
    proxy: {
      "/api": apiTarget,
      "/uploads": apiTarget,
      "/health": apiTarget,
    },
  },
  };
});
