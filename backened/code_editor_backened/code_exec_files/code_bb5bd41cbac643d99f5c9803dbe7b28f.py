import numpy as np

def print_menu():
    """Print the menu of available operations."""
    print("\n==== Matrix Operations Menu ====")
    print("1. Display the matrix")
    print("2. Get matrix dimensions")
    print("3. Calculate transpose")
    print("4. Calculate determinant")
    print("5. Calculate inverse")
    print("6. Calculate eigenvalues and eigenvectors")
    print("7. Calculate matrix rank")
    print("8. Calculate trace (sum of diagonal elements)")
    print("9. Enter a second matrix")
    print("10. Add matrices")
    print("11. Subtract matrices")
    print("12. Multiply matrices")
    print("13. Perform element-wise multiplication")
    print("14. Solve system of linear equations (Ax = b)")
    print("15. Calculate matrix power")
    print("16. Normalize matrix (divide by norm)")
    print("17. Calculate matrix norm")
    print("18. Exit")
    print("==============================")

def get_matrix_from_user():
    """Get matrix dimensions and elements from user input."""
    try:
        rows = int(input("Enter number of rows: "))
        cols = int(input("Enter number of columns: "))
        
        if rows <= 0 or cols <= 0:
            print("Error: Dimensions must be positive integers")
            return None
        
        matrix = []
        print(f"Enter the matrix elements row by row ({rows}x{cols}):")
        
        for i in range(rows):
            while True:
                try:
                    # Get row input and convert to list of floats
                    row_input = input(f"Enter row {i+1} elements separated by spaces: ")
                    row = [float(x) for x in row_input.split()]
                    
                    if len(row) != cols:
                        print(f"Error: You must enter exactly {cols} elements for this row")
                        continue
                    
                    matrix.append(row)
                    break
                except ValueError:
                    print("Error: Please enter valid numbers")
        
        return np.array(matrix)
    
    except ValueError:
        print("Error: Please enter valid integers for dimensions")
        return None

def display_matrix(matrix):
    """Display the matrix in a formatted way."""
    if matrix is None:
        print("No matrix to display")
        return
    
    print("\nMatrix:")
    print(matrix)

def matrix_dimensions(matrix):
    """Get and display matrix dimensions."""
    if matrix is None:
        print("No matrix available")
        return
    
    rows, cols = matrix.shape
    print(f"Matrix dimensions: {rows}x{cols}")

def matrix_transpose(matrix):
    """Calculate and display the transpose of the matrix."""
    if matrix is None:
        print("No matrix available")
        return None
    
    transpose = matrix.T
    print("Matrix transpose:")
    print(transpose)
    return transpose

def matrix_determinant(matrix):
    """Calculate and display the determinant of the matrix."""
    if matrix is None:
        print("No matrix available")
        return
    
    if matrix.shape[0] != matrix.shape[1]:
        print("Error: Determinant can only be calculated for square matrices")
        return
    
    try:
        det = np.linalg.det(matrix)
        print(f"Determinant: {det}")
    except np.linalg.LinAlgError:
        print("Error: Could not calculate determinant")

def matrix_inverse(matrix):
    """Calculate and display the inverse of the matrix."""
    if matrix is None:
        print("No matrix available")
        return None
    
    if matrix.shape[0] != matrix.shape[1]:
        print("Error: Inverse can only be calculated for square matrices")
        return None
    
    try:
        inverse = np.linalg.inv(matrix)
        print("Matrix inverse:")
        print(inverse)
        return inverse
    except np.linalg.LinAlgError:
        print("Error: Matrix is singular, cannot calculate inverse")
        return None

def matrix_eigenvalues(matrix):
    """Calculate and display eigenvalues and eigenvectors."""
    if matrix is None:
        print("No matrix available")
        return
    
    if matrix.shape[0] != matrix.shape[1]:
        print("Error: Eigenvalues can only be calculated for square matrices")
        return
    
    try:
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        print("Eigenvalues:")
        print(eigenvalues)
        print("\nEigenvectors:")
        print(eigenvectors)
    except np.linalg.LinAlgError:
        print("Error: Could not calculate eigenvalues and eigenvectors")

def matrix_rank(matrix):
    """Calculate and display the rank of the matrix."""
    if matrix is None:
        print("No matrix available")
        return
    
    rank = np.linalg.matrix_rank(matrix)
    print(f"Matrix rank: {rank}")

def matrix_trace(matrix):
    """Calculate and display the trace of the matrix."""
    if matrix is None:
        print("No matrix available")
        return
    
    if matrix.shape[0] != matrix.shape[1]:
        print("Error: Trace can only be calculated for square matrices")
        return
    
    trace = np.trace(matrix)
    print(f"Matrix trace: {trace}")

def add_matrices(matrix1, matrix2):
    """Add two matrices and display the result."""
    if matrix1 is None or matrix2 is None:
        print("Error: Both matrices must be available")
        return None
    
    if matrix1.shape != matrix2.shape:
        print("Error: Matrices must have the same dimensions for addition")
        return None
    
    result = matrix1 + matrix2
    print("Result of matrix addition:")
    print(result)
    return result

def subtract_matrices(matrix1, matrix2):
    """Subtract matrix2 from matrix1 and display the result."""
    if matrix1 is None or matrix2 is None:
        print("Error: Both matrices must be available")
        return None
    
    if matrix1.shape != matrix2.shape:
        print("Error: Matrices must have the same dimensions for subtraction")
        return None
    
    result = matrix1 - matrix2
    print("Result of matrix subtraction (matrix1 - matrix2):")
    print(result)
    return result

def multiply_matrices(matrix1, matrix2):
    """Multiply matrix1 by matrix2 and display the result."""
    if matrix1 is None or matrix2 is None:
        print("Error: Both matrices must be available")
        return None
    
    try:
        result = np.matmul(matrix1, matrix2)
        print("Result of matrix multiplication (matrix1 @ matrix2):")
        print(result)
        return result
    except ValueError:
        print("Error: Matrix dimensions are not compatible for multiplication")
        print(f"Matrix 1 shape: {matrix1.shape}, Matrix 2 shape: {matrix2.shape}")
        print("For multiplication, the number of columns in the first matrix must equal the number of rows in the second matrix")
        return None

def element_wise_multiply(matrix1, matrix2):
    """Perform element-wise multiplication of two matrices."""
    if matrix1 is None or matrix2 is None:
        print("Error: Both matrices must be available")
        return None
    
    if matrix1.shape != matrix2.shape:
        print("Error: Matrices must have the same dimensions for element-wise multiplication")
        return None
    
    result = matrix1 * matrix2
    print("Result of element-wise multiplication:")
    print(result)
    return result

def solve_linear_system(matrix, b_vector=None):
    """Solve the system of linear equations Ax = b."""
    if matrix is None:
        print("Error: Matrix must be available")
        return
    
    if matrix.shape[0] != matrix.shape[1]:
        print("Error: Coefficient matrix must be square")
        return
    
    # If b_vector is not provided, ask user to input it
    if b_vector is None:
        try:
            n = matrix.shape[0]
            print(f"Enter the b vector ({n} elements):")
            b_input = input("Enter values separated by spaces: ")
            b_vector = np.array([float(x) for x in b_input.split()])
            
            if len(b_vector) != n:
                print(f"Error: b vector must have {n} elements")
                return
        except ValueError:
            print("Error: Please enter valid numbers")
            return
    
    try:
        x = np.linalg.solve(matrix, b_vector)
        print("Solution x for Ax = b:")
        print(x)
    except np.linalg.LinAlgError:
        print("Error: System is singular or not solvable")

def matrix_power(matrix):
    """Calculate a power of the matrix."""
    if matrix is None:
        print("Error: Matrix must be available")
        return None
    
    if matrix.shape[0] != matrix.shape[1]:
        print("Error: Matrix must be square to calculate powers")
        return None
    
    try:
        power = int(input("Enter the power (integer): "))
        result = np.linalg.matrix_power(matrix, power)
        print(f"Matrix raised to power {power}:")
        print(result)
        return result
    except ValueError:
        print("Error: Please enter a valid integer")
        return None
    except np.linalg.LinAlgError:
        print("Error: Could not calculate matrix power")
        return None

def normalize_matrix(matrix):
    """Normalize the matrix by dividing by its Frobenius norm."""
    if matrix is None:
        print("Error: Matrix must be available")
        return None
    
    norm = np.linalg.norm(matrix)
    
    if norm == 0:
        print("Error: Matrix norm is zero, cannot normalize")
        return None
    
    normalized = matrix / norm
    print("Normalized matrix:")
    print(normalized)
    print(f"Verification - norm of normalized matrix: {np.linalg.norm(normalized)}")
    return normalized

def matrix_norm(matrix):
    """Calculate and display various matrix norms."""
    if matrix is None:
        print("Error: Matrix must be available")
        return
    
    frobenius_norm = np.linalg.norm(matrix, 'fro')
    print(f"Frobenius norm: {frobenius_norm}")
    
    if matrix.shape[0] == matrix.shape[1]: # Only for square matrices
        spectral_norm = np.linalg.norm(matrix, 2)
        print(f"Spectral norm (largest singular value): {spectral_norm}")
    
    nuclear_norm = np.linalg.norm(matrix, 'nuc')
    print(f"Nuclear norm (sum of singular values): {nuclear_norm}")
    
    infinity_norm = np.linalg.norm(matrix, np.inf)
    print(f"Infinity norm (maximum absolute row sum): {infinity_norm}")
    
    one_norm = np.linalg.norm(matrix, 1)
    print(f"1-norm (maximum absolute column sum): {one_norm}")

def main():
    """Main function to run the matrix calculator."""
    print("Welcome to the Matrix Operations Calculator!")
    
    # Get the first matrix from user
    matrix1 = get_matrix_from_user()
    matrix2 = None  # Initialize second matrix as None
    
    if matrix1 is None:
        print("Failed to create matrix. Exiting.")
        return
    
    choice = 0
    while choice != 18:
        print_menu()
        
        try:
            choice = int(input("Enter your choice (1-18): "))
            
            if choice == 1:
                display_matrix(matrix1)
            elif choice == 2:
                matrix_dimensions(matrix1)
            elif choice == 3:
                matrix_transpose(matrix1)
            elif choice == 4:
                matrix_determinant(matrix1)
            elif choice == 5:
                matrix_inverse(matrix1)
            elif choice == 6:
                matrix_eigenvalues(matrix1)
            elif choice == 7:
                matrix_rank(matrix1)
            elif choice == 8:
                matrix_trace(matrix1)
            elif choice == 9:
                print("\nEntering second matrix:")
                matrix2 = get_matrix_from_user()
                if matrix2 is not None:
                    print("Second matrix entered successfully")
            elif choice == 10:
                if matrix2 is None:
                    print("Error: Second matrix not available. Please enter it first (option 9)")
                else:
                    add_matrices(matrix1, matrix2)
            elif choice == 11:
                if matrix2 is None:
                    print("Error: Second matrix not available. Please enter it first (option 9)")
                else:
                    subtract_matrices(matrix1, matrix2)
            elif choice == 12:
                if matrix2 is None:
                    print("Error: Second matrix not available. Please enter it first (option 9)")
                else:
                    multiply_matrices(matrix1, matrix2)
            elif choice == 13:
                if matrix2 is None:
                    print("Error: Second matrix not available. Please enter it first (option 9)")
                else:
                    element_wise_multiply(matrix1, matrix2)
            elif choice == 14:
                solve_linear_system(matrix1)
            elif choice == 15:
                matrix_power(matrix1)
            elif choice == 16:
                normalize_matrix(matrix1)
            elif choice == 17:
                matrix_norm(matrix1)
            elif choice == 18:
                print("Exiting the Matrix Calculator. Goodbye!")
            else:
                print("Invalid choice. Please enter a number between 1 and 18.")
        
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()