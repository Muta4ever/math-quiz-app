import random
import sympy as sp

class QuizProblem:
    """
    Represents one problem: arithmetic or calculus
    """

    ARITHMETIC_OPS = ['+', '-', '*', '/']
    CALCULUS_OPS = ['diff', 'integrate']

    def __init__(self, difficulty='easy', type_='arithmetic'):
        self.difficulty = difficulty
        self.type_ = type_
        self.problem = ''
        self.answer = None
        self._generate_problem()

    def _get_max_number(self):
        if self.difficulty == 'easy':
            return 10
        elif self.difficulty == 'medium':
            return 50
        else:  # hard
            return 100

    def _generate_problem(self):
        if self.type_ == 'arithmetic':
            self._generate_arithmetic()
        else:
            self._generate_calculus()

    def _generate_arithmetic(self):
        maxNum = self._get_max_number()
        op = random.choice(self.ARITHMETIC_OPS)
        if op == '+':
            a, b = random.randint(0, maxNum), random.randint(0, maxNum)
            self.problem = f"{a} + {b}"
            self.answer = a + b
        elif op == '-':
            b = random.randint(0, maxNum)
            ans = random.randint(0, maxNum)
            a = b + ans
            self.problem = f"{a} - {b}"
            self.answer = ans
        elif op == '*':
            a, b = random.randint(0, maxNum), random.randint(0, maxNum)
            self.problem = f"{a} * {b}"
            self.answer = a * b
        elif op == '/':
            b = random.randint(1, maxNum)
            ans = random.randint(0, maxNum)
            a = b * ans
            self.problem = f"{a} / {b}"
            self.answer = ans

    def _generate_calculus(self):
        x = sp.symbols('x')
        op = random.choice(self.CALCULUS_OPS)
        coeff = random.randint(1, 10)
        power = random.randint(1, 5)
        expr = coeff * x**power
        if op == 'diff':
            self.problem = f"d/dx of {expr}"
            self.answer = sp.diff(expr, x)
        else:
            self.problem = f"∫ {expr} dx"
            self.answer = sp.integrate(expr, x)

    def check_answer(self, user_input):
        try:
            if self.type_ == 'arithmetic':
                return int(user_input) == self.answer
            else:
                user_expr = sp.sympify(user_input)
                return sp.simplify(user_expr - self.answer) == 0
        except:
            return False

    def __str__(self):
        return self.problem
