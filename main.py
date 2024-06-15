import random
from pandac.PandaModules import NodePath
from panda3d.core import DepthWriteAttrib

from datetime import datetime

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import TextNode
from direct.showbase.Loader import Loader
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AntialiasAttrib
from panda3d.core import PandaNode
from panda3d.core import TransparencyAttrib
from panda3d.core import loadPrcFileData
from direct.actor.Actor import Actor
import re

loadPrcFileData('', 'win-size 1024 1024')

headHeightDict = {'l': 0.75,
                  's': 0.5}

legHeightDict = {'s': 1.5,
                 'm': 2.0,
                 'l': 2.75}

torsoHeightDict = {'s': 1.5,
                   'm': 1.75,
                   'l': 2.25,
                   'ss': 1.5,
                   'ms': 1.75,
                   'ls': 2.25,
                   'sd': 1.5,
                   'md': 1.75,
                   'ld': 2.25}

# 2024 NOTICE: These dicts used to contain a shirt numbered '99' which was the pink and white striped shirt. I believe
# this was done because it was not in phase_3. I've removed it to make it usable with any copy of the TTR's phase
# files, so that shirt will be absent in this version. The shirt is called newStripes in the phase files, if you want to
# rename it and add it. The same was done with some new shorts, which are named newDenim.

# dict of shirts first, then sleeve
shirts = {'1': '1', '2': '2', '3': '3', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10', '11': '1',
          '12': '1', '13': '1', '14': '16', '15': '15', '16': '16', '17': '1', '18': '1', '19': '19', '20': '20',
          '21': '1', '22': '1', '23': '1'}

shorts = ['1', '2', '4', '5', '6', '7', '8', '9', '10']
boyShorts = ['1', '2', '4', '6', '7', '8', '9', '10']
girlShorts = ['1', '5', '10']
skirts = ['1', '2', '3', '4', '5', '6', '7']

toonBodyScales = {
    'm': 0.60,  # Mouse
    'c': 0.73,  # Cat
    'f': 0.66,  # Duck (Fowl)
    'r': 0.74,  # Rabbit
    'h': 0.85,  # Horse
    'd': 0.85,  # Dog
    'p': 0.68,  # Monkey (Primate)
    'b': 0.85,  # Bear
    's': 0.77,  # Pig (Swine)
    'x': 0.74,  # Croc (x)
    'y': 0.79   # Deer (y)
}

toonSpeciesTypes = {'d': 'dog',  # Dog
                    'c': 'cat',  # Cat
                    'h': 'horse',  # Horse
                    'm': 'mouse',  # Mouse
                    'r': 'rabbit',  # Rabbit
                    'f': 'duck',  # Duck (Fowl)
                    'p': 'monkey',  # Monkey (Primate)
                    'b': 'bear',  # Bear
                    's': 'pig',  # Pig (Swine)
                    'x': 'crocodile',  # Crocodile (x)
                    'y': 'deer',  # Deer (y)
                    }  # + -heads-1000.bam & -lashes

legs = {"s": "phase_3/models/char/tt_a_chr_dgs_shorts_legs_",
        "m": "phase_3/models/char/tt_a_chr_dgm_shorts_legs_",
        "l": "phase_3/models/char/tt_a_chr_dgl_shorts_legs_"}

torsos = {"ss": "phase_3/models/char/tt_a_chr_dgs_shorts_torso_",
          "ms": "phase_3/models/char/tt_a_chr_dgm_shorts_torso_",
          "ls": "phase_3/models/char/tt_a_chr_dgl_shorts_torso_",
          "sd": "phase_3/models/char/tt_a_chr_dgs_skirt_torso_",
          "md": "phase_3/models/char/tt_a_chr_dgm_skirt_torso_",
          "ld": "phase_3/models/char/tt_a_chr_dgl_skirt_torso_"}

toonHeadTypes = ["dls", "dss", "dsl", "dll",  # Dog
                 "cls", "css", "csl", "cll",  # Cat
                 "hls", "hss", "hsl", "hll",  # Horse
                 "mls", "mss",                # Mouse
                 "rls", "rss", "rsl", "rll",  # Rabbit
                 "fls", "fss", "fsl", "fll",  # Duck (Fowl)
                 "pls", "pss", "psl", "pll",  # Monkey (Primate)
                 "bls", "bss", "bsl", "bll",  # Bear
                 "sls", "sss", "ssl", "sll",  # Pig (swine)
                 "xls", "xss", "xsl", "xll",  # Croc (x)
                 "yls", "yss", "ysl", "yll"   # Deer (y)
                 ]

toonColours = [
    [1.00000, 0.35294, 0.44314, 1.0],
    [0.80000, 0.75294, 0.61176, 1.0],
    [0.32549, 0.40784, 0.60000, 1.0],
    [0.41176, 0.64314, 0.28235, 1.0],
    [0.65490, 0.17255, 0.25882, 1.0],
    [0.96471, 0.74902, 0.34902, 1.0],
    [0.98431, 0.53725, 0.39608, 1.0],
    [0.19608, 0.72549, 0.71373, 1.0],
    [0.03922, 0.86275, 0.65490, 1.0],
    [0.63922, 0.85490, 0.67059, 1.0],
    [0.74118, 0.87059, 0.95686, 1.0],
    [0.89020, 0.43922, 0.69804, 1.0],
    [0.89804, 0.61569, 0.90588, 1.0],
    [0.72549, 0.47059, 0.85882, 1.0],
    [0.54510, 0.28235, 0.74902, 1.0],
    [0.45882, 0.37647, 0.82353, 1.0],
    [0.28235, 0.32549, 0.72549, 1.0],
    [0.55686, 0.58824, 0.87451, 1.0],
    [0.18039, 0.52941, 0.72549, 1.0],
    [0.34510, 0.81961, 0.94902, 1.0],
    [0.43137, 0.90588, 0.83529, 1.0],
    [0.30196, 0.96471, 0.40000, 1.0],
    [0.24314, 0.74118, 0.51373, 1.0],
    [0.54902, 0.81961, 0.32157, 1.0],
    [0.85490, 0.93333, 0.49020, 1.0],
    [0.99216, 0.95294, 0.59608, 1.0],
    [0.99216, 0.89804, 0.31765, 1.0],
    [0.98824, 0.47843, 0.16863, 1.0],
    [0.83137, 0.49804, 0.29412, 1.0],
    [0.99216, 0.69412, 0.50980, 1.0],
    [0.63922, 0.35294, 0.27059, 1.0],
    [0.56863, 0.44706, 0.16471, 1.0],
    [0.70980, 0.23529, 0.43529, 1.0],
    [0.86275, 0.40392, 0.41569, 1.0],
    [0.92941, 0.26275, 0.27843, 1.0],
    [0.96471, 0.69020, 0.69804, 1.0]
]

clothesColours = [
    [0.32549, 0.40392, 0.60000, 1.0],
    [0.19608, 0.72157, 0.70980, 1.0],
    [0.03922, 0.85882, 0.65098, 1.0],
    [0.63922, 0.85490, 0.67059, 1.0],
    [0.30196, 0.96471, 0.40000, 1.0],
    [0.92941, 0.36863, 0.81569, 1.0],
    [0.35294, 0.23922, 0.50588, 1.0],
    [0.99608, 0.35294, 0.44314, 1.0],
    [0.80000, 0.75294, 0.60784, 1.0],
    [0.88627, 0.53725, 0.64314, 1.0],
    [0.39216, 0.49804, 0.92549, 1.0],
    [0.23529, 0.57255, 0.98039, 1.0],
    [0.40784, 0.63922, 0.28235, 1.0],
    [0.65490, 0.17255, 0.25490, 1.0],
    [0.96471, 0.74510, 0.34902, 1.0],
    [0.98039, 0.53333, 0.39608, 1.0],
    [0.73725, 0.87059, 0.95294, 1.0],
    [0.88627, 0.43922, 0.69412, 1.0],
    [0.99608, 0.99608, 0.99608, 1.0],
    [0.89412, 0.61569, 0.90196, 1.0],
    [0.72549, 0.47059, 0.85490, 1.0],
    [0.55686, 0.58824, 0.87059, 1.0],
    [0.85098, 0.92941, 0.49020, 1.0],
    [0.99216, 0.95294, 0.59608, 1.0],
    [0.96471, 0.69020, 0.69804, 1.0],
    [0.34510, 0.81569, 0.94902, 1.0],
    [0.43137, 0.90196, 0.83137, 1.0],
    [0.54902, 0.81961, 0.32157, 1.0],
    [0.98824, 0.47843, 0.16863, 1.0],
    [0.82745, 0.49804, 0.29412, 1.0],
    [0.99216, 0.69412, 0.50980, 1.0],
    [0.63922, 0.35294, 0.24706, 1.0],
    [0.56863, 0.44706, 0.16471, 1.0],
    [0.54510, 0.27843, 0.74510, 1.0],
    [0.45882, 0.37647, 0.81961, 1.0],
    [0.28235, 0.32549, 0.72549, 1.0],
    [0.19216, 0.56078, 0.76863, 1.0],
    [0.34510, 0.81569, 0.94902, 1.0],
    [0.43137, 0.90196, 0.83137, 1.0],
    [0.24314, 0.74118, 0.51373, 1.0],
    [0.54902, 0.81961, 0.32157, 1.0],
    [0.99216, 0.89412, 0.31765, 1.0],
    [0.98039, 0.47451, 0.16471, 1.0],
    [0.70588, 0.23137, 0.43529, 1.0],
    [0.85882, 0.40392, 0.41569, 1.0],
    [0.92941, 0.26275, 0.27843, 1.0]
]

hideList = ['**/muzzle-*',
            '**/head-*',
            '**/eyes-*',
            '**/ears-*',
            '**/nose-*',
            '**/antler-*',
            '**/head*',
            '**/joint_pupil*']

class toonDNA:
    def __init__(self):
        self.legs = legs
        self.torsos = torsos
        self.shirts = shirts
        self.boyShorts = boyShorts
        self.toonSpeciesTypes = toonSpeciesTypes
        self.toonHeadTypes = toonHeadTypes
        self.clothesColours = clothesColours
        self.toonColours = toonColours
        self.skirts = skirts
        self.girlShorts = girlShorts
        self.shorts = shorts
        self.toonBodyScales = toonBodyScales
        self.hideList = hideList
        self.title = ['Aunt', 'Baron', 'Big', "Cap'n", 'Captain', 'Chef', 'Chief', 'Coach', 'Colonel', 'Cool', 'Count',
                      'Crazy', 'Daring', 'Deputy', 'Dippy', 'Doctor', 'Dr.', 'Duke', 'Fat', "Good ol'", "Grand ol'",
                      'Granny', 'Grumpy', 'Judge', 'King', 'Lady', 'Little', 'Loopy', 'Loud', 'Lucky', 'Master', 'Miss',
                      'Mister', 'Mr.', 'Noisy', 'Prince', 'Princess', 'Prof.', 'Queen', 'Sergeant', 'Sheriff', 'Silly',
                      'Sir', 'Skinny', 'Super', 'Ugly', 'Weird']
        self.first = ['Albert', 'Alvin', 'Arnold', 'Astro', 'B.D.', 'Banjo', 'Barney', 'Bart', 'Batty', 'Beany',
                      'Bebop', 'Bentley', 'Beppo', 'Bert', 'Billy', 'Bingo', 'Binky', 'Biscuit', 'Bizzy', 'Blinky',
                      'Bob', 'Bonbon', 'Bongo', 'Bonkers', 'Bonnie', 'Bonzo', 'Boo Boo', 'Boots', 'Bouncey', 'Bruce',
                      'Bubbles', 'Bud', 'Buford', 'Bumpy', 'Bunky', 'Buster', 'Butch', 'Buzz', 'C.J.', 'C.W.', 'Candy',
                      'Casper', 'Cecil', 'Chester', 'Chewy', 'Chip', 'Chipper', 'Chirpy', 'Chunky', 'Clancy',
                      'Clarence', 'Cliff', 'Clover', 'Clyde', 'Coconut', 'Comet', 'Cookie', 'Corky', 'Corny', 'Cranky',
                      'Crazy', 'Cricket', 'Crumbly', 'Cuckoo', 'Cuddles', 'Curly', 'Curt', 'Daffodil', 'Daffy',
                      'Daphne', 'Dave', 'Davey', 'David', 'Dee Dee', 'Dinky', 'Dizzy', 'Domino', 'Dot', 'Dottie',
                      'Drippy', 'Droopy', 'Dudley', 'Duke', 'Dusty', 'Dynamite', 'Elmer', 'Ernie', 'Fancy', 'Fangs',
                      'Felix', 'Finn', 'Fireball', 'Flapjack', 'Flappy', 'Fleabag', 'Flint', 'Flip', 'Fluffy',
                      'Freckles', 'Fritz', 'Frizzy', 'Funky', 'Furball', 'Gale', 'Garfield', 'Gary', 'Giggles',
                      'Ginger', 'Goopy', 'Graham', 'Grouchy', 'Gulliver', 'Gus', 'Gwen', 'Hans', 'Harry', 'Harvey',
                      'Hector', 'Huddles', 'Huey', 'J.C.', 'Jack', 'Jacques', 'Jake', 'Jazzy', 'Jellyroll', 'Jester',
                      'Jimmy', 'Johan', 'John', 'Johnny', 'Kippy', 'Kit', 'Knuckles', 'Ladybug', 'Lancelot', 'Lefty',
                      'Leo', 'Leonardo', 'Leroy', 'Lily', 'Lionel', 'Lloyd', 'Lollipop', 'Loony', 'Loopy', 'Louie',
                      'Lucky', 'Mac', 'Marigold', 'Max', 'Maxie', 'Maxwell', 'Melody', 'Mildew', 'Milton', 'Mo Mo',
                      'Moe', 'Monty', 'Murky', 'Ned', 'Nutmeg', 'Nutty', 'Olaf', 'Olive', 'Orville', 'Oscar', 'Oswald',
                      'Ozzie', 'Pancake', 'Peaches', 'Peanut', 'Pearl', 'Penny', 'Peppy', 'Petunia', 'Phil', 'Pickles',
                      'Pierre', 'Pinky', 'Poe', 'Popcorn', 'Poppy', 'Presto', 'Rainbow', 'Raven', 'Reggie', 'Rhubarb',
                      'Ricky', 'Robin', 'Rocco', 'Rodney', 'Roger', 'Rollie', 'Romeo', 'Roscoe', 'Rosie', 'Rover',
                      'Roxy', 'Rusty', 'Sadie', 'Sally', 'Salty', 'Sammie', 'Sandy', 'Scooter', 'Skids', 'Skimpy',
                      'Skip', 'Skipper', 'Skippy', 'Slappy', 'Slippy', 'Slumpy', 'Smirky', 'Snappy', 'Sniffy', 'Snuffy',
                      'Soupy', 'Spiffy', 'Spike', 'Spotty', 'Spunky', 'Squeaky', 'Star', 'Stinky', 'Stripey', 'Stubby',
                      'Taffy', 'Teddy', 'Tex', 'Tom', 'Tricky', 'Trixie', 'Tubby', 'Ursula', 'Valentine', 'Vicky',
                      'Violet', 'Wacko', 'Wacky', 'Waldo', 'Wally', 'Wesley', 'Whiskers', 'Wilbur', 'William', 'Willow',
                      'Winky', 'Yippie', 'Z.Z.', 'Zany', 'Ziggy', 'Zilly', 'Zippety', 'Zippy', 'Zowie', 'von']
        self.last1 = ["Bagel", "Banana", "Bean", "Beanie", "Biggen", "Bizzen", "Blubber", "Boingen", "Bumber", "Bumble",
                      "Bumpen", "Cheezy", "Crinkle", "Crumble", "Crunchen", "Crunchy", "Dandy", "Dingle", "Dizzen",
                      "Dizzy", "Doggen", "Dyno", "Electro", "Feather", "Fiddle", "Fizzle", "Flippen", "Flipper",
                      "Frinkel", "Fumble", "Funny", "Fuzzy", "Giggle", "Glitter", "Google", "Grumble", "Gumdrop",
                      "Huckle", "Hula",
                      "Jabber", "Jeeper", "Jinx", "Jumble", "Kooky", "Lemon", "Loopen", "Mac", "Mc", "Mega", "Mizzen",
                      "Nickel", "Nutty", "Octo", "Paddle", "Pale", "Pedal", "Pepper", "Petal", "Pickle", "Pinker",
                      "Poodle",
                      "Poppen", "Precious", "Pumpkin", "Purple", "Rhino", "Robo", "Rocken", "Ruffle", "Smarty",
                      "Sniffle", "Snorkle", "Sour", "Spackle", "Sparkle", "Squiggle", "Super", "Thunder", "Toppen",
                      "Tricky", "Tweedle",
                      "Twiddle", "Twinkle", "Wacky", "Weasel", "Whisker", "Whistle", "Wild", "Witty", "Wonder",
                      "Wrinkle", "Ziller", "Zippen", "Zooble"]
        self.last2 = ["batch", "bee", "berry", "blabber", "bocker", "boing", "boom", "bop", "bounce", "bouncer",
                      "brains", "bubble", "bumble", "bump", "bumper", "burger", "butter", "chomp", "corn", "crash",
                      "crumbs",
                      "crump", "crunch", "dazzle", "doodle", "dorf", "face", "fidget", "fink", "fish", "flap",
                      "flapper", "flinger", "flip", "flipper", "foot", "fuddy", "fussen", "gabber", "gadget", "gargle",
                      "gloop", "glop",
                      "glow", "goober", "goose", "grin", "grooven", "grump", "hoffer", "hopper", "jinks", "klunk",
                      "knees", "loop", "loose", "marble", "mash", "masher", "melon", "mew", "monkey", "mooch", "mouth",
                      "muddle",
                      "muffin", "mush", "nerd", "noodle", "nose", "nugget", "paws", "phew", "phooey", "pocket", "poof",
                      "pop", "pounce", "pow", "pretzel", "quack", "roni", "scooter", "screech", "smirk", "snooker",
                      "snoop",
                      "snout", "socks", "speed", "son", "song", "sparkles", "speed", "spinner", "splat", "sprinkles",
                      "sprocket", "squeak", "sticks", "stink", "swirl", "tail", "teeth", "thud", "toes", "ton", "toon",
                      "tooth",
                      "twist", "whatsit", "whip", "whirl", "wicket", "wig", "wiggle", "wire", "woof", "zaner", "zap",
                      "zapper", "zilla", "zoom", "zoop"]
        self.nametypes = ['titlefirst', 'first', 'titlelast', 'firstlast', 'last', 'all']

    def get_head_list(self, species):
        """
        Returns a list of head types given the species.
        This list returned is a subset of toonHeadTypes pertaining to only that species.
        """
        head_list = []
        for head in self.toonHeadTypes:
            if head[0] == species:
                head_list.append(head)
        return head_list

    # getHead: Takes species type, returns .bam of said species' head.
    # species must be a letter abbreviation defined in toonSpeciesTypes.
    def get_head(self, species):
        if species == 'd':
            x = ['phase_3/models/char/tt_a_chr_dgm_skirt_head_1000.bam',
                 # this is just here to follow the format of other heads
                 {"neutral": "phase_3/models/char/tt_a_chr_dgs_shorts_head_neutral.bam"},
                 {"dss": 'phase_3/models/char/tt_a_chr_dgm_skirt_head_1000.bam',
                  "dsl": 'phase_3/models/char/tt_a_chr_dgs_shorts_head_1000.bam',
                  "dls": 'phase_3/models/char/tt_a_chr_dgm_shorts_head_1000.bam',
                  "dll": 'phase_3/models/char/tt_a_chr_dgl_shorts_head_1000.bam'}]
            return x
        else:
            x = ["phase_3/models/char/" + self.toonSpeciesTypes[species] + '-heads-1000.bam',
                 {"neutral": "phase_3/models/char/tt_a_chr_dgs_shorts_head_neutral.bam"}]
            return x

    # getLashes: Takes species type, returns .bam of said species' lashes.
    # species must be a two letter abbreviation defined in toonSpeciesTypes.
    def get_lashes(self, species):
        x = 'phase_3/models/char/' + self.toonSpeciesTypes[species] + '-lashes.bam'
        return x

    # getLegs: take leg size (s, m, l) and return list of appropriate legs + neutral animation.
    def get_legs(self, size):
        x = [self.legs[size] + "1000.bam",
             {'neutral': self.legs[size] + "neutral.bam"}]
        return x

    # getTorsoBam: take torso value (see torsoDict) and return list of appropriate torso + neutral animation.
    def get_torso_bam(self, value):
        x = [self.torsos[value] + "1000.bam",
             {'neutral': self.torsos[value] + "neutral.bam"}]
        return x

    # getTorso: take size + gender and translate it into a torso value + input into getTorsoBam
    # size = (s, m, l) gender = (m, f)
    def get_torso(self, size, gender):
        if gender == "m":
            y = size + "s"
        else:
            y = size + "d"
        x = self.get_torso_bam(y)
        return x

    # creates a toon actor from body parts and returns it
    def assemble_toon(self, leg_array, torso_array, head_array):
        toon = Actor({'legs': leg_array[0], 'torso': torso_array[0], 'head': head_array[0]},
                     {'legs': leg_array[1], 'torso': torso_array[1], 'head': head_array[1]})
        toon.attach("torso", "legs", "joint_hips")
        toon.attach("head", "torso", "def_head")
        return toon

    # getShirt: takes in index number and returns a shirt/sleeve combo in a list
    def get_shirt(self, index):
        return ['phase_3/maps/desat_shirt_' + str(index) + ".jpg",
                'phase_3/maps/desat_sleeve_' + str(self.shirts.get(index)) + ".jpg"]

    # getShorts
    def get_shorts(self, index):
        return 'phase_3/maps/desat_shorts_' + index + '.jpg'

    def get_skirt(self, index):
        return 'phase_3/maps/desat_skirt_' + index + '.jpg'

    def apply_shirt(self, actor, shirt_list):
        shirt = loader.loadTexture(shirt_list[0])
        sleeve = loader.loadTexture(shirt_list[1])
        actor.find('**/torso-top').setTexture(shirt, 1)
        actor.find('**/sleeves').setTexture(sleeve, 1)

        return actor

    #applies torso or skirt
    def apply_bottom(self, actor, bottom_text):
        shirt = loader.loadTexture(bottom_text)
        actor.find('**/torso-bot').setTexture(shirt, 1)

        return actor

    def random_name(self):
        l1 = random.choice(self.last1)
        l2 = random.choice(self.last2)
        if l1 == 'Mc' or l1 == 'Mac':
            l2 = l2.capitalize()
        t = random.choice(self.title)
        f = random.choice(self.first)
        nametype = random.choice(self.nametypes)
        if nametype == 'titlefirst' and f == 'von' or nametype == 'first' and f == 'von' or nametype == 'firstlast' and f == 'von':
            f = f.capitalize()
        if nametype == 'titlefirst':
            name = (t + " " + f)
        if nametype == 'first':
            name = f
        if nametype == 'firstlast':
            name = (f + " " + l1 + l2)
        if nametype == 'titlelast':
            name = (t + " " + l1 + l2)
        if nametype == 'last':
            name = (l1 + l2)
        if nametype == 'all':
            name = (t + " " + f + " " + l1 + l2)
        name = re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), name, 1)
        return name

    def random_toon(self):  #RANDOMLY GENERATES TOON
        #first load the body
        possible_sizes = ['l', 'm', 's']
        possible_gender = ['m', 'f']
        species = random.choice(list(toonSpeciesTypes.keys()))
        gender = random.choice(possible_gender)
        sizes = [random.choice(possible_sizes),
                 random.choice(possible_sizes)]  # leg, torso

        full_colour = random.randint(0, 1)
        if full_colour == 1:
            colours = [random.choice(self.toonColours) for _ in
                       range(3)]  # pulls three random colours from toonColours (head,torso,legs)
        else:
            x = random.choice(self.toonColours)
            colours = []
            colours.extend([x] * 3)

        #species, head, snout
        head_size = random.choice(self.get_head_list(species))
        dog_size = head_size  #ignore this, dogs are weird. used later
        head_size_list = []
        for x in head_size:
            head_size_list.append(x)
        head_size = head_size_list

        #this decides whether female toons will have shorts or not
        if gender == "f":
            choice = random.randint(1, 12)
            if choice >= 9:
                torso_gender = "m"
            else:
                torso_gender = "f"
        else:
            torso_gender = "m"

        new_head = ""
        if species == "d":
            x = self.get_head("d")
            x.pop(0)
            x.pop(0)
            new_head = x[0].get(dog_size)
            head = ([new_head, {"neutral": "phase_3/models/char/tt_a_chr_dgs_shorts_head_neutral.bam"}])

            info_list = [self.get_legs(sizes[0]),
                        self.get_torso(sizes[1], torso_gender),
                        head
                        ]
        else:
            info_list = [self.get_legs(sizes[0]),
                        self.get_torso(sizes[1], torso_gender),
                        self.get_head(species)
                        ]

        body = self.assemble_toon(*info_list)

        #animation: neutral
        body.loop('neutral')

        #then load the shirt
        toon_shirt = random.choice(list(self.shirts.keys()))
        shirt = self.get_shirt(toon_shirt)  #gets a random number from the shirts list
        body = self.apply_shirt(body, shirt)

        #load the bottom (skirt/shorts) **TODO**
        if torso_gender == "f":
            torso_text = random.choice(self.skirts)
            self.apply_bottom(body, self.get_skirt(torso_text))
        else:
            if gender == "f":
                torso_text = random.choice(girlShorts)
                self.apply_bottom(body, self.get_shorts(torso_text))
            else:
                torso_text = random.choice(boyShorts)
                self.apply_bottom(body, self.get_shorts(torso_text))

        #colour the toons legs/torso/head
        body.findAllMatches('**/hand*').setColor(1, 1, 1, 1)
        body.findAllMatches('**/head*').setColor(*colours[0])
        if species not in ["p", "d", "h"]:
            body.findAllMatches('**/ear*').setColor(*colours[0])

        body.findAllMatches('**/feet*').setColor(*colours[2])
        body.findAllMatches('**/legs*').setColor(*colours[2])
        body.findAllMatches('**/neck*').setColor(*colours[1])
        body.findAllMatches('**/arms*').setColor(*colours[1])

        #colour the toons clothes
        top_colour = random.choice(self.clothesColours)
        if toon_shirt == "17" or toon_shirt == "13":
            if toon_shirt == "17":
                top_colour = random.choice([[0.99608, 0.99608, 0.99608, 1.0], [0.99216, 0.89412, 0.31765, 1.0],
                                           [0.54902, 0.81961, 0.32157, 1.0],
                                           [0.24314, 0.74118, 0.51373, 1.0], [0.43137, 0.90196, 0.83137, 1.0],
                                           [0.3451, 0.81569, 0.94902, 1.0], [0.19216, 0.56078, 0.76863, 1.0]])
                body.find('**/sleeves').setColor(*top_colour)
            else:
                pass
        else:
            body.find('**/torso-top').setColor(*top_colour)
            body.find('**/sleeves').setColor(*top_colour)

        bot_colour = random.choice(self.clothesColours)
        body.find('**/torso-bot').setColor(*bot_colour)

        #scale the body
        body.setScale(self.toonBodyScales[species])

        #hides all head parts
        for x in self.hideList:
            body.findAllMatches(x).hide()

        #show good parts
        #TODO: i really need to clean this
        if species == "m":
            body.findAllMatches('**/muzzle-short-neutral').show()
        elif species == "y":
            body.findAllMatches('**/head*-short').show()
            body.findAllMatches('**/eyes-short').show()
            body.findAllMatches('**/ears*').show()
            body.findAllMatches('**/**_short').show()

        if species == "r":  #rabbit exclusive
            if head_size[1] == 'l':
                body.findAllMatches('**/*ears-long').show()  #head size for rabbit corresponds to ears, not head
            else:
                body.findAllMatches('**/*ears-short').show()

            if head_size[2] == 'l':
                body.findAllMatches('**/**-long-neutral').show()
                body.findAllMatches('**/*head*long*').show()
                body.findAllMatches('**/**_long').show()
            else:
                body.findAllMatches('**/**-short-neutral').show()
                body.findAllMatches('**/*head*short*').show()
                body.findAllMatches('**/**_short').show()
        elif species == "d":
            body.findAllMatches('**/**').show()
            # this should be done with the head loading as each dog head is individual
        else:
            if head_size[1] == 'l':  #head size = long or short?
                body.findAllMatches('**/**-long').show()
                body.findAllMatches('**/**_long').show()
                body.findAllMatches('**/head-front-long').show()
                body.findAllMatches('**/head-*-long').show()
            else:
                body.findAllMatches('**/**-short').show()
                body.findAllMatches('**/head-front-short').show()
                body.findAllMatches('**/**_short').show()

            if head_size[2] == 'l':  #nose size = long or short?
                body.findAllMatches('**/nose*').hide()
                body.findAllMatches('**/**-long-neutral').show()
                body.findAllMatches('**/nose-long').show()
            else:
                body.findAllMatches('**/nose*').hide()
                body.findAllMatches('**/**-short-neutral').show()
                body.findAllMatches('**/nose-short').show()

        body.findAllMatches('**/boot*').hide()
        body.findAllMatches('**/shoe*').hide()

        #load and apply eyelashes
        if gender == 'f':
            eyelashes = loader.loadModel(modelPath=self.get_lashes(species))
            if head_size[1] == 'l':
                eyes = body.find('**/*eyes-long*')
            else:
                eyes = body.find('**/*eyes-short*')
            eyelashes.findAllMatches('**/*lashes/**').hide()
            eyelashes.findAllMatches('**/*lashes').show()

            if head_size[1] == "l":
                eyelashes.find('**/open-long').show()
            else:
                eyelashes.find('**/open-short').show()
            if species == "d" and "dgs_shorts" in new_head or "dgm_skirt" in new_head:
                #dog eyes are weird and different
                eyelashes.findAllMatches('*open-short*').show()
                eyelashes.findAllMatches('*open-long*').hide()
            eyelashes.show()
            try:
                eyelashes.reparentTo(eyes)
            except:
                eyelashes.reparentTo(body.find('**/*eyes*'))

        # nametag
        width_padding = 0.2
        height_padding = 0.2
        name_bg = (1, 1, 1, 1)
        model = loader.loadModel('phase_3/models/props/panel.bam')
        name_fg = (0.298, 0.298, 0.702, 1)
        word_wrap = 7.5
        display_name = str(self.random_name())
        font = loader.loadFont('phase_3/fonts/ImpressBT.ttf')
        font.setLineHeight(1)
        icon = PandaNode('icon')
        inner_np = PandaNode('nametag')
        inner_np = NodePath.anyPath(inner_np).attachNewNode('nametag_contents')

        # TextNode for the name
        inner_np.attachNewNode(icon)
        text = inner_np.attachNewNode(TextNode('name'), 1)
        text.node().setFont(font)
        text.node().setAlign(TextNode.ACenter)
        text.node().setWordwrap(word_wrap)
        text.node().setText(display_name)
        text.setColor(name_fg)
        text.setTransparency(name_fg[3] < 1.0)

        width, height = text.node().getWidth(), text.node().getHeight()

        text.setY(-0.1)
        text.setAttrib(DepthWriteAttrib.make(0))

        # put panel behind name
        panel = model.copyTo(inner_np, 0)
        panel.setPos((text.node().getLeft() + text.node().getRight()) / 2.0, 0,
                     (text.node().getTop() + text.node().getBottom()) / 2.0)
        panel.setScale(width + width_padding, 1, height + height_padding)
        panel.setColor(name_bg)
        panel.setTransparency(name_bg[3] < 1.0)

        text.setBin("fixed", 1)
        text.setDepthTest(False)
        text.setDepthWrite(False)
        panel.setBin("fixed", 0)
        panel.setDepthTest(False)
        panel.setDepthWrite(False)
        panel.setTransparency(TransparencyAttrib.MAlpha)
        panel.setAlphaScale(.4)
        fullnametag = NodePath('nametag')
        text.reparentTo(fullnametag)
        panel.reparentTo(fullnametag)
        fullnametag.setScale(.25)
        fullnametag.setBillboardPointEye()

        #finally, get nametag scale
        shoulder_height = legHeightDict[sizes[0]] * toonBodyScales[species] + torsoHeightDict[sizes[1]] * \
                         self.toonBodyScales[species]
        body.height = shoulder_height + headHeightDict[head_size[1]] * toonBodyScales[species]

        return body, fullnametag, display_name


DNA = toonDNA()


class Window(ShowBase):
    phrases = ['Hi', 'Heya', 'Hello', 'Howdy', 'Hi there', 'Welcome to Toontown']
    minutes = 2

    def load_toon(self):
        self.body = DNA.random_toon()
        self.body[0].reparentTo(render)
        self.body[1].reparentTo(render)
        self.body[0].setPos(0, .5, 0)
        self.body[1].setPos(self.body[0].getX(), self.body[0].getY(), self.body[0].height + 0.6)
        self.body[0].setH(self.body[0], 30)

    def __init__(self):
        ShowBase.__init__(self)
        render.setAntialias(AntialiasAttrib.MMultisample)
        self.load_toon()

        taskMgr.doMethodLater(0, self.camera_loop, 'cameraFollowTask')
        base.disableMouse()
        self.accept('f', self.reload_toon)
        self.accept('k', self.make_tweet)
        room = loader.loadModel("phase_3/models/makeatoon/tt_m_ara_mat_room.bam")
        shadow = loader.loadModel("phase_3/models/props/drop_shadow.bam")
        room.setH(room, 240)
        room.findAllMatches('**/genderAll/**').hide()
        room.findAllMatches('**/cothAll/**').hide()
        room.findAllMatches('**/colorAll/**').hide()
        room.findAllMatches('**/nameAll/**').hide()
        room.findAllMatches('**/spotlight*').hide()
        room.reparentTo(render)
        shadow.setScale(.4)
        shadow.setTransparency(TransparencyAttrib.MAlpha)
        shadow.setAlphaScale(.7)
        shadow.setPos(self.body[0].getPos())
        shadow.reparentTo(render)
        taskMgr.doMethodLater(0, self.schedule_loop, 'scheduleLoop')

    def camera_loop(self, task):
        base.camera.setPos(0.5, 12, 3.6)
        camera.lookAt(0, -2, 2.5)
        self.graphicsEngine.renderFrame()
        self.screenshot(namePrefix='toon.png', defaultFilename=0, source=None, imageComment='')

    def reload_toon(self):
        self.body[0].delete()
        self.body[1].remove_node()
        self.load_toon()

    def make_tweet(self):
        """This method has had all tweepy functionality removed, so the tweet content is printed and the screenshot is
        simply just saved.
        """
        self.screenshot(namePrefix='toon.png', defaultFilename=0, source=None, imageComment='')
        content = random.choice(self.phrases) + ", " + self.body[2] + "!"
        print(content)
        self.reload_toon()

    def schedule_loop(self, task):
        rest_time = 30
        sleep = rest_time - datetime.now().minute % rest_time
        if sleep == rest_time:
            self.make_tweet()
            sleep = rest_time - datetime.now().minute % rest_time
            taskMgr.doMethodLater(sleep * 60, self.schedule_loop, 'scheduleLoop')
        else:
            taskMgr.doMethodLater(sleep * 60, self.schedule_loop, 'scheduleLoop')


game = Window()
game.run()
input("Press any key to continue...")
