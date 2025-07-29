import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'; // Import necessary function

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
      // Could also be a dictionary or array of multiple entry points
      entry: path.resolve(__dirname, 'src/index.ts'),
      name: 'RoutelitSilicon', // PascalCase name for UMD build
      // the proper extensions will be added
      fileName: (format) => `routelit-silicon.${format}.js`,
      formats: ['es', 'umd'] // Specify desired output formats
    },
    rollupOptions: {
      // make sure to externalize deps that shouldn't be bundled
      // into your library
      external: ['react', 'react-dom', 'react/jsx-runtime', 'routelit-client'],
      output: {
        // Provide global variables to use in the UMD build
        // for externalized deps
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
          'react/jsx-runtime': 'jsxRuntime',
          'routelit-client': 'RoutelitClient',
        }
      }
    },
    // Optional: Minify output for production
    // minify: true,
    // Optional: Generate source maps
    // sourcemap: true,
  }
})
