from kivy.app import App
from kivy_garden.mapview import MapMarkerPopup
from locationpopupmenu import LocationPopupMenu
import requests
import json
import time

class PlaceMarker(MapMarkerPopup):
    """
    Represents a marker on the map that, when clicked, displays detailed
    information about a place including its menu and operational details.

    Inherits from MapMarkerPopup and extends functionality to interact with
    an API to retrieve and display detailed information about a place when
    the marker is clicked.

    Attributes:
        place_data (list): Holds data related to the place, retrieved from the API.

    """
    place_data = []

    def on_release(self):
        """
        Overrides the method from MapMarkerPopup to handle the release event when 
        the marker is clicked. Retrieves place information using an API call and 
        displays it using the LocationPopupMenu.
        """
        app = App.get_running_app()

        # Open up the LocationPopUpMenu
        result = requests.get("INSERT YOUR DOMAIN" + self.place_data[5] + ".json")
        print(result.ok)
        data = json.loads(result.content.decode())

        menu = LocationPopupMenu()
        menu.uid = self.place_data[5]
        menu.name = self.place_data[1]
        menu.address_title = app.dictionary['address_title']
        menu.address = data['address']
        menu.short_address = data['short_address']
        menu.description_title = app.dictionary['description_title']
        menu.description = data['description_' + app.user_language]
        menu.time_table = app.dictionary['time_table']
        menu.telephone_title = app.dictionary['telephone_title']
        menu.telephone = data['telephone']
        menu.parking_title = app.dictionary['parking_title']
        if (data['parking'] == 'no'):
            menu.parking = app.dictionary['no_parking']
        else:
            menu.parking = data['parking'] + ' ' + app.dictionary['car_places']

        menu.monday_title = app.dictionary['monday_title']
        if (data['hours']['monday'] == 'chiuso'):
            menu.monday = app.dictionary['day_closed']
        else:
            menu.monday = data['hours']['monday']

        menu.tuesday_title = app.dictionary['tuesday_title']
        if (data['hours']['tuesday'] == 'chiuso'):
            menu.tuesday = app.dictionary['day_closed']
        else:
            menu.tuesday = data['hours']['tuesday']

        menu.wednesday_title = app.dictionary['wednesday_title']
        if (data['hours']['wednesday'] == 'chiuso'):
            menu.wednesday = app.dictionary['day_closed']
        else:
            menu.wednesday = data['hours']['wednesday']

        menu.thursday_title = app.dictionary['thursday_title']
        if (data['hours']['thursday'] == 'chiuso'):
            menu.thursday = app.dictionary['day_closed']
        else:
            menu.thursday = data['hours']['thursday']

        menu.friday_title = app.dictionary['friday_title']
        if (data['hours']['friday'] == 'chiuso'):
            menu.friday = app.dictionary['day_closed']
        else:
            menu.friday = data['hours']['friday']

        menu.saturday_title = app.dictionary['saturday_title']
        if (data['hours']['saturday'] == 'chiuso'):
            menu.saturday = app.dictionary['day_closed']
        else:
            menu.saturday = data['hours']['saturday']

        menu.sunday_title = app.dictionary['sunday_title']
        if (data['hours']['sunday'] == 'chiuso'):
            menu.sunday = app.dictionary['day_closed']
        else:
            menu.sunday = data['hours']['sunday']

        menu.website = data['website']
        percentuale = 70
        translation = data['translation']

        if menu.uid in app.favorite_list:
            menu.favorite_places_title = app.dictionary['favorite_places_title_sfav']
            menu.favorite_icon = "heart-broken"
        else:
            menu.favorite_places_title = app.dictionary['favorite_places_title_fav']
            menu.favorite_icon = "heart"

        with open('dictionaries/food_Italiano.txt', encoding='utf-8') as file:
            italian_dictionary = file.read()
        italian_dictionary = italian_dictionary.split(',')

        # Menu
        # First plates
        menu.first_plates_name = data['menu']['first_plates_name']
        # 1
        menu.first_plate_1 = data['menu']['first_plates']['first_plate_1']['name']
        menu.first_plate_1_price = data['menu']['first_plates']['first_plate_1']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_1']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if ( value/len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_1 += app.dictionary['suggested']
                menu.color_first_plate_1 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_1 += app.dictionary['intolerant']
                menu.color_first_plate_1 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.first_plate_1_ingredients = ingredients

        # 2
        menu.first_plate_2 = data['menu']['first_plates']['first_plate_2']['name']
        menu.first_plate_2_price = data['menu']['first_plates']['first_plate_2']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_2']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_2 += app.dictionary['suggested']
                menu.color_first_plate_2 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_2 += app.dictionary['intolerant']
                menu.color_first_plate_2 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.first_plate_2_ingredients = ingredients

        # 3
        menu.first_plate_3 = data['menu']['first_plates']['first_plate_3']['name']
        menu.first_plate_3_price = data['menu']['first_plates']['first_plate_3']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_3']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_3 += app.dictionary['suggested']
                menu.color_first_plate_3 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_3 += app.dictionary['intolerant']
                menu.color_first_plate_3 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.first_plate_3_ingredients = ingredients

        # 4
        menu.first_plate_4 = data['menu']['first_plates']['first_plate_4']['name']
        menu.first_plate_4_price = data['menu']['first_plates']['first_plate_4']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_4']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_4 += app.dictionary['suggested']
                menu.color_first_plate_4 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_4 += app.dictionary['intolerant']
                menu.color_first_plate_4 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.first_plate_4_ingredients = ingredients

        # 5
        menu.first_plate_5 = data['menu']['first_plates']['first_plate_4']['name']
        menu.first_plate_5_price = data['menu']['first_plates']['first_plate_5']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_5']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_5 += app.dictionary['suggested']
                menu.color_first_plate_5 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_5 += app.dictionary['intolerant']
                menu.color_first_plate_5 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.first_plate_5_ingredients = ingredients

        # 6
        menu.first_plate_6 = data['menu']['first_plates']['first_plate_6']['name']
        menu.first_plate_6_price = data['menu']['first_plates']['first_plate_6']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_6']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_6 += app.dictionary['suggested']
                menu.color_first_plate_6 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_6 += app.dictionary['intolerant']
                menu.color_first_plate_6 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.first_plate_6_ingredients = ingredients

        # 7
        menu.first_plate_7 = data['menu']['first_plates']['first_plate_7']['name']
        menu.first_plate_7_price = data['menu']['first_plates']['first_plate_7']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_7']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_7 += app.dictionary['suggested']
                menu.color_first_plate_7 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_7 += app.dictionary['intolerant']
                menu.color_first_plate_7 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.first_plate_7_ingredients = ingredients

        # 8
        menu.first_plate_8 = data['menu']['first_plates']['first_plate_8']['name']
        menu.first_plate_8_price = data['menu']['first_plates']['first_plate_8']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_8']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_8 += app.dictionary['suggested']
                menu.color_first_plate_8 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_8 += app.dictionary['intolerant']
                menu.color_first_plate_8 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.first_plate_8_ingredients = ingredients

        # 9
        menu.first_plate_9 = data['menu']['first_plates']['first_plate_9']['name']
        menu.first_plate_9_price = data['menu']['first_plates']['first_plate_9']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_9']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_9 += app.dictionary['suggested']
                menu.color_first_plate_9 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_9 += app.dictionary['intolerant']
                menu.color_first_plate_9 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.first_plate_9_ingredients = ingredients

        # 10
        menu.first_plate_10 = data['menu']['first_plates']['first_plate_10']['name']
        menu.first_plate_10_price = data['menu']['first_plates']['first_plate_10']['price']
        ingredients_split = data['menu']['first_plates']['first_plate_10']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.first_plate_10 += app.dictionary['suggested']
                menu.color_first_plate_10 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.first_plate_10 += app.dictionary['intolerant']
                menu.color_first_plate_10 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.first_plate_10_ingredients = ingredients

        # Second plates
        menu.second_plates_name = data['menu']['second_plates_name']
        # 1
        menu.second_plate_1 = data['menu']['second_plates']['second_plate_1']['name']
        menu.second_plate_1_price = data['menu']['second_plates']['second_plate_1']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_1']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value/len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_1 += app.dictionary['suggested']
                menu.color_second_plate_1 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_1 += app.dictionary['intolerant']
                menu.color_second_plate_1 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.second_plate_1_ingredients = ingredients

        # 2
        menu.second_plate_2 = data['menu']['second_plates']['second_plate_2']['name']
        menu.second_plate_2_price = data['menu']['second_plates']['second_plate_2']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_2']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value/len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_2 += app.dictionary['suggested']
                menu.color_second_plate_2 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_2 += app.dictionary['intolerant']
                menu.color_second_plate_2 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.second_plate_2_ingredients = ingredients

        # 3
        menu.second_plate_3 = data['menu']['second_plates']['second_plate_3']['name']
        menu.second_plate_3_price = data['menu']['second_plates']['second_plate_3']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_3']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_3 += app.dictionary['suggested']
                menu.color_second_plate_3 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_3 += app.dictionary['intolerant']
                menu.color_second_plate_3 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.second_plate_3_ingredients = ingredients

        # 4
        menu.second_plate_4 = data['menu']['second_plates']['second_plate_4']['name']
        menu.second_plate_4_price = data['menu']['second_plates']['second_plate_4']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_4']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_4 += app.dictionary['suggested']
                menu.color_second_plate_4 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_4 += app.dictionary['intolerant']
                menu.color_second_plate_4 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.second_plate_4_ingredients = ingredients

        # 5
        menu.second_plate_5 = data['menu']['second_plates']['second_plate_4']['name']
        menu.second_plate_5_price = data['menu']['second_plates']['second_plate_5']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_5']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_5 += app.dictionary['suggested']
                menu.color_second_plate_5 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_5 += app.dictionary['intolerant']
                menu.color_second_plate_5 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.second_plate_5_ingredients = ingredients

        # 6
        menu.second_plate_6 = data['menu']['second_plates']['second_plate_6']['name']
        menu.second_plate_6_price = data['menu']['second_plates']['second_plate_6']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_6']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_6 += app.dictionary['suggested']
                menu.color_second_plate_6 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_6 += app.dictionary['intolerant']
                menu.color_second_plate_6 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.second_plate_6_ingredients = ingredients

        # 7
        menu.second_plate_7 = data['menu']['second_plates']['second_plate_7']['name']
        menu.second_plate_7_price = data['menu']['second_plates']['second_plate_7']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_7']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_7 += app.dictionary['suggested']
                menu.color_second_plate_7 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_7 += app.dictionary['intolerant']
                menu.color_second_plate_7 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.second_plate_7_ingredients = ingredients

        # 8
        menu.second_plate_8 = data['menu']['second_plates']['second_plate_8']['name']
        menu.second_plate_8_price = data['menu']['second_plates']['second_plate_8']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_8']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_8 += app.dictionary['suggested']
                menu.color_second_plate_8 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_8 += app.dictionary['intolerant']
                menu.color_second_plate_8 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.second_plate_8_ingredients = ingredients

        # 9
        menu.second_plate_9 = data['menu']['second_plates']['second_plate_9']['name']
        menu.second_plate_9_price = data['menu']['second_plates']['second_plate_9']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_9']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_9 += app.dictionary['suggested']
                menu.color_second_plate_9 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_9 += app.dictionary['intolerant']
                menu.color_second_plate_9 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.second_plate_9_ingredients = ingredients

        # 10
        menu.second_plate_10 = data['menu']['second_plates']['second_plate_10']['name']
        menu.second_plate_10_price = data['menu']['second_plates']['second_plate_10']['price']
        ingredients_split = data['menu']['second_plates']['second_plate_10']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.second_plate_10 += app.dictionary['suggested']
                menu.color_second_plate_10 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.second_plate_10 += app.dictionary['intolerant']
                menu.color_second_plate_10 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.second_plate_10_ingredients = ingredients


        # Third plates
        menu.third_plates_name = data['menu']['third_plates_name']
        # 1
        menu.third_plate_1 = data['menu']['third_plates']['third_plate_1']['name']
        menu.third_plate_1_price = data['menu']['third_plates']['third_plate_1']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_1']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value/len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_1 += app.dictionary['suggested']
                menu.color_third_plate_1 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_1 += app.dictionary['intolerant']
                menu.color_third_plate_1 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.third_plate_1_ingredients = ingredients

        # 2
        menu.third_plate_2 = data['menu']['third_plates']['third_plate_2']['name']
        menu.third_plate_2_price = data['menu']['third_plates']['third_plate_2']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_2']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == ( len(ingredients_split) - 1 ):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value/len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_2 += app.dictionary['suggested']
                menu.color_third_plate_2 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_2 += app.dictionary['intolerant']
                menu.color_third_plate_2 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.third_plate_2_ingredients = ingredients

        # 3
        menu.third_plate_3 = data['menu']['third_plates']['third_plate_3']['name']
        menu.third_plate_3_price = data['menu']['third_plates']['third_plate_3']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_3']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_3 += app.dictionary['suggested']
                menu.color_third_plate_3 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_3 += app.dictionary['intolerant']
                menu.color_third_plate_3 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.third_plate_3_ingredients = ingredients

        # 4
        menu.third_plate_4 = data['menu']['third_plates']['third_plate_4']['name']
        menu.third_plate_4_price = data['menu']['third_plates']['third_plate_4']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_4']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_4 += app.dictionary['suggested']
                menu.color_third_plate_4 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_4 += app.dictionary['intolerant']
                menu.color_third_plate_4 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.third_plate_4_ingredients = ingredients

        # 5
        menu.third_plate_5 = data['menu']['third_plates']['third_plate_5']['name']
        menu.third_plate_5_price = data['menu']['third_plates']['third_plate_5']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_5']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_5 += app.dictionary['suggested']
                menu.color_third_plate_5 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_5 += app.dictionary['intolerant']
                menu.color_third_plate_5 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        menu.third_plate_5_ingredients = ingredients

        # 6
        menu.third_plate_6 = data['menu']['third_plates']['third_plate_6']['name']
        menu.third_plate_6_price = data['menu']['third_plates']['third_plate_6']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_6']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_6 += app.dictionary['suggested']
                menu.color_third_plate_6 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_6 += app.dictionary['intolerant']
                menu.color_third_plate_6 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.third_plate_6_ingredients = ingredients

        # 7
        menu.third_plate_7 = data['menu']['third_plates']['third_plate_7']['name']
        menu.third_plate_7_price = data['menu']['third_plates']['third_plate_7']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_7']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_7 += app.dictionary['suggested']
                menu.color_third_plate_7 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_7 += app.dictionary['intolerant']
                menu.color_third_plate_7 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.third_plate_7_ingredients = ingredients

        # 8
        menu.third_plate_8 = data['menu']['third_plates']['third_plate_8']['name']
        menu.third_plate_8_price = data['menu']['third_plates']['third_plate_8']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_8']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_8 += app.dictionary['suggested']
                menu.color_third_plate_8 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_8 += app.dictionary['intolerant']
                menu.color_third_plate_8 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.third_plate_8_ingredients = ingredients

        # 9
        menu.third_plate_9 = data['menu']['third_plates']['third_plate_9']['name']
        menu.third_plate_9_price = data['menu']['third_plates']['third_plate_9']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_9']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_9 += app.dictionary['suggested']
                menu.color_third_plate_9 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_9 += app.dictionary['intolerant']
                menu.color_third_plate_9 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.third_plate_9_ingredients = ingredients

        # 10
        menu.third_plate_10 = data['menu']['third_plates']['third_plate_10']['name']
        menu.third_plate_10_price = data['menu']['third_plates']['third_plate_10']['price']
        ingredients_split = data['menu']['third_plates']['third_plate_10']['ingredients']
        ingredients_split = ingredients_split.split(',')
        ingredients = ''
        value = 0
        all_into = False
        if (translation == 'yes'):
            for index, item in enumerate(ingredients_split):
                if item in italian_dictionary:
                    index_dictionary = italian_dictionary.index(item)
                    item_user_language = app.dictionary_food[index_dictionary]
                    if (app.intolerant[index_dictionary] == 'into'):
                        all_into = True
                    value += float(app.values[index_dictionary])
                    if index == 0:
                        ingredients += item_user_language[0].upper() + item_user_language[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item_user_language + '.'
                    else:
                        ingredients += ', ' + item_user_language
                else:
                    if index == 0:
                        ingredients += item[0].upper() + item[1:]
                    elif index == (len(ingredients_split) - 1):
                        ingredients += ', ' + item + '.'
                    else:
                        ingredients += ', ' + item
            if (value / len(ingredients_split) >= percentuale and all_into == False and app.suggestion == 'active'):
                menu.third_plate_10 += app.dictionary['suggested']
                menu.color_third_plate_10 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                menu.third_plate_10 += app.dictionary['intolerant']
                menu.color_third_plate_10 = [1, 0, 0, 1]
        elif ( translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        menu.third_plate_10_ingredients = ingredients

        menu.open()
        app.menu = menu
