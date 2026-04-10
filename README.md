# 🎵 Music Recommender Simulation

## Project Summary

This project implements a **content-based music recommender system** that suggests songs based on a user's taste profile. Unlike collaborative filtering (which uses "people who liked X also liked Y"), our system uses song attributes like genre, mood, energy, valence, tempo, and acousticness to find matches.

Key components built:
- **UserProfile**: Captures preferred genres, moods, and target values for audio features
- **Scoring Rule**: Calculates similarity between user preferences and song attributes (0-1 score)
- **Ranking Rule**: Orders recommendations by score while enforcing diversity constraints (max 2 songs per artist)

We tested the system with multiple user profiles (pop fan, chill lofi user, workout enthusiast, jazz lover) and analyzed how different features affect recommendations.

---

## How The System Works

Our content-based recommender matches song features to user preferences:

### Song Features Used

| Feature | Type | Description |
|---------|------|-------------|
| `genre` | Categorical | pop, lofi, rock, ambient, jazz, synthwave, indie pop |
| `mood` | Categorical | happy, chill, intense, relaxed, focused, moody |
| `energy` | Numerical (0-1) | Intensity level |
| `valence` | Numerical (0-1) | Emotional positivity (sad ↔ happy) |
| `tempo_bpm` | Numerical | Beats per minute |
| `danceability` | Numerical (0-1) | How suitable for dancing |
| `acousticness` | Numerical (0-1) | Amount of acoustic instruments |

### UserProfile Structure

The user profile stores:
- **preferred_genres**: List of genres the user likes (e.g., ['pop'])
- **preferred_moods**: List of moods (e.g., ['happy'])
- **target_energy**: Desired energy level (0.0-1.0)
- **target_valence**: Desired emotional tone (0.0-1.0)
- **target_tempo**: Desired BPM (e.g., 120)
- **target_acousticness**: Desired acoustic quality (0.0-1.0)

### Scoring Rule

The scoring function calculates a 0-1 similarity score:

```
1. Genre match: +2.0 if matches, +0.0 if not
2. Mood match: +2.0 if matches, +0.0 if not
3. Energy similarity: 1 - |target_energy - song_energy|
4. Valence similarity: 1 - |target_valence - song_valence|
5. Tempo similarity: 1 - (|target_tempo - song_tempo| / 120)
6. Acousticness similarity: 1 - |target_acousticness - song_acousticness|

Final score = weighted_sum / total_weight
```

Weighted by: genre=2.0, mood=2.0, energy=1.5, valence=1.5, tempo=1.0, acousticness=1.0

### Ranking Rule

After scoring all songs:
1. Sort by score (descending)
2. Apply diversity constraint: max 2 songs per artist
3. Return top N recommendations

### Vibe Clusters Identified

| Vibe | Songs | Characteristics |
|------|-------|-----------------|
| Chill/Lofi | Midnight Coding, Library Rain, Focus Flow | Low energy (0.28-0.42), high acousticness |
| Happy Pop | Sunrise City, Rooftop Lights | High valence (0.81-0.84), high energy |
| Intense/Workout | Storm Runner, Gym Hero | High energy (0.91-0.93), fast tempo |
| Moody Synthwave | Night Drive Loop | Medium energy, low valence (0.49) |




---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Experiment 1: Different User Profiles

Tested the system with 4 distinct user types:

| User Profile | Top Recommendation | Score |
|--------------|-------------------|-------|
| Pop/Happy/High Energy | Sunrise City | 0.904 |
| Chill Lofi Fan | Focus Flow | 0.917 |
| Workout Enthusiast | Gym Hero | 0.909 |
| Jazz Lover | Coffee Shop Stories | 0.967 |

**Finding**: The recommender correctly identifies genre-matched songs as top picks for each profile.

### Experiment 2: Mood Filtering Impact

A song can have a high audio-feature score but still be excluded if mood doesn't match:
- **Night Drive Loop**: Raw score 0.75 (good energy/valence match), but excluded for "Pop/Happy" user because mood='mody' ≠ 'happy'

**Finding**: Mood and genre weighting (2.0 each) effectively filters out mismatched songs.

### Experiment 3: Feature Weight Sensitivity

Tested equal weights vs. prioritized weights:

| Weight Strategy | Pop User Top Pick | Score |
|-----------------|-------------------|-------|
| All equal (1.0) | Sunrise City | 0.85 |
| Genre/mood prioritized | Sunrise City | 0.90 |

**Finding**: Prioritizing genre and mood improves recommendation quality for categorical preferences.

### Experiment 4: Diversity Enforcement

Without diversity rule: Top 3 for "Pop" user were all by Neon Echo (if they had more pop songs).
With max 2 per artist: Introduces variety from Max Pulse and Indigo Parade.

**Finding**: Diversity rules prevent monotonous playlists.


---

## Limitations and Risks

### Data Limitations
- **Tiny catalog**: Only 10 songs compared to Spotify's 100M+ tracks
- **Limited genres**: Missing many genres (country, metal, classical, hip-hop, etc.)
- **Binary mood matching**: "happy" or "not happy" misses nuance (e.g., "euphoric" vs "content")

### Technical Limitations
- **No collaborative filtering**: Cannot leverage "users like you also liked X"
- **Static user profile**: Preferences don't change over time
- **No context awareness**: Doesn't consider time of day, activity, or location
- **Arbitrary weights**: Weights (genre=2.0, etc.) were chosen heuristically, not learned

### Potential Risks
- **Filter bubble**: Users only get songs similar to what they already like
- **Genre bias**: Popular genres (pop, lofi) have more representation
- **Opaque scoring**: Users don't understand why "Night Drive Loop" was recommended
- **Cold start**: New genres or moods have no data to match against

### "Vibe" Subjectivity
The features we chose (energy, valence, tempo) align with some musical experiences but miss:
- **Cultural context**: Same tempo can feel different in different genres
- **Lyric themes**: Content-based filtering ignores semantics
- **Production quality**: Audio features don't capture "warmth" or "crunch"
- **Personal associations**: A song might match mathematically but not emotionally

You will go deeper on this in your model card.


---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

### What We Learned

**About how recommenders work**: Building this system revealed that recommenders are fundamentally about **feature engineering** and **similarity measurement**. We don't need complex AI to make useful recommendations—just thoughtful feature selection (genre, mood, energy, valence) and a scoring rule that weights what matters most. The "magic" of Spotify or YouTube comes from combining multiple signals (collaborative + content-based + contextual) at scale.

**About bias and fairness**: Our simple system already shows bias risks: popular genres get recommended more because they have more data; users stuck in a "vibe" never discover new types of music. In real systems, these biases compound—algorithms can create echo chambers, limit discovery of niche artists, or reinforce popularity over quality. The scoring rule itself embeds values: our choice to weight genre=2.0 over tempo=1.0 reflects an assumption about what matters to users.

### Key Takeaways

1. **Scoring ≠ Ranking**: A song can score high but still shouldn't be recommended (diversity, freshness, context)
2. **Feature choice matters**: We chose energy/valence because they capture "vibe"—but many musical qualities are invisible to our features
3. **Simple works**: Even a basic content-based recommender produces sensible results with thoughtful features



---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
