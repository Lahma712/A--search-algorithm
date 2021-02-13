# Pathfinding-Algorithm

This is my Python implementation of the A* pathfinding algorithm. The application is written in Python using <i>Kivy</i> as well as 
<i>PIL</i> (Python Imaging Library) for the GUI. 

# <b>How to use: </b>

<b>Download the latest release</b> and follow the instructions <b>or download the source code</b> and run the <i>Main.py</i> from an IDE 
- The red/green squares represent the starting/goal node respectively.
- You can move the starting/goal node by clicking on it and then clicking on some desired square (where you want to move the node to).
- You can use the mouse cursor to draw obstacles onto the grid (in yellow).
- You can erase a drawn obstacle square by clicking on it again.
- To start the algorithm, click on the "Start" button.
- Clicking on "Clear" once erases the path drawn by the algorithm.
- Clicking on "Clear" a second time also erases the obstacles.
- Zoom in/out by clicking on the +/- buttons.
- You can select one of the distance metrics by clicking on the respective button (Euclidean, Manhattan, Chebyshev)
- You can enter a new heuristic weight into the input box
- After the path has been traced, the total cost is being shown in the "Path Cost" box


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

Each frame, the algorithm will look at all the "available" nodes and visit/explore the one with the lowest <i>F Cost</i>. This will then repeat until the algorithm has arrived at the goal node. Generally, by always picking the lowest <i>F Cost</i>, the overall cost of the path will be kept as low as possible, which will find you the shortest path (although only under certain conditions, as we'll see). 

One unique feature of my implementation is that the <i>H Cost</i> is always being multiplied by some weight (<i>heuristic weight</i>), which the user can change. This weight enables the user to change the behaviour of the search algorithm, so actually:

<i>F Cost = G Cost + H Cost * Weight</i>

(for more details see: https://en.wikipedia.org/wiki/A*_search_algorithm, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm). 


# <b>Features: </b>

- This is the standard configuration, which is the classic <i>A* search algorithm</i>. The <i>heuristic weight</i> is set to 1. With this heuristic, the shortest path
will always be found.
You can also choose from 3 distance metrics, which are used to calculate the distance
between two nodes: <i>Euclidean</i>, <i>Manhattan</i> and <i>Chebyshev</i>.

(Note: these GIFS are not representative of the real framerate/resolution of the application, due to image compression)

<b><i>Euclidean:</i></b>

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/2e0c9ce1b3455cb9e92c6bad6684dbda02f69c82" width = 400/>

<img src="https://media.giphy.com/media/f110ff3f73CgkjiNdm/giphy.gif" width = 400/>

<b><i>Manhattan:</i></b>

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/02436c34fc9562eb170e2e2cfddbb3303075b28e" width = 400/>

<img src="https://media.giphy.com/media/Px5fGcRrnZJi6hXOF4/giphy.gif" width = 400/>

<b><i>Chebyshev:</i></b>


<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/1e41856e4c8dfd7e69948b55735d4464113b9e7e" width = 400/>

<img src="https://media.giphy.com/media/32fixG6E1i1hoiOFpY/giphy.gif" width = 400/>


- By setting the <i>heuristic weight</i> to 0, you remove the heuristic function. This reverts the <i>A* algorithm</i> back to <i>Dijkstra's algorithm</i> which essentially is still <i>A*</i>, just without the <i>H Cost</i>/<i>heuristic</i>. <i>Dijkstra's algorithm</i> will always find the shortest path, although it will take substantially longer than <i>A*</i>:

<img src="https://media.giphy.com/media/3HeVeKFrYq4MBhABfa/giphy.gif" width = 400/>

- By changing the <i>heuristic weight</i>, the algorithm behaves differently. But why?

As described above, <i>F Cost = G Cost + H Cost * Weight</i>

Each frame, the algorithm will explore the node with the lowest <i>F Cost</i>. 

If we set the <i>heuristic weight > 1</i>, the <i>H Cost * Weight</i> term will start to "outweigh" the <i>G Cost</i>. This means that each frame, the node with the lowest <i>F Cost</i> will likely just be the one with the lowest <i>H Cost</i> (closest to the goal node). The more we increase the <i>heuristic weight</i>, the more <i>G Cost</i> becomes negligeable. What does this mean in practice?

Effectively, the algorithm will spend less time exploring other directions (that don't go into the direction of the goal node) which will often result in a shorter runtime, however it may not find the shortest path that exists anymore.
This behaviour will become increasingly apparent as the <i>heuristic weight</i> gets bigger. 

If we set the <i>heuristic weight < 1</i>, the <i>G Cost</i> will start to "outweigh" the <i>H Cost * Weight</i> term. Each frame. the node with the lowest <i>F Cost</i> will likely just be the one with the lowest <i>G Cost</i> (closest to the starting node). As expected, the more we decrease the <i>heuristic weight</i>, the more <i>H Cost</i> becomes negligeable. In practice, the algorithm will prioritize nodes that are closer to the starting node, making it explore nodes more "radially" into every direction. This has the advantage that the algorithm is more likely to find the shortest path, however the runtime is often longer.

With a <i>heuristic weight = 1</i>, neither the <i>G Cost</i>, nor the <i>H Cost</i> are more important than the other. In fact, they are inversely proportional and balance each other out as when the algorithm comes closer to the goal node, the <i>H Cost</i> decreases while the <i>G Cost</i> increases by the same factor. This is the standard <i>A* algorithm</i>.

The changes in behaviour are gradual. Below is the evolution of the algorithm with <i>heuristic weights</i> <b>0</b>, <b>0.2</b>, <b>0.8</b>, <b>1</b>, <b>1.2</b>, <b>1.5</b> and <b>10 </b>. 

<img src="https://media.giphy.com/media/3HeVeKFrYq4MBhABfa/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/324TGzP2vE4ayM03Vz/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/KibQNZMbxd40pXjr22/giphy.gif" width = 250/> 
<img src="https://media.giphy.com/media/f110ff3f73CgkjiNdm/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/RrqTBgtSXVu7mu9iBI/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/btyfFUup4sxunhfTyP/giphy.gif" width = 250/> <img src="https://media.giphy.com/media/m3yC0SAWB7vo9aKpcX/giphy.gif" width = 250/> 

One can see that when the weight is <b>10</b>, the path is clearly
not the shortest one that exists. This is confirmed by looking at the path cost. For weights <b>0</b>, <b>0.2</b>, <b>0.8</b>, <b>1</b>, <b>1.2</b> and <b>1.5</b> the cost is 
<b>238</b>, however for weight <b>10</b>, the cost is <b>262</b>. While the path is more expensive, it is found quicker than the others.

We can draw a general conclusion from this:

- A smaller <i>heuristic weight</i> results in a longer runtime but cheaper path
- A bigger <i>heuristic weight</i> results in a smaller runtime but more expensive path

However, this is more of a general guideline and does not strictly apply to every case, as <b>there are limits to it</b>. This can be seen in the practical example below.
# <b>Practical example:</b>

This is a labyrinth that I drew. 

The respective costs are <b>944</b> (weight: <b>1.0</b>), <b>1102</b> (weight: <b>10.0</b>) and <b>1729</b> (weight: <b>100.0</b>). One notices that with a weight
of <b>10</b>, the algorithm works significantly faster but the path is slightly more expensive (as expected), however if we increase the weight excessively (weight of <b>100</b>), the runtime gets longer again and the path much more expensive. This shows that a <i>heuristic weight</i> that is too large can slow the algorithm down again.

In this case, the optimal weight would be <b>10</b> as it balances <i>speed</i> and <i>optimal cost</i> the best:

<img src="https://media.giphy.com/media/NTKVNjsTskTEhf7KjF/giphy.gif" width = 400/> <img src="https://media.giphy.com/media/8e1yMiT0ibGC9iU45t/giphy.gif" width = 400/> 
<img src="https://media.giphy.com/media/tywtvzro0fwiq9bweR/giphy.gif" width = 400/>




# <b>Dependencies: </b>

- Python 3.8

- Kivy 2.0.0

- PIL (Python Imaging Library)

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
