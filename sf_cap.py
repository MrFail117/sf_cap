import random
import matplotlib.pyplot as plt
import time


def displayer(one_n, two_n, three_n):

    # One star, two star, three star
    name_list = [1, 2, 3]

    # Total units in the pool
    pool_n = one_n + two_n + three_n

    # Probabilities of pulling a one star, two star, or a three star
    one_star_prob = one_n / pool_n
    two_star_prob = two_n / pool_n
    three_star_prob = three_n / pool_n

    # Gets the three choices using a weighted random choice
    display = random.choices(name_list,
                             weights=(one_n, two_n, three_n),
                             k=3)

    # Subtract from the approprite integers if they were picked from
    if 1 in display:
        one_n -= 1
    if 2 in display:
        two_n -= 1
    if 3 in display:
        three_n -= 1

    return (display, one_n, two_n, three_n)


def replacer(display, one_n, two_n, three_n, pick):

    #print(one_n, two_n, three_n)
    display_n = display.index(pick)
    replace = random.choices([1,2,3],
                             weights=(one_n, two_n, three_n),
                             k=1)[0]
    display[display_n] = replace
    
    if 1 == replace:
        one_n -= 1
    if 2 == replace:
        two_n -= 1
    if 3 == replace:
        three_n -= 1

    return (display, one_n, two_n, three_n)
    

def refresher(display, one_n, two_n, three_n):

    # Puts the old display back into the pool
    if 1 in display:
        one_n += 1
    if 2 in display:
        two_n += 1
    if 3 in display:
        three_n += 1

    display = random.choices([1,2,3],
                             weights=(one_n, two_n, three_n),
                             k=3)

    # Subtract from the approprite integers if they were picked from
    if 1 in display:
        one_n -= 1
    if 2 in display:
        two_n -= 1
    if 3 in display:
        three_n -= 1

    return (display, one_n, two_n, three_n)
    

def main():

    time_x = time.time()

    # How many times to simulate one whole time cycle
    runs = 100000

    # A success is defined as capturing the three star unit
    success_tracker = 56*[0]

    # Tracks to see if the three star was seen
    seen_three_star = 0

    for i in range(runs):
    
        # Twenty eight days and you can only pick after 12 hours have passed
        # So two picks a day -> 56 picks in 28 days
        time_count = 0
        time_limit = 56

        # Three days for the reset timer to become available once used
        # Always starts on cooldown
        refresh_time = 6

        # One charge lets you pick one
        charges = 14

        # Number of units in each rarity
        one_n = 78
        two_n = 31
        three_n = 1

        # Gets a set of three units to pick from
        (display, one_n, two_n, three_n) = \
                  displayer(one_n, two_n, three_n)

        # Keeps track of whether or not the three star was seen/captured
        capped = False
        seen = False

        # Progress time as long as the three star wasn't capped
        while time_count != time_limit and not capped:

            # Keeps track of whether or not to skip a time unit
            skip = False

            # Keep on using charges if you're not skipping/if you
            # have charges
            while not skip and charges != 0:

                # Always pick the three star if available
                if 3 in display:

                    # Adds to the number of people that saw the three star
                    if seen == False:
                        seen_three_star += 1
                        seen = True

                    # Generates a number between 1 and 100, inclusive
                    success_n = random.randint(1, 100)

                    # Uses a charge to attempt a capture
                    charges -= 1

                    # Capture chance = 25%
                    if success_n > 75:
                        success_tracker[time_count] += 1
                        capped == True
                        skip == True
                    # Failed the capture
                    else:
                        (display, one_n, two_n, three_n) = \
                                  replacer(display, one_n, two_n, three_n, 3)
                        # Adds the three star back into the pool
                        three_n += 1

                # Pick any available one stars
                elif 1 in display:

                    charges -= 1
                    
                    # 100% chance of one star units being captured
                    (display, one_n, two_n, three_n) = \
                                  replacer(display, one_n, two_n, three_n, 1)

                # Two star section
                elif 2 in display:

                    # Refreshes if only two stars are in the display
                    if refresh_time == 0:
                        (display, one_n, two_n, three_n) = \
                                  refresher(display, one_n, two_n, three_n)
                        refresh_time = 6

                    # Arbitrary leftover amount of one stars to start
                    # capturing two stars
                    elif one_n < 1:
                        
                        charges -= 1

                        success_n = random.randint(1, 100)

                        # Capture chance: 50%
                        if success_n > 50:
                            (display, one_n, two_n, three_n) = \
                                  replacer(display, one_n, two_n, three_n, 2)
                        # Failed the capture
                        else:
                            (display, one_n, two_n, three_n) = \
                                  replacer(display, one_n, two_n, three_n, 2)
                            # Back to pool
                            two_n += 1

                    else:
                        # Skip the current time cycle if 
                        skip = True

            #print(one_n, two_n, three_n, time)

            # Increment the time and charges. Count down the
            # refresh timer
            time_count += 1
            refresh_time -= 1
            charges += 1

    # Print the time elapsed
    # ===============================================================
    time_y = time.time()
    time_diff = time_y - time_x
    hours = int(time_diff // 3600)
    time_diff -= hours * 3600
    minutes = int(time_diff // 60)
    time_diff -= minutes * 60
    seconds = int(time_diff // 1)
    print(str(hours) + " hour(s), " + str(minutes) + " minute(s), and " +
          str(seconds) + " second(s) have passed.")
    # ===============================================================

    print(str(seen_three_star/runs*100) + "% of people saw the three star")
    print(str(sum(success_tracker)/runs*100) + "% of people captured " +
          "the three star")
        


if __name__ == '__main__':
    main()
