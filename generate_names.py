#!/usr/bin/env python3
"""Generate a large names.csv with hundreds of male, female, and last names."""

male_firsts = [
    "James","Robert","John","Michael","David","William","Richard","Joseph","Thomas","Charles",
    "Christopher","Daniel","Matthew","Anthony","Mark","Donald","Steven","Paul","Andrew","Joshua",
    "Kenneth","Kevin","Brian","George","Timothy","Ronald","Edward","Jason","Jeffrey","Ryan",
    "Jacob","Gary","Nicholas","Eric","Jonathan","Stephen","Larry","Justin","Scott","Brandon",
    "Benjamin","Samuel","Raymond","Gregory","Frank","Alexander","Patrick","Jack","Dennis","Jerry",
    "Tyler","Aaron","Nathan","Henry","Peter","Adam","Douglas","Zachary","Walter","Kyle",
    "Harold","Carl","Arthur","Gerald","Roger","Keith","Jeremy","Lawrence","Terry","Sean",
    "Albert","Joe","Christian","Austin","Jesse","Willie","Billy","Bruce","Bryan","Ralph",
    "Roy","Eugene","Russell","Bobby","Mason","Philip","Louis","Harry","Vincent","Dylan",
    "Randy","Johnny","Howard","Carlos","Martin","Ernest","Todd","Craig",
    "Alan","Shawn","Clarence","Travis","Derek","Marcus","Lance","Darren","Curtis",
    "Victor","Dale","Leonard","Melvin","Ray","Glenn","Miguel","Oscar","Gordon","Joel",
    "Warren","Felix","Mitchell","Cameron","Liam","Noah","Oliver","Elijah","Logan","Aiden",
    "Lucas","Ethan","Sebastian","Owen","Caleb","Wyatt","Luke","Jayden",
    "Gabriel","Leo","Isaiah","Lincoln","Hudson","Mateo","Ezra","Maverick","Miles","Asher",
    "Cooper","Landon","Colton","Emmett","Parker","Sawyer","Declan","Easton","Jaxon","Kai",
    "Nolan","Roman","Silas","Beckett","Weston","Rowan","Brooks","Bennett","Rhett","Atlas",
    "Axel","Adrian","Dominic","Ivan","Xavier","Theodore","Jasper","August","Beau","Archer",
    "Colin","Grant","Knox","Nash","Reid","Sullivan","Tate","Tristan","Zane","Bryce",
    "Caden","Cash","Cruz","Drake","Gage","Hayes","Jace","Lane","Maddox","Phoenix",
    "Quinn","Sterling","Tucker","Wade","Barrett","Callum","Finn","Griffin","Hendrix","Hugo",
    "Emmett","Orion","Ryker","Soren","Blaine","Conrad","Dane","Ellis","Ford","Heath",
    "Irving","Jasper","Keegan","Levi","Marcel","Nico","Otto","Pierce","Quentin","Rocco",
]

female_firsts = [
    "Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen",
    "Lisa","Nancy","Betty","Margaret","Sandra","Ashley","Dorothy","Kimberly","Emily","Donna",
    "Michelle","Carol","Amanda","Melissa","Deborah","Stephanie","Rebecca","Sharon","Laura","Cynthia",
    "Kathleen","Amy","Angela","Shirley","Brenda","Emma","Anna","Pamela","Nicole","Samantha",
    "Katherine","Christine","Debra","Rachel","Carolyn","Janet","Catherine","Maria","Heather","Diane",
    "Ruth","Julie","Olivia","Joyce","Virginia","Victoria","Kelly","Lauren","Christina","Joan",
    "Evelyn","Judith","Megan","Andrea","Cheryl","Hannah","Jacqueline","Martha","Gloria","Teresa",
    "Ann","Sara","Madison","Frances","Kathryn","Janice","Jean","Abigail","Alice","Judy",
    "Sophia","Grace","Avery","Riley","Ella","Scarlett","Aria","Chloe","Layla","Mila",
    "Nora","Lily","Eleanor","Hazel","Violet","Aurora","Savannah","Audrey","Brooklyn","Bella",
    "Claire","Skylar","Lucy","Paisley","Everly","Caroline","Nova","Genesis","Emilia",
    "Kennedy","Maya","Willow","Kinsley","Naomi","Aaliyah","Elena","Ariana","Allison",
    "Gabriella","Madelyn","Cora","Ruby","Eva","Serenity","Autumn","Adeline","Hailey",
    "Gianna","Valentina","Isla","Eliana","Nevaeh","Ivy","Sadie","Piper","Lydia",
    "Alexa","Josephine","Emery","Julia","Delilah","Arianna","Vivian","Kaylee","Sophie","Brielle",
    "Madeline","Peyton","Rylee","Clara","Raelynn","Melanie","Melody","Stella","Reagan","Jade",
    "Liliana","Remi","Athena","Leilani","Mackenzie","Daisy","Harmony","Iris","Margot","Sloane",
    "Diana","Fiona","Gemma","Harlow","June","Lennox","Maeve","Ophelia","Palmer","Teagan",
    "Wren","Zara","Bianca","Camille","Daphne","Eden","Freya","Haven","Jolene","Keira",
    "Lena","Mia","Natalie","Paige","Reese","Sage","Tessa","Uma","Vera","Winter",
    "Celeste","Giselle","Ingrid","Juliette","Kaia","Leona","Mirabelle","Noelle","Opal","Penelope",
]

lasts = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
    "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
    "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
    "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts",
    "Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes",
    "Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper",
    "Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson",
    "Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes",
    "Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez",
    "Powell","Jenkins","Perry","Russell","Sullivan","Bell","Coleman","Butler","Henderson","Barnes",
    "Gonzales","Fisher","Vasquez","Simmons","Graham","Murray","Ford","Castro","Stone","Webb",
    "Freeman","Tucker","Burns","Henry","Spencer","Palmer","Walsh","Gibson","Kennedy","Wells",
    "Chambers","Hawkins","Reynolds","Hart","Hunter","Cole","Holland","Fleming","Grant","Porter",
    "Mason","Brady","Holt","Kelley","Chan","Dunn","Quinn","West","Fox","Owen",
    "Berry","Clayton","Knight","Wagner","Lane","Garrett","Abbott","Bates","Dalton","Erickson",
    "Fritz","Graves","Hale","Irving","Joyce","Kane","Larson","Marsh","Norton","Olson",
    "Page","Ramsey","Shaw","Thorne","Underwood","Vance","Weaver","York","Zimmerman","Bishop",
    "Blake","Burke","Chandler","Drake","Ellis","Frost","Greer","Hayes","Ingram","Jennings",
    "Kline","Lambert","Mercer","Neal","Osborne","Proctor","Rowe","Stafford","Tran","Valencia",
    "Winters","Acosta","Barker","Carey","Dawson","Emerson","Finley","Gaines","Harmon","Ibarra",
    "Mckee","Nava","Ochoa","Pickett","Roach","Shields","Terrell","Villarreal","Whitfield","Yoder",
    "Arias","Booth","Crosby","Dillon","Everett","Faulkner","Gilmore","Haney","Irwin","Jarvis",
]

import os

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "names.csv")

male_set = sorted(set(male_firsts))
female_set = sorted(set(female_firsts))
last_set = sorted(set(lasts))

with open(out, "w") as f:
    f.write("type,name\n")
    for n in male_set:
        f.write(f"male_first,{n}\n")
    for n in female_set:
        f.write(f"female_first,{n}\n")
    for n in last_set:
        f.write(f"last,{n}\n")

total_first = len(male_set) + len(female_set)
total_last = len(last_set)
combos = total_first * total_last * 9990  # with digits 10-9999

print(f"✅ names.csv written to: {out}")
print(f"   {len(male_set)} male first names")
print(f"   {len(female_set)} female first names")
print(f"   {total_last} last names")
print(f"   {combos:,} possible unique email combinations")
