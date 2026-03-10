import numpy as np

def multiply_matrices(matrix_a, matrix_b):
    """
    Multiplies two matrices using numpy.
    Input: lists of lists (2D arrays)
    Output: result as list of lists + summary
    """
    try:
        # Convert to numpy arrays
        A = np.array(matrix_a, dtype=float)
        B = np.array(matrix_b, dtype=float)

        # Check if multiplication is possible
        if A.shape[1] != B.shape[0]:
            return {
                "status": "error",
                "message": f"Invalid dimensions: A is {A.shape}, B is {B.shape} — columns of A must match rows of B"
            }

        # Perform multiplication
        result = np.dot(A, B)

        # Convert back to list for JSON serialization
        result_list = result.tolist()

        return {
            "status": "success",
            "result_matrix": result_list,
            "shape": result.shape,
            "dimensions": f"{A.shape} x {B.shape} → {result.shape}",
            "note": "Result computed using numpy.dot"
        }

    except ValueError as ve:
        return {"status": "error", "message": f"Value error: {str(ve)}"}
    except Exception as e:
        return {"status": "error", "message": f"Computation failed: {str(e)}"}
