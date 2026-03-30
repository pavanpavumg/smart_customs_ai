import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from ai_engine import CommsAgent
from database_manager import get_all_logs, save_verdict
from dotenv import load_dotenv

# Ensure the new API key is loaded from the .env file
load_dotenv(override=True)

def render_mermaid(code):
    """Simple wrapper to render Mermaid diagrams in Streamlit."""
    # Cleaning the code of triple backticks if the AI includes them
    clean_code = code.replace("```mermaid", "").replace("```", "").strip()
    
    html_code = f"""
    <div class="mermaid">
        {clean_code}
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    """
    components.html(html_code, height=600, scrolling=True)

# --- UI for Business Standards ---
def main():
    st.set_page_config(page_title="Executive Comms Suite", layout="wide")
    
    # Navigation
    menu = st.sidebar.radio("Navigation", ["Strategy Simulator", "Executive Builder", "SOP Generator", "Ideation Lab", "Strategy & Policy", "Learning Center", "Adaptive Classroom", "Ethics & Risk", "Data Center"])
    
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

    elif menu == "Ideation Lab":
        st.header("🧪 Strategic Ideation Lab")
        st.markdown("Use structured frameworks to generate diverse variations and break creative blocks.")
        
        concept = st.text_input("What is the core idea or problem?", placeholder="e.g., A subscription-based fitness app for busy developers")
        
        framework = st.selectbox("Select Innovation Lens", ["SCAMPER", "Blue Ocean Strategy", "Reverse Thinking", "First Principles"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Spark Innovation"):
                if concept:
                    with st.spinner("Breaking creative blocks..."):
                        ideas = comms.generate_innovation(concept, framework)
                        st.divider()
                        st.markdown(ideas)
                        
                        # Topic 1: Concise Export
                        st.download_button("Export Innovation Strategy", ideas, file_name="innovation_strategy.txt")
                else:
                    st.warning("Please enter a concept to begin brainstorming.")
        
        with col2:
            if st.button("Generate Visual Mind Map"):
                if concept:
                    with st.spinner("Mapping out the brainstorm..."):
                        mermaid_code = comms.generate_mindmap_code(concept)
                        st.subheader("🗺️ Strategic Mind Map")
                        render_mermaid(mermaid_code)
                else:
                    st.warning("Please enter a concept first!")

    elif menu == "Strategy & Policy":
        st.header("🏛️ Executive Strategy & Execution")
        
        # Fetch data from previous Ideation or Simulation
        history_df = get_all_logs()
        
        if not history_df.empty:
            selected_move = st.selectbox("Select a concept to strategize:", 
                                       history_df['scenario'].unique())
            
            context = history_df[history_df['scenario'] == selected_move]['verdict'].iloc[0]
            
            if st.button("Draft Execution Plan"):
                with st.spinner("Drafting Management Strategy..."):
                    plan = comms.generate_strategic_plan(selected_move, context)
                    st.divider()
                    st.markdown(plan)
                    
                    # Topic 3: Export Policy Document
                    st.download_button("Download Strategy Document", plan, file_name="Executive_Strategy.txt")
        else:
            st.info("No concepts found. Please run a Strategy Simulator or Ideation Lab activity first.")

    elif menu == "Learning Center":
        st.header("🎓 Aegis-AI Knowledge Base")
        st.markdown("Transform technical project data into interactive training modules.")
        
        # Topic 1: Stakeholder Update Section
        with st.expander("✉️ Quick Stakeholder Update"):
            project_status = st.text_area("What did you achieve today?", "Completed the WBS and Milestone planning.")
            if st.button("Draft Update Email"):
                email_prompt = f"Draft a professional stakeholder email for this progress: {project_status}"
                st.code(comms.model.generate_content(email_prompt).text)

        st.divider()

        # Topic 2, 3, 4: Course Generation
        topic_input = st.text_input("Enter a topic for the Learning Module:", "How the AI Fitness Coach uses MediaPipe")
        
        if st.button("Build Course & Quiz"):
            with st.spinner("Structuring curriculum..."):
                course_content = comms.generate_educational_content(topic_input)
                st.markdown(course_content)
                
                # Allow downloading for the company handbook
                st.download_button("Export Module", course_content, file_name="Training_Module.txt")

    elif menu == "Adaptive Classroom":
        st.header("🎯 Personalized Learning & Trends")
        st.markdown("Bridge the gap between your current skills and 2026 industry standards.")
        
        col1, col2 = st.columns(2)
        with col1:
            goal = st.selectbox("Your Goal:", ["AI Engineer", "Full-Stack Dev", "Data Scientist"])
            level = st.select_slider("Current Level:", options=["Beginner", "Intermediate", "Advanced"])
        
        with col2:
            trend_focus = st.multiselect("Focus Trends:", ["Agentic AI", "Real-time Edge CV", "RAG Systems", "Vector DBs"])

        if st.button("Generate My Path"):
            profile = f"Goal: {goal}, Level: {level}"
            trends = ", ".join(trend_focus)
            
            with st.spinner("Mapping your career trajectory..."):
                path = comms.generate_adaptive_path(profile, trends)
                st.divider()
                st.markdown(path)
                
                # Save this path to the user's profile in SQLite
                # Using a dummy session state or nested button workaround as Streamlit buttons don't hold state natively
                # The user's code nested a button inside a button which doesn't work in Streamlit. Let's fix that.
                st.session_state['generated_path'] = path
                st.session_state['generated_profile_goal'] = goal
                
        # Streamlit best practice: Check session state outside the button
        if 'generated_path' in st.session_state:
            if st.button("Save Path to My Profile"):
                save_verdict(f"LEARNING PATH: {st.session_state['generated_profile_goal']}", st.session_state['generated_path'], impact=8, likelihood=5)
                st.success("Roadmap saved to your career history!")

    elif menu == "Ethics & Risk":
        st.header("⚖️ AI Ethics & Predictive Safety")
        st.markdown("Ensure your AI is fair, proactive, and accountable.")

        # Select a recent interaction to audit
        history_df = get_all_logs()
        
        if not history_df.empty:
            selected_log = st.selectbox("Select Interaction to Audit:", history_df['scenario'].unique())
            raw_output = history_df[history_df['scenario'] == selected_log]['verdict'].iloc[0]
            
            if st.button("Run Ethical Audit"):
                with st.spinner("Auditing AI logic for bias and risk..."):
                    audit_report = comms.audit_ai_decision(raw_output, "Standard Profile")
                    st.divider()
                    st.subheader("📋 Audit Results")
                    st.markdown(audit_report)
                    
                    # Topic 6: Accountability Export
                    st.download_button("Export Transparency Log", audit_report, file_name="Ethics_Audit.txt")
        else:
            st.info("No interactions found to audit. Please run a simulation or support activity first.")

    elif menu == "Data Center":
        st.title("📂 Business Data Connector")
        st.markdown("Upload and validate business data (CSV) for context-aware communication building.")
        
        uploaded_file = st.file_uploader("Upload Business Data", type=["csv"])

        if uploaded_file is not None:
            try:
                # Topic 11: Secure Data Ingestion
                df = pd.read_csv(uploaded_file)
                
                # EDGE CASE: Empty File
                if df.empty:
                    st.warning("📍 The uploaded file is empty. Please provide a file with data.")
                else:
                    st.success("Data loaded successfully!")
                    st.markdown("### Preview:")
                    st.dataframe(df.head(10))
                    
                    # Store in session state for other tabs to access
                    st.session_state['uploaded_df'] = df
                    
            except Exception as e:
                # Log to console
                print(f"DEBUG FILE ERROR: {e}")
                st.error(f"❌ Critical Error: The file format is not supported. Please upload a valid CSV.")

if __name__ == "__main__":
    main()