# BDD_with_pyEDA
Creating a Binary Decision Tree From a Graph Using pyEDA Package

This is a solo school project for a Design and Analysis of Algorithms course. In it, we were given a graph along with sets of its nodes to represent as a BDD (Binary Decision Diagram).

The project is set up as follows.
- graph G has 32 nodes (node 0 to node 31)
- there is an edge from node i to node j iff (i + 3)%32 = j%32 or (i + 8)%32 = j%32
- "R" is the set of all edges in graph G
- "even" is the set of all even nodes in graph G (0, 2, 4, ...)
- "prime" is the set of all prime nodes in graph G (3, 5, 7, ...)
- ultimately, the final BDD should declare the truth value of Statement A: for each node u in "prime", there is a node v in "even" such that u can reach v
in a positive even number of steps

The steps to complete this project are given.
- create three BDDs names RR, EVEN, and PRIME to represent the sets "R," "even," and "prime" respectively
- verify the three BDDs are correct using these test cases
    - RR(27, 3) is true;
    - RR(16, 20) is false
    - EVEN (14) is true
    - EVEN (13) is false
    - PRIM E(7) is true
    - PRIM E(2) is false 
