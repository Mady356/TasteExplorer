'use client'

import Link from 'next/link'
import { ArrowRight, Database, GitBranch, Target } from 'lucide-react'

export default function LandingPage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="text-sm font-medium tracking-tight">
            TasteExplorer
          </div>
          <a
            href={`${apiUrl}/auth/spotify/login`}
            className="px-4 py-1.5 bg-foreground text-background text-sm font-medium hover:bg-foreground/90 transition-colors"
          >
            Connect Spotify
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-5xl mx-auto px-6 pt-24 pb-16">
        <div className="space-y-8">
          <div className="space-y-4">
            <h1 className="text-4xl md:text-5xl font-medium tracking-tight leading-tight">
              Graph-based music discovery engine
            </h1>
            <p className="text-base text-muted-foreground max-w-2xl">
              TasteExplorer maps your Spotify listening history into a similarity graph,
              detects taste clusters, and discovers niche artists at the edges of your sound.
            </p>
          </div>

          <div className="flex items-center gap-4">
            <a
              href={`${apiUrl}/auth/spotify/login`}
              className="inline-flex items-center gap-2 px-5 py-2 bg-foreground text-background text-sm font-medium hover:bg-foreground/90 transition-colors"
            >
              Connect Spotify
              <ArrowRight className="h-3.5 w-3.5" />
            </a>
            <Link
              href="/architecture"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              View system architecture
            </Link>
          </div>
        </div>
      </section>

      {/* Pipeline Diagram */}
      <section className="max-w-5xl mx-auto px-6 pb-16">
        <div className="border border-border bg-card">
          <div className="border-b border-border px-6 py-3">
            <h2 className="text-xs uppercase tracking-wider text-muted-foreground">
              Data Pipeline
            </h2>
          </div>
          <div className="p-6">
            <div className="flex items-center justify-between text-sm">
              <div className="flex flex-col items-center gap-2 flex-1">
                <Database className="h-5 w-5 text-muted-foreground" />
                <div className="text-center">
                  <div className="font-medium">Spotify Data</div>
                  <div className="text-xs text-muted-foreground">OAuth + API</div>
                </div>
              </div>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
              <div className="flex flex-col items-center gap-2 flex-1">
                <Target className="h-5 w-5 text-muted-foreground" />
                <div className="text-center">
                  <div className="font-medium">Audio Features</div>
                  <div className="text-xs text-muted-foreground">7D vectors</div>
                </div>
              </div>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
              <div className="flex flex-col items-center gap-2 flex-1">
                <GitBranch className="h-5 w-5 text-muted-foreground" />
                <div className="text-center">
                  <div className="font-medium">Similarity Graph</div>
                  <div className="text-xs text-muted-foreground">k-NN cosine</div>
                </div>
              </div>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
              <div className="flex flex-col items-center gap-2 flex-1">
                <Database className="h-5 w-5 text-muted-foreground" />
                <div className="text-center">
                  <div className="font-medium">Clusters</div>
                  <div className="text-xs text-muted-foreground">Communities</div>
                </div>
              </div>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
              <div className="flex flex-col items-center gap-2 flex-1">
                <Target className="h-5 w-5 text-muted-foreground" />
                <div className="text-center">
                  <div className="font-medium">Discovery</div>
                  <div className="text-xs text-muted-foreground">Ranked</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Details */}
      <section className="max-w-5xl mx-auto px-6 pb-24">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Feature Extraction */}
          <div className="border border-border bg-card p-6 space-y-4">
            <div className="text-xs uppercase tracking-wider text-muted-foreground">
              Feature Extraction
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Danceability</span>
                <span className="font-mono">0.0 - 1.0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Energy</span>
                <span className="font-mono">0.0 - 1.0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Valence</span>
                <span className="font-mono">0.0 - 1.0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Tempo</span>
                <span className="font-mono">40 - 200 BPM</span>
              </div>
            </div>
            <div className="text-xs text-muted-foreground pt-2 border-t border-border">
              Z-score normalized for cosine similarity
            </div>
          </div>

          {/* Graph Construction */}
          <div className="border border-border bg-card p-6 space-y-4">
            <div className="text-xs uppercase tracking-wider text-muted-foreground">
              Graph Construction
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Algorithm</span>
                <span className="font-mono">k-NN</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Distance</span>
                <span className="font-mono">Cosine</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">k neighbors</span>
                <span className="font-mono">5-10</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Complexity</span>
                <span className="font-mono">O(n² log k)</span>
              </div>
            </div>
            <div className="text-xs text-muted-foreground pt-2 border-t border-border">
              Adjacency list with edge weights
            </div>
          </div>
        </div>
      </section>

      {/* Example Output */}
      <section className="max-w-5xl mx-auto px-6 pb-24">
        <div className="border border-border bg-card">
          <div className="border-b border-border px-6 py-3">
            <h3 className="text-xs uppercase tracking-wider text-muted-foreground">
              Example Output: Top Tracks with Features
            </h3>
          </div>
          <div className="p-6">
            <table className="w-full">
              <thead>
                <tr>
                  <th className="text-left">#</th>
                  <th className="text-left">Track</th>
                  <th className="text-left">Artist</th>
                  <th className="text-right">Energy</th>
                  <th className="text-right">Valence</th>
                  <th className="text-right">Dance</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="text-muted-foreground">1</td>
                  <td>Midnight City</td>
                  <td className="text-muted-foreground">M83</td>
                  <td className="text-right font-mono text-muted-foreground">0.82</td>
                  <td className="text-right font-mono text-muted-foreground">0.54</td>
                  <td className="text-right font-mono text-muted-foreground">0.67</td>
                </tr>
                <tr>
                  <td className="text-muted-foreground">2</td>
                  <td>Do I Wanna Know?</td>
                  <td className="text-muted-foreground">Arctic Monkeys</td>
                  <td className="text-right font-mono text-muted-foreground">0.68</td>
                  <td className="text-right font-mono text-muted-foreground">0.31</td>
                  <td className="text-right font-mono text-muted-foreground">0.59</td>
                </tr>
                <tr>
                  <td className="text-muted-foreground">3</td>
                  <td>Digital Love</td>
                  <td className="text-muted-foreground">Daft Punk</td>
                  <td className="text-right font-mono text-muted-foreground">0.71</td>
                  <td className="text-right font-mono text-muted-foreground">0.89</td>
                  <td className="text-right font-mono text-muted-foreground">0.81</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border">
        <div className="max-w-5xl mx-auto px-6 py-8">
          <div className="text-xs text-muted-foreground">
            TasteExplorer · Technical showcase for graph-based recommender systems
          </div>
        </div>
      </footer>
    </div>
  )
}
