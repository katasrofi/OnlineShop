import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  build:{
    outDir: "../static/css",
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: "app.js",
        assetFileNames: "styles.css",
      },
    },
  },
})
