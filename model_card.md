# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users. It is designed to demonstrate how content-based filtering works by matching specific song attributes to a manually defined user profile.

---

## 3. How the Model Works  

VibeFinder works like a digital matching assistant. It looks at several characteristics of every song in its library—like its genre, the "mood" it's tagged with, how energetic it feels, and its overall "vibe" (valence). 

It compares these features to what you've said you like. For example, if you say you love "Lo-fi" and "Chill" music, it gives a huge boost to any song with those exact labels. Then, it checks if the song's energy and speed (BPM) are close to your target. It calculates a final "match score" for every song and shows you the ones that fit your preferences the best.

---

## 4. Data  

The dataset consists of **20 songs** stored in `data/songs.csv`.
- **Genres represented:** Pop, Lofi, Rock, Ambient, Jazz, Synthwave, Indie Pop, and Electronic.
- **Moods represented:** Happy, Chill, Intense, Relaxed, Moody, Focused, Energetic, Sad, Romantic, and Dreamy.
- **Source:** This is a curated sample dataset that reflects a diverse mix of "vibes" but is heavily weighted toward chill/ambient and high-energy pop/electronic tracks. It lacks many mainstream genres like Country, Hip-Hop, or Classical.

---

## 5. Strengths  

- **Extreme Transparency:** It is very easy to explain exactly why a song was recommended (e.g., "This song matched your favorite genre and mood").
- **Consistent Results:** For clear-cut user profiles (like a "Workout" profile), it consistently finds the high-energy, high-tempo tracks.
- **Artist Diversity:** It includes a built-in rule to ensure you don't get more than two songs from the same artist in your top 5, preventing a single artist from dominating your playlist.

---

## 6. Limitations and Bias 

- **Simple String Matching:** If you like "Chillhop" but the song is labeled "Lofi," the system sees them as 100% different. It doesn't understand that genres can be related.
- **The Filter Bubble:** It only shows you what you've already said you like. It will never "surprise" you with a great song from a genre you haven't tried yet.
- **No Memory:** The system is "stateless." It doesn't learn from your history. If you skip a song every time it comes up, VibeFinder will still recommend it tomorrow if it matches your profile.
- **Genre Bias:** Because the catalog is small, users who like niche genres (like Jazz or Synthwave) have very few options to choose from compared to Lofi fans.

---

## 7. Evaluation  

I checked the system by creating and testing several distinct user profiles:
- **The Workout Enthusiast:** Verified it correctly recommended high-energy tracks like "Gym Hero."
- **The Chill Lofi Fan:** Confirmed it picked up "Midnight Coding" and "Library Rain."
- **The Jazz Lover:** Tested if it could find the few jazz tracks available ("Coffee Shop Stories").
- **Comparison:** Compared results against expectations to ensure the scoring weights (Genre and Mood being the most important) were working as intended.

---

## 8. Future Work  

- **Collaborative Filtering:** Add the ability to learn from other users' tastes ("People who liked this also liked...") to provide more thorough and surprising recommendations.
- **Context Awareness:** Update the profile to consider the time of day or current activity (e.g., "Study mode" vs "Party mode").
- **Fuzzy Matching:** Improve the logic to recognize that similar genres (like "Pop" and "Indie Pop") should get partial credit for matching.
- **Historical Learning:** Implement a system to track user "likes" and "skips" to refine the profile automatically.

---

## 9. Personal Reflection  

I was surprised that the model was pretty simple to build while still giving out decent recommendations. It showed me that you don't always need "Black Box AI" to create something useful; sometimes, just thoughtful feature matching is enough. This project changed how I think about apps like Spotify—I now realize how much human judgment goes into deciding which "weights" (like genre vs. tempo) matter most for a user's experience.
