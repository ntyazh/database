from sqlalchemy import select, update, insert, delete
from models import *
import asyncio
import time
from dungeon import *


async def move_to(conn, person_id, location_id):
    location_id = int(location_id)
    keys = list(map(lambda pair: pair[0], list(conn.execute(select(locations.c.LocationID)).fetchall())))
    print(keys)
    if int(location_id) not in keys:
        return -1
    cur_id = conn.execute(select(person).where(person.c.UserID == person_id)).first()[13]
    if cur_id == location_id:
        return 2
    if location_id % 2 == 1:
        restore_and_motion = update(person).where(person.c.UserID == person_id).values(
            CurHP=100,
            CurMana=100,
            LocationID=location_id
        )
        conn.execute(restore_and_motion)
    else:
        motion = update(person).where(person.c.UserID == person_id).values(
            LocationID=location_id
        )
        conn.execute(motion)
    time_ = conn.execute(select(movements).where(
        (movements.c.LocationIDCur == cur_id) & (movements.c.LocationIDTo == location_id))).first()[2]
    if time_ == -1:
        return 0
    time.sleep(time_)
    return 1
