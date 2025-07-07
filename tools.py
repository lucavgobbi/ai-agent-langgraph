from langchain_core.tools import tool
import math
from langchain_tavily import TavilySearch

@tool
def calculator(expression: str) -> str:
    """
    A calculator tool that evaluates mathematical expressions.
    Supports: addition (+), subtraction (-), multiplication (*), division (/), 
    exponentiation (^), and square root (sqrt).
    
    Args:
        expression: Mathematical expression as a string (e.g., "2 + 3", "sqrt(16)", "2^3")
    
    Returns:
        The result of the calculation as a string
    """
    try:
        # Replace ^ with ** for Python exponentiation
        expression = expression.replace('^', '**')
        
        # Handle sqrt function
        expression = expression.replace('sqrt(', 'math.sqrt(')
        
        # Evaluate the expression safely
        # Only allow certain safe functions and operators
        allowed_names = {
            'math': math,
            '__builtins__': {},
        }
        
        result = eval(expression, allowed_names)
        return str(result)
        
    except Exception as e:
        return f"Error: {str(e)}. Please check your mathematical expression."


def get_tools():
    tools = [
        TavilySearch(max_results=2),
        calculator,
    ]
    return tools