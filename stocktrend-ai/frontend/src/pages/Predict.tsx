import React, { useState } from 'react'
import { fetchAnalysis } from '../api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'
import RecommendationCard from '../components/RecommendationCard'

function Predict() {
  const [ticker, setTicker] = useState('')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const resp = await fetchAnalysis(ticker)
      setResult(resp.data)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to fetch analysis')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Predict</h2>
      <form onSubmit={handleSubmit} className="flex space-x-2 mb-6">
        <input
          type="text"
          placeholder="Ticker (e.g. RELIANCE)"
          value={ticker}
          onChange={e => setTicker(e.target.value)}
          className="flex-1 px-3 py-2 rounded bg-gray-800 text-white placeholder-gray-400"
          required
        />
        <button
          type="submit"
          className="px-4 py-2 bg-primary text-white rounded hover:bg-blue-500"
          disabled={loading}
        >
          Analyze
        </button>
      </form>
      {loading && <LoadingSpinner />}
      {error && <ErrorBanner message={error} />}
      {result && <RecommendationCard data={result} />}
      <p className="mt-8 text-sm text-gray-400">
        Disclaimer: Educational project, not SEBI‑registered investment advice.
      </p>
    </div>
  )
}

export default Predict
