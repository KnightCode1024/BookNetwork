import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// В Docker используем backend:8000, локально - localhost:8000
const apiTarget = process.env.VITE_API_BASE_URL || 'http://localhost:8000';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@domain': path.resolve(__dirname, './src/domain'),
      '@application': path.resolve(__dirname, './src/application'),
      '@infrastructure': path.resolve(__dirname, './src/infrastructure'),
      '@presentation': path.resolve(__dirname, './src/presentation'),
      '@shared': path.resolve(__dirname, './src/shared'),
    },
  },
  server: {
    port: 3000, // ← Frontend порт
    host: true,
    strictPort: true,
    // Явно настраиваем HMR для WebSocket
    hmr: {
      clientPort: 3000, // ← WebSocket тоже на порту 3000
    },
    // Расширяем proxy для всех API endpoints
    proxy: {
      '/auth': {
        target: apiTarget,
        changeOrigin: true,
      },
      '/api': {
        target: apiTarget,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/authors': {
        target: apiTarget,
        changeOrigin: true,
      },
      '/authors/search': {
        target: apiTarget,
        changeOrigin: true,
      },
      '/feed': {
        target: apiTarget,
        changeOrigin: true,
      },
    },
  },
});