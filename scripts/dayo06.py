with open("input.txt") as f:
    lines = f.readlines()

unique_planets = []
orbit_map = {}
for line in lines:
    line = line.rstrip("\n")
    [center_planet, orbiter_planet] = line.split(")")
    unique_planets.append(orbiter_planet)
    orbit_map[orbiter_planet] = center_planet

# part 1
sum = 0
for planet in unique_planets:
    center_planet = planet
    while center_planet != "COM":
        center_planet = orbit_map[center_planet]
        sum += 1

print(sum)

# part 2
planet = "SAN"
santas_com_route = []
while planet != "COM":
    santas_com_route.append(planet)
    planet = orbit_map[planet]

planet = "YOU"
my_com_route = []
while planet != "COM":
    my_com_route.append(planet)
    planet = orbit_map[planet]

downsteps = 0
for planet in my_com_route[2:]:
    downsteps += 1
    if planet in santas_com_route:
        index = santas_com_route.index(planet)
        upsteps = index - 1
        print(f"steps needed: {downsteps + upsteps}")
        break
