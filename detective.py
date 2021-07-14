import mss
import cv2
from PIL import Image
from platform import system
from pynput import mouse
from random import uniform
from pynput.keyboard import Controller
from time import time


class Detective:
    def __init__(self):
        """
        crime_scene: location of scrrengrab
        screenshot_modifier: if on mac then the screenshot will be too big by a factor of two, this avoids problems
        """
        self.crime_scene = ([0, 0], [0, 0])
        self.screenshot_modifier = 2 if system() == "Darwin" else 1
        self.avg_brightness_of_detection_window = 0

    def select_random_pixel(self) -> tuple:
        """
        This function selects a random pixel in screenshots taken my mss
        :return:
        """
        x_range = self.crime_scene[1][0] - self.crime_scene[0][0]
        x_range = x_range * self.screenshot_modifier
        x_choice = uniform(0, 1)
        x = + x_range * x_choice
        y_range = self.crime_scene[1][1] - self.crime_scene[0][1]
        y_range = y_range * self.screenshot_modifier
        y_choice = uniform(0, 1)
        y = y_range * y_choice
        return x, y

    def setup(self) -> int:
        """
        this method is used to modify the parameters of the class it should be run before start
        :return:
        1001 -> function completed with no error
        2001 -> function crashed unexpectedly
        """

        # setup the detection zone
        print("test active")
        listener = None

        def on_click(x, y, _, pressed):
            if pressed:
                self.crime_scene = ([int(x), int(y)], self.crime_scene[1])
            else:
                self.crime_scene = (self.crime_scene[0], [int(x), int(y)])
                listener.stop()

        with mouse.Listener(
                on_click=on_click
        ) as listener:
            listener.join()

        # take the average brightness of the area when no ball is present
        print("taking average brightness of the area")
        monitor = {
            "top": self.crime_scene[0][1],
            "left": self.crime_scene[0][0],
            "width": self.crime_scene[1][0] - self.crime_scene[0][0],
            "height": self.crime_scene[1][1] - self.crime_scene[0][1]
        }
        with mss.mss() as sct:
            avg_bright_thirty_frame = []
            while len(avg_bright_thirty_frame) < 30:
                avg_bright_one_frame = []
                screenshot = sct.grab(monitor)
                image = Image.frombytes("RGB", screenshot.size, screenshot.bgra)
                image_pixel_count = image.size[0] * image.size[1]
                while len(avg_bright_one_frame)/image_pixel_count < .01:
                    pixel = self.select_random_pixel()
                    red, green, blue = image.getpixel(pixel)
                    avg_bright_one_frame.append(red * 0.2126 + green * 0.7152 + blue * 0.0722)
                avg_bright_one_frame = sum(avg_bright_one_frame) / len(avg_bright_one_frame)
                avg_bright_thirty_frame.append(avg_bright_one_frame)
            self.avg_brightness_of_detection_window = sum(avg_bright_thirty_frame)/len(avg_bright_thirty_frame)


    def start(self) -> int:
        """
        This method takes the class parameters and begins screenshotting the desired area of screen while looking for
        a spike in picture brightness, it can be exited by pressing q when the cv2 screen is selected
        :return:
        1002 -> function exited by user
        2002 -> function crashed unexpectedly
        """
        keyboard = Controller()
        with mss.mss() as sct:
            # TODO look at making a utility to reduce copy pasted code
            # TODO add graceful exit condition
            monitor = {
                "top": self.crime_scene[0][1],
                "left": self.crime_scene[0][0],
                "width": self.crime_scene[1][0] - self.crime_scene[0][0],
                "height": self.crime_scene[1][1] - self.crime_scene[0][1]
            }
            count = 0
            while True:
                screenshot = sct.grab(monitor)
                image = Image.frombytes("RGB", screenshot.size, screenshot.bgra)
                image_pixel_count = image.size[0] * image.size[1]
                average_brighness_of_frame = []
                frame_timer_previous = time()
                while len(average_brighness_of_frame)/image_pixel_count < .3:
                    pixel = self.select_random_pixel()
                    red, green, blue = image.getpixel(pixel)
                    average_brighness_of_frame.append(red * 0.2126 + green * 0.7152 + blue * 0.0722)
                average_brighness_of_frame = sum(average_brighness_of_frame)/len(average_brighness_of_frame)
                frame_timer_current = time()
                print(1/(frame_timer_current-frame_timer_previous))
                frame_timer_previous = frame_timer_current
                if average_brighness_of_frame > self.avg_brightness_of_detection_window + 5:
                    keyboard.press("z")


