"""Demo mode routes for TasteExplorer."""
from fastapi import APIRouter
from typing import Dict, List

router = APIRouter()


@router.get("/", response_model=Dict)
async def get_demo_data():
    """
    Get complete demo data for showcasing TasteExplorer.

    Returns mock user profile, taste clusters, graph, and recommendations.
    No Spotify authentication required.
    """
    return {
        "mode": "demo",
        "user_id": "demo",
        "user": {
            "id": "demo",
            "username": "Demo User",
            "created_at": "2024-01-01T00:00:00Z"
        },
        "profile": {
            "display_name": "Demo User",
            "top_genres": ["indie rock", "electronic", "dream pop", "alternative"]
        },
        "top_tracks": [
            {
                "id": "demo_track_1",
                "name": "Midnight City",
                "artists": ["M83"],
                "album": "Hurry Up, We're Dreaming",
                "image_url": "https://i.scdn.co/image/ab67616d0000b273cd0e6d8c034ea2c0e8a701bb5",
                "preview_url": None,
                "popularity": 85,
                "duration_ms": 244453,
                "audio_features": {
                    "danceability": 0.67,
                    "energy": 0.82,
                    "valence": 0.54,
                    "acousticness": 0.01,
                    "instrumentalness": 0.73,
                    "tempo": 105.0
                }
            },
            {
                "id": "demo_track_2",
                "name": "Do I Wanna Know?",
                "artists": ["Arctic Monkeys"],
                "album": "AM",
                "image_url": "https://i.scdn.co/image/ab67616d0000b2734ae1c4c5c45aabe565499163",
                "preview_url": None,
                "popularity": 88,
                "duration_ms": 272394,
                "audio_features": {
                    "danceability": 0.59,
                    "energy": 0.68,
                    "valence": 0.31,
                    "acousticness": 0.05,
                    "instrumentalness": 0.00,
                    "tempo": 85.0
                }
            },
            {
                "id": "demo_track_3",
                "name": "Electric Feel",
                "artists": ["MGMT"],
                "album": "Oracular Spectacular",
                "image_url": "https://i.scdn.co/image/ab67616d0000b2732920071da38e89ef8c6519ea",
                "preview_url": None,
                "popularity": 82,
                "duration_ms": 229000,
                "audio_features": {
                    "danceability": 0.72,
                    "energy": 0.74,
                    "valence": 0.80,
                    "acousticness": 0.02,
                    "instrumentalness": 0.45,
                    "tempo": 115.0
                }
            },
            {
                "id": "demo_track_4",
                "name": "Breathe",
                "artists": ["Pink Floyd"],
                "album": "The Dark Side of the Moon",
                "image_url": "https://i.scdn.co/image/ab67616d0000b273ea7caaff71dea1051d49b2fe",
                "preview_url": None,
                "popularity": 79,
                "duration_ms": 163840,
                "audio_features": {
                    "danceability": 0.42,
                    "energy": 0.45,
                    "valence": 0.38,
                    "acousticness": 0.35,
                    "instrumentalness": 0.91,
                    "tempo": 60.0
                }
            },
            {
                "id": "demo_track_5",
                "name": "Digital Love",
                "artists": ["Daft Punk"],
                "album": "Discovery",
                "image_url": "https://i.scdn.co/image/ab67616d0000b2739b9b36b0e22870b9f542d937",
                "preview_url": None,
                "popularity": 77,
                "duration_ms": 297893,
                "audio_features": {
                    "danceability": 0.81,
                    "energy": 0.71,
                    "valence": 0.89,
                    "acousticness": 0.01,
                    "instrumentalness": 0.85,
                    "tempo": 123.0
                }
            }
        ],
        "top_artists": [
            {
                "id": "demo_artist_1",
                "name": "M83",
                "genres": ["dream pop", "indietronica", "new rave"],
                "image_url": "https://i.scdn.co/image/ab6761610000e5ebc3b2e8e6f3e2c0d1e9a3f1e9",
                "popularity": 72,
                "followers": 1234567
            },
            {
                "id": "demo_artist_2",
                "name": "Arctic Monkeys",
                "genres": ["garage rock", "indie rock", "modern rock"],
                "image_url": "https://i.scdn.co/image/ab6761610000e5eb7da39dea0a72f581535fb11f",
                "popularity": 85,
                "followers": 18765432
            },
            {
                "id": "demo_artist_3",
                "name": "MGMT",
                "genres": ["indie pop", "indietronica", "neo-psychedelic"],
                "image_url": "https://i.scdn.co/image/ab6761610000e5eb1e9a3a5c6a5c4e1b2c3d4e5f",
                "popularity": 75,
                "followers": 3456789
            },
            {
                "id": "demo_artist_4",
                "name": "Pink Floyd",
                "genres": ["art rock", "progressive rock", "psychedelic rock"],
                "image_url": "https://i.scdn.co/image/ab6761610000e5eb5a00969a4698c3132a15fbb0",
                "popularity": 82,
                "followers": 15432109
            },
            {
                "id": "demo_artist_5",
                "name": "Daft Punk",
                "genres": ["electronic", "filter house", "french house"],
                "image_url": "https://i.scdn.co/image/ab6761610000e5eb0672b0e8d72e19ec4995c9bc",
                "popularity": 83,
                "followers": 12345678
            }
        ],
        "clusters": [
            {
                "cluster_id": 0,
                "name": "Energetic Electronic",
                "suggested_label": "upbeat dance",
                "track_count": 3,
                "coherence_score": 0.78,
                "centroid_vector": [0.73, 0.76, 0.74, 0.01, 0.68, 0.11, 0.04, 114.3],
                "representative_tracks": [
                    {
                        "track_id": "demo_track_1",
                        "track_name": "Midnight City",
                        "artists": ["M83"],
                        "similarity_to_centroid": 0.89
                    },
                    {
                        "track_id": "demo_track_5",
                        "track_name": "Digital Love",
                        "artists": ["Daft Punk"],
                        "similarity_to_centroid": 0.85
                    }
                ],
                "top_artists": [
                    {"artist_name": "M83", "track_count": 1},
                    {"artist_name": "Daft Punk", "track_count": 1},
                    {"artist_name": "MGMT", "track_count": 1}
                ]
            },
            {
                "cluster_id": 1,
                "name": "Melancholic Indie",
                "suggested_label": "melancholic / introspective",
                "track_count": 2,
                "coherence_score": 0.82,
                "centroid_vector": [0.51, 0.57, 0.35, 0.20, 0.46, 0.10, 0.02, 72.5],
                "representative_tracks": [
                    {
                        "track_id": "demo_track_4",
                        "track_name": "Breathe",
                        "artists": ["Pink Floyd"],
                        "similarity_to_centroid": 0.94
                    },
                    {
                        "track_id": "demo_track_2",
                        "track_name": "Do I Wanna Know?",
                        "artists": ["Arctic Monkeys"],
                        "similarity_to_centroid": 0.88
                    }
                ],
                "top_artists": [
                    {"artist_name": "Pink Floyd", "track_count": 1},
                    {"artist_name": "Arctic Monkeys", "track_count": 1}
                ]
            }
        ],
        "graph": {
            "nodes": [
                {
                    "id": "demo_track_1",
                    "type": "track",
                    "name": "Midnight City",
                    "cluster_id": 0
                },
                {
                    "id": "demo_track_2",
                    "type": "track",
                    "name": "Do I Wanna Know?",
                    "cluster_id": 1
                },
                {
                    "id": "demo_track_3",
                    "type": "track",
                    "name": "Electric Feel",
                    "cluster_id": 0
                },
                {
                    "id": "demo_track_4",
                    "type": "track",
                    "name": "Breathe",
                    "cluster_id": 1
                },
                {
                    "id": "demo_track_5",
                    "type": "track",
                    "name": "Digital Love",
                    "cluster_id": 0
                }
            ],
            "edges": [
                {
                    "source": "demo_track_1",
                    "target": "demo_track_5",
                    "similarity": 0.87,
                    "shared_cluster": 0
                },
                {
                    "source": "demo_track_1",
                    "target": "demo_track_3",
                    "similarity": 0.79,
                    "shared_cluster": 0
                },
                {
                    "source": "demo_track_2",
                    "target": "demo_track_4",
                    "similarity": 0.72,
                    "shared_cluster": 1
                },
                {
                    "source": "demo_track_3",
                    "target": "demo_track_5",
                    "similarity": 0.81,
                    "shared_cluster": 0
                },
                {
                    "source": "demo_track_4",
                    "target": "demo_track_2",
                    "similarity": 0.72,
                    "shared_cluster": 1
                }
            ],
            "cluster_edges": [
                {
                    "source": 0,
                    "target": 1,
                    "similarity": 0.35,
                    "edge_type": "feature_similar"
                }
            ]
        },
        "recommendations": {
            "artists": [
                {
                    "id": "rec_artist_1",
                    "name": "Tame Impala",
                    "genres": ["indie rock", "neo-psychedelic", "psychedelic rock"],
                    "image_url": "https://i.scdn.co/image/ab6761610000e5eb90357ef28b3a012a1d1b2fa2",
                    "score": 0.89,
                    "rank": 1,
                    "similarity_score": 0.91,
                    "novelty_score": 0.62,
                    "matched_cluster_id": 0,
                    "explanation": "Strong match to your 'Energetic Electronic' cluster. Similar to M83 and MGMT with high energy (0.82) and danceability (0.75). Moderate popularity makes this a great discovery."
                },
                {
                    "id": "rec_artist_2",
                    "name": "The Strokes",
                    "genres": ["alternative rock", "garage rock", "indie rock"],
                    "image_url": "https://i.scdn.co/image/ab6761610000e5eba4e10b5a3b0e8b9c6d5e7f8a",
                    "score": 0.84,
                    "rank": 2,
                    "similarity_score": 0.88,
                    "novelty_score": 0.45,
                    "matched_cluster_id": 1,
                    "explanation": "Bridges your indie rock taste. Similar to Arctic Monkeys in your 'Melancholic Indie' cluster with strong guitar-driven sound. Well-known but fits your profile perfectly."
                },
                {
                    "id": "rec_artist_3",
                    "name": "Unknown Mortal Orchestra",
                    "genres": ["indie rock", "neo-psychedelic", "psychedelic pop"],
                    "image_url": "https://i.scdn.co/image/ab6761610000e5eb1c2d3e4f5a6b7c8d9e0f1a2b",
                    "score": 0.81,
                    "rank": 3,
                    "similarity_score": 0.85,
                    "novelty_score": 0.78,
                    "matched_cluster_id": 0,
                    "explanation": "Hidden gem in the psychedelic electronic space. Matches your taste for instrumentals and mid-tempo grooves. Low mainstream popularity (35th percentile) means high discovery potential."
                },
                {
                    "id": "rec_artist_4",
                    "name": "Gorillaz",
                    "genres": ["alternative hip hop", "electronic", "trip hop"],
                    "image_url": "https://i.scdn.co/image/ab6761610000e5eb2b3c4d5e6f7a8b9c0d1e2f3a",
                    "score": 0.79,
                    "rank": 4,
                    "similarity_score": 0.82,
                    "novelty_score": 0.38,
                    "matched_cluster_id": 0,
                    "explanation": "Spans electronic and alternative genres like your collection. High energy (0.78) with experimental production. Popular artist that still matches your unique taste profile."
                },
                {
                    "id": "rec_artist_5",
                    "name": "Radiohead",
                    "genres": ["alternative rock", "art rock", "melancholia"],
                    "image_url": "https://i.scdn.co/image/ab6761610000e5eba03696716c9ee605006047fd",
                    "score": 0.77,
                    "rank": 5,
                    "similarity_score": 0.79,
                    "novelty_score": 0.52,
                    "matched_cluster_id": 1,
                    "explanation": "Perfect fit for your introspective cluster. Similar atmospheric qualities to Pink Floyd with modern production. Strong valence match (0.35) and mid-tempo preference."
                }
            ],
            "tracks": [
                {
                    "id": "rec_track_1",
                    "name": "The Less I Know The Better",
                    "artists": ["Tame Impala"],
                    "album": "Currents",
                    "image_url": "https://i.scdn.co/image/ab67616d0000b273f4f6d7d7c3e3e9d3e4f5e6f7",
                    "score": 0.91,
                    "rank": 1,
                    "similarity_score": 0.93,
                    "novelty_score": 0.58,
                    "matched_cluster_id": 0,
                    "popularity": 87,
                    "audio_features": {
                        "danceability": 0.78,
                        "energy": 0.79,
                        "valence": 0.72,
                        "tempo": 116.0
                    },
                    "explanation": "Extremely close match to your electronic/indie cluster. Audio features align perfectly: energy (0.79 vs your 0.76 avg), danceability (0.78), and tempo (116 BPM). Similar to 'Midnight City' and 'Digital Love' in your collection."
                },
                {
                    "id": "rec_track_2",
                    "name": "Reptilia",
                    "artists": ["The Strokes"],
                    "album": "Room on Fire",
                    "image_url": "https://i.scdn.co/image/ab67616d0000b2731c2d3e4f5a6b7c8d9e0f1a2b",
                    "score": 0.87,
                    "rank": 2,
                    "similarity_score": 0.89,
                    "novelty_score": 0.42,
                    "matched_cluster_id": 1,
                    "popularity": 76,
                    "audio_features": {
                        "danceability": 0.56,
                        "energy": 0.71,
                        "valence": 0.38,
                        "tempo": 82.0
                    },
                    "explanation": "Strong indie rock match. Complements 'Do I Wanna Know?' with similar energy and mood profile. Garage rock aesthetic fits your melancholic cluster perfectly."
                },
                {
                    "id": "rec_track_3",
                    "name": "Multi-Love",
                    "artists": ["Unknown Mortal Orchestra"],
                    "album": "Multi-Love",
                    "image_url": "https://i.scdn.co/image/ab67616d0000b2733b4c5d6e7f8a9b0c1d2e3f4a",
                    "score": 0.84,
                    "rank": 3,
                    "similarity_score": 0.87,
                    "novelty_score": 0.81,
                    "matched_cluster_id": 0,
                    "popularity": 42,
                    "audio_features": {
                        "danceability": 0.69,
                        "energy": 0.68,
                        "valence": 0.65,
                        "instrumentalness": 0.52,
                        "tempo": 103.0
                    },
                    "explanation": "Hidden gem with psychedelic production. Low popularity (42) means high novelty score (0.81). Bridges your electronic and indie tastes with groovy basslines and atmospheric synths."
                },
                {
                    "id": "rec_track_4",
                    "name": "Feel Good Inc.",
                    "artists": ["Gorillaz"],
                    "album": "Demon Days",
                    "image_url": "https://i.scdn.co/image/ab67616d0000b2737c5d6e8f9a0b1c2d3e4f5a6b",
                    "score": 0.82,
                    "rank": 4,
                    "similarity_score": 0.84,
                    "novelty_score": 0.35,
                    "matched_cluster_id": 0,
                    "popularity": 88,
                    "audio_features": {
                        "danceability": 0.80,
                        "energy": 0.77,
                        "valence": 0.70,
                        "tempo": 138.0
                    },
                    "explanation": "Iconic electronic track matching your high-energy cluster. Despite popularity, strongly aligns with your taste for electronic production and danceable grooves. Similar vibe to MGMT and Daft Punk."
                },
                {
                    "id": "rec_track_5",
                    "name": "No Surprises",
                    "artists": ["Radiohead"],
                    "album": "OK Computer",
                    "image_url": "https://i.scdn.co/image/ab67616d0000b2738d7e9f0a1b2c3d4e5f6a7b8c",
                    "score": 0.79,
                    "rank": 5,
                    "similarity_score": 0.81,
                    "novelty_score": 0.48,
                    "matched_cluster_id": 1,
                    "popularity": 72,
                    "audio_features": {
                        "danceability": 0.41,
                        "energy": 0.43,
                        "valence": 0.29,
                        "acousticness": 0.28,
                        "tempo": 78.0
                    },
                    "explanation": "Perfect match for your introspective cluster. Low valence (0.29) and energy (0.43) mirror 'Breathe' by Pink Floyd. Melancholic with beautiful instrumentation."
                }
            ]
        }
    }
