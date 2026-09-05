import streamlit as st


def render_home():
    """Render the SemiConnect AI landing page."""

    with st.container(key="home_hero"):
        st.markdown("**SEMICONDUCTOR INTELLIGENCE**")

        st.title("SemiConnect AI")

        st.subheader("Understand. Learn. Decide.")

        st.write(
            "AI-powered intelligence for the semiconductor industry — "
            "from market research and VLSI learning to business analysis "
            "and structured skill development."
        )

    st.markdown("")

    with st.container(key="home_capabilities"):
        st.markdown("### Explore SemiConnect")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(key="capability_market"):
                st.markdown("**01 — Market Intelligence**")
                st.write(
                    "Track semiconductor news, fab investments, OSAT activity, "
                    "supply-chain shifts, and industry developments."
                )

            with st.container(key="capability_business"):
                st.markdown("**03 — Business Ops**")
                st.write(
                    "Analyze datasets, vendors, sourcing decisions, operational "
                    "risks, and semiconductor business questions."
                )

        with col2:
            with st.container(key="capability_vlsi"):
                st.markdown("**02 — VLSI Tutor**")
                st.write(
                    "Learn digital electronics, Verilog, RTL concepts, verification, "
                    "and semiconductor fundamentals step by step."
                )

            with st.container(key="capability_learning"):
                st.markdown("**04 — Learning Path**")
                st.write(
                    "Follow a structured semiconductor learning journey, practice "
                    "concepts, and build knowledge progressively."
                )

    st.markdown("")

    with st.container(key="home_footer"):
        st.caption(
            "Built for semiconductor professionals, engineers, students, and industry teams."
        )
