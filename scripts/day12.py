from functools import reduce
from math import gcd


def get_moons():
    with open("inputs/day12.txt") as f:
        moons = f.readlines()
    moons = [''.join(i for i in item if i.isdigit() or i in ",-").split(",")
             for item in moons]
    return [tuple(map(lambda x: int(x), inner)) for inner in moons]


def apply_gravity(moon, moons, velocity):
    for other in moons:
        velocity = tuple(velocity[field] + (1 if moon[field]
                                            < other[field] else 0) for field in range(3))
        velocity = tuple(velocity[field] + (-1 if moon[field]
                                            > other[field] else 0) for field in range(3))
    return velocity


def apply_velocity(moon, velocity):
    return tuple(moon[field] + velocity[field] for field in range(3))


def total_energy(moons, vels):
    energies = [kinetic_energy(vel) * potential_energy(moon)
                for (moon, vel) in zip(moons, vels)]
    return sum(energies)


def kinetic_energy(vel):
    return sum([abs(i) for i in vel])


def potential_energy(moon):
    return sum([abs(i) for i in moon])


def _lcm(a, b):
    return int(a * b // gcd(a, b))


def lcm(lst):
    return reduce(_lcm, lst)


def simulate(moons):
    velocities = [(0, 0, 0) for _ in moons]
    n = 0
    while True:
        for i, moon in enumerate(moons):
            velocities[i] = apply_gravity(moon, moons, velocities[i])
        for i, velocity in enumerate(velocities):
            moons[i] = apply_velocity(moons[i], velocity)
        yield list(zip(moons, velocities))


if __name__ == "__main__":
    moons = get_moons()
    seenX, seenY, seenZ = set(), set(), set()

    for state in simulate(moons):
        stateX = tuple((m[0], v[0]) for m, v in state)
        stateY = tuple((m[1], v[1]) for m, v in state)
        stateZ = tuple((m[2], v[2]) for m, v in state)
        if stateX in seenX and stateY in seenY and stateZ in seenZ:
            break
        seenX.add(stateX)
        seenY.add(stateY)
        seenZ.add(stateZ)

    print(lcm([len(seenX), len(seenY), len(seenZ)]))
