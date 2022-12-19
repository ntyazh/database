import re

import telebot
from telebot.async_telebot import AsyncTeleBot
import asyncio
import aiohttp

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import insert, select, update, delete

from models import *
from statistics import *
from create import *
from items import *
from motion import *

data_base = sqlite3.connect('game.db')

engine = create_engine('sqlite+pysqlite:///game.db', echo=True)
conn = engine.connect()

TOKEN = '5873285544:AAEbBaBj3SWtS7ukoTIat92Sy1tgPs2Xwxg'
bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['help'])
async def help_message(message):
    await bot.send_message(message.chat.id,
                           f"/start -- start game \n"
                           f"/create_person <nickname> -- create person with the nickname\n"
                           f"/view_items -- view all items \n"
                           f"/view_inventory -- view your inventory \n"
                           f"/buy <item_id> -- buy item with this item_id \n"
                           f"/sell <item_id> -- sell the item \n"
                           f"/put_on <item_id> -- put on the item \n"
                           f"/put_off <item_id> -- put off the item \n"
                           f"/view_person -- get your characteristic \n"
                           f"/view_locations -- view all locations \n"
                           f"/move_to <location_id> -- go to location with id <location_id> \n"
                           f"/put_off <item_id> -- put off the item \n"
                           f"/fight <type> <mob_id> -- fight the mob with the type of attack: type P for physical attack, M - for magical \n"
                           f"/view_mob <mob_id> -- view the mob's characteristic \n"
                           )


@bot.message_handler(commands='start')
async def start_message(message):
    await set_environment(conn, engine)
    await bot.send_message(message.chat.id, "Environment is set")


@bot.message_handler(commands='create_person')
async def create_person_message(message):
    nickname = message.text[15:]
    await create_person(conn, message.from_user.id, nickname)
    await bot.send_message(message.chat.id, f"{message.text[15:]} is created")


@bot.message_handler(commands='view_items')
async def view_items_message(message):
    items_ = await get_characteristic_items(conn)
    nl = '\n'
    for item in items_:
        await bot.send_message(message.chat.id, f"ItemID: {item['ItemID']},{nl}"
                                                f"Cost: {item['Cost']},{nl}"
                                                f"CostToSale: {item['CostToSale']},{nl}"
                                                f"ItemType: {item['ItemType']},{nl}"
                                                f"HP: {item['HP']},{nl}"
                                                f"Mana: {item['Mana']},{nl}"
                                                f"Attack: {item['Attack']},{nl}"
                                                f"MagicAttack: {item['MagicAttack']}, {nl}"
                                                f"Armour: {item['Armour']}, {nl}"
                                                f"MagicArmour: {item['MagicArmour']},{nl}"
                                                f"ReqLevel: {item['ReqLevel']},{nl}"
                                                f"Cities: {item['Cities']}."
                               )


@bot.message_handler(commands='view_inventory')
async def view_inventory_message(message):
    items_ = await get_inventory(conn, message.from_user.id)
    nl = '\n'
    if len(items_) == 0:
        await bot.send_message(message.chat.id, "No items in the inventory")
    for item in items_:
        await bot.send_message(message.chat.id, f"ItemID: {item['ItemID']},{nl}"
                                                f"Quantity: {item['Quantity']},{nl}"
                                                f"On: {item['On']}.")


@bot.message_handler(commands='buy')
async def buy_message(message):
    item_id = re.findall(r'\d+', message.text)[0]
    success = await buy(conn, message.from_user.id, item_id)
    if success == -1:
        await bot.send_message(message.chat.id, f"Item with this id doesn't exist")
    elif success == 3:
        await bot.send_message(message.chat.id, f"The item with id {item_id} is bought")
    elif success == 0:
        await bot.send_message(message.chat.id, f"You don't have enough money")
    elif success == 1:
        await bot.send_message(message.chat.id, f"Your level is lower than the required")
    else:
        await bot.send_message(message.chat.id, f"The item is not available in your city")


@bot.message_handler(commands='sell')
async def sell_message(message):
    item_id = re.findall(r'\d+', message.text)[0]
    success = await sell(conn, message.from_user.id, item_id)
    print(conn.execute(select(persons_items)).fetchall())
    if success:
        await bot.send_message(message.chat.id, f"The item with id {item_id} is sold")
    else:
        await bot.send_message(message.chat.id, f"You don't have this item")


@bot.message_handler(commands='put_on')
async def put_on_message(message):
    item_id = re.findall(r'\d+', message.text)[0]
    success = await put_on(conn, message.from_user.id, item_id)
    if success == 0:
        await bot.send_message(message.chat.id, f"You don't have this item")
    elif success == 1:
        await bot.send_message(message.chat.id, f"The item is already on")
    elif success == 2:
        await bot.send_message(message.chat.id, f"You wore the item with id {item_id}")
    else:
        await bot.send_message(message.chat.id, f"You already wear clothes with this type")


@bot.message_handler(commands='put_off')
async def put_off_message(message):
    item_id = re.findall(r'\d+', message.text)[0]
    success = await put_off(conn, message.from_user.id, item_id)
    if success == 0:
        await bot.send_message(message.chat.id, f"You don't have this item")
    elif success == 1:
        await bot.send_message(message.chat.id, f"The item is already off")
    else:
        await bot.send_message(message.chat.id, f"You put off the item with id {item_id}")


@bot.message_handler(commands='view_person')
async def view_person_statistics(message):
    nl = '\n'
    person_ = await get_statistics_person(conn, message.from_user.id)
    await bot.send_message(message.chat.id, f"Nickname: {person_['Nickname']},{nl}"
                                            f"Level: {person_['Level']},{nl}"
                                            f"HP: {person_['HP']},{nl}"
                                            f"CurHP: {person_['CurHP']},{nl}"
                                            f"Mana: {person_['Mana']},{nl}"
                                            f"CurMana: {person_['CurMana']},{nl}"
                                            f"Money: {person_['Money']},{nl}"
                                            f"Attack: {person_['Attack']},{nl}"
                                            f"MagicAttack: {person_['MagicAttack']},{nl}"
                                            f"XP: {person_['XP']},{nl}"
                                            f"Armour: {person_['Armour']},{nl}"
                                            f"MagicArmour: {person_['MagicArmour']},{nl}"
                                            f"LocationID: {person_['LocationID']}.")


@bot.message_handler(commands='view_locations')
async def view_locations_message(message):
    locations_ = await get_locations(conn)
    nl = '\n'
    for location in locations_:
        await bot.send_message(message.chat.id, f"LocationID: {location['LocationID']},{nl}"
                                                f"XCoord: {location['XCoord']},{nl}"
                                                f"YCoord: {location['YCoord']},{nl}"
                                                f"LocationType: {location['LocationType']}."
                               )


@bot.message_handler(commands='move_to')
async def move_to_message(message):
    location_id = re.findall(r'\d+', message.text)[0]
    success = await move_to(conn, message.from_user.id, location_id)
    if success == 1:
        if int(location_id) % 2 == 1:
            await bot.send_message(message.chat.id, f"You are on the location with id {location_id} now")
        else:
            await dungeon_handler(message)
    elif success == 0:
        await bot.send_message(message.chat.id, "This location is not available from your place (distance > 10)")
    elif success == -1:
        await bot.send_message(message.chat.id, f"No location with such id")
    else:
        await bot.send_message(message.chat.id, "You are already there")


async def injure_person(mob_id, person_id, message):
    success = await fight_person(conn, person_id, mob_id)
    if success == 1:
        await bot.send_message(message.chat.id, "You've got injured by the mob!")
    elif success == 2:
        await bot.send_message(message.chat.id, "You're killed by the mob!")


async def dungeon_handler(message):
    print(message.from_user.id)
    mob = await generate_mob(conn, message.from_user.id)
    if mob == -1:
        await bot.send_message(message.chat.id, "No mobs available for your level")
        return
    await bot.send_message(message.chat.id, f"You are in location with a mob with id {mob}. Your actions?")
    await asyncio.sleep(10)
    await injure_person(mob, message.from_user.id, message)


async def check_xp(message):
    if conn.execute(select(person).where(person.c.UserID == message.from_user.id)).first()[10] % 100 == 0:
        await bot.send_message(message.chat.id, "Your level is up!")


@bot.message_handler(commands='fight')
async def fight_message(message):
    # fight_mode же у всех!!!
    persons_location_id = conn.execute(select(person).where(person.c.UserID == message.from_user.id)).first()[13]
    if persons_location_id != 2:
        await bot.send_message(message.chat.id, "You are not on the location with mobs")
        return
    attack_type = message.text[7:9]
    mob_id = re.findall(r'\d+', message.text)[0]
    success = await fight_mob(conn, message.from_user.id, mob_id, attack_type)
    if success == 1:
        await bot.send_message(message.chat.id, "You've injured the mob!")
    elif success == 0:
        await bot.send_message(message.chat.id, "You can't fight a dead mob :(")
    else:
        await bot.send_message(message.chat.id, "You've killed the mob!")
        mob_id = int(mob_id)
        mob_xp = conn.execute(select(mobs).where(mobs.c.MobID == mob_id)).first()[5]
        print(mob_xp)
        conn.execute(update(person).where(person.c.UserID == message.from_user.id).values(
            XP=person.c.XP + mob_xp
        )
        )
        await check_xp(message)


@bot.message_handler(commands='view_mob')
async def view_mob_message(message):
    mob_id = re.findall(r'\d+', message.text)[0]
    mob = await get_statistics_mob(conn, mob_id)
    nl = '\n'
    await bot.send_message(message.chat.id, f"MobID: {mob['MobID']},{nl}"
                                            f"HP: {mob['HP']},{nl}"
                                            f"Attack: {mob['Attack']},{nl}"
                                            f"AttackType: {mob['AttackType']},{nl}"
                                            f"ReqLevel: {mob['ReqLevel']},{nl}"
                                            f"XP: {mob['XP']},{nl}"
                                            f"Armour: {mob['Armour']},{nl}"
                                            f"MagicArmour: {mob['MagicArmour']}.")


@bot.message_handler(commands='motherlode')
async def motherlode_message(message):
    await mother_lode(conn, message.from_user.id)


async def main():
    await asyncio.gather(bot.infinity_polling())


if __name__ == '__main__':
    asyncio.run(main())
