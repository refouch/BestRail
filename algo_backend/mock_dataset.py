### AI-generated mock dataset to test the algorithm

from data_structure import Route, Stop, Trip

def generate_mock_dataset():
    # -----------------------------
    # Stops
    stops = [
        Stop(0, "Stop A"),
        Stop(1, "Stop B"),
        Stop(2, "Stop C"),
        Stop(3, "Stop D")  # pour tester absence de solution
    ]

    stops_dict = {stop.id: stop for stop in stops}

    # -----------------------------
    # Routes (séquence de stops)
    routes = [
        Route("R1", "Route 1", ["A", "B", "C"]),  # parcours A → B → C
        Route("R2", "Route 2", ["B", "C"]),       # parcours B → C
        Route("R3", "Route 3", ["C", "B"])        # parcours inverse C → B
    ]

    for route in routes:
        for stop_id in route.stop_ids:
            stops_dict[stop_id].add_route(route.id)

    # -----------------------------
    # Trips (horaires en minutes depuis minuit)
    # Trip sur R1 : départ A 8h00, arrivée B 8h10, C 8h20
    trips = [
        Trip("T1", "R1", arrival_times=[0+0, 10, 20], departure_times=[0, 10, 20]),  
        # Trip sur R1 plus tard
        Trip("T2", "R1", arrival_times=[60, 70, 80], departure_times=[60, 70, 80]),  

        # Trip sur R2 : départ B 8h15, arrivée C 8h25
        Trip("T3", "R2", arrival_times=[15, 25], departure_times=[15, 25]),

        # Trip sur R3 : départ C 8h30, arrivée B 8h40
        Trip("T4", "R3", arrival_times=[30, 40], departure_times=[30, 40])
    ]

    mock_dataset = {
        "stop_list": stops,
        "route_list": routes,
        "trip_lists": trips
    }

    return mock_dataset