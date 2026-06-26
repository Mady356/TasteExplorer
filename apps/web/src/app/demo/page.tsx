'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { AlertCircle, Loader2 } from 'lucide-react'

interface DemoData {
  mode: string
  user_id: string
  top_tracks: any[]
  top_artists: any[]
  clusters: any[]
  graph: {
    nodes: any[]
    edges: any[]
    cluster_edges: any[]
  }
  recommendations: {
    artists: any[]
    tracks: any[]
  }
}

export default function DemoPage() {
  const [data, setData] = useState<DemoData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001'

  useEffect(() => {
    async function loadDemoData() {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(`${apiUrl}/demo`)

        if (!response.ok) {
          throw new Error(`Failed to load demo data: ${response.statusText}`)
        }

        const demoData = await response.json()
        setData(demoData)
      } catch (err) {
        console.error('Demo load error:', err)
        setError(err instanceof Error ? err.message : 'Failed to load demo data')
      } finally {
        setLoading(false)
      }
    }

    loadDemoData()
  }, [apiUrl])

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          <div className="text-sm text-muted-foreground">Loading demo data...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="max-w-md mx-auto p-8 border border-border bg-card">
          <div className="flex items-start gap-3 mb-4">
            <AlertCircle className="h-5 w-5 text-destructive mt-0.5" />
            <div>
              <h2 className="text-sm font-medium mb-1">Failed to Load Demo</h2>
              <p className="text-xs text-muted-foreground mb-4">{error}</p>
            </div>
          </div>
          <div className="flex gap-3">
            <Link
              href="/"
              className="text-xs px-4 py-2 border border-border hover:bg-muted transition-colors"
            >
              Back to Home
            </Link>
            <Link
              href={`${apiUrl}/auth/spotify/login`}
              className="text-xs px-4 py-2 bg-foreground text-background hover:bg-foreground/90 transition-colors"
            >
              Connect Spotify Instead
            </Link>
          </div>
        </div>
      </div>
    )
  }

  if (!data) {
    return null
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Demo Mode Banner */}
      <div className="bg-yellow-500/10 border-b border-yellow-500/20">
        <div className="max-w-7xl mx-auto px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="text-xs font-medium">🎭 Demo Mode</div>
              <div className="text-xs text-muted-foreground">
                Using mock data for recruiter testing
              </div>
            </div>
            <Link
              href={`${apiUrl}/auth/spotify/login`}
              className="text-xs px-3 py-1 border border-border hover:bg-muted transition-colors"
            >
              Connect Your Spotify
            </Link>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="text-sm font-medium tracking-tight">
              TasteExplorer
            </Link>

            <div className="hidden md:flex items-center gap-6 text-sm">
              <Link href="/demo" className="text-foreground">
                Demo
              </Link>
              <Link href="/architecture" className="text-muted-foreground hover:text-foreground transition-colors">
                Architecture
              </Link>
            </div>
          </div>

          <Link
            href="/"
            className="text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            Exit Demo
          </Link>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-medium mb-2">Demo Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Showcasing graph-based recommendations with realistic mock data
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-6 mb-12">
          <div className="border border-border p-6">
            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
              Top Tracks
            </div>
            <div className="text-2xl font-medium">{data.top_tracks.length}</div>
          </div>

          <div className="border border-border p-6">
            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
              Top Artists
            </div>
            <div className="text-2xl font-medium">{data.top_artists.length}</div>
          </div>

          <div className="border border-border p-6">
            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
              Clusters
            </div>
            <div className="text-2xl font-medium">{data.clusters.length}</div>
          </div>

          <div className="border border-border p-6">
            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
              Recommendations
            </div>
            <div className="text-2xl font-medium">{data.recommendations.artists.length + data.recommendations.tracks.length}</div>
          </div>
        </div>

        {/* Clusters */}
        <div className="mb-12">
          <h2 className="text-sm font-medium mb-6">Taste Clusters</h2>
          <div className="grid grid-cols-2 gap-6">
            {data.clusters.map((cluster) => (
              <div key={cluster.cluster_id} className="border border-border p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="text-sm font-medium mb-1">{cluster.name}</div>
                    <div className="text-xs text-muted-foreground">{cluster.suggested_label}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground mb-1">Coherence</div>
                    <div className="text-sm font-mono">{cluster.coherence_score.toFixed(3)}</div>
                  </div>
                </div>

                <div className="space-y-3 mb-4">
                  <div>
                    <div className="text-xs text-muted-foreground mb-2">Representative Tracks</div>
                    <div className="space-y-1">
                      {cluster.representative_tracks.map((track: any) => (
                        <div key={track.track_id} className="text-xs">
                          {track.track_name} · {track.artists.join(', ')}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <div className="text-xs text-muted-foreground mb-2">Top Artists</div>
                    <div className="text-xs">
                      {cluster.top_artists.map((a: any) => a.artist_name).join(', ')}
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-border">
                  <div className="text-xs text-muted-foreground">
                    {cluster.track_count} tracks in cluster
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Tracks */}
        <div className="mb-12">
          <h2 className="text-sm font-medium mb-6">Top Tracks</h2>
          <div className="border border-border">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left pl-6 py-3 text-xs text-muted-foreground">#</th>
                  <th className="text-left py-3 text-xs text-muted-foreground">Track</th>
                  <th className="text-left py-3 text-xs text-muted-foreground">Artist</th>
                  <th className="text-right py-3 text-xs text-muted-foreground">Energy</th>
                  <th className="text-right py-3 text-xs text-muted-foreground">Valence</th>
                  <th className="text-right pr-6 py-3 text-xs text-muted-foreground">Dance</th>
                </tr>
              </thead>
              <tbody>
                {data.top_tracks.map((track, idx) => (
                  <tr key={track.id} className="border-b border-border last:border-0">
                    <td className="pl-6 py-3 text-xs text-muted-foreground">{idx + 1}</td>
                    <td className="py-3 text-sm">{track.name}</td>
                    <td className="py-3 text-sm text-muted-foreground">
                      {track.artists.join(', ')}
                    </td>
                    <td className="text-right py-3 text-xs font-mono text-muted-foreground">
                      {track.audio_features.energy.toFixed(2)}
                    </td>
                    <td className="text-right py-3 text-xs font-mono text-muted-foreground">
                      {track.audio_features.valence.toFixed(2)}
                    </td>
                    <td className="text-right pr-6 py-3 text-xs font-mono text-muted-foreground">
                      {track.audio_features.danceability.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Artist Recommendations */}
        <div className="mb-12">
          <h2 className="text-sm font-medium mb-6">Recommended Artists</h2>
          <div className="space-y-4">
            {data.recommendations.artists.map((artist) => (
              <div key={artist.id} className="border border-border p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="text-sm font-medium mb-1">
                      #{artist.rank} {artist.name}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {artist.genres.join(', ')}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground mb-1">Score</div>
                    <div className="text-sm font-mono">{artist.score.toFixed(3)}</div>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 mb-3 text-xs">
                  <div>
                    <span className="text-muted-foreground">Similarity:</span>{' '}
                    <span className="font-mono">{artist.similarity_score.toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Novelty:</span>{' '}
                    <span className="font-mono">{artist.novelty_score.toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Cluster:</span>{' '}
                    <span className="font-mono">{artist.matched_cluster_id}</span>
                  </div>
                </div>

                <div className="text-xs text-muted-foreground pt-3 border-t border-border">
                  {artist.explanation}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Track Recommendations */}
        <div className="mb-12">
          <h2 className="text-sm font-medium mb-6">Recommended Tracks</h2>
          <div className="space-y-4">
            {data.recommendations.tracks.map((track) => (
              <div key={track.id} className="border border-border p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="text-sm font-medium mb-1">
                      #{track.rank} {track.name}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {track.artists.join(', ')} · {track.album}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground mb-1">Score</div>
                    <div className="text-sm font-mono">{track.score.toFixed(3)}</div>
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-4 mb-3 text-xs">
                  <div>
                    <span className="text-muted-foreground">Similarity:</span>{' '}
                    <span className="font-mono">{track.similarity_score.toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Novelty:</span>{' '}
                    <span className="font-mono">{track.novelty_score.toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Cluster:</span>{' '}
                    <span className="font-mono">{track.matched_cluster_id}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Popularity:</span>{' '}
                    <span className="font-mono">{track.popularity}</span>
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-4 mb-3 text-xs">
                  <div>
                    <span className="text-muted-foreground">Energy:</span>{' '}
                    <span className="font-mono">{track.audio_features.energy.toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Valence:</span>{' '}
                    <span className="font-mono">{track.audio_features.valence.toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Dance:</span>{' '}
                    <span className="font-mono">{track.audio_features.danceability.toFixed(2)}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Tempo:</span>{' '}
                    <span className="font-mono">{track.audio_features.tempo.toFixed(0)} BPM</span>
                  </div>
                </div>

                <div className="text-xs text-muted-foreground pt-3 border-t border-border">
                  {track.explanation}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Graph Preview */}
        <div className="mb-12">
          <h2 className="text-sm font-medium mb-6">Graph Structure</h2>
          <div className="border border-border p-6">
            <div className="grid grid-cols-3 gap-6 mb-6">
              <div>
                <div className="text-xs text-muted-foreground mb-2">Nodes</div>
                <div className="text-2xl font-medium">{data.graph.nodes.length}</div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground mb-2">Edges</div>
                <div className="text-2xl font-medium">{data.graph.edges.length}</div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground mb-2">Cluster Edges</div>
                <div className="text-2xl font-medium">{data.graph.cluster_edges.length}</div>
              </div>
            </div>

            <div className="text-xs text-muted-foreground">
              Track similarity graph built with k-NN algorithm and cosine distance.
              Ready for visualization with D3.js or React Flow.
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="border border-border p-8 text-center">
          <h3 className="text-sm font-medium mb-2">Ready to try with your music?</h3>
          <p className="text-xs text-muted-foreground mb-4">
            Connect your Spotify account to get personalized recommendations based on your actual listening history
          </p>
          <Link
            href={`${apiUrl}/auth/spotify/login`}
            className="inline-flex items-center gap-2 px-5 py-2 bg-foreground text-background text-sm font-medium hover:bg-foreground/90 transition-colors"
          >
            Connect Spotify
          </Link>
        </div>
      </div>
    </div>
  )
}
