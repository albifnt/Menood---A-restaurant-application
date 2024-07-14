from kivy.app import App
from smallmapview import SmallMapView
from smallmapmarker import SmallMapMarker
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty
import requests
import json

class DescriptionPage(Screen):
    """
    DescriptionPage is a subclass of Screen, designed to display detailed information
    about a specific place or location. It contains various properties to store and
    present data such as the place's name, address, description, timetable, contact 
    details, and menu items.

    Attributes:
        uid (StringProperty): Unique identifier for the place, defaulting to "Missing data".
        name_place (StringProperty): Name of the place, defaulting to "Name".
        lat (ObjectProperty): Latitude coordinate of the place, defaulting to 45.404.
        lon (ObjectProperty): Longitude coordinate of the place, defaulting to 12.107.
        address_title (StringProperty): Title for the address section, defaulting to "Address".
        address (StringProperty): Full address of the place, defaulting to "Address".
        short_address (StringProperty): Shortened version of the address, defaulting to "Short Address".
        description_title (StringProperty): Title for the description section, defaulting to "Description".
        description (StringProperty): Detailed description of the place, defaulting to "Description".
        time_table (StringProperty): Title for the timetable section, defaulting to "Time table".
        monday_title (StringProperty): Title for Monday's timetable, defaulting to "Monday".
        tuesday_title (StringProperty): Title for Tuesday's timetable, defaulting to "Tuesday".
        wednesday_title (StringProperty): Title for Wednesday's timetable, defaulting to "Wednesday".
        thursday_title (StringProperty): Title for Thursday's timetable, defaulting to "Thursday".
        friday_title (StringProperty): Title for Friday's timetable, defaulting to "Friday".
        saturday_title (StringProperty): Title for Saturday's timetable, defaulting to "Saturday".
        sunday_title (StringProperty): Title for Sunday's timetable, defaulting to "Sunday".
        telephone_title (StringProperty): Title for the telephone section, defaulting to "Telephone".
        telephone (StringProperty): Telephone number of the place, defaulting to "Telephone".
        parking_title (StringProperty): Title for the parking section, defaulting to "Parking".
        parking (StringProperty): Parking details, defaulting to an empty string.
        website (StringProperty): Website URL of the place, defaulting to "Website".
        monday (StringProperty): Monday's opening hours, defaulting to "Monday".
        tuesday (StringProperty): Tuesday's opening hours, defaulting to "Tuesday".
        wednesday (StringProperty): Wednesday's opening hours, defaulting to "Wednesday".
        thursday (StringProperty): Thursday's opening hours, defaulting to "Thurday".
        friday (StringProperty): Friday's opening hours, defaulting to "Friday".
        saturday (StringProperty): Saturday's opening hours, defaulting to "Saturday".
        sunday (StringProperty): Sunday's opening hours, defaulting to "Sunday".
        favorite_places_title (StringProperty): Title for the favorite places section, defaulting to "Add to favorites".
        favorite_icon (StringProperty): Icon for adding to favorites, defaulting to "heart".

        Plus plates information.
        """
    uid = StringProperty("Missing data")
    name_place = StringProperty("Name")
    #place_image = StringProperty("appimages/Place.jpg")
    lat = ObjectProperty(45.404)
    lon = ObjectProperty(12.107)
    address_title = StringProperty("Address")
    address = StringProperty("Address")
    short_address = StringProperty("Short Address")
    description_title = StringProperty("Description")
    description = StringProperty("Description")
    time_table = StringProperty("Time table")
    monday_title = StringProperty("Monday")
    tuesday_title = StringProperty("Tuesday")
    wednesday_title = StringProperty("Wednesday")
    thursday_title = StringProperty("Thursday")
    friday_title = StringProperty("Friday")
    saturday_title = StringProperty("Saturday")
    sunday_title = StringProperty("Sunday")
    telephone_title = StringProperty("Telephone")
    telephone = StringProperty("Telephone")
    parking_title = StringProperty("Parking")
    parking = StringProperty("")
    website = StringProperty("Website")
    monday = StringProperty("Monday")
    tuesday = StringProperty("Tuesday")
    wednesday = StringProperty("Wednesday")
    thursday = StringProperty("Thurday")
    friday = StringProperty("Friday")
    saturday = StringProperty("Saturday")
    sunday = StringProperty("Sunday")
    favorite_places_title = StringProperty("Add to favorites")
    favorite_icon = StringProperty("heart")
    first_plates_name = StringProperty("First Plates")
    first_plate_1 = StringProperty("Missing data")
    color_first_plate_1 = ObjectProperty([0, 0, 0, 1])
    first_plate_1_ingredients = StringProperty("Missing data")
    first_plate_1_price = StringProperty("")
    first_plate_2 = StringProperty("Missing data")
    color_first_plate_2 = ObjectProperty([0, 0, 0, 1])
    first_plate_2_ingredients = StringProperty("Missing data")
    first_plate_2_price = StringProperty("")
    first_plate_3 = StringProperty("Missing data")
    color_first_plate_3 = ObjectProperty([0, 0, 0, 1])
    first_plate_3_ingredients = StringProperty("Missing data")
    first_plate_3_price = StringProperty("")
    first_plate_4 = StringProperty("Missing data")
    color_first_plate_4 = ObjectProperty([0, 0, 0, 1])
    first_plate_4_ingredients = StringProperty("Missing data")
    first_plate_4_price = StringProperty("")
    first_plate_5 = StringProperty("Missing data")
    color_first_plate_5 = ObjectProperty([0, 0, 0, 1])
    first_plate_5_ingredients = StringProperty("Missing data")
    first_plate_5_price = StringProperty("")
    first_plate_6 = StringProperty("Missing data")
    color_first_plate_6 = ObjectProperty([0, 0, 0, 1])
    first_plate_6_ingredients = StringProperty("Missing data")
    first_plate_6_price = StringProperty("")
    first_plate_7 = StringProperty("Missing data")
    color_first_plate_7 = ObjectProperty([0, 0, 0, 1])
    first_plate_7_ingredients = StringProperty("Missing data")
    first_plate_7_price = StringProperty("")
    first_plate_8 = StringProperty("Missing data")
    color_first_plate_8 = ObjectProperty([0, 0, 0, 1])
    first_plate_8_ingredients = StringProperty("Missing data")
    first_plate_8_price = StringProperty("")
    first_plate_9 = StringProperty("Missing data")
    color_first_plate_9 = ObjectProperty([0, 0, 0, 1])
    first_plate_9_ingredients = StringProperty("Missing data")
    first_plate_9_price = StringProperty("")
    first_plate_10 = StringProperty("Missing data")
    color_first_plate_10 = ObjectProperty([0, 0, 0, 1])
    first_plate_10_ingredients = StringProperty("Missing data")
    first_plate_10_price = StringProperty("")
    second_plates_name = StringProperty("Second Plates")
    second_plate_1 = StringProperty("Missing data")
    color_second_plate_1 = ObjectProperty([0, 0, 0, 1])
    second_plate_1_ingredients = StringProperty("Missing data")
    second_plate_1_price = StringProperty("")
    second_plate_2 = StringProperty("Missing data")
    color_second_plate_2 = ObjectProperty([0, 0, 0, 1])
    second_plate_2_ingredients = StringProperty("Missing data")
    second_plate_2_price = StringProperty("")
    second_plate_3 = StringProperty("Missing data")
    color_second_plate_3 = ObjectProperty([0, 0, 0, 1])
    second_plate_3_ingredients = StringProperty("Missing data")
    second_plate_3_price = StringProperty("")
    second_plate_4 = StringProperty("Missing data")
    color_second_plate_4 = ObjectProperty([0, 0, 0, 1])
    second_plate_4_ingredients = StringProperty("Missing data")
    second_plate_4_price = StringProperty("")
    second_plate_5 = StringProperty("Missing data")
    color_second_plate_5 = ObjectProperty([0, 0, 0, 1])
    second_plate_5_ingredients = StringProperty("Missing data")
    second_plate_5_price = StringProperty("")
    second_plate_6 = StringProperty("Missing data")
    color_second_plate_6 = ObjectProperty([0, 0, 0, 1])
    second_plate_6_ingredients = StringProperty("Missing data")
    second_plate_6_price = StringProperty("")
    second_plate_7 = StringProperty("Missing data")
    color_second_plate_7 = ObjectProperty([0, 0, 0, 1])
    second_plate_7_ingredients = StringProperty("Missing data")
    second_plate_7_price = StringProperty("")
    second_plate_8 = StringProperty("Missing data")
    color_second_plate_8 = ObjectProperty([0, 0, 0, 1])
    second_plate_8_ingredients = StringProperty("Missing data")
    second_plate_8_price = StringProperty("")
    second_plate_9 = StringProperty("Missing data")
    color_second_plate_9 = ObjectProperty([0, 0, 0, 1])
    second_plate_9_ingredients = StringProperty("Missing data")
    second_plate_9_price = StringProperty("")
    second_plate_10 = StringProperty("Missing data")
    color_second_plate_10 = ObjectProperty([0, 0, 0, 1])
    second_plate_10_ingredients = StringProperty("Missing data")
    second_plate_10_price = StringProperty("")
    third_plates_name = StringProperty("Third Plates")
    third_plate_1 = StringProperty("Missing data")
    color_third_plate_1 = ObjectProperty([0, 0, 0, 1])
    third_plate_1_ingredients = StringProperty("Missing data")
    third_plate_1_price = StringProperty("")
    third_plate_2 = StringProperty("Missing data")
    color_third_plate_2 = ObjectProperty([0, 0, 0, 1])
    third_plate_2_ingredients = StringProperty("Missing data")
    third_plate_2_price = StringProperty("")
    third_plate_3 = StringProperty("Missing data")
    color_third_plate_3 = ObjectProperty([0, 0, 0, 1])
    third_plate_3_ingredients = StringProperty("Missing data")
    third_plate_3_price = StringProperty("")
    third_plate_4 = StringProperty("Missing data")
    color_third_plate_4 = ObjectProperty([0, 0, 0, 1])
    third_plate_4_ingredients = StringProperty("Missing data")
    third_plate_4_price = StringProperty("")
    third_plate_5 = StringProperty("Missing data")
    color_third_plate_5 = ObjectProperty([0, 0, 0, 1])
    third_plate_5_ingredients = StringProperty("Missing data")
    third_plate_5_price = StringProperty("")
    third_plate_6 = StringProperty("Missing data")
    color_third_plate_6 = ObjectProperty([0, 0, 0, 1])
    third_plate_6_ingredients = StringProperty("Missing data")
    third_plate_6_price = StringProperty("")
    third_plate_7 = StringProperty("Missing data")
    color_third_plate_7 = ObjectProperty([0, 0, 0, 1])
    third_plate_7_ingredients = StringProperty("Missing data")
    third_plate_7_price = StringProperty("")
    third_plate_8 = StringProperty("Missing data")
    color_third_plate_8 = ObjectProperty([0, 0, 0, 1])
    third_plate_8_ingredients = StringProperty("Missing data")
    third_plate_8_price = StringProperty("")
    third_plate_9 = StringProperty("Missing data")
    color_third_plate_9 = ObjectProperty([0, 0, 0, 1])
    third_plate_9_ingredients = StringProperty("Missing data")
    third_plate_9_price = StringProperty("")
    third_plate_10 = StringProperty("Missing data")
    color_third_plate_10 = ObjectProperty([0, 0, 0, 1])
    third_plate_10_ingredients = StringProperty("Missing data")
    third_plate_10_price = StringProperty("")