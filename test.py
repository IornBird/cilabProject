import cv2
import multiprocessing
import time
import numpy as np
# from Realtime_Action_Recognition_master.utils.lib_skeletons import SkeletonDetector


class ReadFromWebcam(object):
    def __init__(self, max_framerate=10):
        ''' A webcam reader class for reading
        Arguments:
            max_framerate {int}: The maximum framerate to read the webcam.
                Default: 10.
        '''
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, max_framerate)
        self._is_stopped = False
        self._imgs_queue = multiprocessing.Queue(maxsize=3)
        self._is_thread_alive = multiprocessing.Value('i', 1)
        self._thread = multiprocessing.Process(target=self._thread_reading_webcam_images)
        self._thread.start()
        self._min_dt = 1.0 / max_framerate
        self._prev_t = time.time() - 1.0 / max_framerate

    def read_image(self):
        dt = time.time() - self._prev_t
        if dt <= self._min_dt:
            time.sleep(self._min_dt - dt)
        self._prev_t = time.time()
        image = self._imgs_queue.get(timeout=10.0)
        return image
    
    def has_image(self):
        return True
    
    def stop(self):
        self._is_thread_alive.value = False
        self.cap.release()
        self._is_stopped = True
        
    def __del__(self):
        if not self._is_stopped:
            self.stop()
            
    def _thread_reading_webcam_images(self):
        while self._is_thread_alive.value:
            ret, frame = self.cap.read()
            if not ret:
                break
            self._imgs_queue.put(frame)
        print("Web camera thread is dead.")
        
class ImageDisplayer(object):
    def __init__(self):
        self._is_stopped = False
        self._imgs_queue = multiprocessing.Queue(maxsize=3)
        self._is_thread_alive = multiprocessing.Value('i', 1)
        self._thread = multiprocessing.Process(target=self._thread_displaying_images)
        self._thread.start()
        
    def display_image(self, image):
        self._imgs_queue.put(image)
        
    def stop(self):
        self._is_thread_alive.value = False
        self._is_stopped = True
        
    def __del__(self):
        if not self._is_stopped:
            self.stop()
            
    def _thread_displaying_images(self):
        while self._is_thread_alive.value:
            image = self._imgs_queue.get()
            cv2.imshow("Webcam", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        print("Image displayer thread is dead.")
        
def test_openpose_on_webcamera():
    webcam_reader = ReadFromWebcam(max_framerate=10)
    img_displayer = ImageDisplayer()
    
    skeleton_detector = SkeletonDetector("mobilenet_thin", "432x368")
    
    import itertools
    for i in itertools.count():
        img = webcam_reader.read_image()
        if img is None:
            break
        print(f"Read {i}th image...")
        
        humans = skeleton_detector.detect(img)
        
        img_disp = img.copy()
        skeleton_detector.draw(img_disp, humans)
        img_displayer.display_image(img_disp)
        
    print("Program ends")
    
def test_save_video_multiprocess():
    video_writer = cv2.VideoWriter("output.mp4", framerate=10)
    
    for i in range(100):
        img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        video_writer.write(img)
        
    print("Program ends")

