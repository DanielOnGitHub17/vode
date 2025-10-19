"""
Mock data for interview questions and test cases
"""

MOCK_QUESTION = {
    'title': 'Two Sum',
    'statement': '''
<div class="question-section">
    <h6 class="text-muted mb-2">Description</h6>
    <p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return <strong>indices of the two numbers</strong> such that they add up to <code>target</code>.</p>
    <p>You may assume that each input would have <strong>exactly one solution</strong>, and you may not use the same element twice.</p>
    <p>You can return the answer in any order.</p>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Examples</h6>
    
    <div class="mb-3">
        <strong>Example 1:</strong>
        <pre class="code-example"><code>Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].</code></pre>
    </div>
    
    <div class="mb-3">
        <strong>Example 2:</strong>
        <pre class="code-example"><code>Input: nums = [3,2,4], target = 6
Output: [1,2]</code></pre>
    </div>
    
    <div class="mb-3">
        <strong>Example 3:</strong>
        <pre class="code-example"><code>Input: nums = [3,3], target = 6
Output: [0,1]</code></pre>
    </div>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Constraints</h6>
    <ul>
        <li>2 ≤ nums.length ≤ 10<sup>4</sup></li>
        <li>-10<sup>9</sup> ≤ nums[i] ≤ 10<sup>9</sup></li>
        <li>-10<sup>9</sup> ≤ target ≤ 10<sup>9</sup></li>
        <li>Only one valid answer exists</li>
    </ul>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Follow-up</h6>
    <p>Can you come up with an algorithm that is less than <strong>O(n²)</strong> time complexity?</p>
</div>
''',
    'test_cases': [
        {
            'input': {
                'nums': [2, 7, 11, 15],
                'target': 9
            },
            'output': [0, 1],
            'explanation': 'Because nums[0] + nums[1] == 9, we return [0, 1].'
        },
        {
            'input': {
                'nums': [3, 2, 4],
                'target': 6
            },
            'output': [1, 2],
            'explanation': 'nums[1] + nums[2] == 6'
        },
        {
            'input': {
                'nums': [3, 3],
                'target': 6
            },
            'output': [0, 1],
            'explanation': 'nums[0] + nums[1] == 6'
        }
    ]
}

QUESTION_GENERATION_PROMPT = """You are an expert technical interviewer tasked with creating a coding interview question.

--- INTERVIEW CONTEXT ---
Difficulty: %(difficulty)s
Topics: %(topics)s

--- RECENTLY USED QUESTIONS (DO NOT REPEAT) ---
%(already_picked)s

--- INSTRUCTIONS ---
Generate a complete coding interview question that:
1. Is appropriate for the given difficulty level and covers the specified topics
2. Is DIFFERENT from the recently used questions listed above
3. Tests the candidate's problem-solving and coding abilities
4. Includes clear examples and test cases
5. Has well-defined constraints
6. Is solvable within the interview time limit

--- OUTPUT FORMAT ---
Return a JSON object with the following structure:

{
    "title": "Brief, descriptive question title (e.g., 'Two Sum', 'Valid Parentheses')",
    "statement": "HTML-formatted question statement including sections for Description, Examples, Constraints, and optionally Follow-up",
    "test_cases": [
        {
            "input": {"param1": value1, "param2": value2},
            "output": expected_output,
            "explanation": "Brief explanation of why this output is correct"
        }
    ]
}

--- STATEMENT HTML STRUCTURE ---
The "statement" field should be formatted as HTML with the following structure:

<div class="question-section">
    <h6 class="text-muted mb-2">Description</h6>
    <p>Clear problem description with <code>code formatting</code> for technical terms.</p>
    <p>Additional context and requirements using <strong>bold</strong> for emphasis.</p>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Examples</h6>
    
    <div class="mb-3">
        <strong>Example 1:</strong>
        <pre class="code-example"><code>Input: param = value
Output: result
Explanation: Why this output is correct.</code></pre>
    </div>
    
    <div class="mb-3">
        <strong>Example 2:</strong>
        <pre class="code-example"><code>Input: param = value
Output: result</code></pre>
    </div>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Constraints</h6>
    <ul>
        <li>Constraint 1 with proper notation (use <sup>superscript</sup> for exponents)</li>
        <li>Constraint 2</li>
        <li>Constraint 3</li>
    </ul>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Follow-up</h6>
    <p>Optional: Additional challenge or optimization question</p>
</div>

--- REQUIREMENTS ---
1. **Title**: Short, descriptive (2-5 words)
2. **Description**: Clear problem statement with all necessary context
3. **Examples**: At least 2-3 examples with input/output pairs
4. **Constraints**: Specific bounds on input size, value ranges, edge cases
5. **Test Cases**: Minimum 3 test cases covering normal cases, edge cases, and corner cases

Generate a question that would take approximately 30-45 minutes for a %(difficulty)s level candidate to solve.

Return ONLY the JSON object, no additional text or explanation."""
