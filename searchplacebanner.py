from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.card import MDSeparator
from kivymd.uix.button import MDIconButton
from kivy.app import App
import requests
import json

class SearchPlaceBanner(GridLayout):
    """
    SearchPlaceBanner:
    Banner displaying a place's information with an image, name, address, and navigation button.

    Attributes:
    - rows: Number of rows in the GridLayout (fixed to 1).
    
    Parameters:
    - kwargs:
        - place_image: Image source URL for the place.
        - uid: Unique identifier of the place.
        - place_name: Name of the place.
        - place_address: Address of the place.

    Components:
    - Left side:
        - Displays the profile image of the place.
        - Includes a bottom separator line.

    - Right side:
        - Displays the name and address of the place.
        - Includes a navigation button to view detailed information.
        - Includes a bottom separator line.

    Methods:
    - set_place(place_name, uid):
        - Sets the selected place's name and unique identifier for navigation.

    """
    rows = 1
    def __init__(self, **kwargs):
        super(SearchPlaceBanner, self).__init__()
        app = App.get_running_app()

        # Left profile image
        left = FloatLayout()
        left_image = Image(source=kwargs['place_image'], size_hint=[1, 1], pos_hint={"top": 1, "right": 0.8})
        left_bottom_line = MDSeparator(pos_hint={"top": 0.01, "left": 1}, size_hint=[1,0.01])
        left.add_widget(left_image)
        left.add_widget(left_bottom_line)

        # Right Friend's Name
        right = FloatLayout()
        hidden_label = MDLabel(text=kwargs['uid'])
        right_label_title = MDLabel(text=kwargs['place_name'], color=[0,0,0,1], size_hint=[1, 0.2], pos_hint={"top": 0.7, "right": 0.6}, font_style="Caption", bold=True)
        right_label_address = MDLabel(text=kwargs['place_address'], color=[0,0,0,1], size_hint=[1, 0.2], pos_hint={"top": 0.5, "right": 0.6}, font_style="Caption")
        right_button = MDIconButton(pos_hint={"center_y": 0.5, "right": 1}, icon="arrow-right")
        app.root.ids['firstpage'].ids['screen_manager_1'].transition.direction = 'left'
        right_button.bind(on_press=lambda x: app.change_screen("screen_manager_1", "search_description_page"))
        right_button.bind(on_press=lambda x: self.set_place(right_label_title.text, hidden_label.text))
        right_bottom_line = MDSeparator(pos_hint={"top": 0.01, "right": 1}, size_hint=[1, 0.01])
        right.add_widget(right_label_title)
        right.add_widget(right_button)
        right.add_widget(right_label_address)
        right.add_widget(right_bottom_line)

        # Bottom MD Separator
        self.add_widget(left)
        self.add_widget(right)

    def set_place(self, place_name, uid):
        """
        Sets the details of a place on the description page based on the provided UID.

        Args:
        - place_name: Name of the place.
        - uid: Unique identifier of the place.
        """
        app = App.get_running_app()
        description_page = app.root.ids['firstpage'].ids['search_description_page']

        result = requests.get("INSERT YOUR DOMAIN" + uid + ".json")
        data = json.loads(result.content.decode())

        description_page.uid = uid
        description_page.name_place = place_name
        description_page.lat = data['coordinates']['lat']
        description_page.lon = data['coordinates']['lon']
        description_page.address_title = app.dictionary['address_title']
        description_page.address = data['address']
        description_page.short_address = data['short_address']
        description_page.description_title = app.dictionary['description_title']
        description_page.description = data['description_' + app.user_language]
        description_page.time_table = app.dictionary['time_table']
        description_page.telephone_title = app.dictionary['telephone_title']
        description_page.telephone = data['telephone']
        description_page.parking_title = app.dictionary['parking_title']
        if (data['parking'] == 'no'):
            description_page.parking = app.dictionary['no_parking']
        else:
            description_page.parking = data['parking'] + ' ' + app.dictionary['car_places']

        description_page.monday_title = app.dictionary['monday_title']
        if (data['hours']['monday'] == 'chiuso'):
            description_page.monday = app.dictionary['day_closed']
        else:
            description_page.monday = data['hours']['monday']

        description_page.tuesday_title = app.dictionary['tuesday_title']
        if (data['hours']['tuesday'] == 'chiuso'):
            description_page.tuesday = app.dictionary['day_closed']
        else:
            description_page.tuesday = data['hours']['tuesday']

        description_page.wednesday_title = app.dictionary['wednesday_title']
        if (data['hours']['wednesday'] == 'chiuso'):
            description_page.wednesday = app.dictionary['day_closed']
        else:
            description_page.wednesday = data['hours']['wednesday']

        description_page.thursday_title = app.dictionary['thursday_title']
        if (data['hours']['thursday'] == 'chiuso'):
            description_page.thursday = app.dictionary['day_closed']
        else:
            description_page.thursday = data['hours']['thursday']

        description_page.friday_title = app.dictionary['friday_title']
        if (data['hours']['friday'] == 'chiuso'):
            description_page.friday = app.dictionary['day_closed']
        else:
            description_page.friday = data['hours']['friday']

        description_page.saturday_title = app.dictionary['saturday_title']
        if (data['hours']['saturday'] == 'chiuso'):
            description_page.saturday = app.dictionary['day_closed']
        else:
            description_page.saturday = data['hours']['saturday']

        description_page.sunday_title = app.dictionary['sunday_title']
        if (data['hours']['sunday'] == 'chiuso'):
            description_page.sunday = app.dictionary['day_closed']
        else:
            description_page.sunday = data['hours']['sunday']

        description_page.website = data['website']
        percentuale = 70
        translation = data['translation']

        if description_page.uid in app.favorite_list:
            description_page.favorite_places_title = app.dictionary['favorite_places_title_sfav']
            description_page.favorite_icon = "heart-broken"
        else:
            description_page.favorite_places_title = app.dictionary['favorite_places_title_fav']
            description_page.favorite_icon = "heart"

        with open('dictionaries/food_Italiano.txt', encoding='utf-8') as file:
            italian_dictionary = file.read()
        italian_dictionary = italian_dictionary.split(',')

        # Menu
        # First plates
        description_page.first_plates_name = data['menu']['first_plates_name']
        # 1
        description_page.first_plate_1 = data['menu']['first_plates']['first_plate_1']['name']
        description_page.color_first_plate_1 = [0, 0, 0, 1]
        description_page.first_plate_1_price = data['menu']['first_plates']['first_plate_1']['price']
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
                description_page.first_plate_1 += app.dictionary['suggested']
                description_page.color_first_plate_1 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_1 += app.dictionary['intolerant']
                description_page.color_first_plate_1 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_1_ingredients = ingredients

        # 2
        description_page.first_plate_2 = data['menu']['first_plates']['first_plate_2']['name']
        description_page.color_first_plate_2 = [0, 0, 0, 1]
        description_page.first_plate_2_price = data['menu']['first_plates']['first_plate_2']['price']
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
                description_page.first_plate_2 += app.dictionary['suggested']
                description_page.color_first_plate_2 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_2 += app.dictionary['intolerant']
                description_page.color_first_plate_2 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_2_ingredients = ingredients

        # 3
        description_page.first_plate_3 = data['menu']['first_plates']['first_plate_3']['name']
        description_page.color_first_plate_3 = [0, 0, 0, 1]
        description_page.first_plate_3_price = data['menu']['first_plates']['first_plate_3']['price']
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
                description_page.first_plate_3 += app.dictionary['suggested']
                description_page.color_first_plate_3 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_3 += app.dictionary['intolerant']
                description_page.color_first_plate_3 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_3_ingredients = ingredients

        # 4
        description_page.first_plate_4 = data['menu']['first_plates']['first_plate_4']['name']
        description_page.color_first_plate_4 = [0, 0, 0, 1]
        description_page.first_plate_4_price = data['menu']['first_plates']['first_plate_4']['price']
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
                description_page.first_plate_4 += app.dictionary['suggested']
                description_page.color_first_plate_4 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_4 += app.dictionary['intolerant']
                description_page.color_first_plate_4 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_4_ingredients = ingredients

        # 5
        description_page.first_plate_5 = data['menu']['first_plates']['first_plate_5']['name']
        description_page.color_first_plate_5 = [0, 0, 0, 1]
        description_page.first_plate_5_price = data['menu']['first_plates']['first_plate_5']['price']
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
                description_page.first_plate_5 += app.dictionary['suggested']
                description_page.color_first_plate_5 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_5 += app.dictionary['intolerant']
                description_page.color_first_plate_5 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_5_ingredients = ingredients

        # 6
        description_page.first_plate_6 = data['menu']['first_plates']['first_plate_6']['name']
        description_page.color_first_plate_6 = [0, 0, 0, 1]
        description_page.first_plate_6_price = data['menu']['first_plates']['first_plate_6']['price']
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
                description_page.first_plate_6 += app.dictionary['suggested']
                description_page.color_first_plate_6 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_6 += app.dictionary['intolerant']
                description_page.color_first_plate_6 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_6_ingredients = ingredients

        # 7
        description_page.first_plate_7 = data['menu']['first_plates']['first_plate_7']['name']
        description_page.color_first_plate_7 = [0, 0, 0, 1]
        description_page.first_plate_7_price = data['menu']['first_plates']['first_plate_7']['price']
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
                description_page.first_plate_7 += app.dictionary['suggested']
                description_page.color_first_plate_7 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_7 += app.dictionary['intolerant']
                description_page.color_first_plate_7 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_7_ingredients = ingredients

        # 8
        description_page.first_plate_8 = data['menu']['first_plates']['first_plate_8']['name']
        description_page.color_first_plate_8 = [0, 0, 0, 1]
        description_page.first_plate_8_price = data['menu']['first_plates']['first_plate_8']['price']
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
                description_page.first_plate_8 += app.dictionary['suggested']
                description_page.color_first_plate_8 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_8 += app.dictionary['intolerant']
                description_page.color_first_plate_8 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_8_ingredients = ingredients

        # 9
        description_page.first_plate_9 = data['menu']['first_plates']['first_plate_9']['name']
        description_page.color_first_plate_9 = [0, 0, 0, 1]
        description_page.first_plate_9_price = data['menu']['first_plates']['first_plate_9']['price']
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
                description_page.first_plate_9 += app.dictionary['suggested']
                description_page.color_first_plate_9 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_9 += app.dictionary['intolerant']
                description_page.color_first_plate_9 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_9_ingredients = ingredients

        # 10
        description_page.first_plate_10 = data['menu']['first_plates']['first_plate_10']['name']
        description_page.color_first_plate_10 = [0, 0, 0, 1]
        description_page.first_plate_10_price = data['menu']['first_plates']['first_plate_10']['price']
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
                description_page.first_plate_10 += app.dictionary['suggested']
                description_page.color_first_plate_10 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.first_plate_10 += app.dictionary['intolerant']
                description_page.color_first_plate_10 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.first_plate_10_ingredients = ingredients

        # Second plates
        description_page.second_plates_name = data['menu']['second_plates_name']
        # 1
        description_page.second_plate_1 = data['menu']['second_plates']['second_plate_1']['name']
        description_page.color_second_plate_1 = [0, 0, 0, 1]
        description_page.second_plate_1_price = data['menu']['second_plates']['second_plate_1']['price']
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
                description_page.second_plate_1 += app.dictionary['suggested']
                description_page.color_second_plate_1 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_1 += app.dictionary['intolerant']
                description_page.color_second_plate_1 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.second_plate_1_ingredients = ingredients

        # 2
        description_page.second_plate_2 = data['menu']['second_plates']['second_plate_2']['name']
        description_page.color_second_plate_2 = [0, 0, 0, 1]
        description_page.second_plate_2_price = data['menu']['second_plates']['second_plate_2']['price']
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
                description_page.second_plate_2 += app.dictionary['suggested']
                description_page.color_second_plate_2 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_2 += app.dictionary['intolerant']
                description_page.color_second_plate_2 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.second_plate_2_ingredients = ingredients

        # 3
        description_page.second_plate_3 = data['menu']['second_plates']['second_plate_3']['name']
        description_page.color_second_plate_3 = [0, 0, 0, 1]
        description_page.second_plate_3_price = data['menu']['second_plates']['second_plate_3']['price']
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
                description_page.second_plate_3 += app.dictionary['suggested']
                description_page.color_second_plate_3 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_3 += app.dictionary['intolerant']
                description_page.color_second_plate_3 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        description_page.second_plate_3_ingredients = ingredients

        # 4
        description_page.second_plate_4 = data['menu']['second_plates']['second_plate_4']['name']
        description_page.color_second_plate_4 = [0, 0, 0, 1]
        description_page.second_plate_4_price = data['menu']['second_plates']['second_plate_4']['price']
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
                description_page.second_plate_4 += app.dictionary['suggested']
                description_page.color_second_plate_4 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_4 += app.dictionary['intolerant']
                description_page.color_second_plate_4 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        description_page.second_plate_4_ingredients = ingredients

        # 5
        description_page.second_plate_5 = data['menu']['second_plates']['second_plate_4']['name']
        description_page.color_second_plate_5 = [0, 0, 0, 1]
        description_page.second_plate_5_price = data['menu']['second_plates']['second_plate_5']['price']
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
                description_page.second_plate_5 += app.dictionary['suggested']
                description_page.color_second_plate_5 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_5 += app.dictionary['intolerant']
                description_page.color_second_plate_5 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        description_page.second_plate_5_ingredients = ingredients

        # 6
        description_page.second_plate_6 = data['menu']['second_plates']['second_plate_6']['name']
        description_page.color_second_plate_6 = [0, 0, 0, 1]
        description_page.second_plate_6_price = data['menu']['second_plates']['second_plate_6']['price']
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
                description_page.second_plate_6 += app.dictionary['suggested']
                description_page.color_second_plate_6 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_6 += app.dictionary['intolerant']
                description_page.color_second_plate_6 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.second_plate_6_ingredients = ingredients

        # 7
        description_page.second_plate_7 = data['menu']['second_plates']['second_plate_7']['name']
        description_page.color_second_plate_7 = [0, 0, 0, 1]
        description_page.second_plate_7_price = data['menu']['second_plates']['second_plate_7']['price']
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
                description_page.second_plate_7 += app.dictionary['suggested']
                description_page.color_second_plate_7 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_7 += app.dictionary['intolerant']
                description_page.color_second_plate_7 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.second_plate_7_ingredients = ingredients

        # 8
        description_page.second_plate_8 = data['menu']['second_plates']['second_plate_8']['name']
        description_page.color_second_plate_8 = [0, 0, 0, 1]
        description_page.second_plate_8_price = data['menu']['second_plates']['second_plate_8']['price']
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
                description_page.second_plate_8 += app.dictionary['suggested']
                description_page.color_second_plate_8 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_8 += app.dictionary['intolerant']
                description_page.color_second_plate_8 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.second_plate_8_ingredients = ingredients

        # 9
        description_page.second_plate_9 = data['menu']['second_plates']['second_plate_9']['name']
        description_page.color_second_plate_9 = [0, 0, 0, 1]
        description_page.second_plate_9_price = data['menu']['second_plates']['second_plate_9']['price']
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
                description_page.second_plate_9 += app.dictionary['suggested']
                description_page.color_second_plate_9 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_9 += app.dictionary['intolerant']
                description_page.color_second_plate_9 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.second_plate_9_ingredients = ingredients

        # 10
        description_page.second_plate_10 = data['menu']['second_plates']['second_plate_10']['name']
        description_page.color_second_plate_10 = [0, 0, 0, 1]
        description_page.second_plate_10_price = data['menu']['second_plates']['second_plate_10']['price']
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
                description_page.second_plate_10 += app.dictionary['suggested']
                description_page.color_second_plate_10 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.second_plate_10 += app.dictionary['intolerant']
                description_page.color_second_plate_10 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.second_plate_10_ingredients = ingredients

        # Third plates
        description_page.third_plates_name = data['menu']['third_plates_name']
        # 1
        description_page.third_plate_1 = data['menu']['third_plates']['third_plate_1']['name']
        description_page.color_third_plate_1 = [0, 0, 0, 1]
        description_page.third_plate_1_price = data['menu']['third_plates']['third_plate_1']['price']
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
                description_page.third_plate_1 += app.dictionary['suggested']
                description_page.color_third_plate_1 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_1 += app.dictionary['intolerant']
                description_page.color_third_plate_1 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.third_plate_1_ingredients = ingredients

        # 2
        description_page.third_plate_2 = data['menu']['third_plates']['third_plate_2']['name']
        description_page.color_third_plate_2 = [0, 0, 0, 1]
        description_page.third_plate_2_price = data['menu']['third_plates']['third_plate_2']['price']
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
                description_page.third_plate_2 += app.dictionary['suggested']
                description_page.color_third_plate_2 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_2 += app.dictionary['intolerant']
                description_page.color_third_plate_2 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.third_plate_2_ingredients = ingredients

        # 3
        description_page.third_plate_3 = data['menu']['third_plates']['third_plate_3']['name']
        description_page.color_third_plate_3 = [0, 0, 0, 1]
        description_page.third_plate_3_price = data['menu']['third_plates']['third_plate_3']['price']
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
                description_page.third_plate_3 += app.dictionary['suggested']
                description_page.color_third_plate_3 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_3 += app.dictionary['intolerant']
                description_page.color_third_plate_3 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        description_page.third_plate_3_ingredients = ingredients

        # 4
        description_page.third_plate_4 = data['menu']['third_plates']['third_plate_4']['name']
        description_page.color_third_plate_4 = [0, 0, 0, 1]
        description_page.third_plate_4_price = data['menu']['third_plates']['third_plate_4']['price']
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
                description_page.third_plate_4 += app.dictionary['suggested']
                description_page.color_third_plate_4 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_4 += app.dictionary['intolerant']
                description_page.color_third_plate_4 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        description_page.third_plate_4_ingredients = ingredients

        # 5
        description_page.third_plate_5 = data['menu']['third_plates']['third_plate_5']['name']
        description_page.color_third_plate_5 = [0, 0, 0, 1]
        description_page.third_plate_5_price = data['menu']['third_plates']['third_plate_5']['price']
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
                description_page.third_plate_5 += app.dictionary['suggested']
                description_page.color_third_plate_5 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_5 += app.dictionary['intolerant']
                description_page.color_third_plate_5 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item

        description_page.third_plate_5_ingredients = ingredients

        # 6
        description_page.third_plate_6 = data['menu']['third_plates']['third_plate_6']['name']
        description_page.color_third_plate_6 = [0, 0, 0, 1]
        description_page.third_plate_6_price = data['menu']['third_plates']['third_plate_6']['price']
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
                description_page.third_plate_6 += app.dictionary['suggested']
                description_page.color_third_plate_6 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_6 += app.dictionary['intolerant']
                description_page.color_third_plate_6 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.third_plate_6_ingredients = ingredients

        # 7
        description_page.third_plate_7 = data['menu']['third_plates']['third_plate_7']['name']
        description_page.color_third_plate_7 = [0, 0, 0, 1]
        description_page.third_plate_7_price = data['menu']['third_plates']['third_plate_7']['price']
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
                description_page.third_plate_7 += app.dictionary['suggested']
                description_page.color_third_plate_7 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_7 += app.dictionary['intolerant']
                description_page.color_third_plate_7 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.third_plate_7_ingredients = ingredients

        # 8
        description_page.third_plate_8 = data['menu']['third_plates']['third_plate_8']['name']
        description_page.color_third_plate_8 = [0, 0, 0, 1]
        description_page.third_plate_8_price = data['menu']['third_plates']['third_plate_8']['price']
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
                description_page.third_plate_8 += app.dictionary['suggested']
                description_page.color_third_plate_8 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_8 += app.dictionary['intolerant']
                description_page.color_third_plate_8 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.third_plate_8_ingredients = ingredients

        # 9
        description_page.third_plate_9 = data['menu']['third_plates']['third_plate_9']['name']
        description_page.color_third_plate_9 = [0, 0, 0, 1]
        description_page.third_plate_9_price = data['menu']['third_plates']['third_plate_9']['price']
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
                description_page.third_plate_9 += app.dictionary['suggested']
                description_page.color_third_plate_9 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_9 += app.dictionary['intolerant']
                description_page.color_third_plate_9 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.third_plate_9_ingredients = ingredients

        # 10
        description_page.third_plate_10 = data['menu']['third_plates']['third_plate_10']['name']
        description_page.color_third_plate_10 = [0, 0, 0, 1]
        description_page.third_plate_10_price = data['menu']['third_plates']['third_plate_10']['price']
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
                description_page.third_plate_10 += app.dictionary['suggested']
                description_page.color_third_plate_10 = [.11, .72, .24, 1]
            elif (all_into == True and app.suggestion == 'active'):
                description_page.third_plate_10 += app.dictionary['intolerant']
                description_page.color_third_plate_10 = [1, 0, 0, 1]
        elif (translation == 'no'):
            for index, item in enumerate(ingredients_split):
                if index == 0:
                    ingredients += item[0].upper() + item[1:]
                elif index == (len(ingredients_split) - 1):
                    ingredients += ', ' + item + '.'
                else:
                    ingredients += ', ' + item
        description_page.third_plate_10_ingredients = ingredients

        app.menu = description_page