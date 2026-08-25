import streamlit as st


def render_home():
    st.subheader("What is SemiConnect?")

    st.write(
        """
        SemiConnect is an AI platform focused on the semiconductor ecosystem.

        It brings together semiconductor market intelligence, VLSI learning,
        and business operations support in one place.
        """
    )

    st.markdown("### What SemiConnect offers")

    st.markdown(
        """
        **📊 Market Intelligence**  
        Track semiconductor news, OSAT activity, fab investments, and supply-chain developments.

        **📚 VLSI Tutor**  
        Learn digital electronics and Verilog step by step.

        **💼 Business Operations**  
        Analyze vendors, sourcing decisions, and semiconductor supply-chain risks.

        **🎓 Learning Path**  
        Follow structured learning notes, complete a test, and progress to the next topic.
        """
    )