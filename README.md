# Open House Router

## Inspiration
I have been looking for houses. When I add open houses to my Google Calendar, I am able to request direction to whatever house is open next in time, but I was thinking…

*“What if two houses are significantly far apart, open at similar times, and there are other houses in each of their respective neighborhoods that open at different times? Is there a way I can plan my day of house hunting so that I can attend all of the open houses?”*

## What will it do
### Application
The web app will allow the user enter a series of open houses and the applications will attempt to find a route that will allow the user to visit the maximum number of open houses given the constraints of travel time between locations and when the open houses are open.

### Mathematics
I have described this problem to many people and almost everyone thinks it is just the [Travelling Salesman Problem](https://www.wikiwand.com/en/Travelling\_salesman\_problem) (TSP), but I prefer to think of it as a [Hamiltonian cycle problem](https://www.wikiwand.com/en/Hamiltonian_path_problem) or some form of [Metric TSP](https://www.wikiwand.com/en/Travelling_salesman_problem#/Metric_TSP).

## Resources
### Version Control
* [apjansing/open-house-router](https://github.com/apjansing/open-house-router)

### Planning
* [Trello - Open House Router](https://trello.com/b/q1hinbru)

### APIs
* [Setting up a Node development environment
](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/development_environment)
* [Esri/node-arcgis](https://github.com/Esri/node-arcgis)
* [Esri/arcgis-rest-js](https://github.com/Esri/arcgis-rest-js)
* [ArcGIS Developer](https://developers.arcgis.com/)

#### Contributors to initial codebase
I would like to acknowledge the intial help I received in starting this project to those listed below. I refer to their LinkedIn pages as I do not have all of their GitHub profiles available.
* [Jennifer Tran](https://www.linkedin.com/in/jennifertrantrinity/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BWDMhsn3%2FS8%2BSVXTAQASRNg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile)
* [Sylvia Pericles](https://www.linkedin.com/in/sylvia-pericles-753054a4/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BWDMhsn3%2FS8%2BSVXTAQASRNg%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile)
* [Zhushun Cai](https://www.linkedin.com/in/zhushun-cai-bb4301114/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BjKNSHhO3SYesa3pKPzhP6g%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile)
* [Oliver Medonza](https://www.linkedin.com/in/oliver-medonza/?lipi=urn%3Ali%3Apage%3Ad_flagship3_people_connections%3BjKNSHhO3SYesa3pKPzhP6g%3D%3D&licu=urn%3Ali%3Acontrol%3Ad_flagship3_people_connections-connection_profile)