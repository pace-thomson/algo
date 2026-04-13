import time
import random

# ==========================================
# 1. Naive Matrix Multiplication
# ==========================================
def naiveMultiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# ==========================================
# Helper Functions for Matrix Operations
# ==========================================
def add_matrix(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub_matrix(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def split_matrix(matrix):
    n = len(matrix)
    mid = n // 2
    A11 = [row[:mid] for row in matrix[:mid]]
    A12 = [row[mid:] for row in matrix[:mid]]
    A21 = [row[:mid] for row in matrix[mid:]]
    A22 = [row[mid:] for row in matrix[mid:]]
    return A11, A12, A21, A22

def combine_matrix(C11, C12, C21, C22):
    mid = len(C11)
    n = mid * 2
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j+mid] = C12[i][j]
            C[i+mid][j] = C21[i][j]
            C[i+mid][j+mid] = C22[i][j]
    return C

# ==========================================
# 2. Strassen's Matrix Multiplication
# ==========================================
def strassenMultiply(A, B, threshold=32):
    n = len(A)
    
    # Base Case: Switch to naive for small matrices to save overhead
    if n <= threshold:
        return naiveMultiply(A, B)
        
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)
    
    M1 = strassenMultiply(add_matrix(A11, A22), add_matrix(B11, B22), threshold)
    M2 = strassenMultiply(add_matrix(A21, A22), B11, threshold)
    M3 = strassenMultiply(A11, sub_matrix(B12, B22), threshold)
    M4 = strassenMultiply(A22, sub_matrix(B21, B11), threshold)
    M5 = strassenMultiply(add_matrix(A11, A12), B22, threshold)
    M6 = strassenMultiply(sub_matrix(A21, A11), add_matrix(B11, B12), threshold)
    M7 = strassenMultiply(sub_matrix(A12, A22), add_matrix(B21, B22), threshold)
    
    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(add_matrix(sub_matrix(M1, M2), M3), M6)
    
    return combine_matrix(C11, C12, C21, C22)

# ==========================================
# 3. Performance Comparison
# ==========================================
def generate_random_matrix(n):
    return [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]

def check_correctness(C_naive, C_strassen):
    n = len(C_naive)
    for i in range(n):
        for j in range(n):
            if C_naive[i][j] != C_strassen[i][j]:
                return False
    return True

def run_benchmark():
    sizes = [64, 128, 256, 512]
    
    print(f"{'Size':<10} | {'Naïve time (s)':<18} | {'Strassen time (s)':<18} | {'Correct?'}")
    print("-" * 65)
    
    for n in sizes:
        A = generate_random_matrix(n)
        B = generate_random_matrix(n)
        
        # Benchmark Naive
        start_time = time.time()
        C_naive = naiveMultiply(A, B)
        naive_time = time.time() - start_time
        
        # Benchmark Strassen
        start_time = time.time()
        C_strassen = strassenMultiply(A, B)
        strassen_time = time.time() - start_time
        
        # Check Correctness
        is_correct = "Yes" if check_correctness(C_naive, C_strassen) else "No"
        
        # Print row
        print(f"{n:<10} | {naive_time:<18.4f} | {strassen_time:<18.4f} | {is_correct}")

if __name__ == "__main__":
    run_benchmark()