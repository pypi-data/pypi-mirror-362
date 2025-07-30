ANTHROPIC_PREFIX = "anthropic"
CHATGPT_PREFIX = "openai"
CRIL_PREFIX = "cril"
GOOGLE_PREFIX = "google"

BASE_CRIL_URL = "http://172.17.141.34/api"
BASE_GOOGLE_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


MODELS = [
    f"{CRIL_PREFIX}  [phi4:14b]",
    f"{CRIL_PREFIX}  [llama3.2:latest]",
    f"{CRIL_PREFIX} [qwen3:14b]",
    f"{CRIL_PREFIX}  [deepseek-r1:14b]",
    f"{ANTHROPIC_PREFIX} [claude-sonnet-4-20250514]",
    f"{ANTHROPIC_PREFIX} [claude-3-7-sonnet-20250219]",
    f"{ANTHROPIC_PREFIX} [claude-3-5-sonnet-20241022]",
    f"{CHATGPT_PREFIX}  [gpt-3.5]",
    f"{CHATGPT_PREFIX}  [gpt-4.1]",
    f"{GOOGLE_PREFIX}  [gemini-2.0-flash]",
]


# Example problems
EXAMPLE_PROBLEMS = {
    "Custom": "Enter your own problem description",
    "N-Queens": "Solve the 8-Queens problem: place 8 queens on a chessboard so no two queens attack each other",
    "Sudoku": "Create a 4x4 Sudoku solver with variables for each cell and constraints for rows, columns, and blocks",
    "Graph Coloring": "Color a graph with 4 nodes and edges [(0,1), (1,2), (2,3), (3,0)] using minimum colors",
    "Knapsack": "Knapsack problem with items having weights [2,3,4,5] and values [3,4,5,6], capacity 5",
}

QUICK_EXAMPLE_PROBLEMS = {
    "3x3 magic square": "Create a 3x3 magic square where all rows, columns, and diagonals sum to 15",
    "Simple graph coloring": "Color a triangle graph (3 nodes, all connected) with minimum colors",
    "Coin change problem": "Find ways to make change for 10 cents using coins [1,5,10]",
    "Assignment problem": "Assign 3 tasks to 3 workers with cost matrix [[1,2,3],[2,1,3],[3,2,1]]",
}

SYSTEM_PROMPT = """
You are an assistant specializing in solving any type of constraint problems in PyCSP3(academic,crafted,realistic,recreational,single,and much more). 

In addition to your knowledge of PyCSP3, here are links to some useful resources : 
    
- The git repository (https://github.com/xcsp3team/pycsp3) that contains the latest version of PyCSP3
- The git repository (https://github.com/xcsp3team/pycsp3-models) that contains more than 340 model examples for various kinds of problems within the PyCSP3 code proposed(academic,crafted,realistic,recreational,single),
together with some data files, from frameworks known as CSP (Constraint Satisfaction Problem) and COP ( Constraint Optimization Problem).
- Documentation website (https://pycsp.org/) which explains everything there is to know about PyCSP3 its syntax used to model different types of constraints

During PyCSP3 code generation, avoid errors like using an identifier twice, etc.

With the information mentioned above, you are able to generate PyCSP3 code to solve the following constraint programming problem:

{problem_description}

Requirements:
1. Use PyCSP3 syntax (from pycsp3 import *)
2. Define variables with appropriate domains
3. Add all necessary constraints
4. Include solve() call
5. Print the solution clearly
6. Make the code executable and complete


Provide only the Python code with PyCSP3, no explanations.
Use code blocks with proper markdown syntax (```python, ```, etc.).
"""
