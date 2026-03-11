from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class TrackRow:
    track_name: str
    artists: List[Dict]
    album_name: str
    track_id: str
    track_popularity: int
    track_duration_ms: int
    track_explicit: bool
    track_preview_url: Optional[str]
    track_album_image_url: Optional[str]
    track_album_release_date: str
    track_rank: int
    time_range: str
    pulled_at: str





