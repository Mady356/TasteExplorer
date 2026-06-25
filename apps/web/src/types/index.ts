export interface Artist {
  id: string
  name: string
  genres: string[]
  popularity: number
  followers: number
  image_url: string
  spotify_url: string
}

export interface Track {
  id: string
  name: string
  artists: Artist[]
  album_name: string
  duration_ms: number
  explicit: boolean
  popularity: number
  preview_url: string | null
  spotify_url: string
}

export interface AudioFeatures {
  danceability: number
  energy: number
  speechiness: number
  acousticness: number
  instrumentalness: number
  liveness: number
  valence: number
  tempo: number
  loudness: number
}

export interface UserTrack {
  track: Track
  rank: number
  time_range: string
  audio_features?: AudioFeatures
}

export interface UserArtist {
  artist: Artist
  rank: number
  time_range: string
}

export interface Recommendation {
  id: string
  type: 'artist' | 'track'
  name: string
  image_url: string
  score: number
  rank: number
  explanation: string
  metadata: Record<string, any>
  spotify_url: string
}

export interface GraphNode {
  id: string
  label: string
  type: 'track' | 'artist' | 'cluster'
  color?: string
  size?: number
  metadata?: Record<string, any>
}

export interface GraphEdge {
  source: string
  target: string
  weight: number
  type: string
}

export interface TasteGraph {
  nodes: GraphNode[]
  edges: GraphEdge[]
  clusters: Array<{
    id: string
    name: string
    size: number
    centroid: number[]
  }>
}
