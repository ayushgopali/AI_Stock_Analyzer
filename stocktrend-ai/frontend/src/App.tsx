import React from 'react'
import { Routes, Route, NavLink } from 'react-router-dom'
import Predict from './pages/Predict'
import ChartPage from './pages/ChartPage'
import ModelsPage from './pages/ModelsPage'
import FeaturesPage from './pages/FeaturesPage'
import NewsPage from './pages/NewsPage'
import WatchlistPage from './pages/WatchlistPage'
import HistoryPage from './pages/HistoryPage'

function App() {
  const navClass = ({ isActive }: { isActive: boolean }) =>
    isActive ? 'text-blue-400' : 'text-gray-300 hover:text-white'
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <nav className="p-4 bg-gray-800 flex space-x-4">
        <NavLink to="/" className={navClass}>Predict</NavLink>
        <NavLink to="/chart" className={navClass}>Chart</NavLink>
        <NavLink to="/models" className={navClass}>Models</NavLink>
        <NavLink to="/features" className={navClass}>Features</NavLink>
        <NavLink to="/news" className={navClass}>News</NavLink>
        <NavLink to="/watchlist" className={navClass}>Watchlist</NavLink>
        <NavLink to="/history" className={navClass}>History</NavLink>
      </nav>
      <main className="p-6">
        <Routes>
          <Route path="/" element={<Predict />} />
          <Route path="/chart" element={<ChartPage />} />
          <Route path="/models" element={<ModelsPage />} />
          <Route path="/features" element={<FeaturesPage />} />
          <Route path="/news" element={<NewsPage />} />
          <Route path="/watchlist" element={<WatchlistPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App;
