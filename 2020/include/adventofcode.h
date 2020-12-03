#pragma once

#include "pch.h"


class Day {
public:
    virtual void part1(const std::string &filename) = 0;

    virtual void part2(const std::string &filename) = 0;
};

class Reader {
public:
    template<typename T>
    [[nodiscard]] static std::vector<T> read_numbers(const std::string &filename) {
        std::vector<T> numbers;
        std::ifstream file{filename};

        if (!file.is_open())
            throw std::runtime_error{"failed to load file from: " + filename};

        T a = 0;
        while (file >> a) {
            numbers.push_back(a);
        }

        return std::move(numbers);
    }
};
