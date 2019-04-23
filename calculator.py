import math, argparse, numpy, decimal
from fractions import Fraction
def parseall():
    parser = argparse.ArgumentParser(description="Calculator")
    parser.add_argument("-a", "--angle", metavar="Float",default=None, dest='angle', help="L'angle à convertir, il faut définir l'unité après la valeur (deg ou rad)")
    parser.add_argument("-dp", "--dotproduct",nargs='+',default=None, type= tuple, dest='dproduct', help='Calcule le produit scalaire, prends des vecteurs en entrée')
    parser.add_argument("-q", "--quadratic",nargs='+',default=None, dest='quad',type=float,help="Calcule les zéros d'une fonction quadratique")
    parser.add_argument("-f", "--fraction",metavar="Float", default=None, dest='fraction', type=float, help="Calcule la fraction associée à un chiffre decimal")
    return parser.parse_args()


class Calculator():
    def __init__(self):
        self.memory = 0
        self.pi = math.pi
    def getfraction(self, decimal):
        return str(Fraction(decimal))
    def getcrossproduct(self):
        pass
    def getdotproduct(self):
        pass
    def dotproduct(self, vector_list):
        return sum(i*j for i,j in zip(vector_list[0],  vector_list[1]))
    def crossproduct(self, vector_list):
        return numpy.cross(vector_list[0], vector_list[1])
    def getangle(self, angle):
        if "rad" in str(angle):
            print("Angle : {} is {} deg".format(angle,calc.radtodeg(angle)))
        elif "deg" in str(angle):
            print("Angle : {} is {} rad".format(angle, calc.degtorad(angle)))
        else:
            print("y dude")
    def degtorad(self, angle):
        return(2*self.pi*self.extractfloat(angle)/360)
    def radtodeg(self, angle):
        return(360*self.extractfloat(angle)/(self.pi*2))
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

if __name__ == "__main__":
    ARGS = parseall()
    calc = Calculator()
    if ARGS.angle is not None:
        calc.getangle(ARGS.angle)
    elif ARGS.dproduct is not None:
        calc.getdotproduct()
    elif ARGS.quad is not None:
        calc.getzeros(ARGS.quad[0], ARGS.quad[1], ARGS.quad[2])
    elif ARGS.fraction is not None:
        calc.getfraction(ARGS.fraction)
