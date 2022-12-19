from sqlalchemy import select
from models import *


async def get_statistics_mob(conn, mob_id):
    ex = conn.execute(select(mobs).where(mobs.c.MobID == mob_id))
    keys = list(ex.keys())
    info = list(ex.first())
    statistics = dict(zip(keys, info))
    return statistics


async def get_statistics_person(conn, person_id):
    ex = conn.execute(select(person).where(person.c.UserID == person_id))
    keys = list(ex.keys())
    info = list(ex.first())
    statistics = dict(zip(keys, info))
    return statistics


async def get_characteristic_items(conn):
    items_ = conn.execute(select(items)).fetchall()
    items_to_return = []
    keys = ['ItemID', 'Cost', 'CostToSale', 'ItemType', 'HP', 'Mana', 'Attack', 'MagicAttack', 'Armour', 'MagicArmour', 'ReqLevel', 'Cities']
    for item in items_:
        item = list(item)
        item_id = item[0]
        item_cities = list(conn.execute(select(cities_items).where(cities_items.c.ItemID == item_id)).fetchall())
        cities = []
        for item_pair in item_cities:
            cities.append(item_pair[0])
        item.append(cities)
        print(item_cities)
        item_to_return = dict(zip(keys, list(item)))
        items_to_return.append(item_to_return)
    return items_to_return


async def get_inventory(conn, person_id):
    invs = conn.execute(select(persons_items).where(persons_items.c.UserID == person_id)).fetchall()
    invs_to_return = []
    keys = ['UserID', 'ItemID', 'Quantity', 'On']
    for item in invs:
        inv_to_return = dict(zip(keys, list(item)))
        invs_to_return.append(inv_to_return)
    return invs_to_return


async def get_locations(conn):
    locs = conn.execute(select(locations))
    keys = locs.keys()
    locs = locs.fetchall()
    locs_to_return = []
    for loc in locs:
        loc_to_return = dict(zip(keys, list(loc)))
        locs_to_return.append(loc_to_return)
    return locs_to_return
