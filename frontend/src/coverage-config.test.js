/**
 * Test that coverage configuration is properly set up for frontend.
 */
import { describe, it, expect } from 'vitest'
import fs from 'fs'
import path from 'path'

describe('Frontend Coverage Configuration', () => {
  it('should have vitest.config.js configured', () => {
    const configPath = path.resolve(__dirname, '../vitest.config.js')
    expect(fs.existsSync(configPath)).toBe(true)
  })

  it('should have setupTests.js configured', () => {
    const setupPath = path.resolve(__dirname, 'setupTests.js')
    expect(fs.existsSync(setupPath)).toBe(true)
  })

  it('vitest config should include coverage provider', () => {
    const configPath = path.resolve(__dirname, '../vitest.config.js')
    const config = fs.readFileSync(configPath, 'utf-8')
    expect(config).toContain('coverage')
    expect(config).toContain('provider')
  })

  it('package.json should have test scripts', () => {
    const packagePath = path.resolve(__dirname, '../package.json')
    const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf-8'))
    expect(pkg.scripts).toHaveProperty('test')
    expect(pkg.scripts).toHaveProperty('test:coverage')
  })

  it('test:coverage script should reference vitest', () => {
    const packagePath = path.resolve(__dirname, '../package.json')
    const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf-8'))
    expect(pkg.scripts['test:coverage']).toContain('vitest')
  })
})
