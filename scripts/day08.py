
with open("inputs/day08.txt", "r") as f:
    content = f.readlines()[0]

layers = []
HEIGHT, WIDTH = 6, 25
numbers_per_layer = HEIGHT * WIDTH
num_of_layers = int(len(content) / numbers_per_layer)

for i in range(num_of_layers):
    layer = []
    for j in range(numbers_per_layer):
        layer.append(content[i * numbers_per_layer + j])
    layers.append(layer)

min_layer = sorted(layers, key=lambda layer: sum(
    [1 for pixel in layer if pixel == '0']))[0]

ones = min_layer.count('1')
twos = min_layer.count('2')
# part 1
print(f"{ones} * {twos} = {ones * twos}")

# part 2
# 0 = black, 1 = white, 2 = transparent
image = []
for pixel in range(numbers_per_layer):
    values = [pixels[pixel] for pixels in layers if pixels[pixel] != '2']
    color = values.pop(0)
    if color == "0":
        image.append("_")
    elif color == "1":
        image.append("X")

for i in range(HEIGHT):
    for j in range(WIDTH):
        print(image[i * WIDTH + j], end=" ")
    print()
