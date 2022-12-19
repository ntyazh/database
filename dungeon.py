from sqlalchemy import select, update, insert, delete
from models import *
import random


async def generate_mob(conn, person_id):
    person_level = conn.execute(select(person).where(person.c.UserID == person_id)).first()[2]
    mobs_ = list(conn.execute(select(mobs).where(mobs.c.ReqLevel <= person_level)).fetchall())
    if len(mobs_) == 0:
        return -1 #No mobs for your level
    random.shuffle(mobs_)
    mob = mobs_[(len(mobs_) - 1) // 2][0]
    return mob


async def fight_mob(conn, person_id, mob_id, attack_type):
    person_char = conn.execute(select(person).where(person.c.UserID == person_id)).first()
    mob_id = int(mob_id)
    mob_char = conn.execute(select(mobs).where(mobs.c.MobID == mob_id)).first()
    if mob_char[1] <= 0:
        return 0
    print(mob_char)
    if attack_type == "P":
        person_attack = person_char[8]
        mob_armour = mob_char[6]

    else:
        person_attack = person_char[9]
        mob_armour = mob_char[7]

    hp_lost = person_attack - mob_armour
    print(hp_lost)
    injure_mob = update(mobs).where(mobs.c.MobID == mob_id).values(
        HP=mobs.c.HP - hp_lost
    )
    conn.execute(injure_mob)
    print(conn.execute(select(mobs)).fetchall())
    mob_new_char = conn.execute(select(mobs).where(mobs.c.MobID == mob_id)).first()
    if mob_new_char[1] <= 0:
        return 2
    return 1


async def fight_person(conn, person_id, mob_id):
    person_char = list(conn.execute(select(person).where(person.c.UserID == person_id)).first())
    mob_id = int(mob_id)
    mob_char = list(conn.execute(select(mobs).where(mobs.c.MobID == mob_id)).first())
    print(mob_char)
    print(person_char)
    attack_type = mob_char[3]
    if mob_char[1] <= 0:
        return 0
    mob_attack = mob_char[2]
    print(mob_char)
    if attack_type == "Physical":
        person_armour = person_char[11]
    else:
        person_armour = person_char[12]

    hp_lost = mob_attack - person_armour
    print(hp_lost)
    injure_person = update(person).where(person.c.UserID == person_id).values(
        CurHP=person.c.CurHP - hp_lost
    )
    conn.execute(injure_person)
    print(conn.execute(select(mobs)).fetchall())
    person_new_char = conn.execute(select(person).where(person.c.UserID == person_id)).first()
    if person_new_char[3] <= 0:
        return 2
    return 1
