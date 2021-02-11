# Pathfinding-Algorithm

This is my Python implementation of the A* pathfinding algorithm. The application is written in Python using <i>Kivy</i> as well as 
<i>PIL</i> (Python Imaging Library) for the GUI. 

# <b>How to use: </b>

- Execute <b>Main.py</b>
- The red/green squares represent the starting/goal node respectively.
- You can move the starting/goal node by clicking on it and then clicking on some desired square (where you want to move the node to).
- You can use the mouse cursor to draw obstacles onto the grid (in yellow).
- You can erase a drawn obstacle square by clicking on it again.
- To start the algorithm, click on the "Start" button.
- Clicking on "Clear" once erases the path drawn by the algorithm.
- Clicking on "Clear" a second time also erases the obstacles.
- Zoom in/out by clicking on the +/- buttons.
- After the path has been traced, the total cost is printed in the terminal.


# <b>How it works: </b>

Each cell on the grid, also called a "node" can be:

- "Explored", node that the algorithm already visited (neon pink cells)
- "Unavailable", node that the algorithm has not seen yet (black cells)
- "Available", node that the algorithm is aware of but hasn't visited/explored yet (dark pink cells)

There are also obstacle cells (yellow cells) which the algorithm cannot visit. 
Upon finding the goal node, the path is traced back to the starting node.

When a node becomes "available", it is assigned 3 values:

- <i>F Cost, G Cost and H Cost </i>, where <i>F Cost = G Cost + H Cost</i>,
- <i>G Cost</i> is the cost from that node to the starting node.
- <i>H Cost</i> is the approximated cost from that node to the goal node. (also called the <i>heuristic function</i>)

This <i>heuristic function</i> will allow <i>A*</i> to give preference to nodes that are closer to the goal node, which saves a lot of time.

Each frame, the algorithm will look at all the "available" nodes and visit/explore the one with the lowest <i>F Cost</i>. Doing this will keep the overall cost of the path as low as possible, which will give you the shortest path (although only under certain conditions, as we'll see).

One unique feature of my implementation is that the <i>H Cost</i> is always being multiplied by some weight, which the user can change. This weight enables the user to change the behaviour of the search algorithm, so actually:

<i>F Cost = G Cost + H Cost * Weight</i>

(for more details see: https://en.wikipedia.org/wiki/A*_search_algorithm, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm). 


# <b>Examples: </b>

- This is the standard configuration, which is the classic <i>A* search algorithm</i>. The <i>heuristic weight</i> is set to 1. With this heuristic, the shortest path
will always be found.
You can also choose from 3 distance metrics: <i>Euclidean</i>, <i>Manhatten</i> and <i>Chebyshev</i>. 

<b><i>Euclidean:</i></b>

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/2e0c9ce1b3455cb9e92c6bad6684dbda02f69c82" width = 400/>

<img src="https://media.giphy.com/media/9yONohNwZvvVEqcKur/giphy.gif" width = 400/>

<b><i>Manhattan:</i></b>

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/02436c34fc9562eb170e2e2cfddbb3303075b28e" width = 400/>

<img src="https://media.giphy.com/media/RtlKjZVBKZdYlXktCO/giphy.gif" width = 400/>

<b><i>Chebyshev:</i></b>

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/1e41856e4c8dfd7e69948b55735d4464113b9e7e" width = 400/>

<img src="https://media.giphy.com/media/iVC1VIJdMpScqgbfkO/giphy.gif" width = 400/>


- By setting the <i>heuristic weight</i> to 0, you remove the heuristic function which effectively reverts the <i>A* algorithm</i> to the <i>Dijkstra's algorithm</i>. <i>Dijkstra's algorithm</i> will always find the shortest path:

<img src="https://media.giphy.com/media/h9PdmF5V5LHIpvKEHh/giphy.gif" width = 400/>

- By increasing the <i>heuristic weight</i>, the algorithm effectively gives more preference to nodes that make it go into the direction of the goal node. Effectively, the algorithm will spend less time exploring other directions which will make it find a possible path in a shorter amount of time, however it may not be the shortest path that exists. This behaviour will become apparent when you set the <i>heuristic weight > 1</i>:

<img src="https://media.giphy.com/media/Ql0euJ6RWwriRUiWMz/giphy.gif" width = 400/>

You can play around with the <i>G</i> and <i>H Cost</i> multipliers. By increasing the <i>G Cost</i> multiplier, the algorithm stays longer around the starting node.
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
