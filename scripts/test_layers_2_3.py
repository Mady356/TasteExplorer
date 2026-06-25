#!/usr/bin/env python3
"""
Test script for Layers 2 and 3.

Tests the full pipeline:
1. Layer 1: Build track graph with clusters
2. Layer 2: Build cluster-level taste map
3. Layer 3: Score candidate tracks and rank artists

Usage:
    python scripts/test_layers_2_3.py
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.graph import build_track_graph, build_cluster_graph
from pipeline.recommender import build_discovery_graph


def load_mock_user_tracks():
    """
    Create mock user track records (Layer 1 input).

    TODO: Replace with:
        from pipeline.storage import load_dataset
        records, metadata = load_dataset("data/user_tracks_enriched.parquet")
    """
    return [
        {
            "track_id": "user_track_001",
            "track_name": "Midnight City",
            "artists": [{"artist_name": "M83"}],
            "rank": 1,
            "time_range": "medium_term",
            "danceability": 0.67,
            "energy": 0.82,
            "valence": 0.54,
            "acousticness": 0.01,
            "instrumentalness": 0.73,
            "liveness": 0.12,
            "speechiness": 0.04,
            "tempo": 105.0,
        },
        {
            "track_id": "user_track_002",
            "track_name": "Do I Wanna Know?",
            "artists": [{"artist_name": "Arctic Monkeys"}],
            "rank": 2,
            "time_range": "medium_term",
            "danceability": 0.59,
            "energy": 0.68,
            "valence": 0.31,
            "acousticness": 0.05,
            "instrumentalness": 0.00,
            "liveness": 0.09,
            "speechiness": 0.03,
            "tempo": 85.0,
        },
        {
            "track_id": "user_track_003",
            "track_name": "Digital Love",
            "artists": [{"artist_name": "Daft Punk"}],
            "rank": 3,
            "time_range": "medium_term",
            "danceability": 0.81,
            "energy": 0.71,
            "valence": 0.89,
            "acousticness": 0.01,
            "instrumentalness": 0.85,
            "liveness": 0.11,
            "speechiness": 0.03,
            "tempo": 123.0,
        },
        {
            "track_id": "user_track_004",
            "track_name": "Breathe",
            "artists": [{"artist_name": "Pink Floyd"}],
            "rank": 4,
            "time_range": "long_term",
            "danceability": 0.42,
            "energy": 0.45,
            "valence": 0.38,
            "acousticness": 0.35,
            "instrumentalness": 0.91,
            "liveness": 0.10,
            "speechiness": 0.03,
            "tempo": 60.0,
        },
        {
            "track_id": "user_track_005",
            "track_name": "September",
            "artists": [{"artist_name": "Earth, Wind & Fire"}],
            "rank": 5,
            "time_range": "short_term",
            "danceability": 0.76,
            "energy": 0.73,
            "valence": 0.95,
            "acousticness": 0.02,
            "instrumentalness": 0.00,
            "liveness": 0.31,
            "speechiness": 0.05,
            "tempo": 126.0,
        },
        {
            "track_id": "user_track_006",
            "track_name": "Time",
            "artists": [{"artist_name": "Pink Floyd"}],
            "rank": 6,
            "time_range": "long_term",
            "danceability": 0.38,
            "energy": 0.40,
            "valence": 0.25,
            "acousticness": 0.28,
            "instrumentalness": 0.88,
            "liveness": 0.08,
            "speechiness": 0.02,
            "tempo": 65.0,
        },
    ]


def load_mock_candidate_tracks():
    """
    Create mock candidate tracks (Layer 3 input).

    TODO: In production, fetch these from:
    - Spotify Related Artists API
    - Spotify Recommendations API
    - Custom candidate sources
    """
    return [
        {
            "track_id": "candidate_001",
            "track_name": "Wait",
            "artists": [{"artist_id": "artist_001", "artist_name": "M83"}],
            "popularity": 45,
            "danceability": 0.65,
            "energy": 0.80,
            "valence": 0.50,
            "acousticness": 0.02,
            "instrumentalness": 0.70,
            "liveness": 0.10,
            "speechiness": 0.03,
            "tempo": 110.0,
        },
        {
            "track_id": "candidate_002",
            "track_name": "Instant Crush",
            "artists": [{"artist_id": "artist_002", "artist_name": "Daft Punk"}],
            "popularity": 68,
            "danceability": 0.75,
            "energy": 0.68,
            "valence": 0.85,
            "acousticness": 0.01,
            "instrumentalness": 0.50,
            "liveness": 0.12,
            "speechiness": 0.04,
            "tempo": 118.0,
        },
        {
            "track_id": "candidate_003",
            "track_name": "505",
            "artists": [{"artist_id": "artist_003", "artist_name": "Arctic Monkeys"}],
            "popularity": 72,
            "danceability": 0.54,
            "energy": 0.65,
            "valence": 0.28,
            "acousticness": 0.08,
            "instrumentalness": 0.01,
            "liveness": 0.11,
            "speechiness": 0.03,
            "tempo": 82.0,
        },
        {
            "track_id": "candidate_004",
            "track_name": "Comfortably Numb",
            "artists": [{"artist_id": "artist_004", "artist_name": "Pink Floyd"}],
            "popularity": 78,
            "danceability": 0.35,
            "energy": 0.42,
            "valence": 0.30,
            "acousticness": 0.25,
            "instrumentalness": 0.85,
            "liveness": 0.09,
            "speechiness": 0.02,
            "tempo": 63.0,
        },
        {
            "track_id": "candidate_005",
            "track_name": "Let's Groove",
            "artists": [{"artist_id": "artist_005", "artist_name": "Earth, Wind & Fire"}],
            "popularity": 75,
            "danceability": 0.78,
            "energy": 0.75,
            "valence": 0.92,
            "acousticness": 0.03,
            "instrumentalness": 0.01,
            "liveness": 0.28,
            "speechiness": 0.06,
            "tempo": 122.0,
        },
        {
            "track_id": "candidate_006",
            "track_name": "Oblivion",
            "artists": [{"artist_id": "artist_001", "artist_name": "M83"}],
            "popularity": 52,
            "danceability": 0.62,
            "energy": 0.78,
            "valence": 0.48,
            "acousticness": 0.02,
            "instrumentalness": 0.68,
            "liveness": 0.11,
            "speechiness": 0.03,
            "tempo": 108.0,
        },
        {
            "track_id": "candidate_007",
            "track_name": "Electric Feel",
            "artists": [{"artist_id": "artist_006", "artist_name": "MGMT"}],
            "popularity": 35,
            "danceability": 0.72,
            "energy": 0.74,
            "valence": 0.80,
            "acousticness": 0.02,
            "instrumentalness": 0.45,
            "liveness": 0.13,
            "speechiness": 0.05,
            "tempo": 115.0,
        },
        {
            "track_id": "candidate_008",
            "track_name": "Fluorescent Adolescent",
            "artists": [{"artist_id": "artist_003", "artist_name": "Arctic Monkeys"}],
            "popularity": 66,
            "danceability": 0.60,
            "energy": 0.70,
            "valence": 0.35,
            "acousticness": 0.06,
            "instrumentalness": 0.00,
            "liveness": 0.10,
            "speechiness": 0.03,
            "tempo": 88.0,
        },
        {
            "track_id": "candidate_009",
            "track_name": "Us and Them",
            "artists": [{"artist_id": "artist_004", "artist_name": "Pink Floyd"}],
            "popularity": 70,
            "danceability": 0.40,
            "energy": 0.38,
            "valence": 0.22,
            "acousticness": 0.30,
            "instrumentalness": 0.90,
            "liveness": 0.07,
            "speechiness": 0.02,
            "tempo": 58.0,
        },
        {
            "track_id": "candidate_010",
            "track_name": "Kids",
            "artists": [{"artist_id": "artist_006", "artist_name": "MGMT"}],
            "popularity": 42,
            "danceability": 0.68,
            "energy": 0.76,
            "valence": 0.75,
            "acousticness": 0.01,
            "instrumentalness": 0.55,
            "liveness": 0.15,
            "speechiness": 0.04,
            "tempo": 120.0,
        },
    ]


def test_full_pipeline():
    """Test Layers 1, 2, and 3 together."""
    print("=" * 70)
    print("Testing TasteExplorer Layers 1, 2, and 3")
    print("=" * 70)
    print()

    # ========== LAYER 1 ==========
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ Layer 1: Track Similarity Graph                                │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()

    user_tracks = load_mock_user_tracks()
    print(f"Loaded {len(user_tracks)} user tracks")

    layer1_graph = build_track_graph(user_tracks, k=3, n_clusters=2)
    print(f"✓ Built Layer 1 graph:")
    print(f"  - {len(layer1_graph['nodes'])} track nodes")
    print(f"  - {len(layer1_graph['edges'])} similarity edges")
    print(f"  - {len(layer1_graph['clusters'])} clusters")
    print()

    # ========== LAYER 2 ==========
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ Layer 2: Cluster-Level Taste Map                               │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()

    layer2_graph = build_cluster_graph(layer1_graph)
    print(f"✓ Built Layer 2 cluster graph:")
    print(f"  - {len(layer2_graph['cluster_nodes'])} cluster nodes")
    print(f"  - {len(layer2_graph['cluster_edges'])} cluster edges")
    print()

    # Print cluster details
    print("Cluster Nodes:")
    for i, cluster in enumerate(layer2_graph['cluster_nodes'], 1):
        print(f"\n{i}. Cluster {cluster['cluster_id']}: {cluster['suggested_label']}")
        print(f"   Track count: {cluster['track_count']}")
        print(f"   Coherence: {cluster['coherence_score']:.3f}")
        print(f"   Top artists: {', '.join(a['artist_name'] for a in cluster['top_artists'][:3])}")
        print(f"   Representatives:")
        for rep in cluster['representative_tracks'][:2]:
            print(f"     - {rep['track_name']} (sim={rep['similarity_to_centroid']:.3f})")

    # Print cluster edges
    if layer2_graph['cluster_edges']:
        print("\nCluster Edges:")
        for i, edge in enumerate(layer2_graph['cluster_edges'], 1):
            print(f"{i}. Cluster {edge['source_cluster_id']} ↔ Cluster {edge['target_cluster_id']}")
            print(f"   Type: {edge['edge_type']}")
            print(f"   Centroid similarity: {edge['centroid_similarity']:.3f}")
            print(f"   Shared artists: {edge['shared_artist_count']}")

    print()

    # ========== LAYER 3 ==========
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ Layer 3: Discovery Graph                                       │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()

    candidate_tracks = load_mock_candidate_tracks()
    print(f"Loaded {len(candidate_tracks)} candidate tracks")

    # Extract known track/artist IDs from user tracks
    known_track_ids = {t["track_id"] for t in user_tracks}
    known_artist_ids = set()
    for t in user_tracks:
        for artist in t.get("artists", []):
            if isinstance(artist, dict):
                aid = artist.get("artist_id")
                if aid:
                    known_artist_ids.add(aid)

    layer3_graph = build_discovery_graph(
        layer2_graph,
        candidate_tracks,
        known_track_ids=known_track_ids,
        known_artist_ids=known_artist_ids,
        top_n_tracks=10,
        top_n_artists=5,
    )

    print(f"✓ Built Layer 3 discovery graph:")
    print(f"  - {layer3_graph['metadata']['scored_tracks']} tracks scored")
    print(f"  - {len(layer3_graph['ranked_artists'])} top artists")
    print(f"  - {len(layer3_graph['ranked_tracks'])} top tracks")
    print()

    # Print top recommended artists
    print("=" * 70)
    print("Top Recommended Artists")
    print("=" * 70)
    for i, artist in enumerate(layer3_graph['ranked_artists'], 1):
        print(f"\n{i}. {artist['artist_name']}")
        print(f"   Score: {artist['artist_score']:.3f}")
        print(f"   Tracks: {artist['track_count']}")
        print(f"   Matched clusters: {artist['matched_clusters']}")
        print(f"   Best tracks:")
        for track in artist['best_tracks'][:2]:
            print(f"     - {track['track_name']} (score={track['final_score']:.3f})")

    # Print top recommended tracks
    print()
    print("=" * 70)
    print("Top Recommended Tracks")
    print("=" * 70)
    for i, track_node in enumerate(layer3_graph['candidate_track_nodes'][:5], 1):
        print(f"\n{i}. {track_node['track_name']} by {track_node['artist_name']}")
        print(f"   Score: {track_node['final_score']:.3f}")
        print(f"   Similarity: {track_node['similarity_score']:.3f}")
        print(f"   Novelty: {track_node['novelty_score']:.3f}")
        print(f"   Matched cluster: {track_node['matched_cluster_id']}")
        print(f"   Explanation: {track_node['explanation']}")

    print()
    print("=" * 70)
    print("✓ All layers tested successfully!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_full_pipeline()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Make sure all dependencies are installed:")
        print("  pip install scikit-learn")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
