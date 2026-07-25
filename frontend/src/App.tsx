import { useState } from 'react'
import { Routes, Route, NavLink, Navigate } from 'react-router-dom'
import Header from '@/components/Header'
import Setup from '@/pages/Setup'
import PipelinePage from '@/pages/Pipeline'
import HypothesesPage from '@/pages/Hypotheses'
import CausalSimPage from '@/pages/CausalSim'
import ReportPage from '@/pages/Report'
import type { PipelineResponse } from '@/lib/api'

const tabs = [
  { path: '/', label: 'Setup' },
  { path: '/pipeline', label: 'Pipeline' },
  { path: '/hypotheses', label: 'Hypotheses' },
  { path: '/causal-sim', label: 'Causal & Sim' },
  { path: '/report', label: 'Report' },
]

function App() {
  const [runId, setRunId] = useState<string | null>(null)
  const [researchGoal, setResearchGoal] = useState('')

  function handlePipelineComplete(result: PipelineResponse) {
    setRunId(result.run_id)
  }

  return (
    <div className="max-w-5xl mx-auto p-6">
      <Header researchGoal={researchGoal} />
      <nav className="flex gap-1 mb-6 border-b border-border-default overflow-x-auto">
        {tabs.map((t) => (
          <NavLink
            key={t.path}
            to={t.path}
            end={t.path === '/'}
            className={({ isActive }) =>
              `px-3 py-2 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
                isActive
                  ? 'border-accent-primary text-accent-primary'
                  : 'border-transparent text-text-secondary hover:text-text-primary'
              }`
            }
          >
            {t.label}
          </NavLink>
        ))}
      </nav>
      <Routes>
        <Route
          path="/"
          element={
            <Setup
              onPipelineComplete={handlePipelineComplete}
              onResearchGoalChange={setResearchGoal}
            />
          }
        />
        <Route path="/pipeline" element={<PipelinePage runId={runId} />} />
        <Route path="/hypotheses" element={<HypothesesPage runId={runId} />} />
        <Route path="/causal-sim" element={<CausalSimPage runId={runId} />} />
        <Route path="/report" element={<ReportPage runId={runId} />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  )
}

export default App
