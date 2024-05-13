"""
if a video in cv2.VideoCapture modified, this capture can no longer get frame
therefore, we need a shared memory to tell that video modified
"""

import multiprocessing.managers
_manager = multiprocessing.Manager()
MODIFIED = _manager.list()

SH_FRAME = _manager.list()
