/**
 * Test that Vitest and React Testing Library are properly configured.
 */
import { describe, it, expect } from 'vitest'
import React from 'react'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from './App'

describe('App Setup Tests', () => {
  it('should render without crashing', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    expect(screen.getByText(/Metal List/i)).toBeInTheDocument()
  })

  it('should have navigation links', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    expect(screen.getByRole('link', { name: /^List$/ })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Management/ })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Import/ })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Audit/ })).toBeInTheDocument()
  })
})
