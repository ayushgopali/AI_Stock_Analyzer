import React from 'react'

type Props = {
  data: {
    ticker: string
    recommendation: string
    confidence: number
    stop_loss?: number | null
    target?: number | null
    reasons: string[]
    risk_level: string
  }
}

function RecommendationCard({ data }: Props) {
  const {
    ticker,
    recommendation,
    confidence,
    stop_loss,
    target,
    reasons,
    risk_level,
  } = data

  const bgColor =
    recommendation === 'BUY'
      ? 'bg-green-700'
      : recommendation === 'SELL'
      ? 'bg-red-700'
      : 'bg-yellow-700'

  return (
    <div className={`p-6 rounded ${bgColor} text-white`}>
      <h3 className="text-xl font-bold mb-2">{ticker.toUpperCase()}</h3>
      <div className="flex items-center space-x-3 mb-3">
        <span className="px-2 py-1 bg-white text-black rounded">{recommendation}</span>
        <span className="text-sm">Risk: {risk_level}</span>
      </div>
      <div className="mb-2">
        <strong>Confidence:</strong> {(confidence * 100).toFixed(1)}%
      </div>
      {stop_loss !== undefined && stop_loss !== null && (
        <div className="mb-1"><strong>Stop‑loss:</strong> {stop_loss}</div>
      )}
      {target !== undefined && target !== null && (
        <div className="mb-1"><strong>Target:</strong> {target}</div>
      )}
      {reasons && reasons.length > 0 && (
        <div className="mt-3">
          <strong>Reasons:</strong>
          <ul className="list-disc list-inside">
            {reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default RecommendationCard
