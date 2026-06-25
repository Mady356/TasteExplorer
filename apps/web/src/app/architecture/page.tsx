'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Database, GitBranch, Cpu, FileCode } from 'lucide-react'
import { fetcher } from '@/lib/utils'

interface PipelineStage {
  name: string
  description: string
  input: string
  output: string
  status: string
}

interface DatabaseTable {
  name: string
  description: string
  row_count_estimate: string
  key_columns: string[]
}

interface EngineModule {
  name: string
  description: string
  status: string
  methods: string[]
}

interface ArchitectureData {
  pipeline: PipelineStage[]
  database: DatabaseTable[]
  engine_modules: EngineModule[]
  tech_stack: Record<string, string[]>
  key_algorithms: Array<{
    name: string
    description: string
    complexity: string
    status: string
  }>
}

export default function ArchitecturePage() {
  const [data, setData] = useState<ArchitectureData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadArchitecture() {
      try {
        const result = await fetcher<ArchitectureData>('/users/architecture')
        setData(result)
      } catch (error) {
        console.error('Failed to load architecture:', error)
      } finally {
        setLoading(false)
      }
    }

    loadArchitecture()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-sm text-muted-foreground">Loading architecture...</div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-sm text-muted-foreground">Failed to load architecture data</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <Link href="/" className="text-sm font-medium tracking-tight hover:text-muted-foreground transition-colors">
            ← TasteExplorer
          </Link>
        </div>
      </nav>

      {/* Header */}
      <div className="max-w-7xl mx-auto px-6 py-12 border-b border-border">
        <div className="space-y-2">
          <h1 className="text-3xl font-medium tracking-tight">System Architecture</h1>
          <p className="text-sm text-muted-foreground max-w-2xl">
            Technical overview of TasteExplorer's data pipeline, graph construction,
            and recommendation engine. Built for SWE/FDSE recruiting showcase.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12 space-y-16">
        {/* Data Pipeline */}
        <section>
          <div className="flex items-center gap-2 mb-6">
            <GitBranch className="h-4 w-4 text-muted-foreground" />
            <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
              Data Pipeline
            </h2>
          </div>

          <div className="space-y-3">
            {data.pipeline.map((stage, i) => (
              <div key={i} className="border border-border p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="font-medium mb-1">{stage.name}</div>
                    <div className="text-sm text-muted-foreground">{stage.description}</div>
                  </div>
                  <div className={`text-xs px-2 py-1 border ${
                    stage.status === 'implemented'
                      ? 'border-green-500/20 text-green-600 dark:text-green-400'
                      : 'border-border text-muted-foreground'
                  }`}>
                    {stage.status}
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 text-xs pt-3 border-t border-border">
                  <div>
                    <span className="text-muted-foreground">Input:</span> {stage.input}
                  </div>
                  <div>
                    <span className="text-muted-foreground">Output:</span> {stage.output}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Database Schema */}
        <section>
          <div className="flex items-center gap-2 mb-6">
            <Database className="h-4 w-4 text-muted-foreground" />
            <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
              Database Schema
            </h2>
          </div>

          <div className="border border-border">
            <table className="w-full">
              <thead>
                <tr>
                  <th className="text-left pl-6">Table</th>
                  <th className="text-left">Description</th>
                  <th className="text-left">Est. Rows</th>
                  <th className="text-left pr-6">Key Columns</th>
                </tr>
              </thead>
              <tbody>
                {data.database.map((table, i) => (
                  <tr key={i}>
                    <td className="pl-6 font-mono text-sm">{table.name}</td>
                    <td className="text-sm text-muted-foreground max-w-xs">
                      {table.description}
                    </td>
                    <td className="text-sm text-muted-foreground">{table.row_count_estimate}</td>
                    <td className="text-sm text-muted-foreground pr-6">
                      {table.key_columns.join(', ')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Engine Modules */}
        <section>
          <div className="flex items-center gap-2 mb-6">
            <Cpu className="h-4 w-4 text-muted-foreground" />
            <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
              Recommendation Engine Modules
            </h2>
          </div>

          <div className="space-y-3">
            {data.engine_modules.map((module, i) => (
              <div key={i} className="border border-border p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="font-medium mb-1">{module.name}</div>
                    <div className="text-sm text-muted-foreground">{module.description}</div>
                  </div>
                  <div className={`text-xs px-2 py-1 border ${
                    module.status === 'implemented'
                      ? 'border-green-500/20 text-green-600 dark:text-green-400'
                      : 'border-yellow-500/20 text-yellow-600 dark:text-yellow-400'
                  }`}>
                    {module.status}
                  </div>
                </div>
                <div className="pt-3 border-t border-border">
                  <div className="text-xs text-muted-foreground mb-2">Methods:</div>
                  <ul className="space-y-1 text-xs">
                    {module.methods.map((method, j) => (
                      <li key={j} className="text-muted-foreground font-mono">
                        · {method}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Key Algorithms */}
        <section>
          <div className="flex items-center gap-2 mb-6">
            <FileCode className="h-4 w-4 text-muted-foreground" />
            <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
              Key Algorithms
            </h2>
          </div>

          <div className="border border-border">
            <table className="w-full">
              <thead>
                <tr>
                  <th className="text-left pl-6">Algorithm</th>
                  <th className="text-left">Description</th>
                  <th className="text-left">Complexity</th>
                  <th className="text-left pr-6">Status</th>
                </tr>
              </thead>
              <tbody>
                {data.key_algorithms.map((algo, i) => (
                  <tr key={i}>
                    <td className="pl-6 font-medium">{algo.name}</td>
                    <td className="text-sm text-muted-foreground max-w-md">
                      {algo.description}
                    </td>
                    <td className="text-sm font-mono text-muted-foreground">{algo.complexity}</td>
                    <td className="text-sm text-muted-foreground pr-6">{algo.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Tech Stack */}
        <section>
          <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground mb-6">
            Technology Stack
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {Object.entries(data.tech_stack).map(([category, technologies]) => (
              <div key={category} className="border border-border p-4">
                <div className="text-xs uppercase tracking-wider text-muted-foreground mb-3">
                  {category}
                </div>
                <ul className="space-y-1 text-sm">
                  {technologies.map((tech, i) => (
                    <li key={i}>{tech}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* Implementation Notes */}
        <section className="border border-border p-6 bg-muted/10">
          <div className="text-sm font-medium mb-2">Implementation Status</div>
          <div className="text-sm text-muted-foreground space-y-2">
            <p>
              <strong>Completed:</strong> Data ingestion, feature extraction, database schema, FastAPI backend, Next.js frontend
            </p>
            <p>
              <strong>To Implement:</strong> Graph construction, clustering algorithm, candidate generation, scoring/ranking, explanation engine
            </p>
            <p>
              All recommendation engine modules are stubbed with clear interfaces and TODO markers.
              The system is designed for manual implementation of custom graph-based algorithms.
            </p>
          </div>
        </section>
      </div>
    </div>
  )
}
