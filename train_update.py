from get_json import get_json
import datetime
from data import TFL_APP_ID, TFL_APP_KEY, TUBE_STATION_FROM, TUBE_STATION_TO

def next_trains(origin_naptan, destination_naptan, num_to_get):
    """Retrieve time to next n trains between given stations based on their
        NaPTAN (National Public Transport Access Node) id.

    Parameters
    ----------
    station_naptan : str
        NaPTAN id of starting station
    
    destination_naptan : str
        NaPTAN id of destination station

    num_to_get : int
        Number of next trains to fetch (up to 9)

    Returns
    -------
    message : str
        Message containing countdown to next trains in minutes, in the format of:
        "Trains to {destination name}: {time 0}, {time 2}, ... , {time n-1} minutes."
    """
    arrival_times = []
    next_trains_message = ''
    json_result = get_json('https://api.tfl.gov.uk/Line/jubilee/Arrivals/{}?direction=outbound&destinationStationId={}'.format(TUBE_STATION_FROM, TUBE_STATION_TO))
    try:
        destination_name = json_result[0]['towards']
    except (KeyError, IndexError):
        next_trains_message = "No trains in the next 30 minutes."
        return next_trains_message
    # Find number of seconds to station for all trains in next 30 mins
    for train in range(len(json_result)):
        arrival_times.append(json_result[train]['timeToStation'])
        
    
    # Sort trains based on arrival time and next n closest trains
    sorted_times = sorted(arrival_times)
    if len(sorted_times) < num_to_get:
        next_n_trains = sorted_times
    else:
        next_n_trains = sorted_times[0:num_to_get]
        
    # List of arrival times in minutes
    minutes_to_station = [int(i/60) for i in next_n_trains]
    for i in minutes_to_station:
        if i == 0:
            minutes_to_station[i] = 'Due'
    minutes_to_station = [str(i) for i in minutes_to_station]
    # Final message
    prefix = "Trains to {}: ".format(destination_name)
    if len(minutes_to_station) == 1:
        if minutes_to_station == ['1']:
            suffix = "{} minute.".format(minutes_to_station[0])
        elif minutes_to_station == ['Due']:
            suffix = "{}.".format(minutes_to_station[0])
        else:
            suffix = "{} minutes.".format(minutes_to_station[0])
        middle = ''
    else:
        middle = ", ".join(minutes_to_station[:-1])
        suffix = ", {} minutes.".format(minutes_to_station[-1])
                  
    next_trains_message = prefix + middle + suffix
    
    return next_trains_message

def main():

    trains = next_trains(TUBE_STATION_FROM, TUBE_STATION_TO, 3)
    print(trains)

if __name__ == '__main__':
    
    main()
