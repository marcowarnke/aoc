from math import floor

def get_fuel_for_mass(mass):
    div = int(mass) / 3
    floored = floor(div)
    result = floored - 2
    if result < 0:
        return 0
    return result + get_fuel_for_mass(result)

def main():
    with open("d:/aoc/day01/input.txt", "r") as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    fuel = []

    for mass in content:
        required_fuel = get_fuel_for_mass(mass)
        fuel.append(required_fuel)
    
    print(fuel)
    print(f"Sum: {sum(fuel)}")

if __name__ == "__main__":
    main()