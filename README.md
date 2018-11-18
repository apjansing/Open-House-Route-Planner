# Open House Router

## Inspiration
I have been looking for houses. When I add open houses to my Google Calendar, I am able to request direction to whatever house is open next in time, but I was thinking…

*“What if two houses are significantly far apart, open at similar times, and there are other houses in each of their respective neighborhoods that open at different times? Is there a way I can plan my day of house hunting so that I can attend all of the open houses?”*

## What will it do
### Application
The web app will allow the user enter a series of open houses and the applications will attempt to find a route that will allow the user to visit the maximum number of open houses given the constraints of travel time between locations and when the open houses are open.

### Mathematics
I have described this problem to many people and almost everyone thinks it is just the <a href="https://www.wikiwand.com/en/Travelling\_salesman\_problem" target="_blank">Travelling Salesman Problem</a> (TSP), but I prefer to think of it as a <a href="https://www.wikiwand.com/en/Hamiltonian_path_problem" target="_blank">Hamiltonian cycle problem</a> or some form of <a href="https://www.wikiwand.com/en/Travelling_salesman_problem#/Metric_TSP" target="_blank">Metric TSP</a>.

## Resources
### Version Control
* <a href="https://github.com/apjansing/open-house-router" target="_blank">apjansing/open-house-router</a>

### Planning
* <a href="https://trello.com/b/q1hinbru" target="_blank">Trello - Open House Router</a>

### APIs
* <a href="https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/development_environment" target="_blank">Setting up a Node development environment</a>
* <a href="https://github.com/Esri/node-arcgis" target="_blank">Esri/node-arcgis</a>
* <a href="https://github.com/Esri/arcgis-rest-js" target="_blank">Esri/arcgis-rest-js</a>
* <a href="https://developers.arcgis.com/" target="_blank">ArcGIS Developer</a>

#### Contributors to initial codebase
I would like to acknowledge the intial help I received in starting this project to those listed below. I refer to their LinkedIn pages as I do not have all of their GitHub profiles available.
* <a href="https://www.linkedin.com/in/jennifertrantrinity/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BWDMhsn3%2FS8%2BSVXTAQASRNg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile" target="_blank">Jennifer Tran</a>
* <a href="https://www.linkedin.com/in/sylvia-pericles-753054a4/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BWDMhsn3%2FS8%2BSVXTAQASRNg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile" target="_blank">Sylvia Pericles</a>
* <a href="https://www.linkedin.com/in/zhushun-cai-bb4301114/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BjKNSHhO3SYesa3pKPzhP6g%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile" target="_blank">Zhushun Cai</a>
* <a href="https://www.linkedin.com/in/oliver-medonza/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BjKNSHhO3SYesa3pKPzhP6g%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile" target="_blank">Oliver Medonza</a>