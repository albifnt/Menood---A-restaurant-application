from kivy_garden.mapview  import MapView
from kivy.clock import Clock
from kivy.app import App
from placemarker import PlaceMarker
from kivymd.uix.dialog import CucinaMDInputDialog
from urllib import parse
from kivy.network.urlrequest import UrlRequest
from clusterplacemarker import ClusterPlaceMarker
import certifi

class PlaceMapView(MapView):
    """
    Custom map view class to manage place markers based on user interaction and filters.

    Attributes:
        getting_places_timer: Timer object to delay fetching places until user interaction stops.
        place_names: List to store names of currently displayed places.
        flag: Flag to manage marker display based on zoom level changes.
        lista: Dictionary to map place names to their corresponding markers.
        types: String to accumulate active place types based on user filters.
        name_memory: List to temporarily store names of places to be removed from the map.

    """

    # This is the reference time
    getting_places_timer = None
    place_names = []
    flag = 1
    lista = {}
    types = ''
    name_memory = []

    def start_getting_places_in_FOV(self):
        """
        Initiates a timer to fetch places within the field of view after a 1-second delay.

        This method ensures that places are fetched only after the user has stopped interacting
        with the map, preventing frequent updates while the user scrolls.

        """
        try:
            self.getting_places_timer.cancel()
        except:
            pass

        self.getting_places_timer = Clock.schedule_once(self.get_places_in_FOV, 1)

    def get_places_in_FOV(self, *args):
        """
        Fetches and updates map markers based on the current field of view (FOV) of the map.

        This method retrieves places from the database based on the map's current zoom level and
        filters defined by the user (restaurant, pizzeria, sushi). It dynamically adds or removes
        markers (PlaceMarker or ClusterPlaceMarker) based on the fetched data and zoom level.

        """
        # Get reference to main app and database cursor
        app = App.get_running_app()

        if (app.root.ids['firstpage'].ids['filter_page'].ids['restaurant'].active == True):
            self.types += 'restaurant'
        if (app.root.ids['firstpage'].ids['filter_page'].ids['pizzeria'].active == True):
            self.types += 'pizzeria'
        if (app.root.ids['firstpage'].ids['filter_page'].ids['sushi'].active == True):
            self.types += 'sushi'

        if (self.zoom < 10):
            if (self.flag == 0):
                for mark in self.lista:
                    self.remove_widget(self.lista[mark])
                self.lista = {}
                self.place_names = []
                self.flag = 1

            min_lat, min_lon, max_lat, max_lon = self.get_bbox()
            sql_statement = "SELECT * FROM cities WHERE city_lon > %s AND city_lon < %s AND city_lat > %s AND city_lat < %s "%(min_lon, max_lon, min_lat, max_lat)
            app.cursor.execute(sql_statement)
            places = app.cursor.fetchall()
            for place in places:
                name = place[1]
                if name in self.place_names:
                    continue
                else:
                    self.add_place_cluster(place)

        elif (self.zoom >= 10):
            if (self.flag == 1):
                for mark in self.lista:
                    self.remove_widget(self.lista[mark])
                self.lista = {}
                self.place_names = []
                self.flag = 0
            min_lat, min_lon, max_lat, max_lon = self.get_bbox()
            sql_statement = "SELECT * FROM food_places WHERE place_lon > %s AND place_lon < %s AND place_lat > %s AND place_lat < %s"%(min_lon, max_lon, min_lat, max_lat)
            app.cursor.execute(sql_statement)
            places = app.cursor.fetchall()
            for place in places:
                name = place[1]
                type = place[4]
                if type in self.types:
                    if name in self.place_names:
                        continue
                    else:
                        self.add_place(place)
            for place in self.place_names:
                sql_statement = "SELECT * FROM food_places WHERE place_name = '%s'" %(place)
                app.cursor.execute(sql_statement)
                data = app.cursor.fetchall()
                name_type = data[0][1]
                check_type = data[0][4]
                if check_type in self.types:
                    continue
                else:
                    self.remove_widget(self.lista[name_type])
                    del self.lista[name_type]
                    self.name_memory.append(name_type)

            if self.name_memory != []:
                for index in self.name_memory:
                    self.place_names.remove(index)
                self.name_memory = []

        self.types = ''

    def add_place(self, place):
        """
        Adds a marker (PlaceMarker) to the map for the given place data.

        Parameters:
        - place (tuple): Tuple containing place data fetched from the database.

        """

        # Create the marker
        lat, lon = place[2], place[3]
        marker = PlaceMarker(lat=lat, lon=lon)
        if (self.zoom >= 10):
            marker.source = "appimages/" + place[4] + ".png"
        marker.place_data = place

        # Add the marker to the map
        self.add_widget(marker)
        self.lista[place[1]] = marker

        # Keep the track of the marker name
        name = place[1]
        self.place_names.append(name)

    def add_place_cluster(self, place):
        """
        Adds a cluster marker (ClusterPlaceMarker) to the map for the given place data.

        Parameters:
        - place (tuple): Tuple containing place data fetched from the database.

        """
        # Create the marker
        lat, lon = place[2], place[3]
        marker = ClusterPlaceMarker(lat=lat, lon=lon)

        # Add the marker to the map
        self.add_widget(marker)
        self.lista[place[1]] = marker

        # Keep the track of the marker name
        name = place[1]
        self.place_names.append(name)

    def zoom_center(self):
        """
        Centers the map view on a specific location defined by the `blinker` widget's coordinates.
        """
        self.center_on(self.ids['blinker'].lat, self.ids['blinker'].lon)



class SearchPopupMenu(CucinaMDInputDialog):
    """
    A custom popup menu for location search.

    Inherits from CucinaMDInputDialog and adds functionality for geocoding
    address input provided by the user. The popup includes an "Ok" button
    for confirming the input, and upon confirmation, it triggers a callback
    function to initiate geocoding.

    Attributes:
        text_button_ok (str): Text label for the confirmation button ("Ok").
    """

    text_button_ok = "Ok"
    def __init__(self):
        super().__init__()
        self.size_hint = [0.9, 0.27]
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.events_callback = self.callback

    def open(self):
        """
        Opens the popup and schedules focus on the input field.
        """
        super().open()
        Clock.schedule_once(self.set_field_focus, 0.5)

    def callback(self, *args):
        """
        Callback function invoked when the "Ok" button is pressed,
        retrieves the entered address and initiates geocoding.
        """
        address = self.text_field.text
        self.geocode_get_lat_lon(address)

    def geocode_get_lat_lon(self, address):
        """
        Sends a geocoding request to retrieve latitude and longitude for the address.
        """
        app_key = "INSERT YOUR APP KEY"
        address = parse.quote(address)
        url = "https://geocoder.ls.hereapi.com/search/6.2/geocode.json?languages=en-US&maxresults=4&searchtext=%s&apiKey=%s"%(address, app_key)
        UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error, ca_file=certifi.where())

    def success(self, urlrequest, result):
        """
        Handles successful geocoding response, centers the map view on the retrieved location.
        """
        print("Success")
        self.text_field.text = ""
        if result['Response']['View'] != []:
            latitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
            longitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
            app = App.get_running_app()
            mapview = app.root.ids['firstpage'].ids['place_map_view']
            mapview.center_on(latitude, longitude)
            mapview.zoom = 17
        else:
            pass

    def failure(self, urlrequest, result):
        """
        Handles failed geocoding response.
        """
        print("Failure")
        print(result)

    def error(self, urlrequest, result):
        """
        Handles errors during geocoding request.
        """
        print("Error")
        print(result)
