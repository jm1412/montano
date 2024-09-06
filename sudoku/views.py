import random
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes


def generate_complete_grid():
    """Generate a completely filled Sudoku grid using backtracking."""

    def is_valid(board, row, col, num):
        """Check if a number can be placed at board[row][col]."""
        # Check row and column
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        # Check 3x3 sub-grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def solve(board):
        """Solve the Sudoku board using backtracking."""
        for row in range(9):
            for col in range(9):
                if board[row][col] is None:
                    nums = list(range(1, 10))
                    random.shuffle(nums)  # Shuffle numbers to ensure randomness
                    for num in nums:
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve(board):
                                return True
                            board[row][col] = None  # Reset cell if no solution found
                    return False
        return True

    # Initialize an empty board
    board = [[None for _ in range(9)] for _ in range(9)]
    solve(board)
    return board

def create_sudoku_puzzle(request, numbers_to_remove):
    """Create a Sudoku puzzle by removing numbers from a complete grid."""
    
    def remove_numbers(board, num_remove):
        """Remove a specified number of cells from the board."""
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)  # Randomize cell selection
        for r, c in cells[:num_remove]:
            board[r][c] = None
        return board

    # Validate number of cells to remove
    if not (0 <= numbers_to_remove <= 81):
        return JsonResponse({'error': 'Number of cells to remove must be between 0 and 81'}, status=400)

    # Generate complete board and create puzzle
    board = generate_complete_grid()
    puzzle = remove_numbers(board, numbers_to_remove)
    return JsonResponse({'puzzle': puzzle})

@csrf_exempt
def validate_sudoku_board(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            board = data.get('board')

            # Check if the board is valid
            if board and len(board) == 9 and all(len(row) == 9 for row in board):
                is_valid = is_valid_sudoku(board)
                return JsonResponse({'valid': is_valid, 'completed': True})
            else:
                return JsonResponse({'valid': False, 'completed': False})
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'valid': False, 'completed': False})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def is_valid_sudoku(board):
    def is_valid_unit(unit):
        return len(set(unit)) == len(unit) - unit.count(None)

    # Validate rows
    for row in board:
        if not is_valid_unit(row):
            return False

    # Validate columns
    for col in range(9):
        column = [board[row][col] for row in range(9)]
        if not is_valid_unit(column):
            return False

    # Validate 3x3 subgrids
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = [board[row][col] for row in range(box_row, box_row + 3) for col in range(box_col, box_col + 3)]
            if not is_valid_unit(box):
                return False

    return True