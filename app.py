import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Game Stats Analyzer")

@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df.dropna(subset=['name'], inplace=True)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{filepath}' was not found.")
        st.error("Please make sure 'game_addictiveness.csv' is in the same directory as this app.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

st.title("🎮 Game Addictiveness & Stats Analyzer")
st.info("Select a game from the dropdown menu below to see its detailed statistics, charts, and addictiveness rating.")

df = load_data("data/game_addictiveness.csv")

if not df.empty:
    game_names = sorted(df['name'].unique())
    selected_game = st.selectbox(
        "Select a Game:",
        options=game_names
    )

    if selected_game:
        game_data = df[df['name'] == selected_game].iloc[0]

        st.header(f"Analysis for: {game_data['name']}")

        addictiveness_status = "Addictive" if game_data['is_addictive'] == 1 else "Not Addictive"
        emoji = "🔥" if game_data['is_addictive'] == 1 else "👍"

        if addictiveness_status == "Addictive":
            st.warning(f"**Addictiveness Rating: {addictiveness_status} {emoji}**")
            st.markdown("This game is flagged as potentially addictive based on the available data.")
        else:
            st.success(f"**Addictiveness Rating: {addictiveness_status} {emoji}**")
            st.markdown("This game is not flagged as potentially addictive based on the available data.")

        st.subheader("Key Information")
        col1, col2, col3 = st.columns(3)
        col1.metric("Release Date", str(game_data['release_date']))
        col2.metric("Price", f"${game_data['price']:.2f}")
        col3.metric("Developer", game_data['developer'])

        st.markdown(f"**Publisher:** {game_data['publisher']}")
        st.markdown(f"**Genres:** {game_data['genres']}")
        st.markdown(f"**Platforms:** {game_data['platforms']}")

        st.subheader("Game Statistics")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            ratings_df = pd.DataFrame({
                'Rating Type': ['Positive Ratings', 'Negative Ratings'],
                'Count': [game_data['positive_ratings'], game_data['negative_ratings']]
            })

            ratings_chart = alt.Chart(ratings_df).mark_bar(cornerRadius=5, size=50).encode(
                x=alt.X('Rating Type', title=None),
                y=alt.Y('Count', title="Total Ratings"),
                color=alt.Color('Rating Type',
                                scale={'domain': ['Positive Ratings', 'Negative Ratings'],
                                       'range': ['#2E8B57', '#DC143C']},
                                legend=None),
                tooltip=['Rating Type', 'Count']
            ).properties(
                title="Positive vs. Negative Ratings"
            )
            st.altair_chart(ratings_chart, use_container_width=True)

        with chart_col2:
            playtime_df = pd.DataFrame({
                'Playtime Type': ['Average Playtime (min)', 'Median Playtime (min)'],
                'Minutes': [game_data['average_playtime'], game_data['median_playtime']]
            })

            playtime_chart = alt.Chart(playtime_df).mark_bar(cornerRadius=5, size=50).encode(
                x=alt.X('Playtime Type', title=None),
                y=alt.Y('Minutes', title="Playtime in Minutes"),
                color=alt.Color('Playtime Type',
                                scale={'domain': ['Average Playtime (min)', 'Median Playtime (min)'],
                                       'range': ['#1E90FF', '#FF8C00']},
                                legend=None),
                tooltip=['Playtime Type', 'Minutes']
            ).properties(
                title="Average vs. Median Playtime"
            )
            st.altair_chart(playtime_chart, use_container_width=True)

        st.subheader("Playtime Comparison")

        avg_playtime_all = df['average_playtime'].mean()
        avg_playtime_game = game_data['average_playtime']

        comparison_df = pd.DataFrame({
            'Category': ['All Games (Average)', game_data['name']],
            'Average Playtime (min)': [avg_playtime_all, avg_playtime_game]
        })

        comparison_chart = alt.Chart(comparison_df).mark_bar(cornerRadius=5).encode(
            x=alt.X('Category', title=None),
            y=alt.Y('Average Playtime (min)', title='Average Playtime (min)'),
            color=alt.Color('Category', legend=None),
            tooltip=['Category', 'Average Playtime (min)']
        ).properties(
            title=f"'{game_data['name']}' vs. All Games Average Playtime"
        )

        st.altair_chart(comparison_chart, use_container_width=True)

        with st.expander("Show Raw Data for " + game_data['name']):
            st.dataframe(game_data)

elif df.empty:
    st.error("Could not load game data. The app cannot continue. Please check the file path and data.")
