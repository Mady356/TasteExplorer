'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { RefreshCw, LogOut } from 'lucide-react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { fetcher } from '@/lib/utils'
import type { UserArtist, UserTrack } from '@/types'

export default function DashboardPage() {
  const router = useRouter()
  const [userId, setUserId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [syncing, setSyncing] = useState(false)
  const [topArtists, setTopArtists] = useState<UserArtist[]>([])
  const [topTracks, setTopTracks] = useState<UserTrack[]>([])
  const [stats, setStats] = useState<any>(null)

  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id')
    if (!storedUserId) {
      router.push('/')
      return
    }

    setUserId(storedUserId)
    loadDashboardData(storedUserId)
  }, [router])

  async function loadDashboardData(uid: string) {
    try {
      setLoading(true)

      const [artists, tracks, userStats] = await Promise.all([
        fetcher<UserArtist[]>(`/users/${uid}/artists?time_range=medium_term&limit=12`),
        fetcher<UserTrack[]>(`/users/${uid}/tracks?time_range=medium_term&limit=12`),
        fetcher(`/users/${uid}/stats`),
      ])

      setTopArtists(artists)
      setTopTracks(tracks)
      setStats(userStats)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  async function handleSync() {
    if (!userId) return

    try {
      setSyncing(true)
      await fetcher(`/spotify/sync?user_id=${userId}`, { method: 'POST' })

      // Reload data
      await loadDashboardData(userId)
    } catch (error) {
      console.error('Sync failed:', error)
      alert('Failed to sync Spotify data')
    } finally {
      setSyncing(false)
    }
  }

  function handleLogout() {
    localStorage.removeItem('user_id')
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-sm text-muted-foreground">Loading...</div>
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
              <Link href="/dashboard" className="text-foreground">
                Dashboard
              </Link>
              <Link href="/discovery" className="text-muted-foreground hover:text-foreground transition-colors">
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

          <div className="flex items-center gap-4">
            <button
              onClick={handleSync}
              disabled={syncing}
              className="text-xs text-muted-foreground hover:text-foreground transition-colors disabled:opacity-50"
            >
              {syncing ? 'Syncing...' : 'Sync'}
            </button>

            <button
              onClick={handleLogout}
              className="text-xs text-muted-foreground hover:text-foreground transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-medium mb-2">Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Listening history analysis · Last synced: {stats?.last_synced ? new Date(stats.last_synced).toLocaleDateString() : 'Never'}
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-6 mb-12">
          <div className="border border-border p-6">
            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
              Artists
            </div>
            <div className="text-2xl font-medium">{stats?.total_artists || 0}</div>
          </div>

          <div className="border border-border p-6">
            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
              Tracks
            </div>
            <div className="text-2xl font-medium">{stats?.total_tracks || 0}</div>
          </div>

          <div className="border border-border p-6">
            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
              Clusters
            </div>
            <div className="text-2xl font-medium">{stats?.total_clusters || 0}</div>
          </div>

          <div className="border border-border p-6">
            <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">
              Time Ranges
            </div>
            <div className="text-2xl font-medium">3</div>
          </div>
        </div>

        {/* Top Tracks Table */}
        <div className="mb-12">
          <h2 className="text-sm font-medium mb-6">Top Tracks</h2>
          <div className="border border-border">
            <table className="w-full">
              <thead>
                <tr>
                  <th className="text-left pl-6 w-12">#</th>
                  <th className="text-left">Track</th>
                  <th className="text-left">Artist</th>
                  <th className="text-right pr-6">Duration</th>
                </tr>
              </thead>
              <tbody>
                {topTracks.slice(0, 20).map((ut) => (
                  <tr key={ut.track.id}>
                    <td className="pl-6 text-muted-foreground">{ut.rank}</td>
                    <td className="font-medium">{ut.track.name}</td>
                    <td className="text-muted-foreground">
                      {ut.track.artists.map(a => a.name).join(', ')}
                    </td>
                    <td className="text-right pr-6 text-muted-foreground">
                      {Math.floor(ut.track.duration_ms / 60000)}:
                      {String(Math.floor((ut.track.duration_ms % 60000) / 1000)).padStart(2, '0')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Artists Grid */}
        <div>
          <h2 className="text-sm font-medium mb-6">Top Artists</h2>
          <div className="grid grid-cols-5 gap-4">
            {topArtists.slice(0, 10).map((ua) => (
              <div key={ua.artist.id} className="border border-border p-4 hover:bg-muted/30 transition-colors">
                <div className="aspect-square mb-3 bg-muted relative overflow-hidden">
                  {ua.artist.image_url && (
                    <Image
                      src={ua.artist.image_url}
                      alt={ua.artist.name}
                      fill
                      className="object-cover"
                    />
                  )}
                </div>
                <div className="text-xs text-muted-foreground mb-1">#{ua.rank}</div>
                <div className="text-sm font-medium truncate">{ua.artist.name}</div>
                <div className="text-xs text-muted-foreground truncate">
                  {ua.artist.genres?.[0] || '—'}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
