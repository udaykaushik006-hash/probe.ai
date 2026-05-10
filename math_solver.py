import sympy as sp

def solve_math_steps(expr):
    try:
        x = sp.symbols('x')
        result = sp.sympify(expr)

        simplified = sp.simplify(result)

        return f"🧮 Solution:\nExpression: {expr}\nResult: {simplified}"

    except Exception as e:
        return f"Math error: {str(e)}"