## Starting Point 
## This is a robust vector projection function including all factors such as: 
## direction, magnitude, edge cases, and dimensionality checks 

## Key aspects to include: 
### 1. Input Validation and Error Handling 
### 2. Performance Optimization 
### --> For large vectors or repeated projections --> cache intermediate results like norm squared
### 3. Precision and Floating Point Issues 
### 4. Documentation and Testing --> write tests to cover edge cases such as zero vectors, orthogonal vectors and vegtors with negative components

from typing import List, Union # Are we allowed to use this?? 
def dot(a: List[Union[int, float]], b: List[Union[int, float]]) -> float:
    # Compute the dot product of two vectors 
    # Raise ValueError if dimensions do not match or inputs are invalid
    if not (isinstance(a, list) and isinstance(b, list)):
        raise TypeError("Inputs much be lists")
    if len(a) != len(b):
        raise ValueError("Vectors must be the same dimension")
    return sum(x*y for x, y in zip(a, b))

def norm_sq(v: List[Union[int, float]]) -> float:
    # Return the squared norm of vector v
    return dot(v, v)

def is_zero(v: List[Union[int, float]], tol: float = 1e-12) -> bool:
    # Check if vector v is effectively zero within a tolerance
    return all(x == 0 for x in v)

def proj(v: List[Union[int, float]], u: List[Union[int, float]]) -> List[float]:
    # Project vector v onto vector u
    # Return the projection vector
    # Edge case: zero vector
    if is_zero(u):
        return ValueError("Connot project into the zero vector.")
    # Projection formula
    scalar = dot(v, u) / norm_sq(u)
    return [scalar * x for x in u]

def rejection(v, u):
    # Orthogonal component
    # V is relative to u --> (v - projection of v onto u)
    p = proj(v, u)
    return [x - y for x, y in zip(v, p)]

# Example Unit Tests
if __name__ == "__main__":
    # Test vectors
    v1 = [3.0, 4.0]
    u1 = [1.0, 0.0]

    projection1 = proj(v1, u1)
    orthogonal1 = rejection(v1, u1)

    print("Projection of v1 onto u1:", projection1)
    print("Orthogonal component of v1 to u1:", orthogonal1)

    # Edge case: zero vector
    try:
        proj(v1, [0.0, 0.0])
    except ValueError as e:
        print("Caught error:", e)

    # Dimension mismatch
    try:
        proj([1, 2], [1, 2, 3])
    except ValueError as e:
        print("Caught error:", e)
