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
        # Capture stdout
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                if dry_run:
                    main.run_dry_run_simulation(prompt)
                else:
                    asyncio.run(main.run_live_pipeline(prompt))
            except SystemExit as e:
                st.error(f"The pipeline exited early (SystemExit: {e}).")
            except ValueError as e:
                st.error(f"Validation Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        
        output = f.getvalue()
        
        # Extract the final report
        report_text = ""
        lines = output.splitlines()
        capturing = False
        report_lines = []
        for line in lines:
            if "Recommendation Report" in line:
                capturing = True
                continue
            if capturing and line.startswith("---"):
                capturing = False
                continue
            if capturing:
                report_lines.append(line)
                
        if report_lines:
            report_text = "\n".join(report_lines)
            st.markdown("### Final Recommendation Report")
            st.markdown(report_text)
        else:
            st.warning("Could not parse the final recommendation report from the agent output.")
            
        with st.expander("See agent activity log"):
            st.text(output)
