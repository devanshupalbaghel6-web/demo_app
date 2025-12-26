import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './index.css'
import App from './App.jsx'

// Create a client for TanStack Query
const queryClient = new QueryClient()

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* Provide the client to the App */}
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)
