from sqlalchemy import select, update, insert, delete
from models import *


async def buy(conn, person_id, item_id):
    item_state = list(conn.execute(select(items).where(items.c.ItemID == item_id)).fetchall())
    if len(item_state) == 0:
        return -1
    item_state = item_state[0]
    price = item_state[1]
    cur_state = list(conn.execute(select(person).where(person.c.UserID == person_id)).first())
    cur_money = cur_state[7]
    if cur_money - price < 0:
        return 0
    item_level = item_state[10]
    cur_level = cur_state[2]
    if cur_level < item_level:
        return 1
    person_city = list(conn.execute(select(person).where(person.c.UserID == person_id)).first())[13]
    item_city = list(conn.execute(select(cities_items).where(cities_items.c.ItemID == item_id)).first())[0]
    if person_city != item_city:
        return 2
    purchase = update(person).where(person.c.UserID == person_id).values(
        Money=cur_money - price,
    )
    conn.execute(purchase)

    persons_items_ = conn.execute(select(persons_items).where(
        (persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id))).fetchall()
    print(persons_items_)
    if len(persons_items_) == 0:
        ins = insert(persons_items)
        conn.execute(ins, [
            {
                'UserID': person_id,
                'ItemID': item_id,
            }
        ]
                        )

    else:
        persons_items_ = list(persons_items_[0])
        cur_quantity = persons_items_[2]
        put = update(persons_items).where(
            (persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id)).values(
            Quantity=cur_quantity + 1
        )
        conn.execute(put)
    return 3


async def sell(conn, person_id, item_id):
    cur_state = conn.execute(select(persons_items).where((persons_items.c.UserID == person_id) &
                                                         (persons_items.c.ItemID == item_id))).fetchall()
    if len(cur_state) == 0:
        return False
    ex = conn.execute(select(items).where(items.c.ItemID == item_id))
    price = list(ex.first())[2]
    selling = update(person).where(person.c.UserID == person_id).values(
        Money=person.c.Money + price,
    )
    conn.execute(selling)
    ex = conn.execute(
        select(persons_items).where((persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id)))
    ex = list(ex.first())
    cur_quantity = ex[2]
    if cur_quantity > 1:
        take = update(persons_items).where(
            (persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id)).values(
            Quantity=cur_quantity - 1
        )
    else:
        take = delete(persons_items).where((persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id))
    conn.execute(take)
    return True


async def put_on(conn, person_id, item_id):
    cur_state = conn.execute(select(persons_items).where(
        (persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id))).fetchall()
    if len(cur_state) == 0:
        return 0
    if (cur_state[0])[3]:
        return 1
    cur_items = list(conn.execute(select(persons_items).where(persons_items.c.UserID == person_id)).fetchall())
    cur_items_ids = []
    for item in cur_items:
        cur_item_id = item[1]
        if item[3]:
            cur_items_ids.append(cur_item_id)
    print(cur_items_ids)
    cur_items = list(conn.execute(select(items).where(items.c.ItemID.in_(cur_items_ids))).fetchall())
    cur_items_types = []
    for item in cur_items:
        cur_item_type = item[3]
        cur_items_types.append(cur_item_type)
    item_char = list(conn.execute(select(items).where(items.c.ItemID == item_id)).first())
    if item_char[3] in cur_items_types:
        return 3
    wear = update(persons_items).where(
        (persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id)).values(
        On=True
    )
    conn.execute(wear)
    change_char = update(person).where(person.c.UserID == person_id).values(
        CurHP=(person.c.CurHP + item_char[4]) % 101,
        CurMana=person.c.CurMana + item_char[5] % 101,
        Attack=person.c.Attack + item_char[6],
        MagicAttack=person.c.MagicAttack + item_char[7],
        Armour=person.c.Armour + item_char[8],
        MagicArmour=person.c.MagicArmour + item_char[9],
    )
    conn.execute(change_char)
    return 2


async def put_off(conn, person_id, item_id):
    cur_state = conn.execute(select(persons_items).where(
        (persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id))).fetchall()
    if len(cur_state) == 0:
        return 0
    if not (cur_state[0])[3]:
        return 1
    unwear = update(persons_items).where(
        (persons_items.c.UserID == person_id) & (persons_items.c.ItemID == item_id)).values(
        On=False
    )
    conn.execute(unwear)
    item_char = list(conn.execute(select(items).where(items.c.ItemID == item_id)).first())
    change_char = update(person).where(person.c.UserID == person_id).values(
        CurHP=person.c.CurHP - item_char[4],
        CurMana=person.c.CurMana - item_char[5],
        Attack=person.c.Attack - item_char[6],
        MagicAttack=person.c.MagicAttack - item_char[7],
        Armour=person.c.Armour - item_char[8],
        MagicArmour=person.c.MagicArmour - item_char[9],
        # Mana?
    )
    conn.execute(change_char)
    return 2


async def mother_lode(conn, person_id):
    conn.execute(update(person).where(person.c.UserID == person_id).values(
        Money=5000
    )
    )
    conn.execute(update(mobs).where(mobs.c.MobID == 1).values(
        HP=50
    )
    )
