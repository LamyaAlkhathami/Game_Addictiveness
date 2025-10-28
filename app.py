import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ✅ Page Setup
st.set_page_config(layout="wide", page_title="Game Stats Analyzer")

# 🎨 Enhanced UI Styling
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background-image: url("https://cdna.artstation.com/p/assets/images/images/041/648/690/large/luke-viljoen-okd2-moon-festival-keyart-07d.jpg");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.85);
        z-index: 0;
    }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        color: #F2F2F2 !important;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    h1 {
        color: #FFFFFF !important;
        text-align: center !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px rgba(255,255,255,0.8);
    }

    h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 600;
        font-size: 1.5rem !important;
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }




    [data-baseweb="option"] {
        background-color: #1E1E2F !important;
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }

    [data-baseweb="option"]:hover {
        background-color: #2D2950 !important;
        color: #FFFFFF !important;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1E1E2F 0%, #2D2950 100%);
        border-radius: 12px;
        padding: 25px;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        border: 2px solid rgba(155,93,229,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(155,93,229,0.4);
    }

    .metric-label {
        color: #C9C9C9;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 1.6rem;
        font-weight: 700;
    }

    /* Info Card */
    .info-card {
        background: linear-gradient(135deg, #1E1E2F 0%, #2D2950 100%);
        border-radius: 12px;
        padding: 25px;
        margin-top: 15px;
        line-height: 2;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        border: 2px solid rgba(155,93,229,0.3);
        font-size: 1.1rem;
        color: #FFFFFF !important;
    }

    /* Alert Boxes */
    .stAlert {
        background-color: #1E1E2F !important;
        color: white !important;
        border-radius: 10px !important;
        border: 2px solid rgba(155,93,229,0.3) !important;
    }

    .stAlert p strong {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }

    .stAlert p {
        color: #FFFFFF !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        text-align: center !important;
    }

    /* Recommendation Card */
    .recommend-card {
        background: linear-gradient(135deg, #1E1E2F 0%, #2D2950 100%);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        border: 2px solid rgba(155,93,229,0.4);
    }

    .recommend-card h3 {
        color: #FFFFFF !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.2rem;
        text-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }

    .recommend-card p {
        color: #E0E0E0 !important;
        font-size: 1.1rem !important;
        margin-bottom: 1.5rem;
        line-height: 1.8;
    }

    /* Game Recommendation Item */
    .game-recommendation {
        background-color: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #9b5de5;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .game-recommendation:hover {
        background-color: rgba(155,93,229,0.15);
        transform: translateX(8px);
        box-shadow: 0 6px 20px rgba(155,93,229,0.4);
    }

    .game-rec-title {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin-bottom: 8px;
    }

    .game-rec-details {
        font-size: 1rem !important;
        color: #C9C9C9 !important;
        margin: 5px 0;
    }

    .game-rec-score {
        display: inline-block;
        background: linear-gradient(135deg, #9b5de5 0%, #f15bb5 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 8px;
        box-shadow: 0 4px 10px rgba(155,93,229,0.4);
    }

    /* Image Styling */
    .game-image-main {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        border: 3px solid rgba(155,93,229,0.5);
    }

    .game-image-rec {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(0,0,0,0.6);
        border: 2px solid rgba(155,93,229,0.4);
        transition: all 0.3s ease;
    }

    .game-image-rec:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(155,93,229,0.6);
    }

    /* Image Container */
    img {
        border-radius: 12px;
    }

    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(155,93,229,0.5), transparent);
        margin: 2rem 0;
    }
    /* Force white text color for both Select label and Expander title */
    .stSelectbox label, .streamlit-expanderHeader p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

/* Optional: make the arrow icon also white */
.streamlit-expanderHeader svg {
    fill: #FFFFFF !important;
}

    </style>
""", unsafe_allow_html=True)

# 🧠 Load Data
@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df.dropna(subset=['name'], inplace=True)

        # Add image URL automatically
        if 'appid' in df.columns:
            df['image_url'] = df['appid'].apply(
                lambda x: f"https://cdn.cloudflare.steamstatic.com/steam/apps/{int(x)}/header.jpg"
                if pd.notna(x) else None
            )

        return df
    except FileNotFoundError:
        st.error(f"❌ File '{filepath}' not found. Please check the path.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        st.stop()

# 🎯 Smart Recommendation System
def get_smart_recommendations(df, current_game_data, num_recommendations=5):
    try:
        # Extract main genres
        genres = str(current_game_data['genres']).split(";")
        main_genres = [g.strip().lower() for g in genres[:3]]

        current_price = float(current_game_data['price']) if pd.notna(current_game_data['price']) else 0
        is_free = current_price == 0
        current_playtime = float(current_game_data['average_playtime']) if pd.notna(current_game_data['average_playtime']) else 0

        # Filter games - only non-addictive games
        recommendations = df[
            (df['is_addictive'].astype(int) == 0) &
            (df['name'] != current_game_data['name'])
        ].copy()

        # Calculate match score with improved logic
        def calculate_match_score(row):
            score = 0

            # Genre match (40 points) - Highest priority for similar experience
            row_genres = str(row['genres']).lower()
            genre_matches = sum(1 for genre in main_genres if genre in row_genres)
            if genre_matches == len(main_genres):
                score += 40  # Perfect match
            elif genre_matches >= 2:
                score += 30  # Good match
            elif genre_matches == 1:
                score += 20  # Partial match

            # Price match (30 points) - Critical for user budget
            try:
                rec_price = float(row['price']) if pd.notna(row['price']) else 0

                if is_free:
                    # If current game is free, strongly prefer free alternatives
                    if rec_price == 0:
                        score += 30
                    elif rec_price <= 5:
                        score += 10
                    elif rec_price <= 10:
                        score += 5
                else:
                    # For paid games, match similar price ranges
                    if rec_price == 0:
                        score += 20  # Free is always good
                    else:
                        price_diff = abs(current_price - rec_price)
                        if price_diff < 5:
                            score += 30
                        elif price_diff < 10:
                            score += 25
                        elif price_diff < 15:
                            score += 20
                        elif price_diff < 25:
                            score += 15
                        else:
                            score += 5
            except:
                pass

            # Rating quality (20 points) - Ensure quality recommendations
            try:
                positive = float(row['positive_ratings'])
                negative = float(row['negative_ratings'])
                total = positive + negative

                if total > 100:  # Only consider games with substantial reviews
                    positive_ratio = positive / (total + 1)
                    if positive_ratio >= 0.85:
                        score += 20
                    elif positive_ratio >= 0.75:
                        score += 15
                    elif positive_ratio >= 0.65:
                        score += 10
                    else:
                        score += 5
            except:
                pass

            # Playtime balance (10 points) - Avoid addiction patterns
            try:
                playtime = float(row['average_playtime'])
                playtime_diff = abs(current_playtime - playtime)

                # Sweet spot: moderate playtime (not too short, not too long)
                if 100 < playtime < 500:
                    score += 10
                    # Bonus for similar engagement level
                    if playtime_diff < 150:
                        score += 5
                elif 50 < playtime <= 100:
                    score += 8
                elif playtime <= 50:
                    score += 5
                else:  # Very high playtime might indicate addictive patterns
                    score += 2
            except:
                pass

            return score

        recommendations['match_score'] = recommendations.apply(calculate_match_score, axis=1)

        # Filter out low-quality games
        recommendations = recommendations[
            (recommendations['positive_ratings'].astype(float) >= 100)
        ]

        # Get top recommendations
        top_recommendations = recommendations.nlargest(num_recommendations, 'match_score')

        # If not enough recommendations, relax filters
        if len(top_recommendations) < 3:
            recommendations = df[
                (df['is_addictive'].astype(int) == 0) &
                (df['name'] != current_game_data['name']) &
                (df['positive_ratings'].astype(float) >= 50)
            ].copy()
            recommendations['match_score'] = recommendations.apply(calculate_match_score, axis=1)
            top_recommendations = recommendations.nlargest(num_recommendations, 'match_score')

        return top_recommendations

    except Exception as e:
        st.warning(f"Error generating recommendations: {e}")
        return pd.DataFrame()

# 🏷️ Title
st.title("🎮 Game Addictiveness Prediction")

df = load_data("data/game_addictiveness.csv")

# Verify required columns
required_cols = ['name', 'is_addictive', 'genres', 'average_playtime']
if not all(col in df.columns for col in required_cols):
    st.error("⚠️ Missing required columns in dataset.")
    st.stop()

if not df.empty:
    game_names = sorted(df['name'].unique())
    selected_game = st.selectbox("Select a Game:", options=game_names)

    st.markdown("<br><br>", unsafe_allow_html=True)

    if selected_game:
        game_data = df[df['name'] == selected_game].iloc[0]

        st.markdown("<br>", unsafe_allow_html=True)

        # 🎮 TOP SECTION: Image on Left + Analysis on Right
        col_image, col_info = st.columns([2, 3])

        with col_image:
            if 'appid' in game_data and pd.notna(game_data['appid']):
                try:
                    app_id = int(game_data['appid'])
                    image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg"
                    st.markdown('<div class="game-image-main" style="max-width: 320px; margin: 0 auto;">', unsafe_allow_html=True)
                    st.image(image_url, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"⚠️ Could not load image: {e}")
            else:
                st.info("🖼️ No App ID found for this game.")

        with col_info:
            st.header(f"{game_data['name']}")

            # ✅ Addictiveness Classification
            try:
                is_addictive = int(float(game_data['is_addictive']))
            except (ValueError, TypeError):
                is_addictive = 0

            status = "Addictive" if is_addictive == 1 else "Not Addictive"
            emoji = "🔥" if is_addictive == 1 else "👍"

            if is_addictive == 1:
                st.warning(f"*Addictiveness Rating: {status} {emoji}*")
            else:
                st.success(f"*Addictiveness Rating: {status} {emoji}*")
                st.info("✨ Seems like a well-balanced title! You're safe from the addictive zone 🧘")

        st.markdown("---")

        # 📋 KEY INFORMATION - 3 Columns

        st.subheader("🔑 Key Information")

        # Custom styled metric cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>📅 Release Date</div>
                <div class='metric-value'>{str(game_data['release_date'])}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>💰 Price</div>
                <div class='metric-value'>${game_data['price']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>👨‍💻 Developer</div>
                <div class='metric-value'>{game_data['developer'][:25] + '...' if len(str(game_data['developer'])) > 25 else game_data['developer']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Additional info in styled cards
        st.markdown(f"""
        <div class='info-card'>
            <strong>🏢 Publisher:</strong> {game_data['publisher']}<br>
            <strong>🎮 Genres:</strong> {game_data['genres']}<br>
            <strong>💻 Platforms:</strong> {game_data['platforms']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        # 📊 GAME STATISTICS - 3 Charts in Row
        st.subheader("📊 Game Statistics")
        chart1, chart2, chart3 = st.columns(3)

        # Chart 1: Price Bar Chart
        with chart1:
            fig1, ax1 = plt.subplots(figsize=(4, 4), facecolor="#1E1E2F")
            try:
                game_price = float(game_data['price'])
                avg_price = df['price'].astype(float).mean()

                categories = ['This Game', 'Average']
                prices = [game_price, avg_price]

                ax1.bar(categories, prices, color=["#9b5de5", "#f15bb5"], alpha=0.9, width=0.5)
                ax1.set_title("Price Comparison", color='white', fontsize=12, fontweight='bold', pad=10)
                ax1.set_ylabel("Price ($)", color='white', fontsize=10)

                for i, v in enumerate(prices):
                    ax1.text(i, v + (v*0.02), f"${v:.2f}", ha='center', color='white', fontsize=9, fontweight='bold')

                for spine in ax1.spines.values():
                    spine.set_visible(False)
                ax1.set_facecolor('#1E1E2F')
                ax1.tick_params(colors='white', labelsize=9)
                st.pyplot(fig1)
            except:
                st.info("Price data unavailable")

        # Chart 2: Positive Rating Pie Chart
        with chart2:
            fig2, ax2 = plt.subplots(figsize=(4, 4), facecolor="#1E1E2F")
            try:
                positive = int(game_data['positive_ratings'])
                negative = int(game_data['negative_ratings'])
                total = positive + negative

                if total > 0:
                    positive_pct = (positive / total) * 100
                    negative_pct = (negative / total) * 100

                    sizes = [positive_pct, negative_pct]
                    labels = ['Positive', 'Negative']
                    colors = ['#9b5de5', '#f15bb5']

                    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                           colors=colors, textprops={'color': 'white', 'fontsize': 10, 'fontweight': 'bold'})
                    ax2.set_title("Rating Distribution", color='white', fontsize=12, fontweight='bold', pad=10)
                    st.pyplot(fig2)
                else:
                    st.info("No ratings available")
            except:
                st.info("Rating data unavailable")

        # Chart 3: Playtime Comparison
        with chart3:
            fig3, ax3 = plt.subplots(figsize=(4, 4), facecolor="#1E1E2F")
            avg_all = df['average_playtime'].astype(float).mean()
            avg_game = float(game_data['average_playtime'])
            categories = ['All Games', 'This Game']
            ax3.bar(categories, [avg_all, avg_game], color=["#9b5de5", "#f15bb5"], alpha=0.9, width=0.5)
            ax3.set_title("Playtime Comparison", color='white', fontsize=12, fontweight='bold', pad=10)
            ax3.set_ylabel("Time", color='white', fontsize=10)
            for i, v in enumerate([avg_all, avg_game]):
                ax3.text(i, v + (v*0.02), f"{v:.0f}", ha='center', color='white', fontsize=9, fontweight='bold')
            for spine in ax3.spines.values():
                spine.set_visible(False)
            ax3.set_facecolor('#1E1E2F')
            ax3.tick_params(colors='white', labelsize=9)
            st.pyplot(fig3)

        st.markdown("---")


        # 🎯 SMART RECOMMENDATIONS - Last Section
        if is_addictive == 1:
            smart_recommendations = get_smart_recommendations(df, game_data, num_recommendations=5)

            if len(smart_recommendations) > 0:
                st.markdown("""
                <div class='recommend-card'>
                    <h3>🎯 Recommended Healthier Alternatives</h3>
                    <p>These games match your preferences while promoting balanced gameplay:</p>
                </div>
                """, unsafe_allow_html=True)

                for idx, game in smart_recommendations.iterrows():
                    try:
                        positive_ratio = (float(game['positive_ratings']) /
                                        (float(game['positive_ratings']) + float(game['negative_ratings']) + 1) * 100)
                        price_str = f"${float(game['price']):.2f}" if pd.notna(game['price']) else "Free"
                        match_score = int(game['match_score'])

                        col1, col2 = st.columns([2, 3])

                        with col1:
                            if 'appid' in game and pd.notna(game['appid']):
                                rec_app_id = int(game['appid'])
                                rec_image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{rec_app_id}/header.jpg"
                                st.markdown('<div class="game-image-rec">', unsafe_allow_html=True)
                                st.image(rec_image_url, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                            else:
                                st.info("No image available")

                        with col2:
                            st.markdown(f"""
                            <div class='game-recommendation'>
                                <div class='game-rec-title'>🎮 {game['name']}</div>
                                <div class='game-rec-details'>📂 Genre: {game['genres'].split(';')[0]}</div>
                                <div class='game-rec-details'>💰 Price: {price_str} | ⭐ Positive: {positive_ratio:.0f}%</div>
                                <div class='game-rec-details'>⏱️ Avg Playtime: {int(float(game['average_playtime']))} minutes</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("---")

                    except Exception as e:
                        continue
            else:
                st.info("🔎 No suitable recommendations found. Try exploring different genres!")


st.markdown("<br><br>", unsafe_allow_html=True)

# 📂 COMPLETE DATASET SECTION (Dark Expander Style)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color: white; text-align: left;'>📂 Complete Dataset</h3>", unsafe_allow_html=True)

with st.expander("🔽 View complete dataset for this game", expanded=False):
    st.markdown("""
        <style>
        /* Force expander label text color */
        div[data-testid="stExpander"] div[role="button"] p,
        div[data-testid="stExpander"] div[role="button"] span,
        div[data-testid="stExpander"] div[role="button"] {
            color: white !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }

        /* Remove dataframe background */
        div[data-testid="stDataFrame"] {
            background-color: transparent !important;
        }

        /* Remove default expander background */
        div[data-testid="stExpander"] {
            background-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.dataframe(
        game_data.to_frame().T,
        use_container_width=True
    )
