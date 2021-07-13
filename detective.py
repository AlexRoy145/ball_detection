from pynput import mouse


class Detective:
    def __init__(self):
        self.crime_scene = [0, 0]

    def setup(self) -> int:
        """
        this method is used to modify the parameters of the class it should be run before start
        :return:
        1001 -> function completed with no error
        2001 -> function crashed unexpectedly
        """
        print("test active")
        listener = None

        def on_click(x, y, _, pressed):
            if pressed:
                self.crime_scene = ([int(x), int(y)], self.crime_scene[1])
            else:
                self.crime_scene = (self.crime_scene[0], [int(x), int(y)])
                print(self.crime_scene)
                listener.stop()

        with mouse.Listener(
                on_click=on_click
        ) as listener:
            listener.join()

    def start(self) -> int:
        """
        This method takes the class parameters and begins screenshotting the desired area of screen while looking for
        a spike in picture brightness, it can be exited by pressing q when the cv2 screen is selected
        :return:
        1002 -> function exited by user
        2002 -> function crashed unexpectedly
        """