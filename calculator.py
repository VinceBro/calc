import math, argparse, numpy, decimal
from fractions import Fraction


class Calculator():
    def __init__(self):
        self.memory = 0
        self.pi = math.pi
    def getfraction(self, decimal):
        return decimal.as_integer_ratio()
    def getcrossproduct(self, vector1, vector2):
        return numpy.cross(vector1, vector2)
    def getdotproduct(self, vector1, vector2):
        return numpy.dot(vector1, vector2)
    def getangle(self, angle):
        if "rad" in str(angle):
            print("Angle : {} is {} deg or {} deg rectified".format(angle, self.radtodeg(angle), self.rectifyangle(angle)))
        elif "deg" in str(angle):
            print("Angle : {} is {} rad or {} rad rectified".format(angle, self.degtorad(angle),self.rectifyangle(angle)))
        else:
            print("Specify rad or deg")
    def degtorad(self, angle):
        return(2*self.pi*self.extractfloat(angle)/360)
    def radtodeg(self, angle):
        return(360*self.extractfloat(angle)/(self.pi*2))
    def rectifyangle(self, angle):
        if "deg" in angle:
            rect_angle = self.degtorad(angle)
            while rect_angle > 2*self.pi:
                rect_angle-= 2*self.pi
        elif "rad" in angle:
            rect_angle = self.radtodeg(angle)
            while rect_angle > 360:
                rect_angle -= 360
        return rect_angle

    def extractfloat(self, angle):
        newstr = ''.join((ch if ch in '0123456789.-' else ' ') for ch in angle)
        rect_angle = [float(i) for i in newstr.split()]
        if "pi/" in str(angle) or "pi /" in str(angle):
            return self.pi/rect_angle[0]
        elif "/pi" in str(angle) or "/ pi" in str(angle):
            return rect_angle[0]/self.pi
        elif "pi" in str(angle):
            return rect_angle[0]*self.pi
        else:
            return rect_angle[0]
    def getzeros(self, a, b, c):
        radical = b**2-4*a*c
        denum = 2*a
        reel = -b/denum
        if radical >= 0:
            print("Zeros are : {} and {}".format((-b+math.sqrt(radical))/denum, (-b-math.sqrt(radical))/denum))
        elif radical < 0 and len(str(math.sqrt(abs(radical))).split('.')[1]) <= 1:
            print("Zeros are complex and are : {} + {} i and {} - {} i".format(reel, abs(radical)/denum, reel, abs(radical)/denum))
        else:
            print("Zeros are complex and are : {} + √{}/{} i and {} - √{}/{} i".format(reel, abs(radical), denum, reel, abs(radical), denum))

    def a_parmi_b(self, a, b):
        return math.factorial(b)/(math.factorial(a)*(math.factorial(b-a)))


def parseall():
    parser = argparse.ArgumentParser(description="Calculator")
    parser.add_argument("-a", "--angle", metavar="Float",default=None, dest='angle', help="L'angle à convertir, il faut définir l'unité après la valeur (deg ou rad)")
    parser.add_argument("-v1", "--vector1", metavar="Vector", default=None,type=float, dest='vector1',nargs='+', help="Composantes du premier vecteur")
    parser.add_argument("-v2", "--vector2", metavar="Vector", default=None,type=float, dest='vector2',nargs='+', help="Composantes du deuxième vecteur")
    parser.add_argument("-dp", "--dotproduct",default=False, action='store_true', dest='dproduct', help='Calcule le produit scalaire, prends des vecteurs en entrée')
    parser.add_argument("-cp", "--crossproduct",default=False,action='store_true', dest='cproduct', help='Calcule le produit vectoriel, prends des vecteurs en entrée')
    parser.add_argument("-q", "--quadratic",metavar = "Float", nargs='+',default=None, dest='quad',type=float,help="Calcule les zéros d'une fonction quadratique")
    parser.add_argument("-f", "--fraction",metavar="Float", default=None, dest='fraction', type=float, help="Calcule la fraction associée à un chiffre decimal")
    parser.add_argument("-ab", "--abyb", metavar="Int", default=None,type=int, dest='abyb',nargs='+', help="Calcule a parmi b")
    return parser.parse_args()

def main():
    ARGS = parseall()
    calc = Calculator()
    if ARGS.angle is not None:
        calc.getangle(ARGS.angle)
    elif ARGS.quad is not None:
        calc.getzeros(ARGS.quad[0], ARGS.quad[1], ARGS.quad[2])
    elif ARGS.fraction is not None:
        print(calc.getfraction(ARGS.fraction))
    elif ARGS.dproduct is True and ARGS.vector1 is not None and ARGS.vector2 is not None:
        print("Dot product between vector {} and vector {} is {}".format(ARGS.vector1, ARGS.vector2, calc.getdotproduct(ARGS.vector1, ARGS.vector2)))
    elif ARGS.cproduct is True and ARGS.vector1 is not None and ARGS.vector2 is not None:
        print("Cross product between vector {} and vector {} is {}".format(ARGS.vector1, ARGS.vector2, calc.getcrossproduct(ARGS.vector1, ARGS.vector2)))
    elif ARGS.abyb is not None:
        print(calc.a_parmi_b(ARGS.abyb[0], ARGS.abyb[1]))



if __name__ == "__main__":
    main()
