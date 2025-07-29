"""  A module to query Transport NSW (Australia) departure times.         """
"""  First created by Dav0815 ( https://pypi.org/user/Dav0815/)           """
"""  Extended by AndyStewart999 ( https://pypi.org/user/andystewart999/ ) """

from datetime import datetime, timedelta
from google.transit import gtfs_realtime_pb2
import requests.exceptions
import requests
import logging
import re
import json					#For the output
import time
#from ratelimit import limits, sleep_and_retry	# API rate limiting

ATTR_DUE_IN = 'due'

ATTR_ORIGIN_STOP_ID = 'origin_stop_id'
ATTR_ORIGIN_NAME = 'origin_name'
ATTR_DEPARTURE_TIME = 'departure_time'
ATTR_DELAY = 'delay'

ATTR_DESTINATION_STOP_ID = 'destination_stop_id'
ATTR_DESTINATION_NAME = 'destination_name'
ATTR_ARRIVAL_TIME = 'arrival_time'

ATTR_ORIGIN_TRANSPORT_TYPE = 'origin_transport_type'
ATTR_ORIGIN_TRANSPORT_NAME = 'origin_transport_name'
ATTR_ORIGIN_LINE_NAME = 'origin_line_name'
ATTR_ORIGIN_LINE_NAME_SHORT = 'origin_line_name_short'
ATTR_CHANGES = 'changes'

ATTR_OCCUPANCY = 'occupancy'

ATTR_REAL_TIME_TRIP_ID = 'real_time_trip_id'
ATTR_LATITUDE = 'latitude'
ATTR_LONGITUDE = 'longitude'

ATTR_ALERTS = 'alerts'

logger = logging.getLogger(__name__)

class TransportNSWv2(object):
    """The Class for handling the data retrieval."""

    # The application requires an API key. You can register for
    # free on the service NSW website for it.
    # You need to register for both the Trip Planner and Realtime Vehicle Position APIs

    def __init__(self):
        """Initialize the data object with default values."""
        self.origin_id = None
        self.destination_id = None
        self.api_key = None
        self.journey_wait_time = None
        self.transport_type = None
        self.strict_transport_type = None
        self.raw_output = None
        self.journeys_to_return = None
        self.info = {
            ATTR_DUE_IN : 'n/a',
            ATTR_ORIGIN_STOP_ID : 'n/a',
            ATTR_ORIGIN_NAME : 'n/a',
            ATTR_DEPARTURE_TIME : 'n/a',
            ATTR_DELAY : 'n/a',
            ATTR_DESTINATION_STOP_ID : 'n/a',
            ATTR_DESTINATION_NAME : 'n/a',
            ATTR_ARRIVAL_TIME : 'n/a',
            ATTR_ORIGIN_TRANSPORT_TYPE : 'n/a',
            ATTR_ORIGIN_TRANSPORT_NAME : 'n/a',
            ATTR_ORIGIN_LINE_NAME : 'n/a',
            ATTR_ORIGIN_LINE_NAME_SHORT : 'n/a',
            ATTR_CHANGES : 'n/a',
            ATTR_OCCUPANCY : 'n/a',
            ATTR_REAL_TIME_TRIP_ID : 'n/a',
            ATTR_LATITUDE : 'n/a',
            ATTR_LONGITUDE : 'n/a',
            ATTR_ALERTS: '[]'
            }

    def get_trip(self, name_origin, name_destination , api_key, journey_wait_time = 0, transport_type = 0, \
                 strict_transport_type = False, raw_output = False, journeys_to_return = 1, route_filter = '', include_realtime_location = True, include_alerts = 'none', alert_type = 'all'):
                 # or 'lineInfo|stopInfo' etc as a list
        """Get the latest data from Transport NSW."""
        fmt = '%Y-%m-%dT%H:%M:%SZ'

        self.name_origin = name_origin
        self.destination = name_destination
        self.api_key = api_key
        self.journey_wait_time = journey_wait_time
        self.transport_type = transport_type
        self.strict_transport_type = strict_transport_type
        self.raw_output = raw_output
        self.journeys_to_return = journeys_to_return
        self.route_filter = route_filter.lower()
        self.include_realtime_location = include_realtime_location
        self.include_alerts = include_alerts.lower()
        self.alert_type = alert_type.lower()

        # This query always uses the current date and time - but add in any 'journey_wait_time' minutes
        now_plus_wait = datetime.now() + timedelta(minutes = journey_wait_time)
        itdDate = now_plus_wait.strftime('%Y%m%d')
        itdTime = now_plus_wait.strftime('%H%M')

        # First, check if the source and dest stops are valid
        stop_list = [name_origin, name_destination]
        auth = 'apikey ' + self.api_key
        header = {'Accept': 'application/json', 'Authorization': auth}

        for stop in stop_list:
            url = \
                'https://api.transport.nsw.gov.au/v1/tp/stop_finder?' \
                'outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326' \
                '&type_sf=stop&name_sf=' + stop + \
                '&TfNSWSF=true'

            # Send the query and return an error if something goes wrong
            try:
                response = requests.get(url, headers=header, timeout=20)
            except:
                logger.error("Network or Timeout error when calling /v1/tp/stop_finder API")
                return None

            # If we get bad status code, log error and return with None
            if response.status_code != 200:
                if response.status_code == 429:
                    logger.error("Error " + str(response.status_code) + " calling /v1/tp/stop_finder API; rate limit exceeded")
                else:
                    logger.error("Error " + str(response.status_code) + " calling /v1/tp/stop_finder API; check api key")

                return None

            # Parse the result as a JSON object
            result = response.json()

            # Just a quick check - the presence of systemMessages signifies an error
            if 'systemMessages' in result:
                logger.error("Stop ID " + stop + " does not exist")

            # Put in a pause here to try and make sure we stay under the 5 API calls/second limit
            # Not usually an issue but if multiple processes are running multiple calls we might hit it
            time.sleep(1.0)

        # We don't control how many journeys are returned any more, so need to be careful of running out of valid journeys if there is a filter in place, particularly a strict filter
        # It would be more efficient to return one journey, check if the filter is met and then retrieve the next one via a new query if not, but for now we'll only be making use of the journeys we've been given

        # Build the entire URL
        url = \
            'https://api.transport.nsw.gov.au/v1/tp/trip?' \
            'outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326' \
            '&depArrMacro=dep&itdDate=' + itdDate + '&itdTime=' + itdTime + \
            '&type_origin=any&name_origin=' + self.name_origin + \
            '&type_destination=any&name_destination=' + self.destination + \
            '&TfNSWTR=true'
            # '&calcNumberOfTrips=' + str(journeys_to_retrieve) + \


        # Send the query and return an error if something goes wrong
        # Otherwise store the response
        try:
            response = requests.get(url, headers=header, timeout=20)
        except:
            logger.error("Network or timeout error")
            return None

        # If we get bad status code, log error and return with n/a or an empty string
        if response.status_code != 200:
           if response.status_code == 429:
               logger.error("Error " + str(response.status_code) + " calling /v1/tp/stop_finder API; rate limit exceeded")
           else:
               logger.error("Error " + str(response.status_code) + " calling /v1/tp/stop_finder API; check api key")

           return None

        # Parse the result as a JSON object
        result = response.json()

        # The API will always return a valid trip, so it's just a case of grabbing what we need...
        # We're only reporting on the origin and destination, it's out of scope to discuss the specifics of the ENTIRE journey
        # This isn't a route planner, just a 'how long until the next journey I've specified' tool
        # The assumption is that the travelee will know HOW to make the defined journey, they're just asking WHEN it's happening next
        # All we potentially have to do is find the first trip that matches the transport_type filter

        if raw_output == True:
            # Just return the raw output
            return json.dumps(result)
            exit

        retrieved_journeys = len(result['journeys'])

        # Loop through the results applying filters where required, and generate the appropriate JSON output including an array of in-scope trips
        json_output=''
        found_journeys = 0
        no_valid_journeys = False

        for current_journey_index in range (0, retrieved_journeys, 1):
            # Look for a trip with a matching transport type filter in at least one of its legs.  Either ANY, or the first leg, depending on how strict we're being
            journey, next_journey_index = self.find_next_journey(result['journeys'], current_journey_index, transport_type, strict_transport_type, route_filter)

            if ((journey is None) or (journey['legs']) is None):
                pass
            else:
                legs = journey['legs']
                first_leg = self.find_first_leg(legs, transport_type, strict_transport_type, route_filter)

                #Executive decision - don't be strict on the last leg, there's often some walking (transport type 100) involved.
                last_leg = self.find_last_leg(legs, transport_type, False)
                changes = self.find_changes(legs, transport_type)

                origin = first_leg['origin']
                first_stop = first_leg['destination']
                destination = last_leg['destination']
                transportation = first_leg['transportation']

                # Origin info
                origin_stop_id = origin['id']
                origin_name = origin['name']
                origin_departure_time = origin['departureTimeEstimated']
                origin_departure_time_planned = origin['departureTimePlanned']

                t1 = datetime.strptime(origin_departure_time, fmt).timestamp()
                t2 = datetime.strptime(origin_departure_time_planned, fmt).timestamp()
                delay = int((t1-t2) / 60)

                # How long until it leaves?
                due = self.get_due(datetime.strptime(origin_departure_time, fmt))

                # Destination info
                destination_stop_id = destination['id']
                destination_name = destination['name']
                destination_arrival_time = destination['arrivalTimeEstimated']

                # Origin type info - train, bus, etc
                #origin_mode_temp = transportation['product']['class']
                origin_mode = self.get_mode(transportation['product']['class'])
                origin_mode_name = transportation['product']['name']

                # RealTimeTripID info so we can try and get the current location later
                realtimetripid = 'n/a'
                if 'properties' in transportation:
                    if 'RealtimeTripId' in transportation['properties']:
                        realtimetripid = transportation['properties']['RealtimeTripId']

                # Line info
                origin_line_name_short = "unknown"
                if 'disassembledName' in transportation:
                    origin_line_name_short = transportation['disassembledName']

                origin_line_name = "unknown"
                if 'number' in transportation:
                    origin_line_name = transportation['number']

                # Occupancy info, if it's there
                occupancy = 'unknown'
                if 'properties' in first_stop:
                    if 'occupancy' in first_stop['properties']:
                        occupancy = first_stop['properties']['occupancy']

                alerts = "[]"
                if (include_alerts != 'none'):
                    # We'll be adding these to the returned JSON string as an array
                    # Only include alerts of the specified priority or greater, and of the specified type
                    alerts = self.find_alerts(legs, self.include_alerts, self.alert_type)

                latitude = 'n/a'
                longitude = 'n/a'

                if ((realtimetripid != 'n/a') and (self.include_realtime_location) == True):
                    # See if we can get the latitute and longitude via the Realtime Vehicle Positions API
                    # Build the URL(s) - some modes have multiple GTFS sources, unforunately
                    url_path = self.get_url(origin_mode)
                    url_list = self.get_url_path(origin_mode)
                    bFoundTripID = False

                    auth = 'apikey ' + self.api_key
                    header = {'Authorization': auth}

                    for mode_url in url_list:
                        url = url_path + mode_url

                        response = requests.get(url, headers=header, timeout=10)

                        # Only try and process the results if we got a good return code
                        if response.status_code == 200:
                            # Search the feed and see if we can match realtimetripid to trip_id
                            # If we do, capture the latitude and longitude
                            feed = gtfs_realtime_pb2.FeedMessage()
                            feed.ParseFromString(response.content)

                            reg = re.compile(realtimetripid)

                            for entity in feed.entity:
                                if bool(re.match(reg, entity.vehicle.trip.trip_id)):
                                    latitude = entity.vehicle.position.latitude
                                    longitude = entity.vehicle.position.longitude

                                    # We found it, so flag it and break out
                                    bFoundTripID = True
                                    break

                        if bFoundTripID == True:
                            # No need to look any further
                            break

                        # Put in a quick pause here to try and make sure we stay under the 5 API calls/second limit
                        # Not usually an issue but if multiple processes are running multiple calls we might hit it
                        time.sleep(0.5)


                self.info = {
                    ATTR_DUE_IN: due,
                    ATTR_DELAY: delay,
                    ATTR_ORIGIN_STOP_ID : origin_stop_id,
                    ATTR_ORIGIN_NAME : origin_name,
                    ATTR_DEPARTURE_TIME : origin_departure_time,
                    ATTR_DESTINATION_STOP_ID : destination_stop_id,
                    ATTR_DESTINATION_NAME : destination_name,
                    ATTR_ARRIVAL_TIME : destination_arrival_time,
                    ATTR_ORIGIN_TRANSPORT_TYPE : origin_mode,
                    ATTR_ORIGIN_TRANSPORT_NAME: origin_mode_name,
                    ATTR_ORIGIN_LINE_NAME : origin_line_name,
                    ATTR_ORIGIN_LINE_NAME_SHORT : origin_line_name_short,
                    ATTR_CHANGES: changes,
                    ATTR_OCCUPANCY : occupancy,
                    ATTR_REAL_TIME_TRIP_ID : realtimetripid,
                    ATTR_LATITUDE : latitude,
                    ATTR_LONGITUDE : longitude,
                    ATTR_ALERTS: json.loads(alerts)
                    }

                found_journeys = found_journeys + 1

                # Add to the return array
                if (no_valid_journeys == True):
                    break

                if (found_journeys >= 2):
                    json_output = json_output + ',' + json.dumps(self.info)
                else:
                    json_output = json_output + json.dumps(self.info)

                if (found_journeys == journeys_to_return):
                    break

                current_journey_index = next_journey_index

        json_output='{"journeys_to_return": ' + str(self.journeys_to_return) + ', "journeys_with_data": ' + str(found_journeys) + ', "journeys": [' + json_output + ']}'
        return json_output


#    def find_first_journey(self, journeys, journeytype, strictness):
#        # Find the first journey that has a leg is of the requested type
#        journey_count = len(journeys)
#        for journey in range (0, journey_count, 1):
#            leg = self.find_first_leg(journeys[journey]['legs'], journeytype, strictness)
#            if leg is not None:
#                return journeys[journey]
#
#        # Hmm, we didn't find one
#        return None


    def find_next_journey(self, journeys, start_journey_index, journeytype, strict, route_filter):
        # Fnd the next journey that has a leg of the requested type, and/or that satisfies the route filter
        journey_count = len(journeys)

        # Some basic error checking
        if start_journey_index > journey_count:
            return None, None

        for journey_index in range (start_journey_index, journey_count, 1):
            leg = self.find_first_leg(journeys[journey_index]['legs'], journeytype, strict, route_filter)
            if leg is not None:
                return journeys[journey_index], journey_index + 1
            else:
                return None, None

        # Hmm, we didn't find one
        return None, None


    def find_first_leg(self, legs, legtype, strict, route_filter):
        # Find the first leg of the requested type
        leg_count = len(legs)
        for leg_index in range (0, leg_count, 1):
            #First, check against the route filter
            origin_line_name_short = 'n/a'
            origin_line_name = 'n/a'

            if 'transportation' in legs[leg_index]:
                if 'disassembledName' in legs[leg_index]['transportation']:
                    origin_line_name_short = legs[leg_index]['transportation']['disassembledName'].lower()
                    origin_line_name = legs[leg_index]['transportation']['number'].lower()

            if (route_filter in origin_line_name_short or route_filter in origin_line_name):
                leg_class = legs[leg_index]['transportation']['product']['class']
                # We've got a filter, and the leg type matches it, so return that leg
                if legtype != 0 and leg_class == legtype:
                    return legs[leg_index]

                # We don't have a filter, and this is the first non-walk/cycle leg so return that leg
                if  legtype == 0 and leg_class < 99:
                    return legs[leg_index]

                # Exit if we're doing strict filtering and we haven't found that type in the first leg
                if legtype != 0 and strict == True:
                    return None

        # Hmm, we didn't find one
        return None


    def find_last_leg(self, legs, legtype, strict):
        # Find the last leg of the requested type
        leg_count = len(legs)
        for leg_index in range (leg_count - 1, -1, -1):
            leg_class = legs[leg_index]['transportation']['product']['class']

            # We've got a filter, and the leg type matches it, so return that leg
            if legtype != 0 and leg_class == legtype:
                return legs[leg_index]

            # We don't have a filter, and this is the first non-walk/cycle leg so return that leg
            if  legtype == 0 and leg_class < 99:
                return legs[leg_index]

            # Exit if we're doing strict filtering and we haven't found that type in the first leg
            if legtype != 0 and strict == True:
                return None

        # Hmm, we didn't find one
        return None


    def find_changes(self, legs, legtype):
        # Find out how often we have to change
        changes = 0
        leg_count = len(legs)

        for leg_index in range (0, leg_count, 1):
            leg_class = legs[leg_index]['transportation']['product']['class']
            if leg_class == legtype or legtype == 0:
                changes = changes + 1

        return changes - 1


    def find_alerts(self, legs, priority_filter, alert_type):
        # Return an array of all the alerts on this trip that meet the priority level and alert type
        leg_count = len(legs)
        found_alerts = []
        priority_minimum = self.get_alert_priority(priority_filter)
        alert_list = alert_type.split("|")

        for leg_index in range (0, leg_count, 1):
            current_leg = legs[leg_index]
            if 'infos' in current_leg:
                alerts = current_leg['infos']
                for alert in alerts:
                    if (self.get_alert_priority(alert['priority'])) >= priority_minimum:
                        if (alert_type == 'all') or (alert['type'].lower() in alert_list):
                            found_alerts.append (alert)

        return json.dumps(found_alerts)


    def find_hints(self, legs, legtype, priority):
        # Return an array of all the hints on this trip that meet the priority type
        leg_count = len(legs)

        for leg_index in range (0, leg_count, 1):
            current_leg = legs[leg_index]
            leg_class = current_leg['transportation']['product']['class']
            if 'hints' in current_leg:
                hints = current_leg['hints']


    def get_mode(self, iconId):
        """Map the iconId to a full text string"""
        modes = {
            1   : "Train",
            2   : "Metro",
            4   : "Light rail",
            5   : "Bus",
            7   : "Coach",
            9   : "Ferry",
            11  : "School bus",
            99  : "Walk",
            100 : "Walk",
            107 : "Cycle"
        }
        return modes.get(iconId, None)

    def get_url(self, mode):
        """Map the journey mode to the proper base real time location URL """
        v1_url = "https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos"
        v2_url = "https://api.transport.nsw.gov.au/v2/gtfs/vehiclepos"

        url_options = {
            "Train"      : v2_url,
            "Metro"      : v2_url,
            "Light rail" : v1_url,
            "Bus"        : v1_url,
            "Coach"      : v1_url,
            "Ferry"      : v1_url,
            "School bus" : v1_url
        }
        return url_options.get(mode, None)


    def get_alert_priority(self, alert_priority):
        """Map the alert priority to a number so we can filter later """

        alert_priorities = {
            "all"      : 0,
            "veryLow"  : 1,
            "low"      : 2,
            "normal"   : 3,
            "high"     : 4,
            "veryHigh" : 5
        }
        return alert_priorities.get(alert_priority, 99)


    def get_url_path(self, mode):
        """Map the journey mode to the proper modifier URL """
        # There's probably a better way of mapping the bus route/stop/line number to the correct URL to call in the GTFS API, but as of now I don't know it... hence the brute force approach, although I hate the lack of elegance
        bus_list = ["/buses", "/regionbuses/centralwestandorana", "/regionbuses/centralwestandorana2", "/regionbuses/newenglandnorthwest", "/regionbuses/northcoast", "/regionbuses/northcoast2", "/regionbuses/northcoast3", "/regionbuses/riverinamurray", "/regionbuses/riverinamurray2", "/regionbuses/southeasttablelands", "/regionbuses/southeasttablelands2", "/regionbuses/sydneysurrounds", "/regionbuses/newcastlehunter", "/regionbuses/farwest"]

        url_options = {
            "Train"      : ["/sydneytrains"],
            "Metro"      : ["/metro"],
            "Light rail" : ["/lightrail/innerwest", "/lightrail/cbdandsoutheast", "/lightrail/newcastle"],
            "Bus"        : bus_list,
            "Coach"      : bus_list,
            "Ferry"      : ["/ferries/sydneyferries"],
            "School bus" : bus_list
        }
        return url_options.get(mode, None)


    def get_due(self, estimated):
        """Min until departure"""
        due = 0
        if estimated > datetime.utcnow():
            due = round((estimated - datetime.utcnow()).seconds / 60)
        return due
