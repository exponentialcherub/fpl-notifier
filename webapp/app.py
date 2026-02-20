import streamlit as st

st.set_page_config(
    page_title="FPL Notifier",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    st.sidebar.title("⚽ FC Bathelona FPL Draft")
    st.sidebar.markdown("---")

    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🏆 League", "🏅 Cup", "🎰 Bets"],
        index=0,
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("FC Bathelona - FPL Draft")

    # Page routing
    # Check session state for navigation
    if "page" in st.session_state:
        page = st.session_state.page
        del st.session_state.page  # Clear after use
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "🏆 League":
        show_league_page()
    elif page == "🏅 Cup":
        st.switch_page("pages/cup.py")
    elif page == "🎰 Bets":
        show_bets_page()


def show_home_page():
    st.title("🏠 Welcome to FC Bathelona FPL Draft")
    st.markdown("---")
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            ### 🏆 League
            View league standings and stats.
            """
        )
        if st.button("League", use_container_width=True, key="league_btn"):
            st.switch_page("pages/league.py")

    with col2:
        st.markdown(
            """
            ### 🏅 Cup
            Check cup fixtures, results, and group tables.
            """
        )
        if st.button("Cup", use_container_width=True, key="cup_btn"):
            st.switch_page("pages/cup.py")

    with col1:
        st.markdown(
            """
            ### 🎰 Bets
            Track bets and predictions among managers.
            """
        )
        if st.button("Bets", use_container_width=True, key="bets_btn"):
            st.switch_page("pages/bets.py")
    
    with col2:
        st.markdown(
            """
            ###  📊 History
            Historic records of FPL draft league.
            """
        )
        if st.button("History", use_container_width=True, key="history_btn"):
            st.switch_page("pages/history.py")

def show_league_page():
    st.title("🏆 League")
    st.markdown("---")
    st.info("League standings and stats coming soon...")


def show_bets_page():
    st.title("🎰 Bets")
    st.markdown("---")
    st.info("Bets tracking coming soon...")


if __name__ == "__main__":
    main()
