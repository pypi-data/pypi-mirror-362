import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url';

// Get current directory in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../routelit_silicon/static',
    emptyOutDir: true,
    manifest: true, // Generate manifest.json for asset tracking
    lib: {
      entry: path.resolve(__dirname, 'src/index.ts'),
      name: 'RoutelitSilicon',
      fileName: (format) => `routelit-silicon.${format}.js`,
      formats: ['es', 'umd']
    },
    rollupOptions: {
      external: ['react', 'react-dom', 'react/jsx-runtime', 'routelit-client'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
          'react/jsx-runtime': 'jsxRuntime',
          'routelit-client': 'RoutelitClient',
        }
      }
    },
    minify: true,
    sourcemap: true,
  }
})
