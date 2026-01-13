// Type definitions for Vite environment variables
// This file ensures TypeScript recognizes import.meta.env

interface ImportMetaEnv {
  readonly VITE_API_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
