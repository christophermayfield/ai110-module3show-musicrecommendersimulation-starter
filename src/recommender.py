"""
Music Recommender System Implementation

A content-based recommender that suggests songs based on matching user preferences
to song attributes like genre, mood, energy, valence, tempo, and acousticness.
"""

import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Song:
    """
    Represents a song and its attributes.

    Attributes:
        id: Unique identifier for the song
        title: Song title
        artist: Artist name
        genre: Music genre (pop, lofi, rock, jazz, etc.)
        mood: Emotional mood (happy, chill, intense, etc.)
        energy: Intensity level from 0.0 to 1.0
        tempo_bpm: Beats per minute
        valence: Musical positiveness from 0.0 (sad) to 1.0 (happy)
        danceability: How suitable for dancing from 0.0 to 1.0
        acousticness: Amount of acoustic instrumentation from 0.0 to 1.0
    """

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

    def to_dict(self) -> Dict:
        """Convert Song dataclass to dictionary for compatibility."""
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "mood": self.mood,
            "energy": self.energy,
            "tempo_bpm": self.tempo_bpm,
            "valence": self.valence,
            "danceability": self.danceability,
            "acousticness": self.acousticness,
        }


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.

    Attributes:
        favorite_genre: Primary genre the user enjoys
        favorite_mood: Primary mood the user seeks
        target_energy: Desired energy level from 0.0 to 1.0
        likes_acoustic: Whether user prefers acoustic music
        target_valence: Desired emotional tone from 0.0 to 1.0
        target_tempo: Desired tempo in BPM
    """

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.7
    target_tempo: float = 100.0


class TasteProfile:
    """
    Defines a comprehensive taste profile for music preferences.

    This class provides a more detailed preference model than UserProfile,
    including secondary preferences and contextual factors. It's used to
    build a more nuanced understanding of what makes music "feel right"
    for a particular listener.

    Attributes:
        primary_genre: The main genre you gravitate toward
        secondary_genres: Additional genres you enjoy (list)
        primary_mood: Your go-to emotional mood for music
        mood_range: Tuple of (min_mood_valence, max_mood_valence)
        energy_preference: Preferred intensity level (0.0-1.0)
        energy_tolerance: How much variation from target energy you accept
        valence_preference: Preferred emotional tone (0.0=sad, 1.0=happy)
        tempo_preference: Preferred tempo in BPM
        tempo_tolerance: +/- BPM tolerance for tempo matching
        acoustic_preference: How much you value acoustic elements (0.0-1.0)
        danceable_preference: How much you value danceable music (0.0-1.0)
        favorite_artists: List of artists you particularly enjoy
        avoided_attributes: Things to avoid (e.g., 'high_energy', 'low_valence')
    """

    def __init__(
        self,
        primary_genre: str,
        primary_mood: str,
        energy_preference: float,
        valence_preference: float,
        tempo_preference: float,
        acoustic_preference: float,
        danceable_preference: float,
        secondary_genres: List[str] = None,
        mood_range: Tuple[float, float] = (0.4, 0.8),
        energy_tolerance: float = 0.2,
        tempo_tolerance: int = 20,
        favorite_artists: List[str] = None,
        avoided_attributes: List[str] = None,
    ):
        self.primary_genre = primary_genre
        self.secondary_genres = secondary_genres or []
        self.primary_mood = primary_mood
        self.mood_range = mood_range
        self.energy_preference = energy_preference
        self.energy_tolerance = energy_tolerance
        self.valence_preference = valence_preference
        self.tempo_preference = tempo_preference
        self.tempo_tolerance = tempo_tolerance
        self.acoustic_preference = acoustic_preference
        self.danceable_preference = danceable_preference
        self.favorite_artists = favorite_artists or []
        self.avoided_attributes = avoided_attributes or []

    def to_user_profile(self) -> UserProfile:
        """
        Convert TasteProfile to basic UserProfile for the recommender.

        Returns:
            UserProfile with core preferences extracted from TasteProfile
        """
        return UserProfile(
            favorite_genre=self.primary_genre,
            favorite_mood=self.primary_mood,
            target_energy=self.energy_preference,
            likes_acoustic=self.acoustic_preference >= 0.6,
            target_valence=self.valence_preference,
            target_tempo=self.tempo_preference,
        )

    def __str__(self) -> str:
        """Human-readable representation of the taste profile."""
        return f"""Taste Profile:
  Primary Genre: {self.primary_genre}
  Secondary Genres: {", ".join(self.secondary_genres) if self.secondary_genres else "None specified"}
  Primary Mood: {self.primary_mood}
  Mood Range: {self.mood_range[0]:.0%}-{self.mood_range[1]:.0%} valence
  Energy Preference: {self.energy_preference:.0%} (±{self.energy_tolerance:.0%})
  Valence Preference: {self.valence_preference:.0%} (0=sad, 1=happy)
  Tempo Preference: {self.tempo_preference:.0f} BPM (±{self.tempo_tolerance})
  Acoustic Preference: {self.acoustic_preference:.0%}
  Danceable Preference: {self.danceable_preference:.0%}
  Favorite Artists: {", ".join(self.favorite_artists) if self.favorite_artists else "None specified"}
  Avoided Attributes: {", ".join(self.avoided_attributes) if self.avoided_attributes else "None"}

  -> Converts to UserProfile: {self.primary_genre}, {self.primary_mood}, energy={self.energy_preference:.0f}"""


# Pre-defined taste profiles for common user types
TASTE_PROFILES = {
    "chill": TasteProfile(
        primary_genre="lofi",
        primary_mood="chill",
        energy_preference=0.35,
        valence_preference=0.60,
        tempo_preference=80,
        acoustic_preference=0.80,
        danceable_preference=0.50,
        secondary_genres=["ambient", "jazz"],
        mood_range=(0.50, 0.70),
        energy_tolerance=0.15,
        tempo_tolerance=15,
        favorite_artists=["LoRoom", "Paper Lanterns"],
        avoided_attributes=["intense", "high_energy"],
    ),
    "workout": TasteProfile(
        primary_genre="pop",
        primary_mood="intense",
        energy_preference=0.90,
        valence_preference=0.75,
        tempo_preference=130,
        acoustic_preference=0.10,
        danceable_preference=0.90,
        secondary_genres=["rock", "electronic"],
        mood_range=(0.60, 0.90),
        energy_tolerance=0.10,
        tempo_tolerance=25,
        favorite_artists=["Max Pulse", "Club Masters"],
        avoided_attributes=["chill", "low_energy", "sad"],
    ),
    "focus": TasteProfile(
        primary_genre="lofi",
        primary_mood="focused",
        energy_preference=0.40,
        valence_preference=0.55,
        tempo_preference=85,
        acoustic_preference=0.75,
        danceable_preference=0.45,
        secondary_genres=["ambient", "classical"],
        mood_range=(0.45, 0.65),
        energy_tolerance=0.15,
        tempo_tolerance=15,
        favorite_artists=["LoRoom", "Morning Calm"],
        avoided_attributes=["intense", "party", "high_danceability"],
    ),
    "party": TasteProfile(
        primary_genre="pop",
        primary_mood="energetic",
        energy_preference=0.88,
        valence_preference=0.85,
        tempo_preference=128,
        acoustic_preference=0.08,
        danceable_preference=0.95,
        secondary_genres=["electronic", "synthwave"],
        mood_range=(0.75, 1.0),
        energy_tolerance=0.12,
        tempo_tolerance=20,
        favorite_artists=["Festival Beats", "Club Masters"],
        avoided_attributes=["sad", "low_energy", "low_valence"],
    ),
}


def create_christopher_profile() -> TasteProfile:
    """
    Create Christopher Mayfield's personal taste profile.

    This profile is based on the song catalog he built, which includes:
    - Diverse genres: pop, lofi, rock, jazz, ambient, synthwave, indie pop, electronic
    - Mood variety: happy, chill, intense, relaxed, focused, moody, energetic, sad, romantic, dreamy
    - Energy range: mostly medium (0.3-0.8) with some high (0.9+) tracks
    - Balance of acoustic and electronic elements

    The profile reflects someone who appreciates:
    - Versatility across multiple genres
    - A preference for positive/varied emotional tones
    - Moderate energy levels (not too intense, not too mellow)
    - A mix of acoustic warmth and electronic production
    - Music that works for different contexts (work, relaxation, activities)

    Returns:
        TasteProfile representing Christopher's music preferences
    """
    return TasteProfile(
        primary_genre="lofi",
        primary_mood="chill",
        energy_preference=0.50,
        valence_preference=0.68,
        tempo_preference=95,
        acoustic_preference=0.55,
        danceable_preference=0.58,
        secondary_genres=["pop", "ambient", "synthwave", "jazz"],
        mood_range=(0.40, 0.85),
        energy_tolerance=0.25,
        tempo_tolerance=30,
        favorite_artists=[
            "LoRoom",
            "Neon Echo",
            "Orbit Bloom",
            "Slow Stereo",
            "Paper Lanterns",
        ],
        avoided_attributes=["extremely_sad", "overwhelmingly_loud"],
    )


# Christopher's default taste profile instance
CHRISTOPHER_PROFILE = create_christopher_profile()


class Recommender:
    """
    OOP implementation of the music recommendation logic.

    This class manages a catalog of songs and provides methods
    to generate personalized recommendations for users.

    Uses content-based filtering to recommend songs that match
    the user's stated preferences.
    """

    # Default feature weights for scoring
    DEFAULT_WEIGHTS = {
        "genre": 2.0,
        "mood": 2.0,
        "energy": 1.5,
        "valence": 1.5,
        "tempo": 1.0,
        "acousticness": 1.0,
    }

    def __init__(self, songs: List[Song], weights: Optional[Dict[str, float]] = None):
        """
        Initialize the recommender with a list of songs.

        Args:
            songs: List of Song objects
            weights: Optional custom weights for scoring features
        """
        self.songs = songs
        self.weights = weights if weights else self.DEFAULT_WEIGHTS.copy()

    def _calculate_feature_score(
        self, user: UserProfile, song: Song
    ) -> Tuple[float, Dict]:
        """
        Calculate how well a song matches user preferences.

        Returns:
            Tuple of (overall_score, details_dict)
        """
        total_weight = 0.0
        weighted_score = 0.0
        details = {}

        # 1. Genre match (binary: 1.0 or 0.0)
        genre_match = 1.0 if song.genre == user.favorite_genre else 0.0
        weighted_score += self.weights["genre"] * genre_match
        total_weight += self.weights["genre"]
        details["genre_match"] = genre_match

        # 2. Mood match (binary: 1.0 or 0.0)
        mood_match = 1.0 if song.mood == user.favorite_mood else 0.0
        weighted_score += self.weights["mood"] * mood_match
        total_weight += self.weights["mood"]
        details["mood_match"] = mood_match

        # 3. Energy similarity (1 - absolute difference)
        energy_diff = abs(user.target_energy - song.energy)
        energy_score = 1.0 - energy_diff
        weighted_score += self.weights["energy"] * energy_score
        total_weight += self.weights["energy"]
        details["energy_score"] = energy_score

        # 4. Valence similarity (1 - absolute difference)
        valence_diff = abs(user.target_valence - song.valence)
        valence_score = 1.0 - valence_diff
        weighted_score += self.weights["valence"] * valence_score
        total_weight += self.weights["valence"]
        details["valence_score"] = valence_score

        # 5. Tempo similarity (normalized by 120 BPM range)
        tempo_diff = abs(user.target_tempo - song.tempo_bpm) / 120.0
        tempo_score = max(0.0, 1.0 - tempo_diff)
        weighted_score += self.weights["tempo"] * tempo_score
        total_weight += self.weights["tempo"]
        details["tempo_score"] = tempo_score

        # 6. Acousticness similarity (1 - absolute difference)
        acoustic_target = 0.8 if user.likes_acoustic else 0.2
        acoustic_diff = abs(acoustic_target - song.acousticness)
        acoustic_score = 1.0 - acoustic_diff
        weighted_score += self.weights["acousticness"] * acoustic_score
        total_weight += self.weights["acousticness"]
        details["acousticness_score"] = acoustic_score

        # Calculate final normalized score
        final_score = weighted_score / total_weight if total_weight > 0 else 0.0

        return final_score, details

    def _build_explanation(self, user: UserProfile, song: Song, details: Dict) -> str:
        """Generate a human-readable explanation for why this song is recommended."""
        parts = []

        # Check category matches first (most important)
        if details["genre_match"] == 1.0:
            parts.append(f"matches your favorite genre: {song.genre}")
        if details["mood_match"] == 1.0:
            parts.append(f"has the perfect mood: {song.mood}")

        # Add numerical feature feedback
        if details["energy_score"] > 0.8:
            parts.append("high energy that matches your target")
        elif details["energy_score"] < 0.5:
            parts.append("lower energy than your target")

        if details["valence_score"] > 0.8:
            parts.append("happy/positive tone")
        elif details["valence_score"] < 0.5:
            parts.append("more melancholic tone")

        if details["tempo_score"] > 0.8:
            parts.append(f"tempo close to your {song.tempo_bpm:.0f} BPM target")

        if details["acousticness_score"] > 0.7:
            parts.append("acoustic sound you enjoy")

        # Build the explanation string
        if parts:
            explanation = f"{song.title} by {song.artist} is recommended because it "
            explanation += ", ".join(parts[:2])  # Limit to 2 reasons
            if len(parts) > 2:
                explanation += f" (and {len(parts) - 2} other factors)"
            return explanation
        else:
            return f"{song.title} by {song.artist} moderately matches your preferences"

    def set_weights(self, weights: Dict[str, float]) -> None:
        """Customize feature weights for scoring."""
        self.weights = weights

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Generate song recommendations for a user.

        Args:
            user: UserProfile with preferences
            k: Number of recommendations to return

        Returns:
            List of Song objects sorted by relevance score (highest first)
        """
        # Score all songs
        scored_songs = []
        for song in self.songs:
            score, _ = self._calculate_feature_score(user, song)
            scored_songs.append((song, score))

        # Sort by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)

        # Apply diversity constraint (max 2 songs per artist)
        recommendations = []
        artist_counts = {}

        for song, score in scored_songs:
            artist = song.artist
            if artist_counts.get(artist, 0) < 2:  # Max 2 songs per artist
                recommendations.append(song)
                artist_counts[artist] = artist_counts.get(artist, 0) + 1

            if len(recommendations) >= k:
                break

        return recommendations

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Generate detailed explanation for why a specific song is recommended.

        Args:
            user: UserProfile with preferences
            song: Song to explain

        Returns:
            Human-readable explanation string
        """
        score, details = self._calculate_feature_score(user, song)
        return self._build_explanation(user, song, details)

    def get_score(self, user: UserProfile, song: Song) -> float:
        """
        Get the relevance score for a specific song.

        Args:
            user: UserProfile with preferences
            song: Song to score

        Returns:
            Similarity score from 0.0 to 1.0
        """
        score, _ = self._calculate_feature_score(user, song)
        return score

    def get_all_scores(self, user: UserProfile) -> List[Tuple[Song, float]]:
        """
        Get scores for all songs.

        Args:
            user: UserProfile with preferences

        Returns:
            List of (Song, score) tuples sorted by score descending
        """
        scored = []
        for song in self.songs:
            score, _ = self._calculate_feature_score(user, song)
            scored.append((song, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored


def load_songs(csv_path: str) -> List[Song]:
    """
    Loads songs from a CSV file.

    Args:
        csv_path: Path to the songs CSV file

    Returns:
        List of Song objects
    """
    songs = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = Song(
                id=int(row["id"]),
                title=row["title"],
                artist=row["artist"],
                genre=row["genre"],
                mood=row["mood"],
                energy=float(row["energy"]),
                tempo_bpm=float(row["tempo_bpm"]),
                valence=float(row["valence"]),
                danceability=float(row["danceability"]),
                acousticness=float(row["acousticness"]),
            )
            songs.append(song)

    return songs


def recommend_songs(user_prefs: Dict, songs: List, k: int = 5) -> List[Dict]:
    """
    Functional implementation of the recommendation logic.

    Args:
        user_prefs: Dictionary with user preferences
        songs: List of Song objects
        k: Number of recommendations to return

    Returns:
        List of song dictionaries (the recommended songs)
    """
    # Convert dict list to Song objects if needed
    song_objects = []
    for s in songs:
        if isinstance(s, dict):
            song_objects.append(
                Song(
                    id=s["id"],
                    title=s["title"],
                    artist=s["artist"],
                    genre=s["genre"],
                    mood=s["mood"],
                    energy=s["energy"],
                    tempo_bpm=s["tempo_bpm"],
                    valence=s["valence"],
                    danceability=s["danceability"],
                    acousticness=s["acousticness"],
                )
            )
        else:
            song_objects.append(s)

    # Create user profile from preferences
    user = UserProfile(
        favorite_genre=user_prefs.get("genre", "pop"),
        favorite_mood=user_prefs.get("mood", "happy"),
        target_energy=user_prefs.get("energy", 0.7),
        likes_acoustic=user_prefs.get("acoustic", False),
        target_valence=user_prefs.get("valence", 0.7),
        target_tempo=user_prefs.get("tempo", 100.0),
    )

    # Create recommender and get recommendations
    recommender = Recommender(song_objects)
    recommended_songs = recommender.recommend(user, k=k)

    # Convert back to dict format for compatibility
    return [s.to_dict() if hasattr(s, "to_dict") else s for s in recommended_songs]
