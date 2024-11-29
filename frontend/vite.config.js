import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/v1': {
        target: process.env.REACT_APP_API_BASE_URL,
        changeOrigin: true,
        logLevel: 'debug',
      },
    },
  },
});
