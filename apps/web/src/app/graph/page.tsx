'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { fetcher } from '@/lib/utils'
import type { TasteGraph } from '@/types'

export default function GraphPage() {
  const router = useRouter()
  const [userId, setUserId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [graph, setGraph] = useState<TasteGraph | null>(null)

  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id')
    if (!storedUserId) {
      router.push('/')
      return
    }

    setUserId(storedUserId)
    loadGraph(storedUserId)
  }, [router])

  async function loadGraph(uid: string) {
    try {
      setLoading(true)

      const graphData = await fetcher<TasteGraph>(`/users/${uid}/graph`)
      setGraph(graphData)
    } catch (error) {
      console.error('Failed to load graph:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/dashboard" className="text-sm font-medium tracking-tight">
              TasteExplorer
            </Link>

            <div className="hidden md:flex items-center gap-6 text-sm">
              <Link href="/dashboard" className="text-muted-foreground hover:text-foreground transition-colors">
                Dashboard
              </Link>
              <Link href="/discovery" className="text-muted-foreground hover:text-foreground transition-colors">
                Discovery
              </Link>
              <Link href="/graph" className="text-foreground">
                Graph
              </Link>
              <Link href="/architecture" className="text-muted-foreground hover:text-foreground transition-colors">
                Architecture
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="mb-12">
          <h1 className="text-2xl font-medium mb-2">Taste Graph</h1>
          <p className="text-sm text-muted-foreground">
            Visual representation of similarity connections
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-96">
            <div className="text-sm text-muted-foreground">Loading graph...</div>
          </div>
        ) : (
          <div className="grid grid-cols-[1fr_300px] gap-6">
            {/* Graph Canvas */}
            <div className="border border-border aspect-[4/3] flex items-center justify-center bg-muted/10">
              <div className="text-center max-w-md px-6">
                <div className="text-sm text-muted-foreground mb-4">
                  Graph visualization placeholder
                </div>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Integrate React Flow or D3.js here to render nodes (tracks, artists, clusters)
                  and edges (similarity connections) from the graph data.
                </p>
              </div>
            </div>

            {/* Side Panel */}
            <div className="space-y-6">

              {/* Graph Stats */}
              <div className="border border-border p-6">
                <div className="text-xs uppercase tracking-wider text-muted-foreground mb-4">
                  Graph Statistics
                </div>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Nodes</span>
                    <span className="font-medium">{graph?.nodes.length || 0}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Edges</span>
                    <span className="font-medium">{graph?.edges.length || 0}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Clusters</span>
                    <span className="font-medium">{graph?.clusters.length || 0}</span>
                  </div>
                </div>
              </div>

              {/* Clusters */}
              <div className="border border-border p-6">
                <div className="text-xs uppercase tracking-wider text-muted-foreground mb-4">
                  Taste Clusters
                </div>
                <div className="space-y-4">
                  {graph?.clusters.map((cluster, i) => (
                    <div key={cluster.id} className="space-y-2">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-2 h-2 rounded-full"
                          style={{
                            backgroundColor: ['#000000', '#666666', '#999999'][i] || '#cccccc'
                          }}
                        />
                        <span className="text-sm font-medium">{cluster.name}</span>
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {cluster.size} tracks
                      </div>
                      <div className="grid grid-cols-2 gap-1 text-xs">
                        <div>
                          <span className="text-muted-foreground">Energy:</span>{' '}
                          {cluster.centroid[1].toFixed(2)}
                        </div>
                        <div>
                          <span className="text-muted-foreground">Valence:</span>{' '}
                          {cluster.centroid[6].toFixed(2)}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
