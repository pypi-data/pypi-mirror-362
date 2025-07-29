# TransportNSWv2
Python lib to access Transport NSW information.

## How to Use

### Get an API Key
An OpenData account and API key is required to request the data. More information on how to create the free account can be found here:
https://opendata.transport.nsw.gov.au/user-guide.  You need to register an application that needs both the Trip Planner and Realtime Vehicle Positions APIs

### Get the stop IDs
The function needs the stop IDs for the source and destination, and optionally how many minutes from now the departure should be, and if you want to filter trips by a specific transport type, or to only include trips that have specific text somewhere in the line/service details (see below).  The easiest way to get the stop ID is via https://transportnsw.info/stops#/. It provides the option to search for either a location or a specific platform, bus stop or ferry wharf.  Regardless of if you specify a general location for the origin or destination, the return information shows the stop_id for the actual arrival and destination platform, bus stop or ferry wharf.

If it's available, the general occupancy level and the latitude and longitude of the selected journey's vehicle (train, bus, etc) will be returned, unless you specifically set ```include_realtime_location``` to ```False```.

### API Documentation
The source API details can be found here: https://opendata.transport.nsw.gov.au/sites/default/files/2023-08/Trip%20Planner%20API%20manual-opendataproduction%20v3.2.pdf

### Parameters
```python
.get_trip(origin_stop_id, destination_stop_id, api_key, [trip_wait_time = 0], [transport_type = 0], [strict_transport_type = True|False], [raw_output = True|False], [journeys_to_return = 1], [route_filter = ''], [include_realtime_location = True], [include_alerts = 'none'], [alert_type = 'all'] )
```

Transport types:
```
1:      Train
2:      Metro
4:      Light rail
5:      Bus
7:      Coach
9:      Ferry
11:     School bus
99:     Walk
100:    Walk
107:    Cycle
```

Alert priorities:
```
veryLow
low
normal
high
veryHigh
```
Specifying an alert priority in ```include_alerts``` means that any alerts of that priority or higher will be included in the output as a raw JSON array, basically a collation of the alerts that the Trip API sent back.  If you've specified that alerts of a given priority should be included then by default ALL alert types will be included - you can limit the output to specific alert types by setting ```alert_type``` to something like ```'lineInfo|stopInfo|bannerInfo'```.

Alert types:
```
routeInfo:      Alerts relating to a specific route
lineInfo:       Alerts relating to a specific journey
stopInfo:       Alerts relating to specific stops
stopBlocking:   Alerts relating to stop closures
bannerInfo:     Alerts potentially relating to network-wide impacts
```

TransportNSW's trip planner can work better if you use the general location IDs (eg Central Station) rather than a specific Stop ID (eg Central Station, Platform 19) for the destination, depending on the transport type.  Forcing a specific end destination sometimes results in much more complicated trips.  Also note that the API expects (and returns) the Stop IDs as strings, although so far they all appear to be numeric.

### Sample Code - bus journey, no alerts included

The following example returns the next trip that starts from a bus stop in St. Ives (207537) at least five minutes from now, to Central Station's general stop ID (200060):

**Code:**
```python
from TransportNSWv2 import TransportNSWv2
tnsw = TransportNSWv2()
journey = tnsw.get_trip('207537', '200060', 'YOUR_API_KEY', journey_wait_time = 5, transport_type = 5)
print(journey)
```
**Result:**
```python
{"journeys_to_return": 1, "journeys_with_data": 1, "journeys": [
    {"due": 22, "origin_stop_id": "207537", "origin_name": "Mona Vale Rd at Shinfield Ave, St Ives", "departure_time": "2024-09-10T06:34:24Z", "destination_stop_id": "207235", "destination_name": "Gordon Station, Stand C, Gordon", "arrival_time": "2024-09- 
    10T06:40:36Z", "origin_transport_type": "Bus", "origin_transport_name": "Sydney Buses Network", "origin_line_name": "195", "origin_line_name_short": "195", "changes": 0, "occupancy": "FEW_SEATS", "real_time_trip_id": "2197645", "latitude": -33.728271484375, 
    "longitude": 151.1637420654297, "alerts": []
}]}
```

### Sample Code - train journey, all stop-related alerts normal priority or higher included

The following example return the next train journey that starts from Gordon (207537) to Central (200070) one minute from now.  Two journeys have been requested, we want realtime locations if possible, and we also want lineInfo and stopInfo alerts of priority normal or higher:

**Code:**
```python
from TransportNSWv2 import TransportNSWv2
tnsw = TransportNSWv2()
journey = tnsw.get_trip('207210', '200070', '<your API key>', journey_wait_time = 1,transport_type = 1, journeys_to_return = 2, raw_output = False, include_realtime_location = True, include_alerts = 'normal', alert_type = 'lineInfo|stopInfo')
print(journey)
```
**Result:**
```python
{"journeys_to_return": 2, "journeys_with_data": 2, "journeys":[
    {"due": 8, "origin_stop_id": "207262", "origin_name": "Gordon Station, Platform 2, Gordon", "departure_time": "2024-09-10T05:18:00Z", "destination_stop_id": "2000338", "destination_name": "Central Station, Platform 18, Sydney", "arrival_time": "2024-09- 
     10T05:54:00Z", "origin_transport_type": "Train", "origin_transport_name": "Sydney Trains Network", "origin_line_name": "T1 North Shore & Western Line", "origin_line_name_short": "T1", "changes": 0, "occupancy": "unknown", "real_time_trip_id": 
     "171L.1915.100.8.A.8.83064399", "latitude": -33.755828857421875, "longitude": 151.1542205810547, "alerts": [
         {"priority": "normal", "id": "ems-39380", "version": 3, "type": "stopInfo", "infoLinks": [{"urlText": "Central Station Lift 20 between Central Walk and Platform 20/21 is not available", "url": "https://transportnsw.info/alerts/details#/ems-39380", "content": 
          "At Central Station Lift 20 between Central Walk and Platform 20/21 is temporarily out of service.\n\nIf you need help, ask staff or phone 02 9379 1777.", "subtitle": "Central Station Lift 20 between Central Walk and Platform 20/21 is not available", 
          "smsText": "Central Station Lift 20 between Central Walk and Platform 20/21 is not available", "speechText": "At Central Station Lift 20 between Central Walk and Platform 20/21 is temporarily out of service.\n\nIf you need help, ask staff or phone 02 9379 
          1777.", "properties": {"publisher": "ems.comm.addinfo", "infoType": "stopInfo", "appliesTo": "departingArriving", "stopIDglobalID": "200060:2000340,2000341"}}
     ]}
  ]},
    {"due": 11, "origin_stop_id": "207261", "origin_name": "Gordon Station, Platform 1, Gordon", "departure_time": "2024-09-10T05:21:00Z", "destination_stop_id": "2067141", "destination_name": "Chatswood Station, Platform 1, Chatswood", "arrival_time": "2024-09- 
    10T05:30:00Z", "origin_transport_type": "Train", "origin_transport_name": "Sydney Trains Network", "origin_line_name": "T1 North Shore & Western Line", "origin_line_name_short": "T1", "changes": 0, "occupancy": "unknown", "real_time_trip_id": 
     "281G.1915.100.12.H.8.83062682", "latitude": -33.709938049316406, "longitude": 151.10427856445312, "alerts": [
         {"priority": "normal", "id": "ems-38565", "version": 145217, "type": "lineInfo", "infoLinks": [{"urlText": "Metro services temporarily end by 10.30pmMonday to Thursday evenings between Chatswood and Sydenham, please check service times and plan your trip", 
         "url": "https://transportnsw.info/alerts/details#/ems-38565", "content": "<div>\n<div>For the first four weeks after opening, there are reduced operating hours from Monday to Thursday evenings in the City section between Chatswood and Sydenham to support 
         essential engineering and maintenance works during the early phases of operations.</div>\n<div>&nbsp;</div>\n<div>This is temporary and only affects services between Chatswood and Sydenham.&nbsp;Following the first four weeks, metro services will operate 
         between Tallawong and Sydenham on the normal timetable.</div>\n</div>", "subtitle": "Metro services temporarily end by 10.30pm Monday to Thursday evenings between Chatswood and Sydenham, please check service times and plan your trip", "smsText": "Metro 
         services temporarily end by 10.30pm Monday to Thursday evenings between Chatswood and Sydenham, please check service times and plan your trip", "speechText": "There are reduced operating hours from Monday to Thursday evenings in the City section between 
         Chatswood and Sydenham to support essential engineering and maintenance works during the early phases of operations.", "properties": {"publisher": "ems.comm.addinfo", "infoType": "lineInfo"}}
     ]}
  ]}
]}
```
(In this example you can see that the second journey is actually ending at Chatswood.  I checked the raw API data and it does in fact have the last leg of the second journey as being at Chatswood but doesn't give any explanation as to why.  Interesting.)

* due: the time (in minutes) before the journey starts
* origin_stop_id: the specific departure stop id
* origin_name: the name of the departure location
* departure_time: the departure time, in UTC
* destination_stop_id: the specific destination stop id
* destination_name: the name of the destination location
* arrival_time: the planned arrival time at the origin, in UTC
* origin_transport_type: the type of transport, eg train, bus, ferry etc
* origin_transport_name: the full name of the transport provider
* origin_line_name & origin_line_name_short: the full and short names of the journey
* changes: how many transport changes are needed on the journey
* occupancy: how full the vehicle is, if available
* real_time_trip_id: the unique TransportNSW id for that specific journey, if available
* latitude & longitude: The location of the vehicle, if available
* alerts: An array of alerts pertinent to that journey


### Notes ###
Requesting multiple journeys to be returned doesn't always return that exact number of journeys.  The API only ever returns five or six, and if you have any filters applied then that might further reduce the number of 'valid' journeys.

```origin_line_name``` and ```origin_line_name_short``` are the fields that have the route filter applied, if present.  For buses they are usually the same, but for trains and ferries they generally show the full and short line names.  Both fields are checked and if either meet the filter then the journey is returned.

Note also that the origin and destination details are just that - information about the first and last stops on the journey at the time the request was made.  We don't return any intermediate steps, transport change types etc other than the total number of changes - the assumption is that you'll know the details of your specified trip, you just want to know when the next departure is.  If you need much more detailed information then I recommend that you use the full Transport NSW trip planner website or application.

Also note that the 'transport_type' filter, if present, only makes sure that at least **one** leg of the journey includes that transport type unless ```strict_transport_type``` is True, in which case the **first** leg must be of the requested type to be returned.

### Rate limits ###
By default the TransportNSW API allows each API key to make 60,000 calls in a day and up to 5 calls per second.  Usually this wouldn't be an issue but if you're requesting real-time location data for buses, because I haven't found an elegant way to map the bus route to the correct API URL (and there are about 14) it's brute-forcing it by iterating through ALL the possible URLs until it finds the appropriate journey or it runs out of URLs.  From version 0.8.2 I've added in a 0.5 second delay between loops until I can find a better approach.

## Thank you
Thank you Dav0815 for your TransportNSW library that the vast majority of this fork is based on.  I couldn't have done it without you!
https://github.com/Dav0815/TransportNSW
