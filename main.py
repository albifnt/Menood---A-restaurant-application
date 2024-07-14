from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from placemapview import PlaceMapView, SearchPopupMenu
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivymd.toast import toast
import requests
import json
from placemarker import PlaceMarker
from favoriteplacebanner import FavoritePlaceBanner
from searchplacebanner import SearchPlaceBanner
from descriptionpage import DescriptionPage
from searchdescriptionpage import SearchDescriptionPage
from gpshelper import GpsHelper
import os
import sqlite3
import plyer

import urllib.request

from datetime import datetime

class FirstPage(Screen):
    """
    The FirstPage class represents the primary screen of the application.
    """
    pass

class SecondPage(Screen):
    """
    The SecondPage class represents the secondary screen of the application.
    """
    pass

class FoodTastes(Screen):
    """
    The FoodTastes class represents the screen of the application where the user
    specify their preferences.
    """
    pass

class SearchPage(Screen):
    """
    The SearchPage class represents the screen of the application where the user
    can look for specific restaurants.
    """
    pass

class AccountPage(Screen):
    """
    The AccountPage class represents the screen of the application where the user
    can see the accont details.
    """
    pass

class LanguagePage(Screen):
    """
    The LanguagePage class represents the screen of the application where the user
    can select the language.
    """
    pass

class SuggestionPage(Screen):
    """
    The SuggestionPage class represents the screen of the application where the 
    user can receive suggestions.
    """
    pass

class FilterPage(Screen):
    """
    The FilterPage class represents the screen of the application where the user
    can specify the filters.
    """
    pass

class FavoritePage(Screen):
    """
    The FavoritePage class represents the screen of the application where the user
    preferences are specified.
    """
    pass

class LogoutPage(Screen):
    """
    The LogoutPage class represents the logout screen of the application.
    """
    pass

# CLASS FOR THE MAIN APP
class MainApp(MDApp):
    connection = None
    cursor = None
    user_language = ''
    favorite_places_dictionary = {}
    search_list = []

    def set_ids(self, localId, idToken):
        """
        Sets user IDs and initializes UI elements based on user data retrieved from a remote server.

        Args:
            localId (str): The local user ID.
            idToken (str): The authentication token used for accessing user data.

        Notes:
            This method fetches user-specific data from a server using the provided IDs and updates various UI elements
            with language-specific content and user preferences.

            It populates buttons, text fields, and other UI components based on the user's language settings and stored data.

            Make sure to replace "INSERT YOUR DOMAIN" in the URL with the appropriate domain for retrieving user data.

        """
        self.localId = localId
        self.idToken = idToken
        self.refresh_token_file = self.root.ids['firebase_login_screen'].refresh_token_file
        data_request = requests.get("INSERT YOUR DOMAIN" + self.localId + ".json?auth=" + self.idToken)
        data = json.loads(data_request.content.decode())
        if (data_request.ok == True and data == None):
            with open('data/initial_data.txt') as file:
                data = file.read()
            data = json.loads(data)
            self.values = data['values'].split(",")
            self.index = data['index']
            self.intolerant = data['intolerant'].split(",")
            self.flag = 'no_block'

        # LANGUAGE
        # User_language
        self.user_language = data['user_language']

        # SUGGESTION
        self.suggestion = data['suggestion']

        # Set the buttons text to the proper language
        with open('dictionaries/' + self.user_language + '.txt', encoding='utf-8') as file:
            dictionary = file.read()
        self.dictionary = json.loads(dictionary)

        # AccountPage: language
        self.root.ids['firstpage'].ids['account_page'].ids['button_language'].text = self.dictionary['button_language']
        self.root.ids['firstpage'].ids['language_page'].ids['button_language'].text = self.dictionary['button_language']
        self.root.ids['firstpage'].ids['language_page'].ids[self.user_language].color = [0,0.635,0.910,1]
        self.root.ids['firstpage'].ids['account_page'].ids['suggestion'].text = self.dictionary['suggestion']
        self.root.ids['firstpage'].ids['account_page'].ids['button_favorite'].text = self.dictionary['button_favorite']
        self.root.ids['firstpage'].ids['account_page'].ids['tutorial'].text = self.dictionary['tutorial']
        self.root.ids['firstpage'].ids['account_page'].ids['button_logout'].text = self.dictionary['button_logout']
        self.root.ids['firstpage'].ids['suggestion_page'].ids['suggestion'].text = self.dictionary['suggestion']
        self.root.ids['firstpage'].ids['suggestion_page'].ids[self.suggestion].color = [0, 0.635, 0.910, 1]
        self.root.ids['firstpage'].ids['suggestion_page'].ids['active'].text = self.dictionary['active']
        self.root.ids['firstpage'].ids['suggestion_page'].ids['inactive'].text = self.dictionary['inactive']
        self.root.ids['firstpage'].ids['account_page'].ids['filters'].text = self.dictionary['filters']
        self.root.ids['firstpage'].ids['filter_page'].ids['filters'].text = self.dictionary['filters']
        self.root.ids['firstpage'].ids['account_page'].ids['website'].text = self.dictionary['website']
        self.root.ids['firstpage'].ids['logout_page'].ids['exit_sentence'].text = self.dictionary['exit_sentence']
        self.root.ids['firstpage'].ids['logout_page'].ids['no'].text = self.dictionary['no']
        self.root.ids['firstpage'].ids['logout_page'].ids['yes'].text = self.dictionary['yes']
        self.root.ids['firstpage'].ids['search_page'].ids['name_place'].hint_text = self.dictionary['name_place']
        self.root.ids['firstpage'].ids['search_page'].ids['city_place'].hint_text = self.dictionary['city_place']
        # Filters: Button-switch filters
        self.root.ids['firstpage'].ids['filter_page'].ids['restaurant_filter'].text = self.dictionary['restaurant_filter']
        self.root.ids['firstpage'].ids['filter_page'].ids['pizzeria_filter'].text = self.dictionary['pizzeria_filter']
        self.root.ids['firstpage'].ids['filter_page'].ids['sushi_filter'].text = self.dictionary['sushi_filter']
        # FavoritePage: title
        self.root.ids['firstpage'].ids['favorite_page'].ids['favorite_places_title'].text = self.dictionary['favorite_places_title']

        # Populate favorite place page
        banner_favorite = self.root.ids['firstpage'].ids['favorite_page'].ids['favorite_place_banner']
        self.favorite_list = data['favorites']
        for key in self.favorite_list:
            if (key == '__no_data__'):
                pass
            else:
                W = FavoritePlaceBanner(uid=key, place_image="appimages/pizzeria.png", place_name=self.favorite_list[key]['name'], place_address=self.favorite_list[key]['short_address'])
                self.favorite_places_dictionary[key] = W
                banner_favorite.add_widget(W)

        self.values = data['values'].split(",")
        self.index = data['index']
        self.intolerant = data['intolerant'].split(",")
        self.flag = 'no_block'

        # Open dictionary for food
        with open('dictionaries/food_' + self.user_language + '.txt', encoding='utf-8') as file:
            dictionary_food = file.read()
        self.dictionary_food = dictionary_food.split(',')

        # Display First Image
        self.root.ids['firstpage'].ids['food_tastes'].ids['food_image'].source = f"./foodimages/{self.index}.jpg"
        self.root.ids['firstpage'].ids['food_tastes'].ids['food_name'].text = "[b]" + self.dictionary_food[self.index][0].upper() + self.dictionary_food[self.index][1:] + "[/b]"
        self.root.ids['firstpage'].ids['food_tastes'].ids['progress_slider'].value = 1

        # Instantiate SearchPopUpMenu
        self.search_menu = SearchPopupMenu()

        self.root.ids['firstpage'].ids['bottom_navigation']._refresh_tabs()

        # Initialize GPS
        GpsHelper().run()

    def on_start(self):
        """
        Initializes the application upon startup.

        Notes:
        This method sets establishes a connection to the local SQLite database located at 
        'databases/database.db',and optionally, it connects to a MySQL database (commented 
        out for SQLite usage).

        """
        self.theme_cls.primary_palette = 'LightBlue'
        # Connect to database
        self.connection = sqlite3.connect("databases/database.db")
        self.cursor = self.connection.cursor()

        #self.connection = mysql.connector.connect(host="34.65.120.28", user="root", passwd="INSERT YOUR PASSWORD", database="INSERT YOUR DB")
        #self.cursor = self.connection.cursor()

    def option_callback_1(self, text_of_the_option):
        """
        Callback function triggered when a language option is selected.

        Args:
            text_of_the_option (str): The selected language option.

        Notes:
        This function updates the user's language preference on the server, retrieves and sets
        corresponding language dictionaries, and updates UI elements across multiple pages
        with the new language settings.

        """
        payload = {'user_language': text_of_the_option}
        data_request = requests.patch("INSERT YOUR DOMAIN" + self.localId + ".json?auth=" + self.idToken,
                                      data=json.dumps(payload))
        print(data_request.ok)
        if ( data_request.ok == True):
            self.root.ids['firstpage'].ids['language_page'].ids[self.user_language].color = [0, 0, 0, 1]
            self.user_language = text_of_the_option
            self.root.ids['firstpage'].ids['language_page'].ids[self.user_language].color = [0,0.635,0.910,1]
            with open('dictionaries/' + self.user_language + '.txt', encoding='utf-8') as file:
                dictionary = file.read()
            self.dictionary = json.loads(dictionary)

            with open('dictionaries/food_' + self.user_language + '.txt', encoding='utf-8') as file:
                dictionary_food = file.read()
            self.dictionary_food = dictionary_food.split(',')
            # Display First Image
            self.root.ids['firstpage'].ids['food_tastes'].ids['food_image'].source = f"./foodimages/{self.index}.jpg"
            self.root.ids['firstpage'].ids['food_tastes'].ids['food_name'].text = "[b]" + self.dictionary_food[self.index][0].upper() + self.dictionary_food[self.index][1:] + "[/b]"
            self.root.ids['firstpage'].ids['food_tastes'].ids['progress_slider'].value = 1
            # AccountPage: language
            self.root.ids['firstpage'].ids['account_page'].ids['button_language'].text = self.dictionary['button_language']
            self.root.ids['firstpage'].ids['language_page'].ids['button_language'].text = self.dictionary['button_language']
            self.root.ids['firstpage'].ids['account_page'].ids['suggestion'].text = self.dictionary['suggestion']
            self.root.ids['firstpage'].ids['account_page'].ids['button_favorite'].text = self.dictionary['button_favorite']
            self.root.ids['firstpage'].ids['account_page'].ids['tutorial'].text = self.dictionary['tutorial']
            self.root.ids['firstpage'].ids['account_page'].ids['button_logout'].text = self.dictionary['button_logout']
            self.root.ids['firstpage'].ids['suggestion_page'].ids['suggestion'].text = self.dictionary['suggestion']
            self.root.ids['firstpage'].ids['suggestion_page'].ids['active'].text = self.dictionary['active']
            self.root.ids['firstpage'].ids['suggestion_page'].ids['inactive'].text = self.dictionary['inactive']
            self.root.ids['firstpage'].ids['account_page'].ids['filters'].text = self.dictionary['filters']
            self.root.ids['firstpage'].ids['filter_page'].ids['filters'].text = self.dictionary['filters']
            self.root.ids['firstpage'].ids['account_page'].ids['website'].text = self.dictionary['website']
            self.root.ids['firstpage'].ids['logout_page'].ids['exit_sentence'].text = self.dictionary['exit_sentence']
            self.root.ids['firstpage'].ids['logout_page'].ids['no'].text = self.dictionary['no']
            self.root.ids['firstpage'].ids['logout_page'].ids['yes'].text = self.dictionary['yes']
            self.root.ids['firstpage'].ids['search_page'].ids['name_place'].hint_text = self.dictionary['name_place']
            self.root.ids['firstpage'].ids['search_page'].ids['city_place'].hint_text = self.dictionary['city_place']
            # Filters: Button-switch filters
            self.root.ids['firstpage'].ids['filter_page'].ids['restaurant_filter'].text = self.dictionary['restaurant_filter']
            self.root.ids['firstpage'].ids['filter_page'].ids['pizzeria_filter'].text = self.dictionary['pizzeria_filter']
            self.root.ids['firstpage'].ids['filter_page'].ids['sushi_filter'].text = self.dictionary['sushi_filter']
            # FavoritePage: title
            self.root.ids['firstpage'].ids['favorite_page'].ids['favorite_places_title'].text = self.dictionary['favorite_places_title']
            del dictionary

    def option_callback_2(self, text_of_the_option):
        """
        Callback function triggered when a suggestion option is selected.

        Args:
            text_of_the_option (str): The selected suggestion option ('active' or 'inactive').

        Notes:
        This function updates the user's suggestion preference on the server,
        and adjusts UI elements on the Suggestion Page accordingly.

        """
        if (text_of_the_option == 'active'):
            payload = {'suggestion': 'active'}
        elif (text_of_the_option == 'inactive'):
            payload = {'suggestion': 'inactive'}
        data_request = requests.patch("INSERT YOUR DOMAIN" + self.localId + ".json?auth=" + self.idToken,
                                      data=json.dumps(payload))
        print(data_request.ok)
        if (data_request.ok == True):
            self.root.ids['firstpage'].ids['suggestion_page'].ids[self.suggestion].color = [0, 0, 0, 1]
            self.suggestion = payload['suggestion']
            self.root.ids['firstpage'].ids['suggestion_page'].ids[self.suggestion].color = [0,0.635,0.910,1]

    def evaluation_2(self):
        """
        Perform evaluation and update data based on user interaction with food tastes.

        Notes:
        This method updates the user's evaluation data (values and intolerant list) based on the current food taste index
        and slider value. It then sends this updated data to the server using a PATCH request.
        If successful, it updates the food image, food name, and slider value on the UI accordingly.

        """
        self.values[self.index] = str(self.root.ids['firstpage'].ids['food_tastes'].ids['progress_slider'].value)[:3]
        self.intolerant[self.index] = '-'
        self.index += 1
        self.flag = 'no_block'
        payload = {"index": self.index, "intolerant": ','.join(self.intolerant), "values": ','.join(self.values)}
        data_request = requests.patch("INSERT YOUR DOMAIN" + self.localId + ".json?auth=" + self.idToken,
                                      data=json.dumps(payload))
        print(data_request.ok)
        if (data_request.ok == True):
            self.root.ids['firstpage'].ids['food_tastes'].ids['food_image'].source = f"./foodimages/{self.index}.jpg"
            self.root.ids['firstpage'].ids['food_tastes'].ids['food_name'].text = "[b]" + self.dictionary_food[self.index][0].upper() + self.dictionary_food[self.index][1:] + "[/b]"
            self.root.ids['firstpage'].ids['food_tastes'].ids['progress_slider'].value = 1

    def go_back_2(self):
        """
        Move back through food tastes and update data accordingly.

        Notes:
        This method handles moving back through previous food tastes if the current flag is 'no_block' and index is greater than 0.
        It updates the user's evaluation data (values and intolerant list) based on the current index.
        It sends this updated data to the server using a PATCH request and updates the food image, food name, and slider value on the UI if successful.

        """
        if (self.flag == 'no_block' and self.index > 0):
            self.values[self.index] = '0'
            self.intolerant[self.index] = '-'
            self.index -= 1
            self.flag = 'block'
            payload = {"index": self.index, "intolerant": ','.join(self.intolerant), "values": ','.join(self.values)}
            data_request = requests.patch("INSERT YOUR DOMAIN" + self.localId + ".json?auth=" + self.idToken,
                                          data=json.dumps(payload))
            print(data_request.ok)
            if (data_request.ok == True):
                self.root.ids['firstpage'].ids['food_tastes'].ids['food_image'].source = f"./foodimages/{self.index}.jpg"
                self.root.ids['firstpage'].ids['food_tastes'].ids['food_name'].text = "[b]" + self.dictionary_food[self.index][0].upper() + self.dictionary_food[self.index][1:] + "[/b]"
                self.root.ids['firstpage'].ids['food_tastes'].ids['progress_slider'].value = 1
        elif (self.flag == 'block'):
            pass

    def skipping_2(self):
        """
        Skip to the next food taste and update data accordingly.

        Notes:
        This method skips to the next food taste by updating the user's evaluation data (values and intolerant list)
        based on the current index. It then sends this updated data to the server using a PATCH request.
        If successful, it updates the food image, food name, and slider value on the UI accordingly.

        """
        self.values[self.index] = '0'
        self.intolerant[self.index] = '-'
        self.index += 1
        self.flag = 'no_block'
        payload = {"index": self.index, "intolerant": ','.join(self.intolerant), "values": ','.join(self.values)}
        data_request = requests.patch("INSERT YOUR DOMAIN" + self.localId + ".json?auth=" + self.idToken,
                                      data=json.dumps(payload))
        print(data_request.ok)
        self.root.ids['firstpage'].ids['food_tastes'].ids['food_image'].source = f"./foodimages/{self.index}.jpg"
        self.root.ids['firstpage'].ids['food_tastes'].ids['food_name'].text = "[b]" + self.dictionary_food[self.index][0].upper() + self.dictionary_food[self.index][1:] + "[/b]"
        self.root.ids['firstpage'].ids['food_tastes'].ids['progress_slider'].value = 1

    def all_into_2(self):
        """
        Update current food taste to 'into' and move to the next taste.

        Notes:
        This method updates the current food taste's intolerant status to 'into' and resets its value.
        It then moves to the next food taste index, updates these changes on the server using a PATCH request.
        If successful, it updates the food image, food name, and slider value on the UI accordingly.

        """
        self.intolerant[self.index] = 'into'
        self.values[self.index] = '0'
        self.index += 1
        self.flag = 'no_block'
        payload = {"index": self.index, "intolerant": ','.join(self.intolerant), "values": ','.join(self.values)}
        data_request = requests.patch("INSERT YOUR DOMAIN" + self.localId + ".json?auth=" + self.idToken,
                                      data=json.dumps(payload))
        print(data_request.ok)
        if (data_request.ok == True):
            self.root.ids['firstpage'].ids['food_tastes'].ids['food_image'].source = f"./foodimages/{self.index}.jpg"
            self.root.ids['firstpage'].ids['food_tastes'].ids['food_name'].text = "[b]" + self.dictionary_food[self.index][0].upper() + self.dictionary_food[self.index][1:] + "[/b]"
            self.root.ids['firstpage'].ids['food_tastes'].ids['progress_slider'].value = 1

    def change_screen(self, screen_manager, screen_name):
        """
        Change the current screen of a screen manager.

        Args:
        - screen_manager (str): The ID of the screen manager widget in the kv file.
        - screen_name (str): The name of the screen to switch to.

        Notes:
        This method retrieves the screen manager widget from the root of the application,
        then changes the current screen to the specified screen name.

        """
        # Get the screen manager from the kv file
        screen_manager = self.root.ids['firstpage'].ids[screen_manager]
        screen_manager.current = screen_name

    def fav_sfav(self, dictionary_uid, dictionary_place, dictionary_address):
        """
        Add or remove a place from favorites based on its UID.

        Args:
        - dictionary_uid (str): UID of the place to add or remove from favorites.
        - dictionary_place (str): Name of the place to add to favorites.
        - dictionary_address (str): Short address of the place to add to favorites.

        Notes:
        This method manages the addition or removal of a place from the user's favorites list.
        If the place with `dictionary_uid` is already in favorites, it removes it.
        If not, it adds it to favorites with the provided name (`dictionary_place`) and address (`dictionary_address`).

        """
        banner_favorite = self.root.ids['firstpage'].ids['favorite_page'].ids['favorite_place_banner']
        if dictionary_uid in self.favorite_list:
            remove_request = requests.delete("INSERT YOUR DOMAIN" + self.localId + "/favorites/" + dictionary_uid + ".json?auth=" + self.idToken)
            print(remove_request.ok)
            if (remove_request.ok == True):
                banner_favorite.remove_widget(self.favorite_places_dictionary[dictionary_uid])
                del self.favorite_places_dictionary[dictionary_uid]
                del self.favorite_list[dictionary_uid]
                self.menu.favorite_places_title = self.dictionary['favorite_places_title_fav']
                self.menu.favorite_icon = "heart"
        else:
            payload = {dictionary_uid: {"name": dictionary_place, "short_address": dictionary_address}}
            data_request = requests.patch("INSERT YOUR DOMAIN" + self.localId + "/favorites.json?auth=" + self.idToken,
                                          data=json.dumps(payload))
            print(data_request.ok)
            if (data_request.ok == True):
                W = FavoritePlaceBanner(uid=dictionary_uid, place_image="appimages/pizzeria.png", place_name=dictionary_place,
                                        place_address=dictionary_address)
                self.favorite_places_dictionary[dictionary_uid] = W
                banner_favorite.add_widget(W)
                self.favorite_list[dictionary_uid] = {"name": dictionary_place, "address": dictionary_address}
                self.menu.favorite_places_title = self.dictionary['favorite_places_title_sfav']
                self.menu.favorite_icon = "heart-broken"
        del dictionary_uid, dictionary_place, dictionary_address

    def phone_call(self, number):
        """
        Initiate a phone call to the specified number using Plyer's makecall function.

        Args:
        - number (str): The phone number to call.

        Notes:
        This method attempts to make a phone call using the Plyer library's makecall function.
        If successful, it initiates a call to the specified number.
        If an exception occurs during the call initiation, it is caught and ignored silently.

        """
        try:
            plyer.call.makecall(tel=number)
        except Exception as exc:
            pass

    def logout(self):
        """
        Log out the user from the application.

        Notes:
        This method performs the following actions:
        1. Removes the refresh token file associated with the user session.
        2. Clears text fields for email and password on sign-in and create account screens.
        3. Switches the current screen of the root screen manager to the firebase login screen.
        4. Deletes user session-related attributes from the instance to clean up memory.

        """
        os.remove(self.refresh_token_file)
        self.root.ids['firebase_login_screen'].ids['sign_in_screen'].ids['email'].text = ''
        self.root.ids['firebase_login_screen'].ids['sign_in_screen'].ids['password'].text = ''
        self.root.ids['firebase_login_screen'].ids['create_account_screen'].ids['email'].text = ''
        self.root.ids['firebase_login_screen'].ids['create_account_screen'].ids['password'].text = ''
        self.root.current = self.root.ids['firebase_login_screen'].name
        del self.localId, self.idToken, self.refresh_token_file, self.user_language, self.dictionary, self.dictionary_food
        del self.favorite_list

    def show_popup(self):
        """
        Display a popup notification with a message from the dictionary.

        Notes:
        This method shows a popup notification using the `toast` function with a message
        retrieved from the dictionary stored in `self.dictionary['no_result']`.

        """
        toast(self.dictionary['no_result'])

    def search_place(self, name_place, city_place):
        """
        Search for food places based on the provided name and city, and display results on the search page.

        Args:
        - name_place (str): The name of the food place to search for.
        - city_place (str): The city where the food place is located.

        Notes:
        This method performs the following actions:
        1. Clears any existing search results from the search banner.
        2. Executes SQL queries based on the provided `name_place` and `city_place`.
        3. Retrieves search results from the database and displays them as SearchPlaceBanner widgets on the search page.
        4. If no results are found, it displays a popup notification using the `show_popup` method.

        """
        banner_search = self.root.ids['firstpage'].ids['search_page'].ids['search_place_banner']
        if (self.search_list != []):
            for index in self.search_list:
                banner_search.remove_widget(index)
                self.search_list = []
        if ( name_place != '' and city_place != ''):
            sql_statement = "SELECT * FROM food_places WHERE place_name = '%s' AND city_place = '%s' "%(name_place, city_place)
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
            print(len(result))
            if (result != []):
                for i in range(len(result)):
                    W = SearchPlaceBanner(uid=result[i][5], place_image=result[i][4] + '.png', place_name=result[i][1],
                                            place_address=result[i][6])
                    self.search_list.append(W)
                    banner_search.add_widget(W)
            else:
                self.show_popup()
        elif (name_place != ''):
            sql_statement = "SELECT * FROM food_places WHERE place_name = '%s' "%(name_place)
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
            print(len(result))
            if (result != []):
                for i in range(len(result)):
                    W = SearchPlaceBanner(uid=result[i][5], place_image=result[i][4] + '.png', place_name=result[i][1],
                                            place_address=result[i][6])
                    self.search_list.append(W)
                    banner_search.add_widget(W)
            else:
                self.show_popup()
        elif (city_place != ''):
            sql_statement = "SELECT * FROM food_places WHERE city_place = '%s' "%(city_place)
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
            print(len(result))
            if (result != []):
                for i in range(len(result)):
                    W = SearchPlaceBanner(uid=result[i][5], place_image=result[i][4] + '.png', place_name=result[i][1],
                                            place_address=result[i][6])
                    self.search_list.append(W)
                    banner_search.add_widget(W)
            else:
                self.show_popup()



MainApp().run()