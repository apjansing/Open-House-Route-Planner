# Open House Router

## Inspiration
I have been looking for houses. When I add open houses to my Google Calendar, I am able to request direction to whatever house is open next in time, but I was thinking…

*“What if two houses are significantly far apart, open at similar times, and there are other houses in each of their respective neighborhoods that open at different times? Is there a way I can plan my day of house hunting so that I can attend all of the open houses?”*

## Objective
### Application
The program will allow the user enter a series of open houses and the applications will attempt to find a route that will allow the user to visit the maximum number of open houses given the constraints of travel time between locations and when the open houses are open.

#### Backend
Most of my focus will be on getting the backend of this project working. My hope here is break the problem down into several manageable parts.

##### Querying
I have a limited number of Esri Developer Credits and I want to limit the number of credits I use. To do this, I plan on 
 * storing the _addresses_, the _geocoded addresses_, and the _driving directions_ between all houses houses,
 * and before a query to Esri is made, 
   * check if a given address has already been geocoded,
   * and check if a the directions between two given points has already been fetched
   
##### Calculation
###### Minimum Viable Product
This will probably be the most time-consuming part of the program. A few references have been provided in the [Mathematics](#Mathematics) section can help in understanding the computation involved in finding the optimal solution to this problem.

An optimal solution would be nice and is probably an attainable goal with the limited number of houses one will feasibly want to see while touring open houses, but even in the case where someone provides an unusual number of houses, the priority will be to find **a solution**. For the sake of getting a minimally viable product, any solutions will be acceptable.

###### Possible Approaches
One approach to this problem will be to first take three points, _{A, B, C}_; where _A, B,_ and _C_ are _(Latitude, Longitude)_ pairs. The directions between these point _{ab, ac, ba, bc, ca, bc}_; where directions are based off of what is returned from [Python RouteLayer object](https://developers.arcgis.com/python/guide/performing-route-analyses/#Drawing-the-result-route-on-a-web-map-as-a-layer) when two points are provided.

With that information I would use SparkGraph to help simulate travelling from point to point and find a path that satisfies the condition that all houses are visited during the open house time windows.

_A [Traveling Salesman API call](https://developers.arcgis.com/python/guide/performing-route-analyses/#Solving-the-traveling-salesperson-problem-(TSP)) is available in the [Esri API](http://resources.arcgis.com/EN/HELP/MAIN/10.2/index.html#/Route_analysis/004700000045000000/) and it looks like there are enough controls to tell the program that once someone arrives at a location, they will want to stay there for some time. **This may or may not be enough to solve the problem described**._


#### Frontend
TODO


## Resources

### Version Control
* <a href="https://github.com/apjansing/Open-House-Route-Planner" target="_blank">apjansing/Open-House-Route-Planner</a>

### Planning
* <a href="https://trello.com/b/q1hinbru" target="_blank">Trello - Open House Router</a>

### APIs
* <a href="https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/development_environment" target="_blank">Setting up a Node development environment</a>
* <a href="https://github.com/Esri/node-arcgis" target="_blank">Esri/node-arcgis</a>
* <a href="https://github.com/Esri/arcgis-rest-js" target="_blank">Esri/arcgis-rest-js</a>
* <a href="https://developers.arcgis.com/" target="_blank">ArcGIS Developer</a>

### Mathematics
I have described this problem to many people and almost everyone thinks it is just the <a href="https://www.wikiwand.com/en/Travelling\_salesman\_problem" target="_blank">Travelling Salesman Problem</a> (TSP), but I prefer to think of it as a <a href="https://www.wikiwand.com/en/Hamiltonian_path_problem" target="_blank">Hamiltonian cycle problem</a> or some form of <a href="https://www.wikiwand.com/en/Travelling_salesman_problem#/Metric_TSP" target="_blank">Metric TSP</a>.

## Contributors to initial codebase
I would like to acknowledge the initial help I received in starting this project to those listed below. I refer to their LinkedIn pages as I do not have all of their GitHub profiles available.
* <a href="https://www.linkedin.com/in/jennifertrantrinity/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BWDMhsn3%2FS8%2BSVXTAQASRNg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile" target="_blank">Jennifer Tran</a>
* <a href="https://www.linkedin.com/in/sylvia-pericles-753054a4/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BWDMhsn3%2FS8%2BSVXTAQASRNg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile" target="_blank">Sylvia Pericles</a>
* <a href="https://www.linkedin.com/in/zhushun-cai-bb4301114/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BjKNSHhO3SYesa3pKPzhP6g%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile" target="_blank">Zhushun Cai</a>
* <a href="https://www.linkedin.com/in/oliver-medonza/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BjKNSHhO3SYesa3pKPzhP6g%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile" target="_blank">Oliver Medonza</a>
