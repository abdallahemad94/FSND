from datetime import date
from datetime import datetime
from os import environ as env

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (Column, Date, DateTime, ForeignKey, Integer, String)
from time import sleep

db = SQLAlchemy()
DATABASE_URL = 'postgres://{0}{1}@{2}:5432/{3}'\
    .format(
        env.get("POSTGRES_USER"),
        ':' + env["POSTGRES_PASSWORD"] if env.get('POSTGRES_PASSWORD', None) else '',
        env.get("POSTGRES_HOST", 'localhost'),
        env.get("POSTGRES_DB", 'casting')
    )


def setup_db(app, database_url=DATABASE_URL):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_db(app)


def init_db(app, tries=0):
    try:
        db.app = app
        db.init_app(app)
        seed_database()
    except Exception as e:
        sleep(5)
        tries += 1
        if tries < 5:
            init_db(app, tries=tries)


def seed_database():
    db.drop_all()
    db.create_all()

    artists = [
        {'name': 'Liu Yifei', 'age': 33, 'gender': 'Female',
         'description': 'Liu Yifei ( born An Feng; August 25, 1987) is a popular Chinese-American actress, model and singer. She was born in China and moved to the United States when she was 11.',
         'image': 'https://walter.trakt.tv/images/people/000/016/108/headshots/thumb/5d54607292.jpg.webp'},
        {'name': 'Jet Li', 'age': 57, 'gender': 'Male',
         'description': "Li Lian Jie (born April 26, 1963), better known by his stage name Jet Li, is a Chinese martial artist, actor, film producer, wushu champion, and international film star who was born in Beijing, China, and who has currently taken up Singapore citizenship. After three years of intensive training with Wu Bin, Li won his first national championship for the Beijing Wushu Team. After retiring from wushu at age 17, he went on to win great acclaim in China as an actor making his debut with the film Shaolin Temple (1982). He went on to star in many critically acclaimed martial arts epic films, most notably the Once Upon A Time In China series, in which he portrayed folk hero Wong Fei-hung. Li's first role in a Hollywood film was as a villain in Lethal Weapon 4 (1998), but his first Hollywood film leading role was in Romeo Must Die (2000). He has gone on to star in many Hollywood action films, most recently starring beside Jackie Chan in The Forbidden Kingdom (2008), and as the title character villain in The Mummy: Tomb Of The Dragon Emperor (2008) opposite Brendan Fraser. Recently, he appeared in the 2010 film The Expendables.",
         'image': 'https://walter.trakt.tv/images/people/000/016/031/headshots/thumb/4353ccfef3.jpg.webp'},
        {'name': 'Kristen Bell', 'age': 40, 'gender': 'Female',
         'description': "Kristen Bell (born July 18, 1980) is an American actress and voice actress. In 2001, she made her Broadway debut. After moving to Los Angeles, she landed various television guest appearances and small film parts, but she gained fame as the title character on Veronica Mars. Besides her tv and movie roles, she provided the voice and face of Lucy Stillman in the Assassin's Creed video game series.",
         'image': 'https://walter.trakt.tv/images/people/000/423/962/headshots/thumb/b158adaa5d.jpg.webp'},
        {'name': 'Idina Menzel', 'age': 49, 'gender': 'Female',
         'description': "Idina Menzel (/ɪˈdiːnə mɛnˈzɛl/; born Idina Kim Mentzel; May 30, 1971) is an American actress, singer, and songwriter. She rose to prominence for her performance as Maureen Johnson in the Broadway musical Rent, a role which she reprised for the 2005 feature film adaptation. In 2004, she won the Tony Award for originating the role of Elphaba in the Broadway blockbuster Wicked. In 2014, she will be returning to Broadway in the musical If/Then. Menzel is also known for her portrayal of Shelby Corcoran, the biological mother of Lea Michele's character Rachel Berry, on the Fox musical comedy-drama series Glee, and as the voice of snow queen Elsa in the Disney animated film, Frozen.",
         'image': 'https://walter.trakt.tv/images/people/000/017/887/headshots/thumb/b66e76b9c9.jpg.webp'},
        {'name': "Auli'i Cravalho", 'age': 19, 'gender': 'Female',
         'description': "Auli'i Cravalho is an American actress and singer. She made her voice acting debut as the title character in the 2016 Disney film Moana.",
         'image': 'https://walter.trakt.tv/images/people/000/574/781/headshots/thumb/e4b5b11dd8.jpg.webp'},
        {'name': 'Dwayne Johnson', 'age': 48, 'gender': 'Male',
         'description': "An American and Canadian actor, producer and semi-retired professional wrestler, signed with WWE. Johnson is half-Black and half-Samoan. His father, Rocky Johnson, is a Black Canadian, from Nova Scotia, and part of the first Black tag team champions in WWE history back when it was known as the WWF along with Tony Atlas. His mother is Samoan and the daughter of Peter Maivia, who was also a pro wrestler. Maivia's wife, Lia Maivia, was one of wrestling's few female promoters, taking over Polynesian Pacific Pro Wrestling after her husband's death in 1982, until 1988. Through his mother, he is considered a non-blood relative of the Anoa'i wrestling family. On March 29, 2008, The Rock inducted his father and his grandfather into the WWE Hall of Fame. As of 2014, Johnson has a home in Southwest Ranches, Florida as well as Los Angeles, California. He also owns a farm in Virginia. In 2009, Johnson gained citizenship in Canada in honor of his father's background. Though Johnson was previously registered as a Republican, he voted for Barack Obama in the 2008 and 2012 United States presidential elections and is now an independent voter. He stated he did not vote in the 2016 U.S. election. In recognition of his service to the Samoan people, and because he is a descendant of Samoan chiefs, Johnson had the noble title of Seiuli bestowed upon him by Malietoa Tanumafili II during his visit there in July 2004. He received a partial Samoan pe'a tattoo on his left side in 2003,and, in 2017, had the small \"Brahma bull\" tattoo on his right arm covered with a larger half-sleeve tattoo of a bull's skull. Johnson married Dany Garcia on May 3, 1997. Their only child together, a daughter named Simone, was born in August 2001. On June 1, 2007, they announced they were splitting up amicably. Johnson then began dating Lauren Hashian, daughter of Boston drummer Sib Hashian. They first met in 2006 while Johnson was filming The Game Plan. Their first child together, a daughter, was born in December 2015. Their second child, another daughter, was born in April 2018. Johnson attended the 2000 Democratic National Convention as part of WWE's non-partisan \"Smackdown Your Vote\" campaign, which aimed to influence young people to vote. He also had a speaking role at the 2000 Republican National Convention that same year. In 2006, Johnson founded the Dwayne Johnson Rock Foundation, a charity working with at-risk and terminally ill children. On October 2, 2007, he and his ex-wife donated $1 million to the University of Miami to support the renovation of its football facilities; it was noted as the largest donation ever given to the university's athletics department by former students. The University of Miami renamed the Hurricanes' locker room in Johnson's honor. In 2015, Johnson donated $1,500 to a GoFundMe to pay for an abandoned dog's surgery. In 2017, he donated $25,000 to Hurricane Harvey relief efforts. In 2018, Johnson donated a gym to a military base in Oahu, Hawaii. After the 2018 Hawaii floods, he worked with Malama Kauai, a nonprofit organization, to help repair damages caused by the floods.",
         'image': 'https://walter.trakt.tv/images/people/000/016/341/headshots/thumb/f19d33bcb7.jpg.webp'},
        {'name': 'Robert Downey Jr.', 'age': 55, 'gender': 'Male',
         'description': "Robert John Downey Jr. (born April 4, 1965) is an American actor and producer. Downey made his screen debut in 1970, at the age of five, when he appeared in his father's film Pound, and has worked consistently in film and television ever since. He received two Academy Award nominations for his roles in films Chaplin (1992) and Tropic Thunder (2008). Downey Jr. is most known for his role in the Marvel Cinematic Universe as Tony Stark/Iron Man. He has appeared as the character in Iron Man (2008), The Incredible Hulk (2008), Iron Man 2 (2010), The Avengers (2012), Iron Man 3 (2013), Avengers: Age of Ultron (2015), Captain America: Civil War (2016), Spider-Man: Homecoming (2017), Avengers: Infinity War (2018), and Avengers: Endgame (2019). The character is the most notable in the Marvel Cinematic Universe, and helped transcend the franchise into the goliath that it is today.",
         'image': 'https://walter.trakt.tv/images/people/000/015/987/headshots/thumb/655134a280.jpg.webp'},
        {'name': 'Chris Evans', 'age': 39, 'gender': 'Male',
         'description': "An American actor. Evans is known for his superhero roles as the Marvel Comics characters Steve Rogers in the Marvel Cinematic Universe and the Human Torch in Fantastic Four (2005) and its 2007 sequel. Evans began his career on the 2000 television series Opposite Sex. Besides his superhero films, he has appeared in such films as Not Another Teen Movie (2001), Sunshine (2007), Scott Pilgrim vs. the World (2010), Snowpiercer (2013), and Gifted (2017). In 2014, he made his directorial debut with the drama film Before We Go, in which he also starred. Evans made his Broadway debut in a 2018 production of Lobby Hero. Courtesy Wikipedia®",
         'image': 'https://walter.trakt.tv/images/people/000/016/494/headshots/thumb/ecebaea4c2.jpg.webp'},
        {'name': 'Matthew Broderick', 'age': 58, 'gender': 'Male',
         'description': "Matthew Broderick is an American actor whose career has spanned both the silver screen and the stage. Broderick got his start off broadway but quickly wound up as the lead in Neil Simon's Brighton Beach Memoirs. His first screen role was Max Dugan Returns, also penned by Neil Simon. His breakout role came the same year for his role as a young hacker in Wargames. Later he stared as the eponymous Ferris Bueller in 1985's Ferris Bueller's Day Off, a film which has achieved cult status and had made Broderick a household name. In 1985 while on Vacation in Ireland with his then fiancee Jennifer Grey, who played his sister in Ferris Bueller's Day Off, Broderick was involved in a head on collision that killed two locals. Broderick was deemed at fault and faced five years in prison but his punishment was lessened to just a fine. In 1997 he married Sarah Jessica Parker and the pair have had 3 children together.",
         'image': 'https://walter.trakt.tv/images/people/000/016/993/headshots/thumb/26bc1a4d5e.jpg.webp'},
        {'name': 'James Earl Jones', 'age': 89, 'gender': 'Male',
         'description': "James Earl Jones (born January 17, 1931) is a multi-award-winning American actor of theater and film, well known for his distinctive bass voice and for his portrayal of characters of substance, gravitas and leadership. He is known for providing the voice of Darth Vader in the Star Wars franchise and the tagline for CNN. James Earl Jones was born in Arkabutla, Mississippi, the son of Ruth (née Connolly) and Robert Earl Jones. At the age of five, he moved to Jackson, Michigan, to be raised by his maternal grandparents, but the adoption was traumatic and he developed a stutter so severe he refused to speak aloud. When he moved to Brethren, Michigan in later years a teacher at the Brethren schools started to help him with his stutter. He remained functionally mute for eight years until he reached high school. He credits his high school teacher, Donald Crouch, who discovered he had a gift for writing poetry, with helping him out of his silence. Jones attended the University of Michigan where he was a pre-med major. While there, he joined the Reserve Officer Training Corps, and excelled. During the course of his studies, Jones discovered he was not cut out to be a doctor. Instead he focused himself on drama, with the thought of doing something he enjoyed, before, he assumed, he would have to go off to fight in the Korean War. After four years of college, Jones left without his degree. In 1953 he found a part-time stage crew job at the Ramsdell Theatre in Manistee, Michigan, which marked the beginning of his acting career. During the 1955–1957 seasons he was an actor and stage manager. He performed his first portrayal of Shakespeare’s Othello in this theater in 1955. After his discharge from the Military, Jones moved to New York, where he attended the American Theatre Wing to further his training and worked as a janitor to earn a living. His first film role was as a young and trim Lt. Lothar Zogg, the B-52 bombardier in Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb in 1964. His first big role came with his portrayal of boxer Jack Jefferson in the film version of the Broadway play The Great White Hope, which was based on the life of boxer Jack Johnson. For his role, Jones was nominated Best Actor by the Academy of Motion Picture Arts and Sciences, making him the second African-American male performer (following Sidney Poitier) to receive a nomination. In 1969, Jones participated in making test films for a proposed children's television series; these shorts, combined with animated segments were the beginnings of the Sesame Street format. The next year, in the early 1970s, James appeared with Diahann Carroll in the film called Claudine. While he has appeared in many roles, he is well known as the voice of Darth Vader in the original Star Wars trilogy. Darth Vader was portrayed in costume by David Prowse in the original trilogy, with Jones dubbing Vader's dialogue in postproduction due to Prowse's strong West Country accent being unsuitable for the role. At his own request, he was originally uncredited for the release of the first two films (he would later be credited for the two in the 1997 re-release). His other voice roles include Mufasa in the 1994 film Disney animated blockbuster The Lion King, and its direct-to-video sequel, The Lion King II: Simba's Pride. He also has done the CNN tagline, \"This is CNN\", as well as \"This is CNN International\", and the Bell Atlantic tagline, \"Bell Atlantic: The heart of communication\". When Bell Atlantic became Verizon, Jones used the tagline greeting of \"Welcome to Verizon\" or \"Verizon 411\" right before a phone call would go through. The opening for NBC's coverage of the 2000 and 2004 Summer Olympics; \"the Big PI in the Sky\" (God) in the computer game Under a Killing Moon; a Claymation film about The Creation; and several guest spots on The Simpsons. In addition to his film and voice over work, Jones is an accomplished stage actor as well; he has won Tony awards in 1969 for The Great White Hope and in 1987 for Fences. Othello, King Lear, Oberon in A Midsummer Night's Dream, Abhorson in Measure for Measure, and Claudius in Hamlet are Shakespearean roles he has played. He received Kennedy Center Honors in 2002. Jones has been married to actress Cecilia Hart since 1982. They have one child, Flynn Earl Jones. He was previously married to American actress/singer Julienne Marie (born March 21, 1933, Toledo, Ohio); they had no children. Jones is a registered Republican.",
         'image': 'https://walter.trakt.tv/images/people/000/000/142/headshots/thumb/1827a15cab.jpg.webp'},
        {'name': 'Will Smith', 'age': 51, 'gender': 'Male',
         'description': "Willard Christopher \"Will\" Smith, Jr. (born September 25, 1968) is an American actor, film producer and pop rapper. He has enjoyed success in music, television and film. In April 2007, Newsweek called him the most powerful actor on the planet. Smith has been nominated for four Golden Globe Awards, two Academy Awards, and has won multiple Grammy Awards. In the late 1980s, Smith achieved modest fame as a rapper under the name The Fresh Prince. In 1990, his popularity increased dramatically when he starred in the popular television series The Fresh Prince of Bel-Air. The show ran for nearly six years (1990–1996) on NBC and has been syndicated consistently on various networks since then. In the mid-1990s, Smith transitioned from television to film, and ultimately starred in numerous blockbuster films that received broad box office success. In fact, he is the only actor in history to have eight consecutive films gross over $100 million in the domestic box office as well as being the only actor to have eight consecutive films in which he starred open at the #1 spot in the domestic box office tally. Fourteen of the 19 fiction films he has acted in have accumulated worldwide gross earnings of over $100 million, and 4 of them took in over $500 million in global box office receipts. His most financially successful films have been Bad Boys, Bad Boys II, Independence Day, Men in Black, Men in Black II, I, Robot, The Pursuit of Happyness, I Am Legend, Hancock, Wild Wild West, Enemy of the State, Shark Tale, Hitch, and Seven Pounds. He also earned critical praise for his performances in Six Degrees of Separation, Ali, and The Pursuit of Happyness, receiving Best Actor Oscar nominations for the latter two.",
         'image': 'https://walter.trakt.tv/images/people/000/008/166/headshots/thumb/eaa201a841.jpg.webp'},
        {'name': 'Mena Massoud', 'age': 23, 'gender': 'Male',
         'description': "Mena Massoud is a Coptic Egyptian-Canadian actor. He was born to Coptic parents in Egypt and raised in Canada. In July 2017, he was cast to play Aladdin in Disney's live-action remake of Aladdin. Massoud was born in Cairo, Egypt to Egyptian Coptic Orthodox Christian parents. He has two older sisters. When he was young he emigrated to Canada. He grew up in Markham, Ontario, where he attended St. Brother André Catholic High School. He is vegan and is the founder of the plant-based food travel show Evolving Vegan.",
         'image': 'https://walter.trakt.tv/images/people/000/904/172/headshots/thumb/36f5278f01.jpg.webp'},
        {'name': 'Kevin Hart', 'age': 41, 'gender': 'Male',
         'description': "Kevin Darnell Hart (born July 6, 1979) is an American stand-up comedian, actor, and producer. Born and raised in Philadelphia, Pennsylvania, Hart began his career by winning several amateur comedy competitions at clubs throughout New England, culminating in his first real break in 2001 when he was cast by Judd Apatow for a recurring role on the TV series Undeclared. The series lasted only one season, but he soon landed other roles in films such as Paper Soldiers (2002), Scary Movie 3 (2003), Soul Plane (2004), In the Mix (2005), and Little Fockers (2010). Hart's comedic reputation continued to grow with the release of his first stand-up album, I'm a Grown Little Man (2008), and performances in the films Think Like a Man (2012), Grudge Match (2013), Ride Along (2014) and its sequel Ride Along 2 (2016), About Last Night (2014), Get Hard (2015), Central Intelligence (2016), The Secret Life of Pets (2016), Captain Underpants: The First Epic Movie (2017), Jumanji: Welcome to the Jungle (2017), and Night School (2018). He also released four more comedy albums, Seriously Funny in 2010, Laugh at My Pain in 2011, Let Me Explain in 2013, and What Now? in 2016. In 2015, Time Magazine named Hart one of the 100 most influential people in the world on the annual Time 100 list. He starred as himself in the lead role of Real Husbands of Hollywood.",
         'image': 'https://walter.trakt.tv/images/people/000/419/127/headshots/thumb/c7547aa3c0.jpg.webp'},
        {'name': 'Martin Lawrence', 'age': 55, 'gender': 'Male',
         'description': "From Wikipedia, the free encyclopedia Martin Fitzgerald Lawrence (born April 16, 1965) is an American actor who was born in Frankfurt am Main, Germany, he's film director, film producer, screenwriter, and comedian. He came to fame during the 1990s, establishing a Hollywood career as a leading actor, most notably the films Bad Boys, Blue Streak, Big Momma's House and Bad Boys II. Lawrence has acted in numerous movie roles and starred in his own television series, Martin, which ran from 1992 to 1997. Description above from the Wikipedia article Martin Lawrence,licensed under CC-BY-SA, full list of contributors on Wikipedia.",
         'image': 'https://walter.trakt.tv/images/people/000/415/131/headshots/thumb/dbac9260ae.jpg.webp'},
    ]
    for a in artists:
        artist = Artist()
        artist.load(a)
        artist.insert()

    movies = [
        {'name': 'Mulan', 'release_date': date(2020, 8, 4),
         'description': 'When the Emperor of China issues a decree that one man per family must serve in the Imperial Chinese Army to defend the country from Huns, Hua Mulan, the eldest daughter of an honored warrior, steps in to take the place of her ailing father. She is spirited, determined and quick on her feet. Disguised as a man by the name of Hua Jun, she is tested every step of the way and must harness her innermost strength and embrace her true potential.',
         'image': 'https://walter.trakt.tv/images/movies/000/218/005/posters/thumb/95f91d6351.jpg.webp'},
        {'name': 'Frozen II', 'release_date': date(2019, 11, 22),
         'description': 'Elsa, Anna, Kristoff and Olaf head far into the forest to learn the truth about an ancient mystery of their kingdom.',
         'image': 'https://walter.trakt.tv/images/movies/000/211/394/posters/thumb/dd9e3d4ce5.jpg.webp'},
        {'name': 'Moana', 'release_date': date(2016, 11, 23),
         'description': "In Ancient Polynesia, when a terrible curse incurred by Maui reaches an impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out the demigod to set things right.",
         'image': 'https://walter.trakt.tv/images/movies/000/175/475/posters/thumb/9545fa634a.jpg.webp'},
        {'name': 'The Avengers', 'release_date': date(2012, 5, 4),
         'description': 'When an unexpected enemy emerges and threatens global safety and security, Nick Fury, director of the international peacekeeping agency known as S.H.I.E.L.D., finds himself in need of a team to pull the world back from the brink of disaster. Spanning the globe, a daring recruitment effort begins!',
         'image': 'https://walter.trakt.tv/images/movies/000/014/701/posters/thumb/293ce7103a.jpg.webp'},
        {'name': 'Avengers: Endgame', 'release_date': date(2019, 4, 26),
         'description': "After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos'actions and restore order to the universe once and for all, no matter what consequences may be in store.",
         'image': 'https://walter.trakt.tv/images/movies/000/191/798/posters/thumb/1700e93125.jpg.webp'},
        {'name': 'Frozen', 'release_date': date(2013, 11, 27),
         'description': "Young princess Anna of Arendelle dreams about finding true love at her sister Elsa’s coronation. Fate takes her on a dangerous journey in an attempt to end the eternal winter that has fallen over the kingdom. She's accompanied by ice delivery man Kristoff, his reindeer Sven, and snowman Olaf. On an adventure where she will find out what friendship, courage, family, and true love really means.",
         'image': 'https://walter.trakt.tv/images/movies/000/077/349/posters/thumb/4913ab7f1b.jpg.webp'},
        {'name': 'The Lion King', 'release_date': date(1994, 6, 23),
         'description': 'A young lion prince is cast out of his pride by his cruel uncle, who claims he killed his father. While the uncle rules with an iron paw, the prince grows up beyond the Savannah, living by a philosophy: No worries for the rest of your days. But when his past comes to haunt him, the young prince must decide his fate: Will he remain an outcast or face his demons and become what he needs to be?',
         'image': 'https://walter.trakt.tv/images/movies/000/004/242/posters/thumb/746f279ac1.jpg.webp'},
        {'name': 'Aladdin', 'release_date': date(2019, 5, 24),
         'description': 'A kindhearted street urchin named Aladdin embarks on a magical adventure after finding a lamp that releases a wisecracking genie while a power-hungry Grand Vizier vies for the same lamp that has the power to make their deepest wishes come true.',
         'image': 'https://walter.trakt.tv/images/movies/000/276/911/posters/thumb/79ae287def.jpg.webp'},
        {'name': 'Jumanji: The Next Level', 'release_date': date(2019, 12, 13),
         'description': 'A kindhearted street urchin named Aladdin embarks on a magical adventure after finding a lamp that releases a wisecracking genie while a power-hungry Grand Vizier vies for the same lamp that has the power to make their deepest wishes come true.',
         'image': 'https://walter.trakt.tv/images/movies/000/360/095/posters/thumb/4ebdd78ffa.jpg.webp'},
        {'name': 'Bad Boys for Life', 'release_date': date(2020, 1, 17),
         'description': 'Marcus and Mike are forced to confront new threats, career changes, and midlife crises as they join the newly created elite team AMMO of the Miami police department to take down the ruthless Armando Armas, the viciousleader of a Miami drug cartel.',
         'image': 'https://walter.trakt.tv/images/movies/000/025/039/posters/thumb/97753b8695.jpg.webp'}
    ]
    for m in movies:
        movie = Movie()
        movie.load(m)
        movie.insert()

    roles = [
        {'movie_id': 1, 'artist_id': 1, 'character': 'Hua Mulan'},
        {'movie_id': 1, 'artist_id': 2, 'character': 'The Emperor'},
        {'movie_id': 2, 'artist_id': 3, 'character': 'Anna'},
        {'movie_id': 2, 'artist_id': 4, 'character': 'Elsa'},
        {'movie_id': 3, 'artist_id': 5, 'character': 'Moana'},
        {'movie_id': 3, 'artist_id': 6, 'character': 'Maui'},
        {'movie_id': 4, 'artist_id': 7, 'character': 'Tony Stark, Iron Man'},
        {'movie_id': 4, 'artist_id': 8, 'character': 'Steve Rogers, Captain America'},
        {'movie_id': 5, 'artist_id': 7, 'character': 'Tony Stark, Iron Man'},
        {'movie_id': 5, 'artist_id': 8, 'character': 'Steve Rogers, Captain America'},
        {'movie_id': 6, 'artist_id': 3, 'character': 'Anna'},
        {'movie_id': 6, 'artist_id': 4, 'character': 'Elsa'},
        {'movie_id': 7, 'artist_id': 9, 'character': 'Simba'},
        {'movie_id': 7, 'artist_id': 10, 'character': 'King Mufasa'},
        {'movie_id': 8, 'artist_id': 11, 'character': 'Genie'},
        {'movie_id': 8, 'artist_id': 12, 'character': 'Aladdin'},
        {'movie_id': 9, 'artist_id': 6, 'character': 'Dr. Smolder Bravestone'},
        {'movie_id': 9, 'artist_id': 13, 'character': "Franklin 'Mouse' Finbar"},
        {'movie_id': 10, 'artist_id': 11, 'character': 'Detective Mike Lowrey'},
        {'movie_id': 10, 'artist_id': 14, 'character': 'Detective Marcus Burnett'}
    ]
    for r in roles:
        role = Role()
        role.load(r)
        role.insert()


class Movie(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    release_date = Column(Date, default=datetime.utcnow())
    description = Column(String)
    image = Column(String)
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, onupdate=datetime.utcnow(), nullable=True)
    roles = db.relationship("Role", backref="movie", lazy='dynamic', cascade="all, delete")

    def __init__(self,
                 movie_id=None,
                 name=None,
                 release_date=None,
                 description=None,
                 image=None):
        self.id = movie_id
        self.name = name
        self.description = description
        self.image = image
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'release_date': self.release_date,
            'cast': sorted([role.format() for role in self.roles.all()], key=lambda x: x.get('artist')),
            'description': self.description,
            'image': self.image
        }

    def load(self, data):
        self.id = data.get('id', None)
        self.name = data.get('name', '')
        self.description = data.get('description', None)
        self.image = data.get('image', None)
        if type(data.get('release_date', None)) is date:
            self.release_date = data.get('release_date', None)
        else:
            try:
                self.release_date = date.fromisoformat(data.get('release_date'))
            except TypeError:
                self.release_date = datetime.strptime(data.get('release_date'), '%Y-%m-%dT%H:%M:%S.%fZ').date()

    def validate(self):
        validation = {'is_valid': True, 'errors': None}
        if not self.name:
            validation['is_valid'] = False
            validation['errors'] = validation['errors'] + ['name'] if validation['errors'] else ['name']
        if not self.release_date:
            validation['is_valid'] = False
            validation['errors'] = validation['errors'] + ['release_date'] if validation['errors'] else ['release_date']
        return validation

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Artist(db.Model):
    __tablename__ = "Artists"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    description = Column(String)
    image = Column(String)
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, onupdate=datetime.utcnow(), nullable=True)
    roles = db.relationship("Role", backref="artist", lazy='dynamic', cascade="all, delete")

    def __init__(self,
                 artist_id=None,
                 name=None,
                 age=None,
                 gender=None,
                 description=None,
                 image=None):
        self.id = artist_id
        self.name = name
        self.description = description
        self.image = image
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': sorted([role.format() for role in self.roles.all()], key=lambda x: x.get('movie')),
            'description': self.description,
            'image': self.image
        }

    def load(self, data):
        self.id = data.get('id', None)
        self.name = data.get('name', '')
        self.age = data.get('age', 0)
        self.gender = data.get('gender', None)
        self.description = data.get('description', None)
        self.image = data.get('image', None)

    def validate(self):
        validation = {'is_valid': True, 'errors': None}
        if not self.name:
            validation['is_valid'] = False
            validation['errors'] = validation['errors'] + ['name'] if validation['errors'] else ['name']
        if not self.age or self.age <= 0:
            validation['is_valid'] = False
            validation['errors'] = validation['errors'] + ['age'] if validation['errors'] else ['age']
        if not self.gender or self.gender.capitalize() not in ['Male', 'Female']:
            validation['is_valid'] = False
            validation['errors'] = validation['errors'] + ['gender'] if validation['errors'] else ['gender']
        return validation

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Role(db.Model):
    __tablename__ = 'Roles'

    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey("Artists.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("Movies.id"), nullable=False)
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, onupdate=datetime.utcnow(), nullable=True)
    character = Column(String)

    def __init__(self,
                 role_id=None,
                 artist_id=None,
                 movie_id=None,
                 character=None):
        self.id = role_id
        self.artist_id = artist_id
        self.movie_id = movie_id
        self.character = character

    def format(self):
        return {
            "id": self.id,
            "artist_id": self.artist_id,
            "artist": Artist.query.get(self.artist_id).name,
            "movie_id": self.movie_id,
            "movie": Movie.query.get(self.movie_id).name,
            "character": self.character
        }

    def load(self, data):
        self.id = data.get('id', None)
        self.artist_id = data.get('artist_id', 0)
        self.movie_id = data.get('movie_id', 0)
        self.character = data.get('character', None)

    def validate(self):
        validation = {'is_valid': True, 'errors': None}
        if not self.artist_id or self.artist_id <= 0:
            validation['is_valid'] = False
            validation['errors'] = validation['errors'] + ['artist_id'] if validation['errors'] else ['artist_id']
        if not self.movie_id or self.movie_id <= 0:
            validation['is_valid'] = False
            validation['errors'] = validation['errors'] + ['movie_id'] if validation['errors'] else ['movie_id']
        if not self.character:
            validation['is_valid'] = False
            validation['errors'] = validation['errors'] + ['character'] if validation['errors'] else ['character']
        return validation

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
