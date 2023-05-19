from threading import Event

import cv2 as cv

import pattern_tracking.proper.utils
from pattern_tracking.proper import constants
from pattern_tracking.proper.GUI import GUI
from pattern_tracking.proper.TemplateTracker import TemplateTracker
from pattern_tracking.proper.VideoReader import VideoReader


class Main:

    def __init__(self):
        self.__halt_event = Event()

        self.__HIGHLIGHTER = TemplateTracker()
        self.__LIVE_FEED = VideoReader(0, False, self.__halt_event)
        self.__LIVE_FEED.run_threaded()

        self.__GUI = GUI(
            constants.WINDOW_NAME,
            self.__LIVE_FEED.grab_frame(block=True)[1].shape,
            self.__HIGHLIGHTER,
            self.__halt_event
        )

    def run(self):
        self.__GUI.start_gui()

        while not self.__halt_event.is_set():
            live_frame = self.__LIVE_FEED.grab_frame(block=True)[1]
            self.__HIGHLIGHTER.update(live_frame, live_frame.copy())
            edited_frame = self.__HIGHLIGHTER.get_edited_frame()
            self.__GUI.change_frame_to_display(edited_frame)
        cv.destroyAllWindows()


if __name__ == '__main__':
    worker = Main()
    worker.run()
