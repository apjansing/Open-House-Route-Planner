# Backend
Most of my focus will be on getting the backend of this project working. My hope here is break the problem down into several manageable parts.

## Querying
I have a limited number of Esri Developer Credits and I want to limit the number of credits I use. To do this, I plan on 
 * storing the _addresses_, the _geocoded addresses_, and the _driving directions_ between all houses houses,
 * and before a query to Esri is made, 
   * check if a given address has already been geocoded,
   * and check if a the directions between two given points has already been fetched
   
##### Calculation
###### Minimum Viable Product
This will probably be the most time-consuming part of the program. A few references have been provided in the [Mathematics](#Mathematics) section can help in understanding the computation involved in finding the optimal solution to this problem.

An optimal solution would be nice and is probably an attainable goal with the limited number of houses one will feasibly want to see while touring open houses, but even in the case where someone provides an unusual number of houses, the priority will be to find **a solution**. For the sake of getting a minimally viable product, any solutions will be acceptable.

### Possible Approaches
One approach to this problem will be to first take three points, _{A, B, C}_; where _A, B,_ and _C_ are _(Latitude, Longitude)_ pairs. The directions between these point _{ab, ac, ba, bc, ca, bc}_; where directions are based off of what is returned from [Python RouteLayer object](https://developers.arcgis.com/python/guide/performing-route-analyses/#Drawing-the-result-route-on-a-web-map-as-a-layer) when two points are provided.

With that information I would use SparkGraph to help simulate travelling from point to point and find a path that satisfies the condition that all houses are visited during the open house time windows.

_A [Traveling Salesman API call](https://developers.arcgis.com/python/guide/performing-route-analyses/#Solving-the-traveling-salesperson-problem-(TSP)) is available in the [Esri API](http://resources.arcgis.com/EN/HELP/MAIN/10.2/index.html#/Route_analysis/004700000045000000/) and it looks like there are enough controls to tell the program that once someone arrives at a location, they will want to stay there for some time. **This may or may not be enough to solve the problem described**._

# Resources
## APIs
* <a href="https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/development_environment" target="_blank">Setting up a Node development environment</a>
* <a href="https://github.com/Esri/node-arcgis" target="_blank">Esri/node-arcgis</a>
* <a href="https://github.com/Esri/arcgis-rest-js" target="_blank">Esri/arcgis-rest-js</a>
* <a href="https://developers.arcgis.com/" target="_blank">ArcGIS Developer</a>

## Mathematics
I have described this problem to many people and almost everyone thinks it is just the <a href="https://www.wikiwand.com/en/Travelling\_salesman\_problem" target="_blank">Travelling Salesman Problem</a> (TSP), but I prefer to think of it as a <a href="https://www.wikiwand.com/en/Hamiltonian_path_problem" target="_blank">Hamiltonian cycle problem</a> or some form of <a href="https://www.wikiwand.com/en/Travelling_salesman_problem#/Metric_TSP" target="_blank">Metric TSP</a>.
