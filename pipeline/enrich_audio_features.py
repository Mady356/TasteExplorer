from services.spotify_fetch import fetch_audio_features
from typing import List, Dict

def enrich_audio_features(sp, records: List[Dict]):
    """
    Enrich records with Spotify audio features.
    """

    # 1. Extract track IDs
    track_ids = [record["track_id"] for record in records]

    # 2. Deduplicate track IDs
    unique_track_ids = list(set(track_ids))

    # 3. Fetch audio features once
    features = fetch_audio_features(sp, unique_track_ids)

    # 4. Build lookup dictionary
    feature_lookup = {}
    for feature in features:
        if feature is not None:
            feature_lookup[feature["id"]] = feature

    # 5. Merge features into records
    enriched_records = []

    for record in records:
        track_id = record["track_id"]
        enriched_record = record.copy()

        feature = feature_lookup.get(track_id)

        if feature:
            enriched_record["danceability"] = feature["danceability"]
            enriched_record["energy"] = feature["energy"]
            enriched_record["acousticness"] = feature["acousticness"]
            enriched_record["instrumentalness"] = feature["instrumentalness"]
            enriched_record["liveness"] = feature["liveness"]
            enriched_record["valence"] = feature["valence"]
            enriched_record["tempo"] = feature["tempo"]
        else:
            enriched_record["danceability"] = None
            enriched_record["energy"] = None
            enriched_record["acousticness"] = None
            enriched_record["instrumentalness"] = None
            enriched_record["liveness"] = None
            enriched_record["valence"] = None
            enriched_record["tempo"] = None

        enriched_records.append(enriched_record)

    return enriched_records
    