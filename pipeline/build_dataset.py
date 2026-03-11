from models.TrackRow import TrackRow
from pipeline.storage import load_dataset, save_dataset
from pipeline.enrich_audio_features import enrich_audio_features

def normalize_track(raw_track, time_range: str, rank: int, pulled_at: str) -> TrackRow:
    """
    Convert a raw Spotify track object into a TrackRow.
    """

    # Album info
    album = raw_track.get("album", {})
    album_name = album.get("name", "")
    album_release_date = album.get("release_date", "")

    # Album image url (may be missing or empty)
    images = album.get("images", [])
    album_image_url = images[0].get("url") if images else None

    # Track fields (some may be None)
    preview_url = raw_track.get("preview_url")  # often None
    duration_ms = raw_track.get("duration_ms", 0)
    explicit = raw_track.get("explicit", False)

    # Artists list (store all artists; influence computed later)
    artists_list = []
    for artist in raw_track.get("artists", []):
        artists_list.append({
            "artist_id": artist.get("id"),
            "artist_name": artist.get("name"),
            "influence": None
        })

    return TrackRow(
        track_id=raw_track.get("id", ""),
        track_name=raw_track.get("name", ""),
        artists=artists_list,
        album_name=album_name,
        track_popularity=raw_track.get("popularity", 0),
        track_duration_ms=duration_ms,
        track_explicit=explicit,
        track_preview_url=preview_url,
        track_album_image_url=album_image_url,
        track_album_release_date=album_release_date,
        track_rank=rank,
        time_range=time_range,
        pulled_at=pulled_at
    )


def build_feature_dataset(sp, dataset_path: str, output_path: str):
    """
    Build a feature dataset from a dataset path.
    """
    records, metadata = load_dataset(dataset_path)
    enriched_records = enrich_audio_features(sp, records)

    new_metadata = metadata.copy()
        # Update metadata for the enriched dataset
    new_metadata["dataset_type"] = "feature_enriched"
    new_metadata["feature_set"] = "spotify_audio_features_v1"
    new_metadata["feature_generated_at"] = datetime.now().isoformat(timespec="seconds")
    new_metadata["num_rows"] = len(enriched_records)
    new_metadata["num_unique_tracks"] = len(
        set(record["track_id"] for record in enriched_records)
    )
    new_metadata["source_dataset"] = dataset_path
    save_dataset(output_path, enriched_records, new_metadata)
    return new_metadata, enriched_records

