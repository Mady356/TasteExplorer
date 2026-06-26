# Demo Mode Implementation

## Overview

Demo Mode allows users to explore TasteExplorer's features without requiring Spotify authentication. Perfect for recruiters, portfolio showcasing, and first-time visitors.

---

## ✅ What Was Implemented

### Backend (Complete)

**1. Demo API Endpoint**
- **Route:** `GET /demo`
- **No authentication required**
- **Returns:** Complete mock data including:
  - User profile
  - Top 5 tracks with audio features
  - Top 5 artists with genres
  - 2 taste clusters (Energetic Electronic, Melancholic Indie)
  - Graph visualization data (nodes & edges)
  - 5 artist recommendations with scores
  - 5 track recommendations with explanations

**2. Spotify Sync Fix**
- ✅ Already implemented properly in `spotify/ingestion.py`
- Uses get-or-create/upsert pattern for Artists, Albums, Tracks
- Deletes existing UserArtist/UserTrack relationships before syncing
- No duplicate inserts across time ranges

---

## 🎯 Demo Data Features

### Realistic Mock Data

**Top Tracks:**
- Midnight City (M83)
- Do I Wanna Know? (Arctic Monkeys)
- Electric Feel (MGMT)
- Breathe (Pink Floyd)
- Digital Love (Daft Punk)

**Taste Clusters:**
1. **Energetic Electronic** (3 tracks, coherence 0.78)
   - M83, Daft Punk, MGMT
   - High energy, danceability, instrumentalness

2. **Melancholic Indie** (2 tracks, coherence 0.82)
   - Pink Floyd, Arctic Monkeys
   - Low valence, introspective, acoustic elements

**Recommendations:**

*Artists:*
1. Tame Impala (score: 0.89, similarity: 0.91, novelty: 0.62)
2. The Strokes (score: 0.84, similarity: 0.88, novelty: 0.45)
3. Unknown Mortal Orchestra (score: 0.81, similarity: 0.85, novelty: 0.78)
4. Gorillaz (score: 0.79, similarity: 0.82, novelty: 0.38)
5. Radiohead (score: 0.77, similarity: 0.79, novelty: 0.52)

*Tracks:*
1. The Less I Know The Better - Tame Impala (score: 0.91)
2. Reptilia - The Strokes (score: 0.87)
3. Multi-Love - Unknown Mortal Orchestra (score: 0.84)
4. Feel Good Inc. - Gorillaz (score: 0.82)
5. No Surprises - Radiohead (score: 0.79)

**Each recommendation includes:**
- Similarity score (0-1)
- Novelty score (0-1)
- Final score (weighted combination)
- Matched cluster ID
- Detailed explanation
- Audio features

---

## 📊 API Response Structure

```json
{
  "mode": "demo",
  "user_id": "demo",
  "user": {
    "id": "demo",
    "username": "Demo User"
  },
  "top_tracks": [...],
  "top_artists": [...],
  "clusters": [
    {
      "cluster_id": 0,
      "name": "Energetic Electronic",
      "suggested_label": "upbeat dance",
      "track_count": 3,
      "coherence_score": 0.78,
      "representative_tracks": [...],
      "top_artists": [...]
    }
  ],
  "graph": {
    "nodes": [...],
    "edges": [...],
    "cluster_edges": [...]
  },
  "recommendations": {
    "artists": [...],
    "tracks": [...]
  }
}
```

---

## 🔧 Testing the Demo API

### 1. Start the Backend

```bash
cd apps/api
uvicorn main:app --reload --port 8001
```

### 2. Test the Endpoint

```bash
curl http://127.0.0.1:8001/demo | jq
```

Or visit in browser:
```
http://127.0.0.1:8001/demo
```

### 3. Verify Response

Should return JSON with:
- ✅ `mode`: "demo"
- ✅ `user_id`: "demo"
- ✅ 5 top tracks
- ✅ 5 top artists
- ✅ 2 clusters
- ✅ Graph data
- ✅ 5 artist + 5 track recommendations

---

## 🎨 Frontend Integration (To Be Implemented)

### Recommended UI Changes

**1. Landing Page**

Add "Try Demo" button next to "Connect Spotify":

```tsx
<div className="flex gap-4">
  <button onClick={() => router.push('/demo')}>
    Try Demo
  </button>
  <button onClick={() => router.push('/auth/spotify/login')}>
    Connect Spotify
  </button>
</div>
```

**2. Demo Dashboard**

Create `/demo` route or reuse existing dashboard with demo data:

```tsx
// pages/demo/page.tsx or app/demo/page.tsx
'use client'

import { useEffect, useState } from 'react'
import Dashboard from '@/components/Dashboard'

export default function DemoPage() {
  const [demoData, setDemoData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://127.0.0.1:8001/demo')
      .then(res => res.json())
      .then(data => {
        setDemoData(data)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <LoadingSpinner />
  }

  return (
    <div>
      <div className="bg-yellow-100 p-2 text-center">
        <span className="font-semibold">Demo Mode</span> - 
        Showcasing features with sample data
      </div>
      <Dashboard data={demoData} isDemo={true} />
    </div>
  )
}
```

**3. Demo Mode Indicator**

Always show when in demo mode:

```tsx
{isDemo && (
  <div className="demo-banner">
    🎭 Demo Mode - Connect Spotify for your personalized recommendations
  </div>
)}
```

**4. Dashboard Components**

Reuse existing components, pass demo data:

```tsx
<TasteClusters clusters={demoData.clusters} />
<GraphVisualization graph={demoData.graph} />
<Recommendations 
  artists={demoData.recommendations.artists}
  tracks={demoData.recommendations.tracks}
/>
```

**5. Loading & Error States**

```tsx
// Loading
<div className="animate-pulse">
  Loading demo data...
</div>

// Error
<div className="text-red-500">
  Failed to load demo. Try again or{' '}
  <a href="/auth/spotify/login">connect your Spotify</a>.
</div>
```

---

## 🎓 Recruiter-Friendly Features

### What Demo Mode Showcases

✅ **Graph-Based Clustering**
- 2 distinct taste clusters with labels
- Coherence scores showing cluster quality
- Representative tracks per cluster

✅ **Recommendation Algorithm**
- Similarity scores (cosine similarity to cluster centroids)
- Novelty scores (inverse popularity)
- Weighted final scores (75% similarity + 25% novelty)
- Matched cluster IDs showing recommendation source

✅ **Explainability**
- Human-readable explanations for each recommendation
- Audio feature breakdowns (danceability, energy, valence, tempo)
- Cluster matching reasoning
- Discovery potential indicators

✅ **Graph Visualization Data**
- Track nodes with cluster assignments
- Similarity edges between tracks
- Cluster-level edges
- Ready for D3.js or React Flow visualization

✅ **Production-Ready Structure**
- Clean API design
- Realistic mock data
- Proper JSON structure
- Error handling ready

---

## 📝 Example Explanations

**Track Recommendation:**
> "Extremely close match to your electronic/indie cluster. Audio features align perfectly: energy (0.79 vs your 0.76 avg), danceability (0.78), and tempo (116 BPM). Similar to 'Midnight City' and 'Digital Love' in your collection."

**Artist Recommendation:**
> "Hidden gem in the psychedelic electronic space. Matches your taste for instrumentals and mid-tempo grooves. Low mainstream popularity (35th percentile) means high discovery potential."

**Cluster Description:**
> "Energetic Electronic: High energy (0.76), danceability (0.73), and instrumentalness (0.68). Representative tracks show preference for electronic production and upbeat tempos around 114 BPM."

---

## 🔄 Switching Between Demo and Real Data

### URL Structure

```
/demo          - Demo mode dashboard
/dashboard     - Real user dashboard (requires auth)
/               - Landing page with both options
```

### State Management

```tsx
// Context or global state
const [userMode, setUserMode] = useState<'demo' | 'real' | null>(null)

// Fetch appropriate data
const data = userMode === 'demo' 
  ? await fetch('/demo').then(r => r.json())
  : await fetch(`/users/${userId}/profile`).then(r => r.json())
```

---

## 🚀 Deployment Considerations

### Environment Variables

No changes needed! Demo mode:
- ✅ No Spotify credentials required
- ✅ No database access needed
- ✅ No authentication required
- ✅ Pure stateless endpoint

### CORS

Demo endpoint is already covered by existing CORS config.

### Caching

Consider caching demo response:

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_demo_data() -> Dict:
    return {...}

@router.get("/")
async def get_demo():
    return get_demo_data()
```

---

## 📊 Analytics Tracking (Optional)

Track demo vs real usage:

```python
@router.get("/")
async def get_demo_data():
    logger.info("Demo mode accessed")
    # Optional: Track in analytics
    return {...}
```

Frontend:

```tsx
// Track demo mode entry
useEffect(() => {
  if (isDemo) {
    analytics.track('demo_mode_entered')
  }
}, [isDemo])
```

---

## ✅ Status

**Backend:**
- ✅ Demo endpoint implemented (`GET /demo`)
- ✅ Realistic mock data with 5 tracks, 5 artists
- ✅ 2 taste clusters with representative tracks
- ✅ 10 recommendations (5 artists, 5 tracks)
- ✅ Detailed explanations with scores
- ✅ Graph visualization data
- ✅ Registered in main.py
- ✅ Spotify sync already handles duplicates correctly

**Frontend (To Do):**
- ⬜ Add "Try Demo" button to landing page
- ⬜ Create demo route/page
- ⬜ Add demo mode indicator
- ⬜ Implement loading/error states
- ⬜ Reuse existing dashboard components

**Documentation:**
- ✅ This file (DEMO_MODE.md)
- ✅ API response examples
- ✅ Frontend integration guide
- ✅ Recruiter-friendly features highlighted

---

## 🎉 Ready to Use!

**Test the demo endpoint:**
```bash
curl http://127.0.0.1:8001/demo
```

**Next steps:**
1. Implement frontend "Try Demo" button
2. Create demo dashboard route
3. Add demo mode indicator UI
4. Test end-to-end flow

The demo showcases TasteExplorer's graph-based recommendation engine with realistic data, perfect for portfolios and recruiter demos! 🚀
