from kivy.app import App
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog

class GpsHelper:
    """
    A helper class to manage GPS functionality within the application.

    Methods:
        run(): Initializes and starts the GPS blinker animation and handles permission requests on Android.
        update_blinker_position(*args, **kwargs): Updates the GPS blinker position with the latest GPS coordinates.
        on_auth_status(general_status, status_message): Handles the authentication status of the GPS provider.
    """
    #has_centered_map = False

    def run(self):
        """
        Starts the GPS blinker animation and requests necessary permissions on Android devices.

        Also configures the GPS settings for Android and iOS platforms.
        """
        # Get reference to GPS blinker, then call blink()
        gps_blinker = App.get_running_app().root.ids['firstpage'].ids['place_map_view'].ids['blinker']

        # Start blinking the GPS blinker
        gps_blinker.blink()

        # Request permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permissions, results):
                """
                Callback function to handle the results of the permission request.
                
                Args:
                    permissions (list): List of permissions requested.
                    results (list): List of results corresponding to the requested permissions.
                """
                if all([res for res in results]):
                    print("Got all permissions")
                else:
                    print("Did not get all permissions")
            request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION], callback)

        # Configure GPS
        if platform == 'android' or platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.update_blinker_position, on_status=self.on_auth_status)
            gps.start(minTime=1000, minDistance=0)

    def update_blinker_position(self, *args, **kwargs):
        """
        Updates the GPS blinker position with the latest GPS coordinates.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments containing GPS coordinates ('lat' and 'lon').
        """
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']
        print("GPS POSITION", my_lat, my_lon)
        # Update GpsBlinker position
        gps_blinker = App.get_running_app().root.ids['firstpage'].ids['place_map_view'].ids['blinker']
        gps_blinker.lat = my_lat
        gps_blinker.lon = my_lon

        # Center map on my GPS
        #if not self.has_centered_map:
        #    map = App.get_running_app().root.ids['firstpage'].ids['place_map_view']
        #    map.center_on(my_lat, my_lon)
        #    self.has_centered_map = True

    def on_auth_status(self, general_status, status_message):
        """
        Handles changes in authentication status related to GPS provider.

        Args:
            general_status (str): The general status of the GPS provider.
            status_message (str): Additional status message related to the provider.

        Notes:
            If the general status indicates the provider is enabled, no action is taken.
            Otherwise, prompts the user to grant GPS access by displaying a popup.

            To enable the popup functionality, uncomment the line: self.open_gps_access_popup()
        """
        if general_status == 'provider-enabled':
            pass
        else:
            pass
            #self.open_gps_access_popup()

    #def open_gps_access_popup(self):
    #    dialog = MDDialog(title="GPS Error", text="You need to enable the GPS access for the app to work properly")
    #    dialog.size_hint = [.8, .8]
    #    dialog.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    #    dialog.open()
