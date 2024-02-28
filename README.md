# Amado-Heuristic-Search-IA-23-24


## Problem Specification

Amado is a single-player, keyboard controlled puzzle game. The game is played on a puzzle grid in which each of the cells is coloured red,blue,yellow. Using the keyboard, the player must move from cell to cell changing the colors of the destination cell based on a combination of both original colors between the move done. The objective of the game is to replicate the pattern of a given board in our own randomnized grid. This also needs to be done before the time limit is reached !

## Problem Formulation

### State Representation
We have a matrix/grid (NxN) composed of squares with 3 different colors(Red,Yellow,Blue)
### Initial State
The initial state is composed essentially by a randomly generated grid with a balanced distribution of colors, a timer and move counter that are both set to 0 and the pre-selected starting square/cell that the player is able to play(this should be the top-left corner cell).

### Objective Test
The objective test checks if the current state meets the criteria to win the game, in our case, this test should verify if all the square colors on the grid match exactly the pre-defined "solution" grid. Basically, examines if the player successfully managed to replicate the wanted end grid. There is also a time limit for each puzzle so 

### Operators   
```
Name     |         Effects         

moveUp   | Move the selected square one cell upward and 
         |  switch the destination cell color


moveDown | Move the selected square one cell downward and
         |  switch the destination cell color


moveLeft | Move the selected square one cell to the left and 
         |  switch the destination cell color


moveRight| Move the selected square one cell to the right and 
         |   switch the destination cell color
```
The precondition of all these operators should be simply that it must exist another cell/square for the current/selected cell to move to.
The cost related to each one of these operators is 1



## Heuristics (Ver e discutir !)

Heuristic 1 - Color Matching:
    This heuristic evaluates the similarity between the colors of the current grid state and the end state. It iterates over each cell in the grid and compares the color of each cell with the corresponding cell in the end state. For every cell where the colors match, the heuristic increments a counter. The final heuristic value represents the number of cells in the grid where the colors match exactly with the end state. This heuristic provides a basic measure of similarity between the current state and the desired end state in terms of color distribution.

Heuristic 2 - Color Neighbours Analysis:
    This heuristic analyzes the influence of different colors on neighboring cells and potential color transitions. It considers the presence of certain colors and their impact on the likelihood of transitioning to other colors. By evaluating how color choices affect neighboring cells, this heuristic guides the search algorithm towards moves that lead to favorable color transitions and maintain beneficial color distributions across the grid. Moves that minimize disruptions to the desired color patterns and maximize progress towards the end state are prioritized.


## Work being done
Programming language selected : Python
Development Environment: VSCode 
Data Structures: Classes for game board + menu +  more to define


## References

https://www.mobygames.com/game/141808/amado/