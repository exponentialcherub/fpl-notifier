import streamlit as st

st.set_page_config(
    page_title="FPL Notifier",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    st.sidebar.title("⚽ FPL Notifier")
    st.sidebar.markdown("---")

    # Navigation
    page = st.sidebar.radio(
        "Navigate to:",
        ["🏠 Home", "🏆 League", "🏅 Cup", "🎰 Bets"],
        index=0,
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Fantasy Premier League Notifier")

    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "🏆 League":
        show_league_page()
    elif page == "🏅 Cup":
        st.switch_page("pages/cup.py")
    elif page == "🎰 Bets":
        show_bets_page()


def show_home_page():
    st.title("🏠 Welcome to FPL Notifier")
    st.markdown("---")

    st.markdown(
        """
        ### Your Fantasy Premier League Hub
        
        Track your mini-league, cup competitions, and bets all in one place.
        """
    )

    # Navigation cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 🏆 League
            View league standings, manager stats, and gameweek performance.
            """
        )
        if st.button("Go to League", key="nav_league", use_container_width=True):
            st.session_state["nav"] = "league"
            st.rerun()

    with col2:
        st.markdown(
            """
            ### 🏅 Cup
            Check cup fixtures, results, and group tables.
            """
        )
        if st.button("Go to Cup", key="nav_cup", use_container_width=True):
            st.switch_page("pages/cup.py")

    with col3:
        st.markdown(
            """
            ### 🎰 Bets
            Track bets and predictions among managers.
            """
        )
        if st.button("Go to Bets", key="nav_bets", use_container_width=True):
            st.session_state["nav"] = "bets"
            st.rerun()


def show_league_page():
    st.title("🏆 League")
    st.markdown("---")
    st.info("League standings and stats coming soon...")


def show_cup_page():
    st.title("🏅 Cup")
    st.markdown("---")
    st.info("Cup fixtures and results coming soon...")


def show_bets_page():
    st.title("🎰 Bets")
    st.markdown("---")
    st.info("Bets tracking coming soon...")


if __name__ == "__main__":
    main()
