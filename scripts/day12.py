from functools import reduce
from math import gcd

with open("inputs/day12.txt") as f:
    moons = f.readlines()
moons = [''.join(i for i in item if i.isdigit() or i in ",-").split(",") for item in moons]
moons = [tuple(map(lambda x: int(x), inner)) for inner in moons]
vels = [(0, 0, 0) for _ in range(len(moons))]
initial_moons = moons[:]
initial_vels = vels[:]

def apply_gravity(moons, vels):
    for i, moon in enumerate(moons):
        for other in moons:
            vels[i] = tuple(vels[i][field] + (1 if moon[field] < other[field] else 0) for field in range(3))
            vels[i] = tuple(vels[i][field] + (-1 if moon[field] > other[field] else 0) for field in range(3))
    return vels

def apply_velocity(moons, vels):
    for i, moon in enumerate(moons):
        moons[i] = tuple(moon[field] + vels[i][field] for field in range(3))
    return moons

def total_energy(moons, vels):
    energies = [kinetic_energy(vel) * potential_energy(moon) for (moon, vel) in zip(moons, vels)]
    return sum(energies)

def kinetic_energy(vel):
    return sum([abs(i) for i in vel])

def potential_energy(moon):
    return sum([abs(i) for i in moon])

def find_reps(moons, vels, reps, count):
    for i, (moon, vel) in enumerate(zip(moons, vels)):
        reps[i] = tuple(count if moon[field] == initial_moons[i][field] and vel[field] == 0 and reps[i][field] == 0 else reps[i][field] for field in range(3))
    return reps

def lcm(a, b):
    return int(a * b // gcd(a, b))

def lcms(numbers):
    return reduce(lcm, numbers)

reps = [(0, 0, 0) for _ in range(len(moons))]
count = 0
while True:
    count += 1
    vels = apply_gravity(moons, vels)
    moons = apply_velocity(moons, vels)
    reps = find_reps(moons, vels, reps, count)
    if all([item for tup in reps for item in tup]):
        break
print(count)
print(reps)
repepe = set([lcms(rep) for rep in reps for num in rep])
print(repepe)
x =  lcms(repepe)
print(f"x: {x}")