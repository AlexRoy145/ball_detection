from detective import Detective


def main() -> int:

    """
    this function sets up and then runs the screen capture responsible for detecting the roulette ball as it passes by
    a portion of the track. This function:
    1. request user input to define the portion of the screen being watched
    2. determines the average brightness of the area when no ball is inside the area
    3. calls the ball detection method while feeding parameters needed to the parent instantiation.
    :return:
    1000 -> function exited by user
    2000 -> function crashed unexpectedly
    """

    detective = Detective()
    detective.setup()
    detective.start()
    return 1001


if __name__ == "__main__":
    main()
