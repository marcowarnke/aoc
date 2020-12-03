#include "pch.h"

#include "adventofcode.h"
#include "day1.h"

int main() {

    std::vector<std::unique_ptr<Day>> days;
    days.reserve(24);
    auto day1 = std::make_unique<Day1>();
    days.push_back(std::move(day1));

    try {
        for (auto &&d : days) {
            d->part1("../input/day1.in");
            d->part2("../input/day1.in");
        }
    } catch (const std::exception &e) {
        std::cout << e.what() << '\n';
    }

    return EXIT_SUCCESS;
}