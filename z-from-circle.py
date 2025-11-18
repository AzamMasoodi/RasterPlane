import math
from scipy.optimize import fsolve

def Z_from_circle(L, curve, Z0):
    """
    Compute Z given L and curve (where curve = 100 / radius)
    for points:
        profile like:
      A = (0, 0)
      B = (L/2, (Z*L/2) + (Z*L/4))  # convex version
      C = (L, Z*L)
        Plan like:
      A = (0, 0)
      B = (L/2, (Z*L) + (Z*L/2))  # convex version
      C = (0, 0)
    """

    def distance(p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def curve_from_Z(Z):
        
        '''# Points profile
        A = (0, 0)
        #B = (L/2, (Z*L/2) - (Z*L/4)) for cancave
        B = (L/2, (Z*L/2) + (Z*L/4))
        C = (L, Z*L)'''
        
        # Points plan
        A = (0.0, 0.0)
        #B = (L/2, (Z*L/2) - (Z*L/4)) for cancave
        B = (L / 2.0, (Z * L / 2.0) + (Z * L / 4.0))
        C = (L, 0)  

        AB = distance(A, B)
        BC = distance(B, C)
        AC = distance(A, C)

        s = (AB + BC + AC) / 2
        area = math.sqrt(max(s * (s - AB) * (s - BC) * (s - AC), 0))
        if area == 0:
            return float('inf')

        R = (AB * BC * AC) / (4 * area)
        return 100 / R  # curvature

    # Function whose root we want: difference between target and actual curve
    def func_to_solve(Z):
        return curve_from_Z(Z) - curve

    # Solve for Z
    Z_solution, = fsolve(func_to_solve, Z0)
    return Z_solution


# Example usage:
if __name__ == "__main__":
    L = 200
    curve = 0.029993
    Z0 = 0.0001
    Z = Z_from_circle(L, curve, Z0)
    print(f"The value of Z: {Z:.4f}")


