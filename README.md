# Pathfinding-Algorithm

This is my Python implementation of the A* pathfinding algorithm. The application is written in Python using the Kivy GUI library and 
PIL (Python Imaging Library). 

# <b>How to use: </b>

-Execute <b>Main.py</b>

-The red/green squares represent the start/goal nodes respectively

-You can move the start/goal nodes by clicking on them and then clicking on a new square

-You can draw obstacles (in yellow) by clicking and moving your mouse cursor

-You can erase one obstacle square by clicking on it again

-To start the algorithm, click on "Start"

-Clicking on "Clear" once erases the path drawn by the algorithm

-Clicking on "Clear" a second time also erases the obstacles


# <b>Parameters: </b>

You can change a total of 4 parameters which changes the behaviour of the algorithm:

-"Hor. Cost" (Horizontal Cost) is the cost of traversing one square horizontally/vertically. This cost is 10 by default.

-"Diag. Cost" (Diagonal Cost) is the cost of traversing one square diagonally. This cost is 14 by default.

With the A* algorithm, each node is assigned 3 values: 

F Cost, G Cost and H Cost (where F Cost = G Cost + H Cost),

which are used to determine the next best node. Specifically, "G Cost" is the cost from the current node to the start node and
"H Cost" is the cost from the current node to the goal node (H Cost is also called the "heuristic function"). This "heuristic function" is what differentiates the 
"A* search algorithm" from "Dijkstra's algorithm" as it enables A* to go into the direction of the goal node first, which often saves a lot of time.

With my implementation, the G and H Cost is being multiplied by a value which you can choose. This "multiplier" can change the behaviour of the search algorithm dramatically (see example GIFS below):

-"G Cost Mult." (G Cost Multiplier) is the value by which G Cost is multiplied. This value is 1 by default.

-"H Cost Mult." (H Cost Multiplier) is the value by which H Cost is multiplied. This value is 1 by default.


(for more details see: https://en.wikipedia.org/wiki/A*_search_algorithm, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm). 


# <b>Examples: </b>

This is the standard configuration, which is the classic A* search algorithm:

<img src="https://media.giphy.com/media/dt1TPJXvb2JPLClRW8/giphy.gif" width = 400/> 


By setting the "H Cost" to 0, you remove the heuristic function which effectively changes the A* algorithm to Dijkstra's algorithm:

<img src="https://media.giphy.com/media/3FfMXksqi4QBYEbTIZ/giphy.gif" width = 400/>

You can also set the "G Cost" to 0, which means the algorithm always tries to go into the direction of the goal node first:

<img src="https://media.giphy.com/media/Ql0euJ6RWwriRUiWMz/giphy.gif" width = 400/>

You can play around with the G and H Cost multipliers. By increasing the G Cost multiplier, the algorithm stays longer around the start node.
By increasing the H Cost multiplier, the algorithm goes faster into the direction of the goal node:
<img src="https://media.giphy.com/media/pCfpHKxsHeUai3IU6k/giphy.gif" width = 400/> 

You can also change the costs of horizontal/vertical and diagonal traversal. This completely changes how the algorithm searches for a path, but obviously this is often not
the shortest path:

<img src="https://media.giphy.com/media/86pEw8wj5dIfVvaWoN/giphy.gif" width = 400/> <img src="https://media.giphy.com/media/dDaaGqUDDR8gNq77NJ/giphy.gif" width = 400/>
<img src="https://media.giphy.com/media/PFOvIveyaW8gyEvKuE/giphy.gif" width = 400/>



