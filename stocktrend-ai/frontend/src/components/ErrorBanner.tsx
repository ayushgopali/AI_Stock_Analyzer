import React from 'react'

type Props = { message: string }

function ErrorBanner({ message }: Props) {
  return (
    <div className="bg-red-800 text-white p-3 rounded mb-4">
      <strong>Error:</strong> {message}
    </div>
  )
}

export default ErrorBanner
