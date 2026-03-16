import streamlit as st
from ai_engine import CommsAgent
from database_manager import get_all_logs, save_verdict

# --- UI for Business Standards ---
def main():
    st.set_page_config(page_title="Executive Comms Suite", layout="wide")
    
    # Navigation
    menu = st.sidebar.radio("Navigation", ["Strategy Simulator", "Executive Builder", "SOP Generator"])
    
    comms = CommsAgent()
    
    if menu == "Strategy Simulator":
        st.title("🤖 Strategy Simulator")
        st.markdown("Run a scenario to add it to the database for future Executive Slide Building.")
        
        user_move = st.text_area("Enter Business Scenario:", placeholder="Our competitor just launched a rival product...")
        
        # We need a mode and tone now since CommsAgent expects them
        mode = st.selectbox("Select Preliminary Output Type", ["Email", "Proposal", "Slides", "Executive Summary"])
        tone = st.select_slider("Select Tone", options=["Direct", "Professional", "Persuasive"])
        
        if st.button("Simulate Context"):
            if user_move:
                with st.spinner("Analyzing with Gemini..."):
                    result = comms.generate_comms(data=user_move, mode=mode, tone=tone)
                    
                    # Save to DB so we have data for the builder
                    save_verdict(user_move, result, impact=5, likelihood=5)
                    
                    st.success("Simulation Saved to Database!")
                    st.markdown("### Result:")
                    st.markdown(result)
            else:
                st.warning("Please enter a scenario first!")

    elif menu == "Executive Builder":
        st.title("✉️ Executive Communication & Slide Builder")
        
        # Sidebar Setup
        st.sidebar.header("Communication Settings")
        content_type = st.sidebar.selectbox("Select Output Type", 
            ["Email", "Proposal", "Slides", "Executive Summary"], key="builder_type")
        
        tone = st.sidebar.select_slider("Select Tone", 
            options=["Direct", "Professional", "Persuasive"], key="builder_tone")

        # Fetch data from our SQLite 'Memory'
        history_df = get_all_logs()

        if not history_df.empty:
            # Topic 5: Select existing data for Summary
            st.subheader("1. Select Source Data")
            choice = st.selectbox("Choose a previous analysis to transform:", 
                                history_df['scenario'].unique())
            
            raw_context = history_df[history_df['scenario'] == choice]['verdict'].iloc[0]
            
            st.info(f"Source: {choice}")

            # Topic 1 & 6: Content Generation
            if st.button(f"Generate {content_type}"):
                with st.spinner(f"Drafting {content_type}..."):
                    final_output = comms.generate_comms(raw_context, content_type, tone)
                    
                    st.divider()
                    st.subheader(f"📄 Generated {content_type}")
                    
                    # Render the output
                    if content_type == "Slides":
                        st.markdown("### 🎞️ Slide Blueprint")
                        st.write(final_output)
                    else:
                        st.text_area("Draft (Ready to Copy):", value=final_output, height=400)
                    
                    # Topic 1: Concise Export
                    st.download_button(f"Export {content_type}", final_output, file_name=f"{content_type}.txt")
        else:
            st.warning("No data found in database. Run a 'Strategy Simulation' first!")

    elif menu == "SOP Generator":
        st.subheader("📋 Automated SOP & Manual Builder")
        st.markdown("Turn any complex task into a structured Standard Operating Procedure.")
        
        raw_process = st.text_area("Describe the task (e.g., 'Updating the Gemini API key in the .env file'):", height=150)
        
        if st.button("Generate SOP"):
            if not raw_process:
                st.warning("Please describe a task first.")
            else:
                with st.spinner("Writing technical documentation..."):
                    sop_result = comms.generate_sop(raw_process)
                    st.divider()
                    st.markdown(sop_result)
                    
                    # Export for the company records
                    st.download_button("Download SOP", sop_result, file_name="SOP_Document.txt")

if __name__ == "__main__":
    main()