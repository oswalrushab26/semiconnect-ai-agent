import streamlit as st


MODES = [
    "Market Intelligence",
    "VLSI Tutor",
    "Business Ops",
    "Learning Path",
]


MODE_DATA = {
    "Market Intelligence": {
        "eyebrow": "RESEARCH",
        "title": "Understand what is happening in semiconductors.",
        "description": (
            "Track semiconductor news, fab investments, OSAT activity, "
            "supply-chain shifts, and industry developments."
        ),
        "examples": "OSATs → fabs → equipment → supply chain → market signals",
    },
    "VLSI Tutor": {
        "eyebrow": "LEARN",
        "title": "Build semiconductor knowledge step by step.",
        "description": (
            "Learn digital electronics, Verilog, RTL concepts, verification, "
            "and semiconductor fundamentals through guided explanations."
        ),
        "examples": "Verilog → RTL → digital logic → verification → VLSI fundamentals",
    },
    "Business Ops": {
        "eyebrow": "ANALYZE",
        "title": "Turn semiconductor data into better decisions.",
        "description": (
            "Analyze datasets, vendors, sourcing decisions, operational "
            "risks, and semiconductor business questions."
        ),
        "examples": "Vendors → sourcing → datasets → operations → risk",
    },
    "Learning Path": {
        "eyebrow": "GROW",
        "title": "Follow a structured path from fundamentals to semiconductor expertise.",
        "description": (
            "Practice concepts, build knowledge progressively, and follow "
            "a guided semiconductor learning journey."
        ),
        "examples": "Fundamentals → practice → progression → skills → VLSI",
    },
}


def render_home():
    """Render the SemiConnect AI product launcher."""

    with st.container(key="home_hero"):
        st.markdown("**SEMICONDUCTOR INTELLIGENCE**")
        st.title("SemiConnect AI")
        st.subheader("Understand. Learn. Decide.")
        st.write(
            "AI-powered intelligence for the semiconductor industry — "
            "bringing market research, VLSI learning, business analysis, "
            "and structured skill development into one workspace."
        )

    st.markdown("")

    with st.container(key="home_capabilities"):
        st.markdown("### Explore SemiConnect")
        st.caption(
            "Choose what you want to accomplish and open the workspace "
            "built for that task."
        )
        st.markdown("")

        with st.container(key="home_value_strip"):
            value1, value2, value3, value4 = st.columns(4, gap="medium")

            with value1:
                st.markdown("**RESEARCH**")
                st.caption("Industry intelligence")

            with value2:
                st.markdown("**LEARN**")
                st.caption("VLSI & semiconductor")

            with value3:
                st.markdown("**ANALYZE**")
                st.caption("Business decisions")

            with value4:
                st.markdown("**GROW**")
                st.caption("Structured learning")

        st.markdown("")

        with st.container(key="home_explorer"):
            st.markdown("### What do you want to do?")

            selected = st.radio(
                "Choose a capability",
                MODES,
                horizontal=True,
                label_visibility="collapsed",
                key="home_mode_selector",
            )

            st.session_state.home_selected_mode = selected

            data = MODE_DATA[selected]

            with st.container(key="home_mode_preview"):
                st.markdown(f"**{data['eyebrow']}**")
                st.markdown(f"#### {data['title']}")
                st.write(data["description"])
                st.caption(f"Explore: {data['examples']}")

            with st.container(key="home_cta"):
                if st.button(
                    "Start Exploring",
                    type="primary",
                    use_container_width=False
                ):
                    st.session_state.show_main_app = True
                    st.rerun()

        st.markdown("")

    st.markdown("")

    with st.container(key="home_footer"):
        st.caption(
            "Built for semiconductor professionals, engineers, students, and industry teams."
        )
