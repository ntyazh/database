from sqlalchemy import MetaData, Table, String, Integer, Column, Boolean, ForeignKey

metadata = MetaData()

person = Table('Person', metadata,
               Column('UserID', Integer(), primary_key=True),
               Column('Nickname', String(50), nullable=False),
               Column('Level', Integer(), default=1),
               Column('HP', Integer(), default=100),
               Column('CurHP', Integer(), default=100),
               Column('Mana', Integer(), default=100),
               Column('CurMana', Integer(), default=100),
               Column('Money', Integer(), default=1000),
               Column('Attack', Integer(), default=10),
               Column('MagicAttack', Integer(), default=10),
               Column('XP', Integer(), default=0),
               Column('Armour', Integer(), default=10),
               Column('MagicArmour', Integer(), default=10),
               Column('LocationID', Integer(), default=1),
               )

mobs = Table('Mobs', metadata,
             Column('MobID', Integer(), primary_key=True),
             Column('HP', Integer()),
             Column('Attack', Integer()),
             Column('AttackType', String(20)),
             Column('ReqLevel', Integer()),
             Column('XP', Integer()),
             Column('Armour', Integer()),
             Column('MagicArmour', Integer()),
             )

locations = Table('Locations', metadata,
                  Column('LocationID', Integer(), primary_key=True),
                  Column('XCoord', Integer()),
                  Column('YCoord', Integer()),
                  Column('LocationType', String(20)),
                  )

items = Table('Items', metadata,
              Column('ItemID', Integer(), primary_key=True),
              Column('Cost', Integer()),
              Column('CostToSale', Integer()),
              Column('ItemType', String(30)), #(оружие, броня, шлем, сапоги, наручи, зелье)
              Column('HP', Integer()),
              Column('Mana', Integer()),
              Column('Attack', Integer()),
              Column('MagicAttack', Integer()),
              Column('Armour', Integer()),
              Column('MagicArmour', Integer()),
              Column('ReqLevel', Integer()),
              )

persons_items = Table('PersonsItems', metadata,
                      Column('UserID', Integer()),
                      Column('ItemID', Integer()),
                      Column('Quantity', Integer(), default=1),
                      Column('On', Boolean(), default=False)
                      )

cities_items = Table('CitiesItems', metadata,
                     Column('LocationID', Integer(),),
                     Column('ItemID', Integer(),),
                     )

movements = Table('Movements', metadata,
                  Column('LocationIDCur', Integer()),
                  Column('LocationIDTo', Integer()),
                  Column('Time', Integer())
                  )
