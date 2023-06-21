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

VALUES_FIX = {"fen ditton":"fenditton",
              "john's":"johns", "catherine's":"catherines",
              "the bridge guest":"bridge guest", "the rajmahal": "rajmahal", "the bedouin":"bedouin",
              "ian hong":"lan hong", "pizza express":"pizza hut",
              "express by holiday inn cambridge":"inn cambridge", "alpha-milton":"alpha-milton guest house", "el shaddai":"el shaddai guesthouse",
              "bringham new street":"birmingham new street",
              "king's lynn":"kings lynn",
              "nightclub":"night club", "concert hall":"concerthall", "guest house guest house":"guest house",
              "kettle's yard":"kettles yard",
              "3 00":"03:00", "9:30":"09:30", "2:30":"02:30", "1515hrs":"15:15", "9:15":"09:15", "109:30":"19:30", "9:45":"09:45", "7:15 p.m.":"07:15", "5:15":"05:15",
              "009:15":"09:15", "009:30":"09:30", "109:30":"19:30", "109:15":"19:15", "102:30":"12:30",
              "after ":"", " nights":"",
              "town centre":"centre",
             
              "free":"yes", "any":"dontcare"}

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
    "area":"cardinal location of the place of interest like north, center, west, etc...",
    "stars":"star rating of the place",
    "name":"name of the place",
    "leaveat":"leaving time",
    "destination":"destination place for the trip",
    "departure":"departure place for the trip",
    "arriveby":"arrival time",
    "food":"type of food",
    "time":"time for the booking",
}
