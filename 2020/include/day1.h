#pragma once

#include "adventofcode.h"

class Day1 : public Day {
public:
    void part1(const std::string &filename) override {
        auto numbers = Reader::read_numbers<int>(filename);

        for (auto a : numbers) {
            for (auto b : numbers) {
                if (a + b == 2020) {
                    std::cout << "part1 result: " << a * b << '\n';
                    return;
                }
            }
        }
    }

    void part2(const std::string &filename) override {
        auto numbers = Reader::read_numbers<int>(filename);

        for (auto a : numbers) {
            for (auto b : numbers) {
                for (auto c : numbers) {
                    if (a + b + c == 2020) {
                        std::cout << "part2 result: " << a * b * c << '\n';
                        return;
                    }
                }
            }
        }
    }
};
