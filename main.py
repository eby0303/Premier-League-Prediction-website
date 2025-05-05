import streamlit as st
import pandas as pd
import altair as alt
from live_standings import scrape_live_standings
from prediction import make_prediction
from scrape_data import scrape_multiple_seasons_data

# Define the main Streamlit application
def app():
    st.set_page_config(page_title="Premier League Insights", layout="wide")

    # Header
    st.title("⚽ Premier League Live Standings & Match Outcome Prediction")
    st.markdown("Get real-time standings and predict the future champion using machine learning!")

    # Columns for layout
    col1, col2 = st.columns([3, 2])

    with col1:
        live_standings = scrape_live_standings()

        if live_standings is not None:
            st.subheader("📊 Live Premier League Standings")
            st.dataframe(live_standings.style.highlight_max(axis=0, color='lightgreen'))

            # Bar chart for visualizing Points by Team (if column exists)
            if 'Pts' in live_standings.columns:
                chart_data = live_standings[['Squad', 'Pts']].sort_values('Pts', ascending=False)
                bar_chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X('Pts:Q', title='Points'),
                    y=alt.Y('Squad:N', sort='-x', title='Team'),
                    color=alt.Color('Pts:Q', scale=alt.Scale(scheme='greens'))
                ).properties(
                    height=500,
                    width=600,
                    title="Team Points Visualization"
                )
                st.altair_chart(bar_chart, use_container_width=True)
            
                        # Extra visualizations using live standings
            with st.expander("📊 Explore More Live Stats"):

                # Scatter plot: Goals For vs Goals Against
                if {'GF', 'GA', 'Squad'}.issubset(live_standings.columns):
                    st.markdown("### ⚔️ Goals Scored vs Goals Conceded")
                    scatter_data = live_standings[['Squad', 'GF', 'GA']]

                    scatter = alt.Chart(scatter_data).mark_circle(size=100).encode(
                        x=alt.X('GF:Q', title='Goals For'),
                        y=alt.Y('GA:Q', title='Goals Against'),
                        color=alt.Color('Squad:N', legend=None),
                        tooltip=['Squad', 'GF', 'GA']
                    ).properties(
                        width=600,
                        height=400
                    ).interactive()

                    st.altair_chart(scatter, use_container_width=True)

                # Stacked bar chart: Wins / Draws / Losses
                if {'W', 'D', 'L', 'Squad'}.issubset(live_standings.columns):
                    st.markdown("### 📦 Win / Draw / Loss Breakdown")
                    stack_df = live_standings[['Squad', 'W', 'D', 'L']].melt(id_vars='Squad', var_name='Result', value_name='Count')

                    stacked_chart = alt.Chart(stack_df).mark_bar().encode(
                        x=alt.X('Count:Q', title='Number of Matches'),
                        y=alt.Y('Squad:N', sort='-x'),
                        color=alt.Color('Result:N', scale=alt.Scale(scheme='set1')),
                        tooltip=['Squad', 'Result', 'Count']
                    ).properties(
                        width=700,
                        height=500
                    )

                    st.altair_chart(stacked_chart, use_container_width=True)

                # Individual Team Breakdown
                st.markdown("### 🔍 View Match Outcome Breakdown for a Team")

                team_options = live_standings['Squad'].dropna().unique().tolist()
                selected_team = st.selectbox("Choose a team:", team_options)

                if selected_team:
                    if {'W', 'D', 'L'}.issubset(live_standings.columns):
                        team_row = live_standings[live_standings['Squad'] == selected_team]
                        if not team_row.empty:
                            w = int(team_row['W'])
                            d = int(team_row['D'])
                            l = int(team_row['L'])
                            outcome_df = pd.DataFrame({
                                'Result': ['Wins', 'Draws', 'Losses'],
                                'Count': [w, d, l]
                            })

                            pie_chart = alt.Chart(outcome_df).mark_arc(innerRadius=50).encode(
                                theta=alt.Theta(field="Count", type="quantitative"),
                                color=alt.Color(field="Result", type="nominal"),
                                tooltip=["Result", "Count"]
                            ).properties(
                                width=400,
                                height=400,
                                title=f"{selected_team} - Match Outcome Distribution"
                            )

                            st.altair_chart(pie_chart, use_container_width=False)    
        else:
            st.warning("⚠️ Unable to load live standings. Please try again later.")

    with col2:
        st.subheader("🔮 Season Winner Prediction")
        season_year = st.number_input("Enter season year (e.g., 2023):", min_value=2020, max_value=2028, step=1, value=2024)

        if st.button("Make Prediction"):
            with st.spinner("Scraping data and predicting winner..."):
                seasons_to_scrape = [season_year - 1, season_year - 2]
                csv_file_path = scrape_multiple_seasons_data(seasons_to_scrape)
                winner, precision, win_probabilities = make_prediction(csv_file_path, return_details=True)

            st.success(f"🏆 The predicted winner of the {season_year}-{season_year + 1} season is: **{winner}**")

            # Bar chart of win probabilities
            st.subheader("📈 Predicted Win Probability by Team")
            prob_df = pd.DataFrame(win_probabilities.items(), columns=['Team', 'Win Probability'])
            prob_df = prob_df.sort_values('Win Probability', ascending=False)

            prob_chart = alt.Chart(prob_df).mark_bar().encode(
                x=alt.X('Win Probability:Q', title='Predicted Win Probability'),
                y=alt.Y('Team:N', sort='-x'),
                color=alt.Color('Win Probability:Q', scale=alt.Scale(scheme='blues'))
            ).properties(
                width=600,
                height=500
            )
            st.altair_chart(prob_chart, use_container_width=True)

if __name__ == "__main__":
    app()
