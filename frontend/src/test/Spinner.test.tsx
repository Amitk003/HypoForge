import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Spinner, { InlineSpinner } from '@/components/Spinner'

describe('Spinner', () => {
  it('renders with text', () => {
    render(<Spinner text="Loading..." />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders without text', () => {
    const { container } = render(<Spinner />)
    expect(container.querySelector('svg')).toBeInTheDocument()
  })
})

describe('InlineSpinner', () => {
  it('renders an svg', () => {
    const { container } = render(<InlineSpinner />)
    expect(container.querySelector('svg')).toBeInTheDocument()
  })
})
