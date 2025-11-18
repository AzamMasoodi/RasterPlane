import math

def circle_from_Z(L, Z):
    """
    Compute the radius and curvature of a circle with three points:
      A = (0, 0)
      B = (L/2, (Z*L/2) + (Z*L/4)) for convex
      or
      B = (L/2, (Z*L/2) - (Z*L/4)) for concave
      C = (L, Z*L)
    
    Input: L , Z
    Output: r, curve

    """

    ''' # Points profile
    A = (0.0, 0.0)
    #B = (L/2, (Z*L/2) - (Z*L/4))
    B = (L / 2.0, (Z * L / 2.0) + (Z * L / 4.0))
    C = (L, Z * L)'''
    
    # Points plan
    A = (0.0, 0.0)
    #B = (L/2, (Z*L/2) - (Z*L/4))
    B = (L / 2.0, (Z * L / 2.0) + (Z * L / 4.0))
    C = (L, 0)

    # distance between two points
    def distance(p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    # Side lengths
    AB = distance(A, B)
    BC = distance(B, C)
    AC = distance(A, C)

    # Semi-perimeter
    s = (AB + BC + AC) / 2

    # Area (Heron's formula)
    area = math.sqrt(s * (s - AB) * (s - BC) * (s - AC))

    # radius
    radius = (AB * BC * AC) / (4 * area)

    # Curve (here scaled by 100 as in method)
    curve = 100 / radius

    return radius, curve


# Example usage:
if __name__ == "__main__":
    L = 25
    Z = 0.01
    radius, curve = circle_from_Z(L, Z)
    print(f"Radius = {radius:.6f}")
    print(f"Curvature = {curve:.6f}")
    

