// vite.config.js
import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import dotenv from 'dotenv';

// Load environment variables from .env.local and other env files
dotenv.config(); // Optional, since loadEnv handles it

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env variables based on the current mode (development, production, etc.)
  const env = loadEnv(mode, process.cwd(), '');

  return {
    define: {
      'process.env': env, // Optional: If you need process.env in your client-side code
    },
    plugins: [react()],
    resolve: {
      alias: {
        '@tailwindConfig': path.resolve(__dirname, 'tailwind.config.js'),
      },
    },
    optimizeDeps: {
      include: ['@tailwindConfig'],
    },
    build: {
      commonjsOptions: {
        transformMixedEsModules: true,
      },
    },
    server: {
      proxy: {
        '/api': {
          target: env.VITE_PUBLIC_API_BASE_URL, // Dynamic target from .env.local
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  };
});
