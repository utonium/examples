/*
 * coin_die_toss.cpp
 *
 * Example code to implement a coin toss function and then build a die toss
 * function using the coin_toss function.
 *
 * Further goal of trying out various C++ std library support as much as possible.
 *
 * Copyright 2015 Kevin Cureton, under MIT License
 */


/*
 * Includes
 */
#include <iostream>
#include <map>
#include <random>
#include <string>

/*
 * Globals and prototypes
 */
// Just for grins, make an enum of die types and a lookup table for
// how many sides each has. Granted, the enum values could be used,
// but the goal of this is demo code so go crazy!
enum DICE { d4=4, d6=6, d8=8, d10=10, d12=12, d20=20 };
static const std::map<int, std::string> die_name = { {d4, "d4"}, {d6, "d6"}, {d8, "d8"}, {d10, "d10"}, {d12, "d12"}, {d20, "d20"} };

static const std::string usage = "Please specify one of --demo, --coin-test, or --die-test";

int coin_toss();
int die_toss(enum DICE die);

int demo();
int testCoinToss();
int testDieToss();


/*
 * Main
 */
int main(int argc, char** argv)
{
    if (argc <= 1) {
        std::cout << usage << "\n"; 
        return 1;
    }

    int exit_status = 0;

    std::string first_arg = std::string(argv[1]);

    if (first_arg.compare("--demo") == 0) {
        exit_status = demo();
    } else if (first_arg.compare("--coin-test") == 0) {
        exit_status = testCoinToss();
    } else if (first_arg.compare("--die-test") == 0) {
        exit_status = testDieToss();
    } else {
        std::cout << usage << "\n"; 
    }

    return exit_status;
}

/*
 * Simple function to toss a coin and return 0 or 1.
 */
int coin_toss()
{
    std::random_device device;

    std::default_random_engine dre(device());
    std::uniform_int_distribution<int> dist(0, 1);
    int flip = dist(dre);
    return flip;
}

/*
 * Function to toss a die of a given sidedness.
 *
 * die: the type of die to toss
 */
int die_toss(enum DICE die)
{
    int number_of_coin_tosses = die - 1;

    // Start die_value with 1. If the coin flips all are 'zero',
    // then the die value is 1. With all ones, it would be the
    // max die face since the number of coin tosses is one less
    // than the number of die faces.
    int die_value = 1;
    for (auto idx = 0; idx < number_of_coin_tosses; idx++) {
        auto result = coin_toss();
//        std::cout << "XXX: coin result is " << result << "\n";
        if (result == 1) {
           die_value++;
        } 
    }

    return die_value;
}

/*
 * A quick demo to show flipping of a coin and rolling
 * of a die.
 *
 */
int demo()
{
    std::cout << "Tossing a coin...\n";
    std::cout << "    " << coin_toss() << "\n";
    std::cout << "    " << coin_toss() << "\n";
    std::cout << "    " << coin_toss() << "\n";
    std::cout << "    " << coin_toss() << "\n";
    std::cout << "    " << coin_toss() << "\n";
    std::cout << "    " << coin_toss() << "\n";

    std::cout << "Tossing a die...\n";
    std::cout << "    " << die_name.at(d4) << " value is '" << die_toss(d4) << "'\n";
    std::cout << "    " << die_name.at(d4) << " value is '" << die_toss(d4) << "'\n";
    std::cout << "    " << die_name.at(d4) << " value is '" << die_toss(d4) << "'\n";
    std::cout << "    " << die_name.at(d4) << " value is '" << die_toss(d4) << "'\n";
    std::cout << "    " << die_name.at(d4) << " value is '" << die_toss(d4) << "'\n";
    std::cout << "    " << die_name.at(d4) << " value is '" << die_toss(d4) << "'\n";
    std::cout << "    " << die_name.at(d4) << " value is '" << die_toss(d4) << "'\n";
    std::cout << "    " << die_name.at(d4) << " value is '" << die_toss(d4) << "'\n";

    return 0;
}

/*
 * Test the coinToss function by rolling X times and graphing
 * (in textual output) the distribution of the coin rolls.
 *
 */
int testCoinToss()
{
    static const int number_of_test_flips = 100;

    std::cout << "Running coin toss tests...\n";

    int number_of_heads = 0;
    int number_of_tails = 0;

    for (auto idx=0; idx < number_of_test_flips; idx++) {
        int result = coin_toss();
        if (result == 1) {
            number_of_tails++;
        } else {
            number_of_heads++;
        }
    }

    // Graph the results.
    std::cout << "Heads: ";
    for (auto idx=0; idx < number_of_heads; idx++) {
        std::cout << "*";
    }
    std::cout << "\n";

    std::cout << "Tails: ";
    for (auto idx=0; idx < number_of_tails; idx++) {
        std::cout << "*";
    }
    std::cout << "\n";

    return 0;
}

/*
 * Test the dieToss function by rolling Y times and graphing
 * (in textual output) the distribution of the die rolls.
 *
 */
int testDieToss()
{
    std::cout << "Running die toss tests...\n";
    

    return 0;
}
