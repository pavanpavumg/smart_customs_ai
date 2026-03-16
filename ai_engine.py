import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load variables from a .env file into the environment
load_dotenv()

class CommsAgent:
    def __init__(self):
        # Using environment variable for API Key
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-flash-latest')

    def generate_comms(self, data, mode, tone):
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