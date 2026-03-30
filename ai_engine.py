import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load variables from a .env file into the environment
load_dotenv(override=True)

class CommsAgent:
    def __init__(self):
        # Using environment variable for API Key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
             print("DEBUG ERROR: GOOGLE_API_KEY not found in environment.")
        else:
             genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('models/gemini-flash-latest')

    def generate_comms(self, data, mode, tone):
        try:
            # Topic 2 & 4: Tone and Structure mapping
            prompts = {
                "Email": f"Draft a concise {tone} business email. Follow BLUF (Bottom Line Up Front). Data: {data}",
                "Proposal": f"Structure a formal project proposal including Problem, Solution, and Timeline. Data: {data}",
                "Slides": f"Generate a 5-slide outline with bullet points for a presentation. Data: {data}",
                "Executive Summary": f"Provide a high-level 3-sentence briefing for a CEO. Data: {data}"
            }
            
            prompt = prompts.get(mode, prompts["Email"])
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Log the real error to the console for you
            print(f"DEBUG ERROR: {e}")
            # Return a "Safe" message for the user
            return "⚠️ AI Engine is temporarily unavailable. Please check your API Key or Internet connection."

    def generate_sop(self, process_description):
        """Converts a raw process into a formal Standard Operating Procedure."""
        prompt = f"""
        Act as a Technical Writer. Convert the following process into a formal SOP (Standard Operating Procedure):
        Process: {process_description}
        
        Structure:
        1. Title & Objective
        2. Scope (Who is this for?)
        3. Prerequisites (What tools/keys are needed?)
        4. Step-by-Step Procedure (Numbered list)
        5. Quality Check (How do we know it worked?)
        
        Tone: Precise, professional, and easy to follow.
        """
        response = self.model.generate_content(prompt)
        return response.text

    def generate_innovation(self, core_concept, framework="SCAMPER"):
        """Generates structured business ideas based on a specific framework."""
        prompt = f"""
        Act as a Startup Innovation Consultant. 
        Use the {framework} framework to brainstorm variations for this concept:
        Concept: {core_concept}
        
        Format the output with:
        1. 💡 The Core Innovation
        2. 🔄 3 Diverse Variations (safe to wildcard)
        3. 🚧 A 'Constraint Challenge' to break creative blocks
        4. 📈 Potential Market Impact
        """
        response = self.model.generate_content(prompt)
        return response.text

    def generate_mindmap_code(self, concept):
        """Generates Mermaid.js mindmap code for a given concept."""
        prompt = f"""
        Act as a Visual Strategist. Create a Mermaid.js mindmap for: {concept}.
        
        Rules:
        - Use the 'mindmap' keyword at the start.
        - Branch out into 4 main categories: Features, Risks, Target Audience, and Marketing.
        - Each category should have 3 sub-nodes.
        - Output ONLY the mermaid code.
        """
        response = self.model.generate_content(prompt)
        return response.text

    def generate_strategic_plan(self, concept, data_context):
        """Converts a concept into a structured Management Strategy and Policy."""
        prompt = f"""
        Act as a Chief Strategy Officer (CSO). 
        Concept: {concept}
        Context: {data_context}
        
        Provide a high-level Executive Strategy:
        1. 🎯 **DECISION FRAMEWORK**: Apply an ICE Score (1-10) for Impact, Confidence, and Ease.
        2. 🗺️ **EXECUTION ROADMAP**: Define 3 distinct phases (Alpha, Beta, Scale).
        3. ⚖️ **POLICY GUARDRAILS**: List 3 non-negotiable rules for execution to ensure quality.
        
        Format: Use tables for scores and bullet points for roadmap phases.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Strategic Engine Error: {e}"

    def generate_educational_content(self, topic):
        """Converts a technical concept into a structured course and quiz."""
        prompt = f"""
        Act as an Instructional Designer. 
        Topic: {topic}
        
        Provide a professional Learning Module:
        1. 📚 **COURSE STRUCTURE**: 3 Lessons (Introduction, Technical Implementation, Best Practices).
        2. 📝 **INTERACTIVE LAB**: One hands-on exercise for the student.
        3. ❓ **ASSESSMENT**: 3 Multiple-choice questions with an 'Answer Key' at the bottom.
        
        Format: Use clear headings and structured lists.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Education Engine Error: {e}"

    def generate_adaptive_path(self, user_profile, tech_trends):
        """Creates a custom learning roadmap based on user level and current trends."""
        prompt = f"""
        Act as a Senior Technical Mentor. 
        User Profile: {user_profile} (Goal, Current Skills, Learning Style)
        Current 2026 Tech Trends: {tech_trends}
        
        Task: Generate a 'Hyper-Personalized' Learning Path.
        1. 🗺️ **THE ROADMAP**: 4 Milestones ordered from fundamental to trend-leading.
        2. 🛠️ **TECH STACK**: Recommend specific libraries/tools relevant to {tech_trends}.
        3. 🔄 **ADAPTIVE STEP**: If the user struggles with Milestone 2, what 'Bridge Project' should they do?
        
        Format: Use a professional table for the roadmap and bold highlights for the tech stack.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Tutor Engine Error: {e}"

    def audit_ai_decision(self, ai_output, user_data):
        """Audits a generated decision for bias, risk, and transparency."""
        prompt = f"""
        Act as an AI Ethics & Risk Auditor. 
        AI Decision: {ai_output}
        User Data: {user_data}
        
        Tasks:
        1. ⚖️ **BIAS CHECK**: Does this advice unfairly target or exclude any demographic?
        2. 🚩 **RISK PREDICTION**: Is the user showing signs of frustration or physical risk?
        3. 🔍 **TRANSPARENCY**: Explain the underlying 'First Principles' logic for this decision.
        4. 📢 **PROACTIVE MOVE**: Suggest one encouraging message to prevent dissatisfaction.
        
        Format: Structured audit report with a 'Safety Rating' (Pass/Fail).
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Auditor Engine Error: {e}"