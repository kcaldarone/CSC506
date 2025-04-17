solarSystem = ["Mercury", "Venus", "Earth", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
while True:
    planetTemp = input("Name a planet in the solar system: ")
    for i, value in enumerate(solarSystem):
        if planetTemp.capitalize() == value:
            planet = planetTemp
            break
        
    else:
        print(f"'{planetTemp}' is not a valid planet. Please try again.")
        continue  # restarts the loop
    
    break #to make sure the loop breaks

def numMaker(index):
    place = index + 1
    if place == 1:
        return "1st"
    elif place == 2:
        return "2nd"
    elif place == 3:
        return "3rd"
    else:
        return str(place) + "th"

def linearSearch(array, target):
    for i, value in enumerate(array):
        if value == target:
            print(f" '{planet}' is the " + numMaker(i) + " planet in the solar system!")

linearSearch(solarSystem, planet)