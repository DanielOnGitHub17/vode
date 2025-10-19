import google.generativeai as genai
from django.conf import settings
from interview.mocks import MOCK_QUESTION
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        self.conversation_history = []
    
    def get_question(self):
        """Return the Two Sum question from mocks"""
        return MOCK_QUESTION
    
    def initialize_context(self, question_data, interview_context):
        """
        Initialize the interview context for the AI agent.
        This establishes the problem space and expectations.
        
        Args:
            question_data: The question details (title, statement, examples, constraints)
            interview_context: Interview metadata (role, round, difficulty)
        """
        context_prompt = f"""
        You are an expert coding interview coach evaluating candidates during a technical interview.
        
        INTERVIEW SETUP:
        - Position: {interview_context.get('role', 'Backend Engineer')}
        - Round: {interview_context.get('round', 1)} of {interview_context.get('total_rounds', 3)}
        - Difficulty Level: {interview_context.get('difficulty', 'Medium')}
        
        PROBLEM BEING SOLVED:
        Title: {question_data.get('title', 'Two Sum')}
        
        Problem Statement:
        {question_data.get('statement', '')}
        
        Constraints:
        {question_data.get('constraints', '')}
        
        Examples:
        {question_data.get('examples', '')}
        
        YOUR ROLE:
        You are a thoughtful, encouraging interviewer. Your goal is to:
        1. Understand the candidate's approach and reasoning
        2. Guide them to think critically about trade-offs (time vs space complexity)
        3. Help them identify edge cases they might have missed
        4. Ask probing questions that make them question their assumptions
        5. Provide constructive feedback that hints at better solutions without giving them away
        
        COMMUNICATION STYLE:
        - Be conversational and approachable, not robotic
        - When they mention an approach, ask "why" or "what if" questions
        - If you spot issues, guide them to discover the problems themselves
        - Balance encouragement with constructive critique
        - Focus on their thought process, not just the code
        
        You will now evaluate the candidate's submission and provide coaching feedback.
        """
        
        # Initialize conversation history with context
        self.conversation_history = [
            {
                "role": "user",
                "parts": [{"text": context_prompt}]
            },
            {
                "role": "model",
                "parts": [{"text": "I understand. I'm ready to coach this candidate through the Two Sum problem. I'll focus on their approach, reasoning, and help them think through trade-offs and edge cases. I'm prepared to ask probing questions that guide them to better solutions."}]
            }
        ]
    
    def agent_reasoning(self, candidate_code, audio_transcript, interview_context):
        """
        AI agent that reasons on the spot about candidate's submission.
        Takes code, audio transcript, and interview context to provide intelligent feedback.
        Uses conversation history to maintain context across all exchanges.
        
        This single method handles:
        - Code submissions
        - Code updates
        - Questions from candidate
        - Follow-ups (via conversation history)
        
        Args:
            candidate_code: Code from editor (may be empty if just asking a question)
            audio_transcript: Audio/voice transcript of candidate's explanation
            interview_context: Dict with interview details (used as context reference)
        
        Returns:
            Agent response with reasoning and feedback
        """
        submission_prompt = f"""
        CANDIDATE'S CURRENT INPUT:
        
        Code:
        ```python
        {candidate_code if candidate_code else '(No code provided)'}
        ```
        
        Candidate's Statement (from voice/text):
        "{audio_transcript if audio_transcript else '(No statement provided)'}"
        
        ANALYZE AND RESPOND:
        Evaluate this by considering:
        1. **Correctness**: Does the code solve the problem? Test against examples.
        2. **Approach**: What strategy are they using? Efficient?
        3. **Understanding**: Does their explanation match their code?
        4. **Edge Cases**: Handling all constraints?
        5. **Trade-offs**: Time vs space complexity considerations?
        
        PROVIDE COACHING FEEDBACK:
        - Acknowledge what they're doing well
        - Ask guiding questions to make them think (not rhetorical, genuine probes)
        - Hint at better approaches without spoiling
        - Challenge assumptions gently
        - Ask ONE powerful question that deepens their thinking
        
        Keep response conversational and actionable (2-3 paragraphs max).
        """
        
        try:
            # Add the submission to conversation history
            self.conversation_history.append({
                "role": "user",
                "parts": [{"text": submission_prompt}]
            })
            
            # Get response using conversation history
            response = self.model.generate_content(self.conversation_history)
            feedback = response.text
            
            # Add response to history for continuity
            self.conversation_history.append({
                "role": "model",
                "parts": [{"text": feedback}]
            })
            
            return feedback
        except Exception as e:
            logger.error(f"Gemini agent reasoning error: {e}")
            raise
    
    def clear_context(self):
        """Clear conversation history between interviews"""
        self.conversation_history = []
