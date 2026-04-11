"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommender import Recommender, Song, UserProfile, load_songs, recommend_songs


def print_banner():
    """Print a welcome banner."""
    print("\n" + "=" * 60)
    print("       🎵 MUSIC RECOMMENDER SIMULATION 🎵")
    print("=" * 60)
    print("\nA content-based recommender that matches your music")
    print("preferences to song attributes like genre, mood, energy,")
    print("valence, tempo, and acousticness.\n")


def print_song_card(song: Song, score: float, explanation: str, rank: int = None):
    """Print a nicely formatted song recommendation card."""
    rank_str = f"#{rank} " if rank is not None else ""
    print(f"{rank_str}{'─' * 50}")
    print(f"  🎵 {song.title}")
    print(f"  👤 {song.artist}")
    print(f"  🏷️  {song.genre} | 😌 {song.mood}")
    print(f"  ⚡ Energy: {song.energy:.0%} | 😊 Valence: {song.valence:.0%}")
    print(
        f"  🥁 Tempo: {song.tempo_bpm:.0f} BPM | 🎸 Acoustic: {song.acousticness:.0%}"
    )
    print(f"  📊 Match Score: {score:.0%}")
    print(f"  💡 {explanation}")
    print()


def demonstrate_with_user_profile(name: str, user_prefs: dict, songs: list, k: int = 5):
    """Demonstrate recommendations for a specific user profile."""
    print(f"\n{'=' * 60}")
    print(f"  👤 USER: {name}")
    print(f"{'=' * 60}")
    print(f"\nProfile preferences:")
    for key, value in user_prefs.items():
        print(f"  • {key}: {value}")

    print(f"\n🎶 TOP {k} RECOMMENDATIONS:")
    print()

    recommendations = recommend_songs(user_prefs, songs, k=k)

    # Create a recommender to get scores and explanations
    song_objects = [
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
        for s in songs
    ]

    user = UserProfile(
        favorite_genre=user_prefs.get("genre", "pop"),
        favorite_mood=user_prefs.get("mood", "happy"),
        target_energy=user_prefs.get("energy", 0.7),
        likes_acoustic=user_prefs.get("acoustic", False),
        target_valence=user_prefs.get("valence", 0.7),
        target_tempo=user_prefs.get("tempo", 100.0),
    )

    recommender = Recommender(song_objects)

    for i, song_dict in enumerate(recommendations):
        song = Song(
            id=song_dict["id"],
            title=song_dict["title"],
            artist=song_dict["artist"],
            genre=song_dict["genre"],
            mood=song_dict["mood"],
            energy=song_dict["energy"],
            tempo_bpm=song_dict["tempo_bpm"],
            valence=song_dict["valence"],
            danceability=song_dict["danceability"],
            acousticness=song_dict["acousticness"],
        )
        score = recommender.get_score(user, song)
        explanation = recommender.explain_recommendation(user, song)
        print_song_card(song, score, explanation, i + 1)


def run_preset_demos(songs: list):
    """Run demonstrations with preset user profiles."""

    # Demo 1: Pop/Happy Music Fan
    demonstrate_with_user_profile(
        "Pop & Happy Enthusiast",
        {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "valence": 0.8,
            "tempo": 120,
            "acoustic": False,
        },
        songs,
        k=5,
    )

    input("\n⏸️  Press Enter to continue to the next demo...")

    # Demo 2: Chill Lofi Fan
    demonstrate_with_user_profile(
        "Chill Lofi Lover",
        {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "valence": 0.6,
            "tempo": 80,
            "acoustic": True,
        },
        songs,
        k=5,
    )

    input("\n⏸️  Press Enter to continue to the next demo...")

    # Demo 3: Workout Enthusiast
    demonstrate_with_user_profile(
        "Workout Warrior",
        {
            "genre": "pop",
            "mood": "intense",
            "energy": 0.9,
            "valence": 0.7,
            "tempo": 130,
            "acoustic": False,
        },
        songs,
        k=5,
    )

    input("\n⏸️  Press Enter to continue to the next demo...")

    # Demo 4: Jazz/Coffee Shop Vibes
    demonstrate_with_user_profile(
        "Jazz & Coffee Shop Vibes",
        {
            "genre": "jazz",
            "mood": "relaxed",
            "energy": 0.4,
            "valence": 0.7,
            "tempo": 90,
            "acoustic": True,
        },
        songs,
        k=5,
    )


def run_edge_case_demos(songs: list):
    """Run demonstrations with adversarial and edge-case user profiles."""

    # Edge Case 1: Conflicting High Energy / Sad Mood
    demonstrate_with_user_profile(
        "Adversarial: High Energy Sadness",
        {
            "genre": "electronic",
            "mood": "sad",
            "energy": 0.95,
            "valence": 0.1,
            "tempo": 140,
            "acoustic": False,
        },
        songs,
        k=3,
    )

    input("\n⏸️  Press Enter to continue to the next edge case...")

    # Edge Case 2: Extreme Minimalist (Zero Energy/Acoustic)
    demonstrate_with_user_profile(
        "Edge Case: The Ultra Minimalist",
        {
            "genre": "ambient",
            "mood": "chill",
            "energy": 0.05,
            "valence": 0.05,
            "tempo": 40,
            "acoustic": True,
        },
        songs,
        k=3,
    )

    input("\n⏸️  Press Enter to continue to the next edge case...")

    # Edge Case 3: Conflicting Fast Acoustic
    demonstrate_with_user_profile(
        "Adversarial: Fast Acoustic",
        {
            "genre": "jazz",
            "mood": "happy",
            "energy": 0.5,
            "valence": 0.8,
            "tempo": 180,
            "acoustic": True,
        },
        songs,
        k=3,
    )


def print_summary():
    """Print a summary of the system."""
    print("\n" + "=" * 60)
    print("  📊 SYSTEM SUMMARY")
    print("=" * 60)
    print("""
This music recommender uses CONTENT-BASED FILTERING:

FEATURES USED:
  • Genre     - Music style (pop, lofi, rock, jazz, etc.)
  • Mood      - Emotional tone (happy, chill, intense, etc.)
  • Energy    - Intensity level (0.0 - 1.0)
  • Valence   - Musical positiveness (0.0 = sad, 1.0 = happy)
  • Tempo     - Beats per minute (BPM)
  • Acousticness - Amount of acoustic instrumentation (0.0 - 1.0)

HOW IT WORKS:
  1. User provides their preferences (genre, mood, target features)
  2. System calculates similarity score for each song
  3. Songs are ranked by score (descending)
  4. Diversity rule: max 2 songs per artist
  5. Top k songs are returned with explanations

FEATURE WEIGHTS:
  • Genre: 2.0 (category match is important)
  • Mood: 2.0 (mood alignment matters)
  • Energy: 1.5 (major vibe factor)
  • Valence: 1.5 (emotional tone)
  • Tempo: 1.0 (moderate importance)
  • Acousticness: 1.0 (moderate importance)
    """)


def main():
    """Main entry point for the application."""
    print_banner()

    # Load songs from CSV
    print("📁 Loading songs from data/songs.csv...")
    songs = load_songs("data/songs.csv")
    print(f"✅ Loaded {len(songs)} songs\n")

    while True:
        print("=" * 60)
        print("  MENU")
        print("=" * 60)
        print("  1. 🎬 Run preset demos (4 user profiles)")
        print("  2. 🧪 Run edge-case & adversarial demos")
        print("  3. 📊 View system summary")
        print("  4. 🚪 Exit")
        print()

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            run_preset_demos(songs)
        elif choice == "2":
            run_edge_case_demos(songs)
        elif choice == "3":
            print_summary()
            input("\n⏸️  Press Enter to return to menu...")
        elif choice == "4":
            print("\n👋 Thanks for using the Music Recommender!")
            print("🎵 Happy listening!\n")
            break
        else:
            print("\n⚠️  Invalid choice. Please select 1-4.\n")


if __name__ == "__main__":
    main()
