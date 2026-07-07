"""
This is the website part of the app (built with Streamlit). It lets a pet
parent type in their pet's info, runs the AI agents from main.py, then
shows a clean, friendly recommendation -- while tucking all the technical
tool-call logs into a "See agent activity log" dropdown for anyone curious.
"""
import streamlit as st
import asyncio
import io
import sys
import contextlib
import main

st.set_page_config(page_title="BiteWise: Pet Food Advisor")

st.title("BiteWise: Pet Food Advisor")
st.caption("An AI-driven multi-agent system delegating tasks to Scout, Vet, Review, Nutritionist, and Safety agents to find the best food for your pet.")

with st.sidebar:
    # Sidebar: quick explanation + a switch to run the fake offline demo
    st.header("How it works")
    st.write("BiteWise uses multiple AI agents working together to research pet food options, analyze veterinary guidelines, check ingredient quality, read online reviews, and verify safety recalls.")
    dry_run = st.checkbox(
        "Dry-run mode (offline simulation, no API calls)",
        value=not main.SDK_AVAILABLE
    )

prompt = st.text_area("Describe your pet and their dietary needs:")

if st.button("Get Recommendation"):
    if not prompt.strip():
        st.error("Please enter a description of your pet's needs.")
    else:
        # While the agents run, we secretly record everything they print
        # (like a security camera) into `f`, so it can be shown later in
        # the "agent activity log" dropdown. Separately, `report_text` is
        # just the final answer handed back directly -- like getting a
        # clean summary note instead of digging through the security
        # footage to find what happened.
        f = io.StringIO()
        report_text = ""
        with contextlib.redirect_stdout(f):
            try:
                if dry_run:
                    report_text = main.run_dry_run_simulation(prompt)
                else:
                    report_text = asyncio.run(main.run_live_pipeline(prompt))
            except SystemExit as e:
                st.error(f"The pipeline exited early (SystemExit: {e}).")
            except ValueError as e:
                st.error(f"Validation Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

        output = f.getvalue()

        if report_text and report_text.strip():
            st.markdown("### Final Recommendation Report")
            st.markdown(report_text.strip())
        else:
            st.warning("Could not retrieve the final recommendation report from the agent output.")

        with st.expander("See agent activity log"):
            st.text(output)
