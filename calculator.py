import re

def solve_math(expression):
    try:
        # allow only safe characters
        if not re.match(r'^[0-9+\-*/(). ]+$', expression):
            return None

        result = eval(expression)
        return f"Answer: {result}"

    except:
        return "sorry, I couldn't solve it"