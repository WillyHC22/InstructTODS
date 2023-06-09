SLOTS_REVERSE_REMAPPING = {
        "addr":"address",
        "post":"postcode",
        "leave":"leaveat",
        "arrive":"arriveby",
        "price":"pricerange",
        "fee":"price",
        "ref":"reference",
        "depart":"departure",
        "dest":"destination",}

SLOTS_REMAPPING = {
        # slots
        "address":"addr",
        "postcode":"post",
        "leaveat":"leave",
        "arriveby":"arrive",
        "pricerange":"price",
        "pickup":"depart",
        # "price":"fee",
        "reference":"ref",
        "departure":"depart",
        "destination":"dest",
        # values
        "not mentioned": "null",
        "unknown":"?", "inform":"?", "unk":"?", "needed":"?", "available":"?", "requested":"?", "request":"?", "n/a":"?",
        "catherine 's":"catherine's", "john 's":'john"s', "rosa 's":'rosa"s', "mary 's":'mary"s', "christ 's":"christ's",
        "alpha - milton":"alpha-milton", "michaelhouse cafe":"mic", " nights": "", " person": "", " night": "", " days": "", "after ": "",
        "kettle 's":"kettle's", "none":"",
        "free":"yes", "free wifi":"yes", "free parking":"yes"
}

GENERAL_TYPO = {
        # type
        "guesthouse":"guest house", "guesthouses":"guest house", "guest":"guest house", "mutiple sports":"multiple sports",
        "sports":"multiple sports", "mutliple sports":"multiple sports","swimmingpool":"swimming pool", "concerthall":"concert hall",
        "concert":"concert hall", "pool":"swimming pool", "night club":"nightclub", "mus":"museum", "ol":"architecture",
        "colleges":"college", "coll":"college", "architectural":"architecture", "musuem":"museum", "churches":"church",
        # area
        "center":"centre", "center of town":"centre", "near city center":"centre", "in the north":"north", "cen":"centre", "east side":"east",
        "east area":"east", "west part of town":"west", "ce":"centre",  "town center":"centre", "centre of cambridge":"centre",
        "city center":"centre", "the south":"south", "scentre":"centre", "town centre":"centre", "in town":"centre", "north part of town":"north",
        "centre of town":"centre", "cb30aq": "none",
        # price
        "mode":"moderate", "moderate -ly": "moderate", "mo":"moderate",
        # day
        "next friday":"friday", "monda": "monday",
        # parking
        "free parking":"free",
        # internet
        "free internet":"yes",
        # star
        "4 star":"4", "4 stars":"4", "0 star rarting":"none",
        # others
        # "y":"yes", "any":"dontcare", "n":"no", "does not care":"dontcare", "not men":"none", "not":"none", "not mentioned":"none",
        # '':"none", "not mendtioned":"none", "3 .":"3", "does not":"no", "fun":"none", "art":"none",
        }

SLOTS_DESCRIPTIONS = {
    "parking":"whether the place has parking or not",
    "pricerange":"price budget for the place",
    "internet":"whether the place has internet or not",
    "stay":"stay duration in the place",
    "type":"type of hotel building or attraction",
    "day":"day of the week for the booking or departure",
    "people":"number of people for booking",
    "area":"cardinal location of place of interest",
    "stars":"star rating of the place",
    "name":"name of the place",
    "leaveat":"leaving time",
    "destination":"destination place for the trip",
    "departure":"departure place for the trip",
    "arriveby":"arrival time",
    "food":"type of food",
    "time":"time for the booking",
}


#Free-form remapping
# FIXED_TYPOS_REMAPPING = {
#     #general
#     "thanks": "thank", "unknown":"?", "required":"?", "do nt care":"any",
#     #taxi
#     "from": "depart", "pickup_location":"depart", "taxi_departure":"depart", "leaving_from":"depart", "taxi_departure_time":"depart",
#     "to": "dest", "destination": "dest",
#     "taxi_time": "leave", "departure_time":"leave", "taxi_pickuptime":"leave", "taxi_leave_time":"leave", "departure time":"leave",
#     "time_arrival": "arrive", "taxi_arrival_time":"arrive",
#     "taxi_type":"car", "taxi_types":"car",
#     "taxi_phone":"phone",
#     # "after 17:15":"17:15", "after 16:30":"16:30", "after 15:00":"15:00", "after 04:30":"4:30", "after 11:00":"11:00",
#     #restaurant
#     "pricerange":"price",
#     "address":"addr",
#     "number_of_people":"people", "reservation_people":"people", "party_size":"people", "book_people":"people", "n_people":"people",
#     "reservation_time":"time", "book_time":"time",
#     "reservation_date":"day", "reservation_day":"day", "book_day":"day",
#     "reference number":"ref",
#     #hotel
#     "pricerange":"price",
#     "nights":"stay", "stay_duration":"stay", "duration":"stay", "reservation_duration":"stay", "n_nights":"stay",
#     "arrival_day":"day", "check_in_day":"day", "start_day":"day", "start_date":"day", "checkin_day":"day", "reservation_start":"day", "starting_date":"day", "date":"day", "date_start":"day",
#     "n":"people", "number_of_guests":"people",
#     "address":"addr", 
#     "postcode":"post",
#     #train
#     "departure": "depart", "departure_location":"depart", "origin":"depart",
#     "destination": "dest",
#     "timeofday": "leave", "pickup_time": "leave", "leaveat": "leave", "desired_departure_time":"leave",
#     "arriveby": "arrive", "arrival_time": "arrive", "arriving_by":"arrive", "arrive_by":"arrive",
#     #attraction
#     "ticket_count":"people", "ticket":"people", "tickets":"people",
#     #others
#     "michaelhouse cafe": "mic",
#     "the holy trinity church": "holy trinity church",
#     "alpha - milton guest house": "alpha-milton guest house",
#     "3:00": "03:00",
# }


