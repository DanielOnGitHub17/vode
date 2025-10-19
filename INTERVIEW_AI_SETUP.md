# Interview AI Agent Setup

## 🎯 Architecture Overview

### Context Management Flow
```
Interview Starts
    ↓
interview() view loads
    ↓
start_interview() called with context
    ↓
GeminiService.initialize_context()
    ↓
Conversation history established with problem details
    ↓
Agent ready for submissions
```

### During Interview
```
Frontend Timer/Activity Detection
    ↓
Sends: Current Code + Current Audio Transcript
    ↓
POST /interview/api/get-response/
    ↓
Gemini Agent Reasoning + Eleven Labs TTS
    ↓
Returns: MP3 Audio Feedback
    ↓
Frontend Plays Audio to Candidate
    ↓
Timer Continues...
```

## 🧠 AI Agent Capabilities

### 1. **Context-Aware Coaching**
- Initializes with full problem statement, constraints, examples
- Maintains conversation history across submissions
- References problem context in all feedback

### 2. **Smart Feedback**
Analyzes:
- **Correctness**: Does code solve the problem?
- **Approach**: Is the strategy sound?
- **Explanation Quality**: Does candidate understand their code?
- **Edge Cases**: Are constraints handled?
- **Trade-offs**: Time vs space complexity

### 3. **Probing Questions**
- Asks "what if" scenarios
- Challenges assumptions gently
- Hints at optimizations without spoiling
- Guides discovery of better solutions

## 📋 Key Methods

### GeminiService
- `initialize_context()` - Sets up problem space (called once at start)
- `agent_reasoning()` - Single method handling all exchanges (submissions, questions, follow-ups)
  - Uses conversation history internally
  - No separate follow-up method needed
- `clear_context()` - Resets for next interview

### InterviewOrchestrator
- `start_interview()` - Initialize with interview context
- `get_question_with_audio()` - Get question as speech
- `agent_evaluate_submission()` - Evaluate code + transcript (handles all cases)
- `end_interview()` - Clean up

## 🔄 Interview Flow

1. **Page Load** → `interview()` view
   - Creates interview context
   - Calls `orchestrator.start_interview(context)`
   - AI agent initializes with problem details

2. **Continuous Updates** → `/interview/api/get-response/`
   - Frontend sends: Current code + current audio/text (intermittently)
   - Triggered by: Inactivity timer or periodic polling
   - **Single endpoint handles everything:**
     - Code submissions
     - Code updates
     - Questions from candidate
     - Follow-ups (via Gemini conversation history)
   - Returns: MP3 audio feedback (binary response)
   - Frontend: Plays audio to candidate

3. **Interview Ends** → Timer runs down
   - Session ends automatically
   - Backend cleans up context

## 💡 Prompt Strategy

### Initialization Prompt
Sets agent personality as coaching interviewer:
- Knowledgeable about the problem
- Focused on thought process, not just code
- Asks questions to make them think
- Hints at solutions without giving answers

### Submission Prompt
Instructs agent to:
1. Test code against examples
2. Evaluate approach and efficiency
3. Check understanding vs explanation
4. Find edge case issues
5. Ask one powerful probing question

### Follow-Up Prompt
Creates questions that:
- Dig deeper into understanding
- Challenge complexity thinking
- Guide toward optimization
- Stay encouraging and conversational

## 🚀 Next Steps

1. Install dependencies:
   ```bash
   pip install google-generativeai requests
   ```

2. Create `.env` file with API keys:
   ```
   GEMINI_API_KEY=AIzaSyCfXYmTJFQ8lI-dKMVcXmVNZDCO66qU9IY
   ELEVENLABS_API_KEY=your_key
   ```

3. Load environment variables in Django settings (optional but recommended):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

4. Test the interview flow:
   - Navigate to interview page
   - Submit code + transcript
   - Verify AI coaching feedback
   - Test follow-up questions

## 📊 Model Choice: Gemini 2.0 Flash-Lite

- **Input tokens**: 1M per minute
- **Output tokens**: 200 per minute
- **Latency**: ~1-2 seconds
- **Cost**: Optimized for coaching feedback
- **Quality**: Excellent for reasoning tasks
