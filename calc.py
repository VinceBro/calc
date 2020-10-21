#!/usr/bin/python3
import math, argparse, numpy, decimal, sys, re
from fractions import Fraction


class TextColorizer():
    def __init__(self):
        self.ESCAPE_CODE = "\033["
        self.END_ESCAPE = self.ESCAPE_CODE + "0m"
        self.GREEN = self.ESCAPE_CODE + "92;1m"
        self.YELLOW = self.ESCAPE_CODE + "93;1m"
        self.BLUE = self.ESCAPE_CODE + "94;1m"
    
    def colorize(self, string_or_number, color):
        return f"{color}{self.stringify(string_or_number)}{self.END_ESCAPE}"

    def colorize_green(self, string_or_number):
        return self.colorize(string_or_number, self.GREEN)

    def colorize_yellow(self, string_or_number):
        return self.colorize(string_or_number, self.YELLOW)

    def colorize_blue(self, string_or_number):
        return self.colorize(string_or_number, self.BLUE)

    def stringify(self, string_or_number):
        return str(string_or_number)

class Calculator():
    def __init__(self, text_colorizer, parser):
        self.rounded_decimals = 4
        self.pi = math.pi
        self.text_colorizer = text_colorizer
        self.parser = parser
    def getfraction(self, decimal):
        ratio = decimal.as_integer_ratio()
        return f"{ratio[0]}/{ratio[1]}"
    def getcrossproduct(self, vector1, vector2):
        return numpy.cross(vector1, vector2)
    def getdotproduct(self, vector1, vector2):
        return numpy.dot(vector1, vector2)
    def getangle(self, angle):
        return_angle = self.radtodeg(angle) if "rad" in angle else self.degtorad(angle) if "deg" in angle else None
        if return_angle is not None:
            suffix = "deg" if "rad" in angle else "rad"
            return f"Angle {self.text_colorizer.colorize_blue(angle)} is : \n{self.text_colorizer.colorize_green(round(return_angle, self.rounded_decimals))} {suffix} or \n{self.text_colorizer.colorize_green(round(self.rectifyangle(angle), self.rounded_decimals))} {suffix} rectified"
        else:
            return "Specify rad or deg"

    def parsemathexpression(self, expression):
        return f"Result : {self.text_colorizer.colorize_green(self.parser.evaluate(expression))}"
    def degtorad(self, angle):
        return(2*self.pi*self.extractfloat(angle)/360)
    def radtodeg(self, angle):
        return(360*self.extractfloat(angle)/(self.pi*2))
    def rectifyangle(self, angle):
        return self.radtodeg(angle) % 360 if "rad" in angle else self.degtorad(angle) % (2*self.pi) if "deg" in angle else None

    def extractstringnumbers(self, number_string):
        string = ''.join((ch if ch in '0123456789.pi' else ' ') for ch in number_string)
        return string.replace("pi", " pi")

    def extractfloat(self, angle):
        fraction_split = angle.split("/")
        numerator = fraction_split[0]
        denumerator = fraction_split[1] if len(fraction_split) > 1 else None
        numerator_string = self.extractstringnumbers(numerator)
        denumerator_string = self.extractstringnumbers(denumerator) if denumerator is not None else None
        numerator_angle = numpy.prod([float(i) if i != "pi" else self.pi for i in numerator_string.split()])
        denumerator_angle = numpy.prod([float(i) if i != "pi" else self.pi for i in denumerator_string.split()]) if denumerator is not None else None
        return numerator_angle/denumerator_angle if denumerator is not None else numerator_angle

    def generatequadraticstring(self, a, b, c):
        out_string = ""
        if a != 0:
            out_string += str(a) + "x²"

        if b != 0:
            out_string += self.generateformatedadditionsstring(b) + "x"
        
        if c != 0:
            out_string += self.generateformatedadditionsstring(c)
        
        return out_string

    def generateformatedadditionsstring(self, x):
        if x > 0:
            return " + " + str(x)
        elif x < 0:
            return " - " + str(abs(x))

    def generateformatedzerosstring(self, x):
        if x < 0:
            return "(x + " + str(abs(x)) + ")"
        elif x > 0:
            return "(x - " + str(x) + ")"
        else:
            return "0"


    def getzeros(self, a, b, c):
        radical = b**2-4*a*c
        denum = 2*a
        reel = -b/denum

        out_string = f"For quadratic expression : " 
        out_string +=  self.text_colorizer.colorize_blue(self.generatequadraticstring(a, b, c)) + "\n"
        if radical >= 0:
            out_string += f"Zeros are : {self.text_colorizer.colorize_green(self.generateformatedzerosstring((-b+math.sqrt(radical))/denum))} and {self.text_colorizer.colorize_green(self.generateformatedzerosstring((-b-math.sqrt(radical))/denum))}"
        elif radical < 0 and len(str(math.sqrt(abs(radical))).split('.')[1]) <= 1:
            sub_string_pos = f"(x - {reel} + {abs(radical)/denum} i)"
            sub_string_neg = f"(x - {reel} - {abs(radical)/denum} i)"
            out_string += f"Zeros are complex and are : {self.text_colorizer.colorize_yellow(sub_string_pos)} and {self.text_colorizer.colorize_yellow(sub_string_neg)}\n"
        else:
            sub_string_pos = f"(x - {reel} + √{abs(radical)}/{denum} i)"
            sub_string_neg = f"(x - {reel} - √{abs(radical)}/{denum} i)"
            out_string += f"Zeros are complex and are : {self.text_colorizer.colorize_yellow(sub_string_pos)} and {self.text_colorizer.colorize_yellow(sub_string_neg)}\n"

        return out_string

    def a_parmi_b(self, a, b):
        return math.factorial(b)/(math.factorial(a)*(math.factorial(b-a)))


class ShuntingYardParser():
    # Shunting Yard algorithm implementation source : http://www.martinbroadhurst.com/shunting-yard-algorithm-in-python.html
    def __init__(self):
        self.precedences = {'+' : 0, '-' : 0, 'x' : 1, '/' : 1, '^': 2}
        self.token_regex = "[+/x*^()-]|[\d.\d]+"

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False
    
    def peek(self, stack):
        return stack[-1] if stack else None
    
    def apply_operator(self, operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        result = 0
        if operator == "+":
            result = left + right
        elif operator == "-":
            result = left - right
        elif operator in ["x", "*"]:
            result = left * right
        elif operator == "/":
            result = left / right
        elif operator == "^":
            result = left ** right
        values.append(result)
    
    def greater_precedence(self, op1, op2):
        return self.precedences[op1] > self.precedences[op2]
    
    def evaluate(self, expression):
        tokens = re.findall(self.token_regex, expression)
        values = []
        operators = []
        for token in tokens:
            if self.is_number(token):
                values.append(float(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                top = self.peek(operators)
                while top is not None and top != '(':
                    self.apply_operator(operators, values)
                    top = self.peek(operators)
                operators.pop() # Discard the '('
            else:
                # Operator
                top = self.peek(operators)
                while top is not None and top not in "()" and self.greater_precedence(top, token):
                    self.apply_operator(operators, values)
                    top = self.peek(operators)
                operators.append(token)
        while self.peek(operators) is not None:
            self.apply_operator(operators, values)
    
        return values[0]


def parseall(parser):
    parser.add_argument("operations", metavar="Operations", type=str, action='store', nargs='+')
    parser.add_argument("-a", "--angle", default=False, action='store_true', dest='angle', help="Treats input as angle and converts it to rad or deg accordingly. Input is treated as string so you can specify rad, deg and pi for your angles. rad or deg must be specified in input string")
    parser.add_argument("-v1", "--vector1", metavar="Vector", default=None,type=float, dest='vector1',nargs='+', help="Composantes du premier vecteur")
    parser.add_argument("-v2", "--vector2", metavar="Vector", default=None,type=float, dest='vector2',nargs='+', help="Composantes du deuxième vecteur")
    parser.add_argument("-dp", "--dotproduct",default=False, action='store_true', dest='dproduct', help='Calcule le produit scalaire, prends des vecteurs en entrée')
    parser.add_argument("-cp", "--crossproduct",default=False,action='store_true', dest='cproduct', help='Calcule le produit vectoriel, prends des vecteurs en entrée')
    parser.add_argument("-q", "--quadratic", default=False, dest='quad',action='store_true',help="Calculates and formats the zeros of a quadratic equation in complex or non complex form")
    parser.add_argument("-f", "--fraction",metavar="Float", default=None, dest='fraction', type=float, help="Calcule la fraction associée à un chiffre decimal")
    parser.add_argument("-ab", "--abyb", metavar="Int", default=None,type=int, dest='abyb',nargs='+', help="Calcule a parmi b")
    return parser.parse_args()

def main():
    parser = argparse.ArgumentParser(description="Calc CLI tool utility")
    ARGS = parseall(parser)
    calc = Calculator(TextColorizer(), ShuntingYardParser())
    if ARGS.angle:
        print(calc.getangle("".join(ARGS.operations)))
    elif ARGS.quad:
        print(calc.getzeros(float(ARGS.operations[0]), float(ARGS.operations[1]), float(ARGS.operations[2])))
    elif ARGS.fraction:
        print(calc.getfraction(ARGS.fraction))
    elif ARGS.dproduct is True and ARGS.vector1 and ARGS.vector2:
        print("Dot product between vector {} and vector {} is {}".format(ARGS.vector1, ARGS.vector2, calc.getdotproduct(ARGS.vector1, ARGS.vector2)))
    elif ARGS.cproduct is True and ARGS.vector1 and ARGS.vector2:
        print("Cross product between vector {} and vector {} is {}".format(ARGS.vector1, ARGS.vector2, calc.getcrossproduct(ARGS.vector1, ARGS.vector2)))
    elif ARGS.abyb:
        print(calc.a_parmi_b(ARGS.abyb[0], ARGS.abyb[1]))
    elif ARGS.operations:
        print(calc.parsemathexpression("".join(ARGS.operations)))




if __name__ == "__main__":
    main()
