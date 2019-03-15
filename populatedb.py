from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, Base, Category, Item 

engine = create_engine('sqlite:///item_category_app.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Adding Categories 

category_1 = Category(category_name="Tools")

session.add(category_1)
session.commit()

category_2 = Category(category_name="Sports")

session.add(category_2)
session.commit()

category_3 = Category(category_name="Movie Genres")

session.add(category_3)
session.commit()

category_4 = Category(category_name="Gadgets")

session.add(category_4)
session.commit()

category_5 = Category(category_name="Operational System")

session.add(category_5)
session.commit()

category_6 = Category(category_name="School Material")

session.add(category_6)
session.commit()

# Adding the first User
user_1 = User(username = 'Admin', google_sub='1',)
session.add(user_1)
session.commit()


# Adding Items - Category 1 
item_1 = Item(item_name='Hammer', item_description = 'Hammer is a tool to use with nails.',  category = category_1)

session.add(item_1)
session.commit()

item_2 = Item(item_name='Screwdriver', item_description = 'Screwdriver is used to put screws in their right place.',  category = category_1)

session.add(item_2)
session.commit()

item_3 = Item(item_name='Saw', item_description = 'With the saw you cut wood, steel and alsop plastic.',  category = category_1)

session.add(item_3)
session.commit()


item_4 = Item(item_name='Pliers', item_description = 'Uhuuu fuck the police.',  category = category_1)

session.add(item_4)
session.commit()


# Adding Items - Category 2
item_5 = Item(item_name='Swimming', item_description = 'Swimming is one of the most complete sports. Is one of the Sports with most gold medals for Brazil',  category = category_2)

session.add(item_5)
session.commit()


item_6 = Item(item_name='Football', item_description = 'Football is the sport that moves more money in the ocident. Cricket is the equivalent in oriental side. Mbappe is the most famous sportler.',  category = category_2)

session.add(item_6)
session.commit()


item_7 = Item(item_name='Chess', item_description = 'Chess is one of the sports that require more strategy. You must have a lot of patience.',  category = category_2)

session.add(item_7)
session.commit()


item_8 = Item(item_name='American Football', item_description = 'Swimming is one of the American football (often called football in the United States) is a team sport. It is played by two teams with 11 players on each side. American football is played with a ball with pointed ends. Points are scored in many ways, usually by one team getting the ball into the end zone of the other team.',  category = category_2)

session.add(item_8)
session.commit()

item_9 = Item(item_name='Fencing', item_description = 'Fencing is a modern and exciting competitive sport involving the skilled use of the three sport weapons – foil, épée and sabre. ... It is a sport which relies on the use of tactics and strategy as well as speed and skill while facing your opponent.',  category = category_2)

session.add(item_9)
session.commit()

item_10 = Item(item_name='Basketball', item_description = 'Basketball is a team sport. Two teams of five players each try to score by shooting a ball through a hoop elevated 10 feet above the ground. The game is played on a rectangular floor called the court, and there is a hoop at each end. The court is divided into two main sections by the mid-court line.',  category = category_2)

session.add(item_10)
session.commit()

item_11 = Item(item_name='Handball', item_description = 'Handball consists of two teams of seven, who aim to score as many goals against the opposing teams using only the hands. 0. Handball consists of two teams of seven, who aim to score as many goals against the opposing teams using only the hands',  category = category_2)

session.add(item_11)
session.commit()


item_12 = Item(item_name='Chess', item_description = 'Athletics is a collection of sporting events that involve competitive running, jumping, throwing, and walking. The most common types of athletics competitions are track and field, road running, cross country running, and walking race. ... Organized athletics are traced back to the Ancient Olympic Games from 776 BC.',  category = category_2)

session.add(item_12)
session.commit()

# Adding items from Category 3

item_13 = Item(item_name='Thriller', item_description = 'Thriller is a broad genre of literature, film and television, having numerous, often overlapping subgenres. Thrillers are characterized and defined by the moods they elicit, giving viewers heightened feelings of suspense, excitement, surprise, anticipation and anxiety.',  category_id = 3)

session.add(item_13)
session.commit()

item_14 = Item(item_name='Drama', item_description = 'Drama is also a type of a play written for theater, television, radio, and film. In simple words, a drama is a composition in verse or prose presenting a story in pantomime or dialogue. It contains conflict of characters, particularly the ones who perform in front of audience on the stage.',  category_id = 3)

session.add(item_14)
session.commit()

item_15 = Item(item_name='Horror', item_description = "A horror film is a film that seeks to elicit fear. ... Horror films often aim to evoke viewers' nightmares, fears, revulsions and terror of the unknown. Plots with in the horror genre often involve the intrusion of an evil force, event, or personage into the everyday world.",  category_id = 3, user_id = 1)

session.add(item_15)
session.commit()

item_16 = Item(item_name='Aventure', item_description = 'Adventure Films are exciting stories, with new experiences or exotic locales. Adventure films are very similar to the action film genre, in that they are designed to provide an action-filled, energetic experience for the film viewer.',  category_id = 3, user_id = 1)

session.add(item_16)
session.commit()

item_17 = Item(item_name='Documentary', item_description = 'A documentary is a broad term to describe a non-fiction movie that in some way "documents" or captures reality. ... Documentary filmmakers are often motivated to make their films because they feel a particular story or viewpoint is not being (adequately) covered by mainstream media.',  category_id = 3, user_id = 1)

session.add(item_17)
session.commit()

# Adding Item from Category 4
item_18 = Item(item_name='Smartphone', item_description = 'A smartphone is a cellular telephone with an integrated computer and other features not originally associated with telephones, such as an operating system, web browsing and the ability to run software applications.',  category_id = 4, user_id = 1)

session.add(item_18)
session.commit()

item_19 = Item(item_name='MP3 Player', item_description = 'A portable consumer electronic device that allows you to store and plays music files in MP3 format. ... While frequently called an MP3 player, it fits under the broader category of digital audio players and often an MP3 players can use other file types such as Windows Media Audio (WMA).',  category_id = 4, user_id = 1)

session.add(item_19)
session.commit()

item_20 = Item(item_name='Palm-top', item_description = 'A small computer that literally fits in your palm. ... Palmtops that use a pen rather than a keyboard for input are often called hand-held computers or PDAs. Because of their small size, most palmtop computers do not include disk drives.',  category_id = 4, user_id = 1)

session.add(item_20)
session.commit()

item_21 = Item(item_name='Walkman', item_description = '''Walkman is a series 
                                    of portable media players and some Xperia
                                    mobile phones manufactured by Sony. The 
                                    original Walkman, released in 1979, was a
                                    portable cassette player that changed 
                                    listening habits by allowing people to listen
                                    to music on the move.''',  category_id = 4,
                                    user_id = 1)

session.add(item_21)
session.commit()

# Adding Items from Categpry 5
item_21 = Item(item_name='MacOS', item_description = "Mac OS is the computer operating system for Apple Computer's Macintosh line of personal computers and workstations. A popular feature of its latest version, Mac OS X , is a desktop interface with some 3-D appearance characteristics.",  category_id = 5, user_id = 1)

session.add(item_21)
session.commit()

item_22 = Item(item_name='Windows', item_description = 'Windows. Windows is a series of operating systems developed by Microsoft. Each version of Windows includes a graphical user interface, with a desktop that allows users to view files and folders in windows. For the past two decades, Windows has been the most widely used operating system for personal computers PCs.',  category_id = 5, user_id = 1)

session.add(item_22)
session.commit()

item_23 = Item(item_name='Linux', item_description = 'The Linux open source operating system, or Linux OS, is a freely distributable, cross-platform operating system based on Unix that can be installed on PCs, laptops, netbooks, mobile and tablet devices, video game consoles, servers, supercomputers and more.',  category_id = 5, user_id = 1)

session.add(item_23)
session.commit()




print("All items added")