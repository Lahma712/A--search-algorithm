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

One unique feature of my implementation is that the <i>H Cost</i> is always being multiplied by some weight (<i>heuristic weight</i>), which the user can change. This weight enables the user to change the behaviour of the search algorithm, so actually:

<i>F Cost = G Cost + H Cost * Weight</i>

(for more details see: https://en.wikipedia.org/wiki/A*_search_algorithm, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm). 


# <b>Preview: </b>

- This is the standard configuration, which is the classic <i>A* search algorithm</i>. The <i>heuristic weight</i> is set to 1. With this heuristic, the shortest path
will always be found.
You can also choose from 3 distance metrics: <i>Euclidean</i>, <i>Manhattan</i> and <i>Chebyshev</i>. 

<b><i>Euclidean:</i></b>

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/2e0c9ce1b3455cb9e92c6bad6684dbda02f69c82" width = 400/>

<img src="https://media.giphy.com/media/9yONohNwZvvVEqcKur/giphy.gif" width = 400/>

<b><i>Manhattan:</i></b>

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/02436c34fc9562eb170e2e2cfddbb3303075b28e" width = 400/>

<img src="https://media.giphy.com/media/RtlKjZVBKZdYlXktCO/giphy.gif" width = 400/>

<b><i>Chebyshev:</i></b>


<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/1e41856e4c8dfd7e69948b55735d4464113b9e7e" width = 400/>

<img src="https://media.giphy.com/media/iVC1VIJdMpScqgbfkO/giphy.gif" width = 400/>


- By setting the <i>heuristic weight</i> to 0, you remove the heuristic function which reverts the <i>A* algorithm</i> back to <i>Dijkstra's algorithm</i> which is essentially still <i>A*</i>, just without the <i>H Cost</i>/<i>heuristic</i>. <i>Dijkstra's algorithm</i> will always find the shortest path, although it will take substantially longer than <i>A*</i>:

<img src="https://media.giphy.com/media/h9PdmF5V5LHIpvKEHh/giphy.gif" width = 400/>

-By increasing the <i>heuristic weight</i>, the algorithm prioritizes nodes that are closer to the goal node. Effectively, the algorithm will spend less time exploring other directions which will result in a shorter runtime, however it may not find the shortest path that exists.
This behaviour will usually become increasingly apparent as
you set the <i>heuristic weight >1</i>. 


Below is the evolution of the algorithm with <i>heuristic weights</i> <b>0, 0.2, 0.8, 1, 1.2, 1.5 and 10 </b>. 

<img src="https://media.giphy.com/media/h9PdmF5V5LHIpvKEHh/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/jkskxPqNFut7WqFjgR/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/EQWoN6goocESFPOwbt/giphy.gif" width = 250/> 
<img src="https://media.giphy.com/media/9yONohNwZvvVEqcKur/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/dMFJ9G9WD0r6NfEkUI/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/omwJ3yMbsZF6e5lORf/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/F4bd3oMB78JcZfmW4A/giphy.gif" width = 250/> 

One can see that when the weight is <b>10</b>, the path is clearly
not the shortest one that exists. This is confirmed by looking at the terminal where the total cost is being printed. For weights <b>0, 0.2, 0.8, 1, 1.2 and 1.5</b> the cost is 
<b>232</b>, however for weight <b>10</b>, the cost is <b>256</b>. While the path is more expensive, it is found faster than the others.

We can draw a general conclusion from this:

- A smaller <i>heuristic weight</i> results in a longer runtime but cheaper path
- A bigger <i>heuristic weight</i> results in a smaller runtime but more expensive path



# <b>Practical example:</b>

This is a labyrinth that I drew. 
The respective costs are <b>1060</b> (weight: <b>1.0</b>), <b>1142</b> (weight: <b>10.0</b>) and <b>1388</b> (weight: <b>100.0</b>):

<img src="https://media.giphy.com/media/0BRBAHu7MwLqVZJyyf/giphy.gif" width = 400/> <img src="https://media.giphy.com/media/wMIM2oyrccVVVl3vCF/giphy.gif" width = 400/> 
<img src="https://media.giphy.com/media/XLZDEH5dPCmaMVp3Pc/giphy.gif" width = 400/>


Note: framerate/quality loss due to GIF conversion 

# <b>Dependencies: </b>

-Python 3.8

-Kivy 2.0.0

-PIL (Python Imaging Library)

# <b>Sources:</b>
- https://en.wikipedia.org/wiki/A*_search_algorithm
- https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- https://www.youtube.com/watch?v=-L-WgKMFuhE
- http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
- https://qiao.github.io/PathFinding.js/visual/
- https://www.redblobgames.com/pathfinding/a-star/introduction.html
- https://wikimedia.org/api/rest_v1/media/math/render/svg/2e0c9ce1b3455cb9e92c6bad6684dbda02f69c82
- https://wikimedia.org/api/rest_v1/media/math/render/svg/02436c34fc9562eb170e2e2cfddbb3303075b28e
- https://wikimedia.org/api/rest_v1/media/math/render/svg/1e41856e4c8dfd7e69948b55735d4464113b9e7e
