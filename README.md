# Stacking-Balls-Problem
Two-Dimensional Crystal Growth in a Wedge

This project was made for solving the Model Solvay 2026 Problem Statement which is provided in '00_Problem Statement.pdf'

Files to be used:
1) 01_Stacking Balls.py: Simulates falling balls in a wedge with all physics based assumptions
2) 02_Run.py: Simulates '01_Stacking Balls.py' multiple times.
3) 03_Ways.py: Calculates the number of ways a shape can be acheived.
4) 04_Permute.py: Provides a sequence to the falling crystal
5) 05_Direct.py: Skips animation and assumptions to display the final shape quickly and in accordance to the problem statement.
6) 06_Multi.py: Runs '05_Direct.py' multiple times.
7) 07_Analysis.py: Analyzes the data of experiments with similar conditions

Other Files:
1) Tools.py: Contain utility tools:-
   1) class Cartesian: Defines Cartesian coordinates for pymunk and pygame modules.
   2) class Counter: Generates global counter variable with scope across classes.
   3) class Timer: Manages the clock in the experiments.
2) Simulation.py: Runs and displays the simulation
3) Data: Manages and stores the data from each experiment.
