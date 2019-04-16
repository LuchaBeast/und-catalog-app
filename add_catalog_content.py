from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Populate Action Figures category
category1 = Category(category_name="Action Figures")

session.add(category1)
session.commit()

item1 = Item(item_name="Masters of the Universe Vintage Skeletor", item_description="By the Power of Grayskull! Super7 is proud to present the MOTU Vintage Collection, the original Masters of the Universe action figures re-imagined to match the character designs from the animated cartoon! The Skeletor 5.5-inch Vintage Figure comes with Havoc Staff, Power Sword, and Half-Sword and features a spring loaded mechanism: Turn the waist and he swings back with a punch! The packaging includes a custom character history card with the figure and has new and original art on the back of each card by classic MOTU artist Errol McCarthy.", category=category1)

session.add(item1)
session.commit()

item2 = Item(item_name="Masters of the Universe Vintage He-Man", item_description="By the Power of Grayskull! Super7 is proud to present the MOTU Vintage Collection, the original Masters of the Universe action figures re-imagined to match the character designs from the animated cartoon! The He-Man 5.5-inch Vintage Figure comes with Power Sword, Half-Sword, and Shield and features a spring loaded mechanism: Turn the waist and he swings back with a punch! The packaging includes a custom character history card with the figure and has new and original art on the back of each card by classic MOTU artist Errol McCarthy.", category=category1)

session.add(item2)
session.commit()

item3 = Item(item_name="Masters of the Universe Classics Club Grayskull Prince Adam", item_description="The Super7 Masters of the Universe Club Grayskull series continues with Wave 4! This super detailed deluxe 7-inch Masters of the Universe Prince Adam figure features details as seen in the original He-Man and the Masters of the Universe Filmation cartoon series. Prince Adam also includes Sword of Power, Sword of Power in transformation mode, and a Photanium Shield. MOTU fans will not want to miss adding this figure to their collection!", category=category1)

session.add(item3)
session.commit()

item4 = Item(item_name="Masters of the Universe Classics Club Grayskull She-Ra", item_description="The Masters of the Universe Classics Club Grayskull She-Ra is a 7 inch tall deluxe, highly articulated and fully poseable action figure. Each super detailed Classics Figure is sculpted by the Four Horsemen and comes packaged in a brand new blister package featuring new artwork inspired by the iconic vintage Masters of the Universe toys.", category=category1)

session.add(item4)
session.commit()

item5 = Item(item_name="Masters of the Universe Classics Club Grayskull Shadow Weaver", item_description="The Super7 Masters of the Universe Club Grayskull series continues with Wave 4! This super detailed deluxe 7-inch Masters of the Universe Shadow Weaver figure features details as seen in the original He-Man and the Masters of the Universe Filmation cartoon series. Shadow Weaver also includes a Wizard's Wand, Wand of Crystal, and a Magical blast. MOTU fans will not want to miss adding this figure to their collection!", category=category1)

session.add(item5)
session.commit()

# Populate Transformers Category
category2 = Category(category_name="Transformers")

session.add(category2)
session.commit()

item1 = Item(item_name="Transformers Masterpiece Movie Series MPM-9 Jazz", item_description="Masterpiece Movie Series Jazz is 6 inches and a perfect, authentic figure for fans and collectors alike, with features inspired by the explosive 2007 Transformers live action movie. The figure showcases the daring Autobot with impressive attention to detail and features articulated hands, sliding visor, die cast detailing, shield weapon accessory and spinal cord attachment. By pressing a back button, Jazz can be split in two and posed with Masterpiece Movie Series Megatron to recreate the tragic death scene from the film. The figure also features 47 points of articulation and includes a Sam Witwicky figurine running with the Allspark Cube.", category=category2)

session.add(item1)
session.commit()

item2 = Item(item_name="Transformers Masterpiece MP-43 Megatron (Beast Wars)", item_description="The mighty Megatron from Transformers: Beast Wars gets a Transformers Masterpiece release from Takara Tomy! He's fully transformable between his robot and dinosaur forms, and he can use his dinosaur head as a handheld weapon!", category=category2)

session.add(item2)
session.commit()

item3 = Item(item_name="Transformers Masterpiece MP-44 Convoy/Optimus Prime (Ver. 3)", item_description="Making a third appearance into the Transformers Masterpiece line is the brave leader of the Autobots, Optimus Prime. This version of Optimus will feature a more cartoon accurate styling.", category=category2)

session.add(item3)
session.commit()

item4 = Item(item_name="Transformers Masterpiece MP-11NT Thrust", item_description="MP-11NT Masterpiece Thrust features the G1 design from the animated television series, multiple points of articulation, and transforms into a fighter jet. In jet mode, the cockpit opens and can fit the hologram pilot figure inside. His wings feature vertical rise fans and anti-aircraft missiles!", category=category2)

session.add(item4)
session.commit()

item5 = Item(item_name="Transformers Masterpiece MP-11NR Ramjet", item_description="Masterpiece MP-11NR Ramjet is the first Conehead retool of the MP-11 Starscream mold and features a black, white and red color scheme. Conehead refers to the fact that the jet nosecone points up in robot mode creating a pointy conehead on the robot. Another distinctive feature is that the wings do not flip up to be part of the upper body of the robot mode and are instead part of the legs.", category=category2)

session.add(item5)
session.commit()

# Populate Transformers Category
category3 = Category(category_name="Funko")

session.add(category3)
session.commit()

item1 = Item(item_name="Pop! Movies: Spider-Man: Far From Home - Molten Man", item_description="Pop! figures bring your favorite superheroes to life with a unique stylized design. Each vinyl figure stands 3.75 inches tall and comes in window box packaging, making them great for display!", category=category3)

session.add(item1)
session.commit()

item2 = Item(item_name="Pop! Movies: Spider-Man: Far From Home - Hydro-Man", item_description="Pop! figures bring your favorite superheroes to life with a unique stylized design. Each vinyl figure stands 3.75 inches tall and comes in window box packaging, making them great for display!", category=category3)

session.add(item2)
session.commit()

item3 = Item(item_name="Pop! Marvel: Avengers: Endgame - War Machine", item_description="From Avengers: Endgame, the Avengers are putting it all on the line to defeat Thanos. Show your support for your favorite Super Heroes by bringing home Pop! Hulk, Captain America, Thor, Black Widow, Ant-Man, Tony Stark, Thanos, Hawkeye, Captain Marvel, Nebula and War Machine.", category=category3)

session.add(item3)
session.commit()

item4 = Item(item_name="Pop! Marvel: Avengers: Endgame - Black Widow", item_description="From Avengers: Endgame, the Avengers are putting it all on the line to defeat Thanos. Show your support for your favorite Super Heroes by bringing home Pop! Hulk, Captain America, Thor, Black Widow, Ant-Man, Tony Stark, Thanos, Hawkeye, Captain Marvel, Nebula and War Machine.", category=category3)

session.add(item4)
session.commit()

item5 = Item(item_name="Pop! Marvel: Spider-Carnage Exclusive", item_description="Pop! figures bring your favorite characters to life with a unique stylized design. Each vinyl figure stands 3.75 inches tall and comes in window box packaging, making them great for display!", category=category3)

session.add(item5)
session.commit()

print("added toy catalog items")