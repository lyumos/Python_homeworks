import os
import sys
from pprint import pprint

menu_file = os.path.join(os.path.dirname(sys.argv[0]), 'recipes.txt')

def menu_into_dict(menu_file):
    with open(menu_file,encoding="utf-8") as menu:
        cook_book = {}
        for line in menu:
            dish_title = line.strip()
            ingredients_list = []
            for item in range(int(menu.readline())):
                ingredient_info = menu.readline()
                ingredients_info_dict = {'ingredient_name': ingredient_info.split(' | ')[0],
                                             'quantity': int(ingredient_info.split(' | ')[1]), 'measure': ingredient_info.split(' | ')[2].strip()}
                ingredients_list.append(ingredients_info_dict)
            cook_book[dish_title] = ingredients_list
            menu.readline()
    return cook_book

def get_shop_list_by_dishes(dishes, person_count):
    shoplist = {}
    for dish in dishes:
        for item in menu_into_dict(menu_file).keys():
            if item == dish:
                for ingredient in menu_into_dict(menu_file)[item]:
                    if ingredient['ingredient_name'] not in shoplist.keys():
                        info_dict = {'measure': ingredient['measure'], 'quantity': ingredient['quantity'] * person_count}
                        shoplist[ingredient['ingredient_name']] = info_dict
                    else:
                        shoplist[ingredient['ingredient_name']]['quantity'] += ingredient['quantity'] * person_count
    pprint(shoplist)

print(f'cook_book = {menu_into_dict(menu_file)}')
get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'],2)





