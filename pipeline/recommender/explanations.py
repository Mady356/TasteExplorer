"""
Recommendation explanations.

Simple rule-based explanations for why a track was recommended.
"""
from typing import Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.feature_space import FEATURE_COLUMNS


def generate_explanation(
    scored_track: Dict,
    cluster_node: Dict,
    candidate_track: Dict = None
) -> str:
    """
    Generate explanation for why a track was recommended.

    Args:
        scored_track: Scored track dict with similarity and novelty scores
        cluster_node: Matched cluster node from Layer 2
        candidate_track: Optional original candidate track (for feature details)

    Returns:
        Human-readable explanation string
    """
    cluster_label = cluster_node.get("suggested_label", "your taste")
    similarity = scored_track.get("similarity_score", 0)
    novelty = scored_track.get("novelty_score", 0)
    popularity = scored_track.get("track_popularity", 50)

    # Base explanation
    parts = []

    # Cluster match
    parts.append(f"Matches your '{cluster_label}' cluster")

    # Similarity level
    if similarity > 0.8:
        parts.append("with very strong similarity")
    elif similarity > 0.6:
        parts.append("with strong similarity")
    elif similarity > 0.4:
        parts.append("with good similarity")
    else:
        parts.append("with moderate similarity")

    # Novelty note
    if novelty > 0.8:
        parts.append("This is a hidden gem with very low popularity")
    elif novelty > 0.6:
        parts.append("This is an undiscovered track")
    elif novelty < 0.3:
        parts.append("This is a popular track")

    # Feature insights (if available)
    if candidate_track and "audio_features" in candidate_track:
        feature_insights = _get_feature_insights(
            candidate_track["audio_features"],
            cluster_node
        )
        if feature_insights:
            parts.append(feature_insights)

    return ". ".join(parts) + "."


def _get_feature_insights(
    audio_features: Dict,
    cluster_node: Dict
) -> str:
    """
    Generate insights about specific audio features.

    Args:
        audio_features: Track's audio features
        cluster_node: Cluster node

    Returns:
        Feature insight string, or empty if no strong patterns
    """
    insights = []

    # Check specific features
    valence = audio_features.get("valence")
    energy = audio_features.get("energy")
    danceability = audio_features.get("danceability")
    acousticness = audio_features.get("acousticness")
    instrumentalness = audio_features.get("instrumentalness")

    if valence is not None:
        if valence > 0.8:
            insights.append("very uplifting")
        elif valence < 0.2:
            insights.append("melancholic")

    if energy is not None:
        if energy > 0.8:
            insights.append("high energy")
        elif energy < 0.2:
            insights.append("calm")

    if danceability is not None and danceability > 0.8:
        insights.append("very danceable")

    if acousticness is not None and acousticness > 0.7:
        insights.append("acoustic")

    if instrumentalness is not None and instrumentalness > 0.7:
        insights.append("instrumental")

    if insights:
        return "Features: " + ", ".join(insights)

    return ""


def generate_artist_explanation(artist_dict: Dict) -> str:
    """
    Generate explanation for why an artist was recommended.

    Args:
        artist_dict: Ranked artist dict

    Returns:
        Human-readable explanation string
    """
    artist_name = artist_dict["artist_name"]
    artist_score = artist_dict["artist_score"]
    track_count = artist_dict["track_count"]
    matched_clusters = artist_dict.get("matched_clusters", [])

    parts = []

    # Score level
    if artist_score > 0.8:
        parts.append(f"{artist_name} is an excellent match for your taste")
    elif artist_score > 0.6:
        parts.append(f"{artist_name} is a strong match for your taste")
    else:
        parts.append(f"{artist_name} matches your taste")

    # Track count
    if track_count > 1:
        parts.append(f"with {track_count} recommended tracks")

    # Cluster matches
    if len(matched_clusters) > 1:
        parts.append(f"spanning {len(matched_clusters)} of your taste clusters")
    elif len(matched_clusters) == 1:
        parts.append("matching one of your taste clusters")

    return ". ".join(parts) + "."


def generate_cluster_specific_explanation(
    scored_track: Dict,
    cluster_node: Dict
) -> str:
    """
    Generate cluster-specific explanation.

    Shorter version for cluster-specific recommendation lists.

    Args:
        scored_track: Scored track dict
        cluster_node: Matched cluster node

    Returns:
        Short explanation string
    """
    similarity = scored_track.get("similarity_score", 0)
    novelty = scored_track.get("novelty_score", 0)

    if similarity > 0.8 and novelty > 0.7:
        return "Perfect match, hidden gem"
    elif similarity > 0.8:
        return "Perfect match"
    elif novelty > 0.8:
        return "Hidden gem"
    elif similarity > 0.6:
        return "Strong match"
    else:
        return "Good match"
