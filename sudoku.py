import requests


class Sudoku:

    def __init__(self):
        response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
        grid_info = response.json()["newboard"]["grids"][0]
        self.grid = grid_info["value"]
        self.solution = grid_info["solution"]
