# Pathfinding-Algorithm

This is my Python implementation of the A* pathfinding algorithm. The application is written in Python using the <i>Kivy</i> as well as 
<i>PIL</i> (Python Imaging Library) for the GUI. 

# <b>How to use: </b>

-Execute <b>Main.py</b>

-The red/green squares represent the starting/goal node respectively.

-You can move the starting/goal node by clicking on it and then clicking on some desired square (where you want to move the node to).

-You can use the mouse cursor to draw obstacles onto the grid (in yellow).

-You can erase a drawn obstacle square by clicking on it again.

-To start the algorithm, click on the "Start" button.

-Clicking on "Clear" once erases the path drawn by the algorithm.

-Clicking on "Clear" a second time also erases the obstacles.

-Zoom in/out by clicking on the +/- buttons.


# <b>Parameters: </b>

You can change a total of 4 parameters which changes the behaviour of the algorithm:

1) The <i>Horizontal Cost</i> is the cost of traversing one square horizontally/vertically. This cost is 10 by default.

2) The <i>Diagonal Cost</i> is the cost of traversing one square diagonally. This cost is 14 by default. 

With the <i>A* algorithm</i>, each node is assigned 3 values: 

<i>F Cost, G Cost and H Cost </i> (where <i>F Cost = G Cost + H Cost</i>),

which are used to determine the next best node. Specifically, <i>G Cost</i> is the cost from the current node to the starting node and
<i>H Cost</i> is the cost from the current node to the goal node (<i>H Cost</i> is also called the <i>heuristic function</i>). This <i>heuristic function</i> is what differentiates the <i>A* search algorithm</i> from <i>Dijkstra's algorithm</i> as it enables <i>A*</i> to give preference to nodes that are closer to the goal node, which often saves a lot of time.

One unique feature of my implementation is that the <i>G Cost</i> and <i>H Cost</i> is always being multiplied by some value, which you can choose. This "multiplier" enables the user to change the behaviour of the search algorithm dramatically (see example GIFS below):

3) The <i>G Cost Multiplier</i> is the value by which <i>G Cost</i> is multiplied. This value is 1 by default.

4) The <i>H Cost Multiplier</i> is the value by which <i>H Cost</i> is multiplied. This value is 1 by default.


(for more details see: https://en.wikipedia.org/wiki/A*_search_algorithm, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm). 


# <b>Examples: </b>

This is the standard configuration, which is the classic <i>A* search algorithm</i>:

<img src="https://media.giphy.com/media/dt1TPJXvb2JPLClRW8/giphy.gif" width = 400/> 


By setting the <i>H Cost</i> multiplier to 0, you remove the heuristic function which effectively changes the <i>A* algorithm</i> to <i>Dijkstra's algorithm</i>:

<img src="https://media.giphy.com/media/3FfMXksqi4QBYEbTIZ/giphy.gif" width = 400/>

You can also set the <i>G Cost</i> multiplier to 0, which means the algorithm always tries to go into the direction of the goal node first, no matter what:

<img src="https://media.giphy.com/media/Ql0euJ6RWwriRUiWMz/giphy.gif" width = 400/>

You can play around with the <i>G</i> and <i>H Cost</i> multipliers. By increasing the <i>G Cost</i> multiplier, the algorithm stays longer around the start node.
By increasing the <i>H Cost</i> multiplier, the algorithm goes faster into the direction of the goal node:

<img src="https://media.giphy.com/media/pCfpHKxsHeUai3IU6k/giphy.gif" width = 400/> 

You can also change the costs of horizontal/vertical and diagonal traversal. This completely changes how the algorithm searches for a path, but obviously this is often not
the shortest path:

<img src="https://media.giphy.com/media/86pEw8wj5dIfVvaWoN/giphy.gif" width = 400/> <img src="https://media.giphy.com/media/dDaaGqUDDR8gNq77NJ/giphy.gif" width = 400/>
<img src="https://media.giphy.com/media/PFOvIveyaW8gyEvKuE/giphy.gif" width = 400/>

Note: framerate/quality loss due to GIF conversion 

# <b>Dependencies: </b>

-Python 3.8

-Kivy 2.0.0

-PIL (Python Imaging Library)
