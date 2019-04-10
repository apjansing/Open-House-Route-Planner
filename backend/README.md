# [Open House Route Planner](https://apjansing.github.io/Open-House-Route-Planner/)
## [Backend](https://apjansing.github.io/Open-House-Route-Planner/backend/)
My focus on this project was getting the backend logic working. I've started the learn some about frontend work, but I am still an extreme novice. If I have time before the end of the Spring 2019 semester, I will make an attempt to get something put together, but it is only a stretch goal.

The [Open House Route Planner](https://apjansing.github.io/Open-House-Route-Planner/) has been broken down into two major pieces: querying and computation. 

### Querying
I have a limited number of Esri Developer Credits and I want to limit the number of credits I use. To do this, I
 * cached the _addresses_, the _geocoded addresses_, and the _driving directions_ between all houses houses,
 * and before a query to Esri is made, I have
   * checked if a given address has already been geocoded,
   * and checked if a the directions between two given points has already been fetched
   
### Computation
#### Approach
##### Process
  1. Given *n* houses to visit, create a **fully connected directional graph**. 
  2. Iterate over each house and then recursively search the graph for a set of **acyclic edges**. 
      * To travel to another edge, keep a version of the current time (scoped to the open house in question) to detemine if you arrive at the open house either early or during the designated hours; adjust time accordingly.
      * If you arrive to late, procede to the next acyclic edge.
  3. When a path has been exhausted, return that path to the recursive level above and keep traveling the graph.
  4. Once all *potential* routes have been identified, identify and return the longest routes.


##### Justification
When thinking about spending a day visiting open houses, you might be lucky to have enough time in the day to visit 7 or 8 houses. With that in mind, my approach is close to a brute force strategy for solving the routing problem. Since the number of houses you can visit is fairly finite, brute force does not take all that long. 
###### An example of how long it might take to find a series of routes 
```
Given 10 locations, Open House routing calculations took 0.04648470878601074 seconds to execute.
The maximum number of houses that could be visited was 6.
```
This output was provided by the test function within the `OpenHouseRouting` class.


### Technologies
#### Databases
 * MongoDB - for simplified storage of data during the ETL process.
#### Frameworks
 * Flask - for providing an endpoint for the program's location data to be parsed and performing queries to the Esri Developer API. 
#### Support
 * Docker - for compartmentalization of the work. In addition to making the work more portable, containers also provide a convenient way of breaking a problem down into its simplest parts.
 * Docker-compose - to put the containers on the same network and so each container can call the others out by name.


## Resources
### APIs
#### Backend
* <a href="https://developers.arcgis.com/python/" target="_blank">Python ArcGIS API</a>
* <a href="https://developers.arcgis.com/" target="_blank">ArcGIS Developer</a>
#### Frontend
* <a href="https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/development_environment" target="_blank">Setting up a Node development environment</a>
* <a href="https://github.com/Esri/node-arcgis" target="_blank">Esri/node-arcgis</a>
* <a href="https://github.com/Esri/arcgis-rest-js" target="_blank">Esri/arcgis-rest-js</a>

### External Code and Research
<!-- I have described this problem to many people and almost everyone thinks it is just the <a href="https://www.wikiwand.com/en/Travelling\_salesman\_problem" target="_blank">Traveling Salesman Problem</a> (TSP), but I prefer to think of it as a <a href="https://www.wikiwand.com/en/Hamiltonian_path_problem" target="_blank">Hamiltonian cycle problem</a> or some form of <a href="https://www.wikiwand.com/en/Travelling_salesman_problem#/Metric_TSP" target="_blank">Metric TSP</a>. -->
A Python graph class from https://www.python-course.eu/graphs_python.php. Changes to include weighted edges from https://towardsdatascience.com/to-all-data-scientists-the-one-graph-algorithm-you-need-to-know-59178dbb1ec2 and additional modification to the author's adaptation that I didn't agree with.