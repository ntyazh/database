from models import *
from sqlalchemy import insert, select


async def set_environment(conn, engine):
    metadata.create_all(engine)
    print('fffffffffffffffffffffffffffffffffffff')
    print(conn.execute(select(mobs)).fetchall())
    if len(conn.execute(select(mobs)).fetchall()) != 0:
        return
    await create_mob(conn, 1, 50, 15, "Magic", 1, 100, 0, 0)
    await create_mob(conn, 2, 100, 10, "Physical", 2, 100, 10, 10)

    await create_location(conn, 1, 0, 0, "City")  # нечётные id - город, чётные - подземелья
    await create_location(conn, 3, 5, 5, "City")
    await create_location(conn, 5, -5, -5, "City")
    await create_location(conn, 2, 0, 1, "Dungeon")

    await create_road(conn, 1, 3)
    await create_road(conn, 3, 1)
    await create_road(conn, 1, 5)
    await create_road(conn, 5, 1)
    await create_road(conn, 3, 5)
    await create_road(conn, 5, 3)
    await create_road(conn, 1, 2)
    await create_road(conn, 2, 1)
    await create_road(conn, 3, 2)
    await create_road(conn, 2, 3)
    await create_road(conn, 5, 2)
    await create_road(conn, 2, 5)
    print(conn.execute(select(movements)).fetchall())

    await create_item(conn, 1, 200, 180, "Armour", 0, 0, 0, 10, 0, 10, 1)
    # item(conn, id:1, cost:200, cost_to_sale:180, "Armour", hp:0, mana:0, attack:0, magic_attack:10,
    # armour:0, magic:armour:10, req_level:1)

    await create_item(conn, 2, 100, 80, "Bracers", 0, 0, 0, 0, 5, 5, 1)
    await create_item(conn, 3, 250, 230, "Weapon", 0, 0, 10, 10, 5, 0, 1)
    await create_item(conn, 4, 160, 140, "Helmet", 0, 0, 0, 0, 50, 20, 5)
    await create_item(conn, 5, 200, 100, "Weapon", 0, 0, 15, 5, 5, 0, 1)
    await create_item(conn, 6, 170, 150, "Boots", 5, 0, 0, 0, 15, 10, 1)
    return 0


async def create_person(conn, user_id, nickname):
    # ins = insert(person)
    conn.execute(insert(person), {
        'UserID': user_id,
        'Nickname': nickname}
                 )
    # ins.compile().params


async def create_mob(conn, mob_id, hp, attack, attack_type, req_level, xp, armour, magic_armour):
    # ins = insert(mobs)
    conn.execute(insert(mobs), [
        {'MobID': mob_id,
         'HP': hp,
         'Attack': attack,
         'AttackType': attack_type,
         'ReqLevel': req_level,
         'XP': xp,
         'Armour': armour,
         'MagicArmour': magic_armour}
    ]
                 )
    # ins.compile().params


async def create_location(conn, location_id, x_coord, y_coord, location_type):
    conn.execute(insert(locations), [
        {
            'LocationID': location_id,
            'XCoord': x_coord,
            'YCoord': y_coord,
            'LocationType': location_type
        }
    ]
                 )
    if location_id == 1:
        conn.execute(insert(cities_items), [
            {
                'LocationID': location_id,
                'ItemID': 1,
            },
            {
                'LocationID': location_id,
                'ItemID': 2,
            },
            {
                'LocationID': location_id,
                'ItemID': 3,
            },
            {
                'LocationID': location_id,
                'ItemID': 4,
            },
            {
                'LocationID': location_id,
                'ItemID': 5,
            },
        ]
                     )
    elif location_id == 3:
        conn.execute(insert(cities_items), [
            {
                'LocationID': location_id,
                'ItemID': 6,
            }
            ]
                     )
        conn.execute(insert(cities_items), [
            {
                'LocationID': location_id,
                'ItemID': 5,
            }
            ]
                     )


async def create_item(conn, item_id, cost, cost_to_sale, item_type, hp, mana, attack, magic_attack, armour,
                      magic_armour,
                      req_level):
    # ins = insert(items)
    conn.execute(insert(items), [
        {
            'ItemID': item_id,
            'Cost': cost,
            'CostToSale': cost_to_sale,
            'ItemType': item_type,
            'HP': hp,
            'Mana': mana,
            'Attack': attack,
            'MagicAttack': magic_attack,
            'Armour': armour,
            'MagicArmour': magic_armour,
            'ReqLevel': req_level
        }
    ]
                 )
    # ins.compile().params


async def create_road(conn, location_cur, location_to):
    state_cur = conn.execute(select(locations).where(locations.c.LocationID == location_cur)).first()
    x_coord_cur = state_cur[1]
    y_coord_cur = state_cur[2]
    state_to = conn.execute(select(locations).where(locations.c.LocationID == location_to)).first()
    x_coord_to = state_to[1]
    y_coord_to = state_to[2]
    time = ((x_coord_to - x_coord_cur) ** 2 + (y_coord_to - y_coord_cur) ** 2) ** 0.5
    if time > 10:
        time = -1
    ins = insert(movements)
    conn.execute(ins, [
        {
            'LocationIDCur': location_cur,
            'LocationIDTo': location_to,
            'Time': time,
        }
    ]
                 )
