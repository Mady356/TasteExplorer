#!/usr/bin/env python3
"""
Test script for Layer 1 track graph.

Usage:
    python scripts/test_layer1_graph.py

If you have an existing dataset, load it and pass records to build_track_graph.
"""
import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.graph import build_track_graph, FEATURE_COLUMNS


def load_mock_records():
    """
    Create mock records for testing.

    In production, replace this with:
        from pipeline.storage import load_dataset
        records, metadata = load_dataset("path/to/dataset.parquet")
    """
    mock_records = [
        {
            "track_id": "track_001",
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
            "track_id": "track_002",
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
            "track_id": "track_003",
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
            "track_id": "track_004",
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
            "track_id": "track_005",
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
    ]

    return mock_records


def test_graph_construction():
    """Test graph construction with mock data."""
    print("=" * 60)
    print("Testing Layer 1: Track Similarity Graph")
    print("=" * 60)
    print()

    # Load records
    print("Loading records...")
    # TODO: If you have a dataset, use:
    # from pipeline.storage import load_dataset
    # records, metadata = load_dataset("data/tracks.parquet")
    records = load_mock_records()
    print(f"✓ Loaded {len(records)} records")
    print()

    # Build graph
    print("Building graph...")
    print(f"  k = 3 neighbors per track")
    print(f"  n_clusters = 2")
    print()

    graph = build_track_graph(records, k=3, n_clusters=2)

    # Print results
    print("=" * 60)
    print("Graph Statistics")
    print("=" * 60)
    print(f"Total nodes:        {len(graph['nodes'])}")
    print(f"Total edges:        {len(graph['edges'])}")
    print(f"Usable records:     {graph['metadata']['usable_records']}/{graph['metadata']['total_input_records']}")
    print(f"Feature dimensions: {len(FEATURE_COLUMNS)}")
    print()

    # Print feature columns
    print("Feature columns:")
    for col in FEATURE_COLUMNS:
        print(f"  - {col}")
    print()

    # Print first 3 nodes
    print("=" * 60)
    print("First 3 Nodes")
    print("=" * 60)
    for i, node in enumerate(graph["nodes"][:3], 1):
        print(f"{i}. {node['track_name']}")
        print(f"   Artists: {', '.join(node['artists'])}")
        print(f"   Track ID: {node['track_id']}")
        print(f"   Cluster: {node.get('cluster_id', 'N/A')}")
        print(f"   Time range: {node.get('time_range', 'N/A')}")
        print(f"   Rank: {node.get('track_rank', 'N/A')}")
        print()

    # Print first 3 edges
    print("=" * 60)
    print("First 3 Edges")
    print("=" * 60)
    for i, edge in enumerate(graph["edges"][:3], 1):
        source_node = next(n for n in graph["nodes"] if n["track_id"] == edge["source_track_id"])
        target_node = next(n for n in graph["nodes"] if n["track_id"] == edge["target_track_id"])

        print(f"{i}. {source_node['track_name']} → {target_node['track_name']}")
        print(f"   Similarity: {edge['similarity']:.4f}")
        print(f"   Distance rank: {edge['distance_rank']}")
        print(f"   Shared cluster: {edge.get('shared_cluster_id', 'No')}")
        print()

    # Print cluster summaries
    if "clusters" in graph:
        print("=" * 60)
        print("Cluster Summaries")
        print("=" * 60)
        for cluster in graph["clusters"]:
            print(f"Cluster {cluster['cluster_id']}")
            print(f"  Track count: {cluster['track_count']}")
            print(f"  Coherence: {cluster['coherence_score']:.4f}")
            print()

            print("  Top artists:")
            for artist in cluster["top_artists"][:3]:
                print(f"    - {artist['artist_name']} ({artist['track_count']} tracks)")
            print()

            print("  Representative tracks:")
            for track in cluster["representative_tracks"]:
                artists_str = ', '.join(track['artists'])
                print(f"    - {track['track_name']} by {artists_str}")
                print(f"      Similarity to centroid: {track['similarity_to_centroid']:.4f}")
            print()

    print("=" * 60)
    print("✓ Layer 1 graph construction successful!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_graph_construction()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Make sure scikit-learn is installed:")
        print("  pip install scikit-learn")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
