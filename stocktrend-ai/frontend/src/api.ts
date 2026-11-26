import axios from 'axios'

export const api = axios.create({
  baseURL: '/api', // Vite proxy will forward to backend
  timeout: 15000,
})

export const fetchAnalysis = (ticker: string) => api.get('/analyze', { params: { ticker } })
export const fetchMarket = () => api.get('/market')
export const fetchWatchlist = () => api.get('/watchlist')
export const addWatchlist = (ticker: string) => api.post('/watchlist', null, { params: { ticker } })
export const deleteWatchlist = (ticker: string) => api.delete('/watchlist', { params: { ticker } })
export const fetchHistory = (ticker: string) => api.get('/history', { params: { ticker } })
export const fetchScan = () => api.get('/scan')
