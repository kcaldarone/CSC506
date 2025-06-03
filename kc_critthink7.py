import heapq

#The Class Graph
# - represents a graph with nodes (which are locations) and weighted edges (which are roads) that can dynamically adjust for traffic scenarios
class Graph:
    def __init__(self): # initializes an empty adjacency list to harbor nodes and their connected edges.
        self.adjacencyList = {}
    def addNode(self, node): # adds a node to the graph if it doesn't already exist.
        if node not in self.adjacencyList:
            self.adjacencyList[node] = []
    def addEdge(self, fromNode, toNode, baseTime): # connects two nodes with a bidirectional edge weighted by the base travel time.
        self.adjacencyList[fromNode].append((toNode, baseTime))
        self.adjacencyList[toNode].append((fromNode, baseTime))  # !this is assuming there are bidirectional roads!
    def updateTrafficWeights(self, trafficData): # updates edge weights in the graph based on the traffic multipliers from real-time traffic data.
        for fromNode in self.adjacencyList:
            updatedEdges = []
            for toNode, baseTime in self.adjacencyList[fromNode]:
                trafficMultiplier = trafficData.get((fromNode, toNode), 1.0)
                updatedEdges.append((toNode, baseTime * trafficMultiplier))
            self.adjacencyList[fromNode] = updatedEdges

#Dijkstra Shortest Path Function
# - calculates the shortest path from a start node to an end node utilizing Dijkstra’s algorithm and returns the path and total time.
def dijkstraShortestPath(graph, startNode, endNode):
    queue = [(0, startNode)]
    visited = set()
    shortestPaths = {startNode: (None, 0)}
    while queue:
        currentTime, currentNode = heapq.heappop(queue)
        if currentNode in visited:
            continue
        visited.add(currentNode)
        if currentNode == endNode:
            break
        for neighbor, travelTime in graph.adjacencyList.get(currentNode, []):
            totalTime = currentTime + travelTime
            if neighbor not in shortestPaths or totalTime < shortestPaths[neighbor][1]:
                shortestPaths[neighbor] = (currentNode, totalTime)
                heapq.heappush(queue, (totalTime, neighbor))

    # Reconstruction of the Path
    path = []
    step = endNode
    if step not in shortestPaths:
        return None, float('inf')
    while step:
        path.insert(0, step)
        step = shortestPaths[step][0]
    return path, shortestPaths[endNode][1]

# Route Planner
# - applies traffic data to graph & computes the optimal path using Dijkstra’s algorithm. It then returns the best route with estimated travel time.
def planRoute(graph, startLocation, endLocation, trafficData):
    graph.updateTrafficWeights(trafficData)
    path, totalTime = dijkstraShortestPath(graph, startLocation, endLocation)
    
    minutes = int(totalTime)
    seconds = int((totalTime - minutes) * 60)
    
    return {
        "optimalPath": path,
        "estimatedTime": f"{minutes} minute(s) and {seconds} second(s)"
    }

if __name__ == "__main__":
    # EXAMPLE USAGE: Constructing a sample graph
    cityGraph = Graph()
    locations = ["Restaurant", "A", "B", "Customer"]
    for loc in locations:
        cityGraph.addNode(loc)

    # Adding roads (edges) with base travel durations
    cityGraph.addEdge("Restaurant", "A", 10)
    cityGraph.addEdge("A", "B", 5)
    cityGraph.addEdge("B", "Customer", 2)
    cityGraph.addEdge("Restaurant", "B", 12)
    cityGraph.addEdge("A", "Customer", 18)

    # Simulates real-time traffic data using edges as traffic multipliers
    trafficData = {
        ("Restaurant", "A"): 1.4,
        ("A", "B"): 1.8,
        ("B", "Customer"): 1.5
    }

    # Plan optimal delivery route
    routeResult = planRoute(cityGraph, "Restaurant", "Customer", trafficData)
    print("Optimal Path:", routeResult["optimalPath"])
    print("Estimated Time:", routeResult["estimatedTime"])