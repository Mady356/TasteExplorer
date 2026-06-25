'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ExternalLink } from 'lucide-react'
import Link from 'next/link'
import { fetcher } from '@/lib/utils'
import type { Recommendation } from '@/types'

export default function DiscoveryPage() {
  const router = useRouter()
  const [userId, setUserId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [artistRecs, setArtistRecs] = useState<Recommendation[]>([])
  const [trackRecs, setTrackRecs] = useState<Recommendation[]>([])

  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id')
    if (!storedUserId) {
      router.push('/')
      return
    }

    setUserId(storedUserId)
    loadRecommendations(storedUserId)
  }, [router])

  async function loadRecommendations(uid: string) {
    try {
      setLoading(true)

      const recs = await fetcher<{ artists: Recommendation[]; tracks: Recommendation[] }>(
        `/users/${uid}/recommendations?num_artists=20&num_tracks=30`
      )

      setArtistRecs(recs.artists)
      setTrackRecs(recs.tracks)
    } catch (error) {
      console.error('Failed to load recommendations:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-sm text-muted-foreground">Loading recommendations...</div>
      </div>
    )
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
              <Link href="/discovery" className="text-foreground">
                Discovery
              </Link>
              <Link href="/graph" className="text-muted-foreground hover:text-foreground transition-colors">
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
          <h1 className="text-2xl font-medium mb-2">Discovery</h1>
          <p className="text-sm text-muted-foreground">
            Ranked recommendations based on your listening history
          </p>
        </div>

        {/* Track Recommendations */}
        <div className="mb-12">
          <h2 className="text-sm font-medium mb-6">Recommended Tracks</h2>
          <div className="border border-border">
            <table className="w-full">
              <thead>
                <tr>
                  <th className="text-left pl-6 w-12">#</th>
                  <th className="text-left w-1/4">Track</th>
                  <th className="text-left">Explanation</th>
                  <th className="text-right w-20">Sim</th>
                  <th className="text-right w-20">Nov</th>
                  <th className="text-right w-20">Score</th>
                  <th className="text-right pr-6 w-16"></th>
                </tr>
              </thead>
              <tbody>
                {trackRecs.slice(0, 20).map((rec) => (
                  <tr key={rec.id}>
                    <td className="pl-6 text-muted-foreground">{rec.rank}</td>
                    <td className="font-medium">{rec.name}</td>
                    <td className="text-xs text-muted-foreground max-w-lg">
                      {rec.explanation}
                    </td>
                    <td className="text-right font-mono text-xs text-muted-foreground">
                      {rec.metadata?.similarity_score?.toFixed(2) || '—'}
                    </td>
                    <td className="text-right font-mono text-xs text-muted-foreground">
                      {rec.metadata?.novelty_score?.toFixed(2) || '—'}
                    </td>
                    <td className="text-right font-mono text-xs">
                      {(rec.score * 100).toFixed(0)}
                    </td>
                    <td className="text-right pr-6">
                      <a
                        href={rec.spotify_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-muted-foreground hover:text-foreground transition-colors"
                      >
                        <ExternalLink className="h-3.5 w-3.5" />
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Artist Recommendations */}
        <div>
          <h2 className="text-sm font-medium mb-6">Recommended Artists</h2>
          <div className="space-y-3">
            {artistRecs.slice(0, 10).map((rec) => (
              <div key={rec.id} className="border border-border p-6 hover:bg-muted/30 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-baseline gap-3 mb-2">
                      <div className="font-medium">{rec.name}</div>
                      <div className="text-xs text-muted-foreground">
                        #{rec.rank}
                      </div>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed mb-3">
                      {rec.explanation}
                    </p>
                    <div className="flex items-center gap-4 text-xs">
                      <div>
                        <span className="text-muted-foreground">Similarity:</span>{' '}
                        <span className="font-mono">{rec.metadata?.similarity_score?.toFixed(2) || '—'}</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Novelty:</span>{' '}
                        <span className="font-mono">{rec.metadata?.novelty_score?.toFixed(2) || '—'}</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Pop:</span>{' '}
                        <span className="font-mono">{rec.metadata?.popularity_percentile || '—'}%</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Cluster:</span>{' '}
                        <span className="font-mono">{rec.metadata?.cluster || '—'}</span>
                      </div>
                    </div>
                  </div>
                  <a
                    href={rec.spotify_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-foreground transition-colors ml-4"
                  >
                    <ExternalLink className="h-3.5 w-3.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
