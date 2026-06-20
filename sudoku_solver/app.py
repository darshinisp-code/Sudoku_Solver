from flask import Flask, render_template, request
from solver import solve_sudoku, is_valid

app = Flask(__name__)

# Instructions page
@app.route('/')
def home():
    return render_template('instructions.html')


# Game page (empty grid)
@app.route('/game')
def game():
    return render_template('index.html')


# Solve
@app.route('/solve', methods=['POST'])
def solve():
    grid = []
    original = []

    for i in range(9):
        row = []
        orig_row = []

        for j in range(9):
            value = request.form.get(f'cell{i}{j}')

            if value == '' or value is None:
                row.append(0)
                orig_row.append(0)
            else:
                if not value.isdigit() or not (1 <= int(value) <= 9):
                    return "❌ Enter numbers 1-9 only"

                num = int(value)
                row.append(num)
                orig_row.append(num)

        grid.append(row)
        original.append(orig_row)

    # ✅ VALIDATION FIX
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                num = grid[i][j]
                grid[i][j] = 0

                if not is_valid(grid, i, j, num):
                    return "❌ Invalid input! Duplicate found."

                grid[i][j] = num

    # ✅ SOLVE
    if not solve_sudoku(grid):
        return "❌ No solution exists"

    return render_template('result.html', grid=grid, original=original)


if __name__ == "__main__":
    app.run(debug=True)