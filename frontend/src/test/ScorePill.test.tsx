import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import ScorePill from '@/components/ScorePill'

describe('ScorePill', () => {
  it('renders label and formatted score', () => {
    render(<ScorePill label="Novelty" score={0.85} />)
    expect(screen.getByText(/Novelty/)).toBeInTheDocument()
    expect(screen.getByText(/0.85/)).toBeInTheDocument()
  })

  it('renders low score formatted to 2 decimals', () => {
    render(<ScorePill label="Test" score={0.3} />)
    expect(screen.getByText(/Test/)).toBeInTheDocument()
    expect(screen.getByText(/0.30/)).toBeInTheDocument()
  })

  it('renders high score', () => {
    render(<ScorePill label="Impact" score={0.95} />)
    expect(screen.getByText(/Impact/)).toBeInTheDocument()
    expect(screen.getByText(/0.95/)).toBeInTheDocument()
  })
})
