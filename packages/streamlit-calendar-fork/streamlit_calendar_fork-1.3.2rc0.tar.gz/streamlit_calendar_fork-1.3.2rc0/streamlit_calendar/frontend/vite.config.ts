import { defineConfig, loadEnv, UserConfig } from "vite"
import react from "@vitejs/plugin-react"

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  const port = env.VITE_PORT ? parseInt(env.VITE_PORT) : 3001

  return {
    base: "./",
    plugins: [react()],
    server: {
      port,
    },
    build: {
      outDir: "build",
    },
  } satisfies UserConfig
})
