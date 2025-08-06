import streamlit as st
import pickle
import pandas as pd

# Load data
df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation logic
def recommend(movie_title):
    movie_title = movie_title.lower()
    if movie_title not in df['title'].str.lower().values:
        return None, []
    
    index = df[df['title'].str.lower() == movie_title].index[0]
    distances = list(enumerate(similarity[index]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    recommended_titles = [df.iloc[i[0]].title for i in sorted_movies]
    return df.iloc[index].title, recommended_titles

# Page setup
st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        /* Background */
        body {
            background: linear-gradient(to right, #1f1c2c, #928dab);
        }

        .stApp {
            background-image: url("https://images.unsplash.com/photo-1497032628192-86f99bcd76bc");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }

        /* Fonts and cards */
        h1 {
            font-family: 'Segoe UI', sans-serif;
            color: #fff;
            animation: fadeIn 2s ease-in-out;
        }

        .recommendation {
            background-color: rgba(0, 0, 0, 0.6);
            color: #fff;
            padding: 1rem;
            border-radius: 1rem;
            margin-top: 1rem;
            animation: fadeIn 1.5s ease-in-out;
        }

        /* Animation */
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }

        /* Input and buttons */
        .stTextInput > div > input {
            background-color: #222;
            color: white;
            border-radius: 10px;
        }
        .stButton > button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- App UI ---
st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("#### Find movies similar to your favorite! 🍿")

movie_input = st.text_input("🔍 Enter a movie title", placeholder="e.g. The Notebook")

if st.button("Get Recommendations"):
    if movie_input.strip() == "":
        st.warning("⚠️ Please enter a movie title.")
    else:
        title, recommendations = recommend(movie_input)
        if recommendations:
            st.markdown(f"<div class='recommendation'><h4>🎬 Recommendations for <u>{title}</u>:</h4>", unsafe_allow_html=True)
            for rec in recommendations:
                st.markdown(f"✅ {rec}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ Movie not found. Try another title.")

# Footer
st.markdown("""
    <hr style='border-top: 1px solid white;'>
    <p style='text-align: center; color: white;'>Built with ❤️ using Streamlit</p>
""", unsafe_allow_html=True)
