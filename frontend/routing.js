require([
    "esri/Map",
    "esri/views/MapView",
    "esri/Graphic",
    "esri/layers/GraphicsLayer",
    "esri/tasks/RouteTask",
    "esri/tasks/support/RouteParameters",
    "esri/tasks/support/FeatureSet",
    "esri/core/urlUtils",
    "esri/geometry/Point"
], function(
    Map, MapView, Graphic, GraphicsLayer, RouteTask, 
    RouteParameters, FeatureSet, urlUtils, Point) {
        // Point the URL to a valid route service
        var routeTask = new RouteTask({
            url: "https://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World"
        });

        // The stops and route result will be stored in this layer
        var routeLayer = new GraphicsLayer();
        var routeResult = null;
        // Setup the route parameters
        var routeParams = new RouteParameters({
            stops: new FeatureSet(),
            outSpatialReference: {
                    wkid: 3857
            },
            findBestSequence: true,
            preserveFirstStop: true,
            preserveLastStop: false,
            returnStops: true,
            returnDirections: true,
            directionsOutputType: 'complete',
            returnStops: true,
            useTimeWindows: true
        });

        // Define the symbology used to display the stops
        var stopSymbol = {
            type: "simple-marker",
            style: "cross",
            size: 15,
            outline: {
                width: 4
            }
        };

        // Define the symbology used to display the route
        var routeSymbol = {
            type: "simple-line",
            color: [0, 0, 255, 0.5],
            width: 5
        };

        var map = new Map({
            basemap: "streets",
            layers: [routeLayer]                    // Add the route layer to the map
        });
        var view = new MapView({
            container: "viewDiv",                   // Reference to the scene div created in step 5
            map: map,                               // Reference to the map object created before the scene
            center: [-76.205665844, 43.103499586],
            zoom: 14
        });

        // Adds a graphic when the user clicks the map. If 2 or more points exist, route is solved.
        view.on("click", addStop);

        function addStop(event) {
            // Add a point at the location of the map click
            var stop = new Graphic({
            geometry: event.mapPoint,
            symbol: stopSymbol
            });
            routeLayer.add(stop);
            routeParams.stops.features.push(stop);
            
            // var stop1 = new Graphic(new Point(-117.21,  34.065), stopSymbol);
            // stop1.attributes = new Object();
            // stop1.attributes.Name = "A";
            // stop1.attributes.TimeWindowStart = "8:00 AM";
            // stop1.attributes.TimeWindowEnd = "8:05 AM";

            // var stop2 = new Graphic(new Point(-117.185, 34.05 ), stopSymbol);
            // stop2.attributes = new Object();
            // stop2.attributes.Name = "B";
            // stop2.attributes.TimeWindowStart = "8:10 AM";
            // stop2.attributes.TimeWindowEnd = "8:15 AM";

            // var stop3 = new Graphic(new Point(-117.19,  34.062), stopSymbol);
            // stop3.attributes = new Object();
            // stop3.attributes.Name = "C";
            // stop3.attributes.TimeWindowStart = "8:20 AM";
            // stop3.attributes.TimeWindowEnd = "8:25 AM";

            // Execute the route task if 2 or more stops are input
            // routeParams.stops.features.push(stop1);
            // routeParams.stops.features.push(stop2);
            // routeParams.stops.features.push(stop3);

            if (routeParams.stops.features.length >= 2) {
                routeLayer.remove(routeResult);
                routeTask.solve(routeParams).then(showRoute);
            }
        }
        // Adds the solved route to the map as a graphic
        function showRoute(data) {
            routeResult = data.routeResults[0].route;
            routeResult.symbol = routeSymbol;
            routeLayer.add(routeResult);
            console.log(data.routeResults[0].directions['strings'])
            console.log(routeResult.attributes)
        }
    });