/*
 * foo.cpp
 *
 * This is a whiteboard for writing code.
 *
 * Copyright 2015 Kevin Cureton, all rights reserved.
 */


/*
 * Includes
 */
#include <iostream>
#include <random>

/*
 * Globals and prototypes
 */
enum DICE { d4, d6, d8, d10, d12, d20 };

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

    if (strcmp(*argv[1], '--demo') == 0) {
        exit_status = demo();
    } else if (strcmp(*argv[1], '--coin-test') == 0) {
        exit_status = testCoinToss();
    } else if (strcmp(*argv[1], '--die-test') == 0) {
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
 * function to toss a die of a given sidedness.
 *
 * die: the type of die to toss
 */
int die_toss(enum DICE die) {

    int die_value = 0;

    int number_of_coin_tosses = 0;

    switch(die) {
        case d4:
            number_of_coin_tosses = 2;
            break;

        case d6:
            number_of_coin_tosses = 3;
            break;

        case d8:
            number_of_coin_tosses = 3;
            break;

        case d10:
            number_of_coin_tosses = 4;
            break;

        case d12:
            number_of_coin_tosses = 4;
            break;

        case d20:
            number_of_coin_tosses = 5;
            break;
    }

    for (auto i = 0; i < number_of_coin_tosses; i++) {

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
