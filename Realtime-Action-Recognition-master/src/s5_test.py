#!/usr/bin/env python
# coding: utf-8

'''
Test action recognition on
(1) a video, (2) a folder of images, (3) or web camera.

Input:
    model: model/trained_classifier.pickle

Output:
    result video:    output/${video_name}/video.avi
    result skeleton: output/${video_name}/skeleton_res/XXXXX.txt
    visualization by cv2.imshow() in img_displayer
'''

'''
Example of usage:

(1) Test on video file:
python src/s5_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type video \
    --data_path data_test/exercise.avi \
    --output_folder output
    
(2) Test on a folder of images:
python src/s5_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type folder \
    --data_path data_test/apple/ \
    --output_folder output

(3) Test on web camera:
python src/s5_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type webcam \
    --data_path 0 \
    --output_folder output
    
'''
'''
touch output/FrontKickRight_10/log.txt | \
    \
python src/s5_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type video \
    --data_path /home/training_data/FHD-240FPS/cut/BackHookKickRight/_BackHookKickRight_6.mp4 \
    --output_folder output | \
        \
    tee output/_BackHookKickRight_6/log.txt
'''
'''
python src/s5_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type webcam \
    --data_path 'https://192.168.219.229:8080/video' \
    --output_folder output/webcam
'''

import time
import numpy as np
import cv2
import argparse
if True:  # Include project path
    import sys
    import os
    ROOT = os.path.dirname(os.path.abspath(__file__))+"/../"
    CURR_PATH = os.path.dirname(os.path.abspath(__file__))+"/"
    sys.path.append(ROOT)

    import utils.lib_images_io as lib_images_io
    import utils.lib_plot as lib_plot
    import utils.lib_commons as lib_commons
    from utils.lib_openpose import SkeletonDetector
    from utils.lib_tracker import Tracker
    from utils.lib_tracker import Tracker
    from utils.lib_classifier import ClassifierOnlineTest
    from utils.lib_classifier import *  # Import all sklearn related libraries
    
    
    # openpose packages
    sys.path.append(ROOT + "src/githubs/tf-pose-estimation")
    from tf_pose import common


def par(path):  # Pre-Append ROOT to the path if it's not absolute
    return ROOT + path if (path and path[0] != "/") else path


# -- Command-line input


def get_command_line_arguments():

    def parse_args():
        parser = argparse.ArgumentParser(
            description="Test action recognition on \n"
            "(1) a video, (2) a folder of images, (3) or web camera.")
        parser.add_argument("-m", "--model_path", required=False,
                            default='model/trained_classifier.pickle')
        parser.add_argument("-t", "--data_type", required=False, default='webcam',
                            choices=["video", "folder", "webcam"])
        parser.add_argument("-p", "--data_path", required=False, default="",
                            help="path to a video file, or images folder, or webcam. \n"
                            "For video and folder, the path should be "
                            "absolute or relative to this project's root. "
                            "For webcam, either input an index or device name. ")
        parser.add_argument("-o", "--output_folder", required=False, default='output/',
                            help="Which folder to save result to.")

        args = parser.parse_args()
        return args
    args = parse_args()
    if args.data_type != "webcam" and args.data_path and args.data_path[0] != "/":
        # If the path is not absolute, then its relative to the ROOT.
        args.data_path = ROOT + args.data_path
    return args


def get_dst_folder_name(src_data_type, src_data_path):
    ''' Compute a output folder name based on data_type and data_path.
        The final output of this script looks like this:
            DST_FOLDER/folder_name/vidoe.avi
            DST_FOLDER/folder_name/skeletons/XXXXX.txt
    '''

    assert (src_data_type in ["video", "folder", "webcam"])

    if src_data_type == "video":  # /root/data/video.avi --> video
        folder_name = os.path.basename(src_data_path).split(".")[-2]

    elif src_data_type == "folder":  # /root/data/video/ --> video
        folder_name = src_data_path.rstrip("/").split("/")[-1]

    elif src_data_type == "webcam":
        # month-day-hour-minute-seconds, e.g.: 02-26-15-51-12
        folder_name = lib_commons.get_time_string()

    return folder_name


args = get_command_line_arguments()

SRC_DATA_TYPE = args.data_type
SRC_DATA_PATH = args.data_path
SRC_MODEL_PATH = args.model_path

DST_FOLDER_NAME = get_dst_folder_name(SRC_DATA_TYPE, SRC_DATA_PATH)

# -- Settings

cfg_all = lib_commons.read_yaml(ROOT + "config/config.yaml")
cfg = cfg_all["s5_test.py"]

CLASSES = np.array(cfg_all["classes"])
SKELETON_FILENAME_FORMAT = cfg_all["skeleton_filename_format"]

# Action recognition: number of frames used to extract features.
WINDOW_SIZE = int(cfg_all["features"]["window_size"])

# Output folder
DST_FOLDER = args.output_folder + "/" + DST_FOLDER_NAME + "/"
DST_SKELETON_FOLDER_NAME = cfg["output"]["skeleton_folder_name"]
# DST_VIDEO_NAME = cfg["output"]["video_name"]
DST_VIDEO_NAME = DST_FOLDER_NAME + ".avi"
# framerate of output video.avi
DST_VIDEO_FPS = float(cfg["output"]["video_fps"])


# Video setttings

# If data_type is webcam, set the max frame rate.
SRC_WEBCAM_MAX_FPS = float(cfg["settings"]["source"]
                           ["webcam_max_framerate"])

# If data_type is video, set the sampling interval.
# For example, if it's 3, then the video will be read 3 times faster.
SRC_VIDEO_SAMPLE_INTERVAL = int(cfg["settings"]["source"]
                                ["video_sample_interval"])

# Openpose settings
OPENPOSE_MODEL = cfg["settings"]["openpose"]["model"]
OPENPOSE_IMG_SIZE = cfg["settings"]["openpose"]["img_size"]

# Display settings
img_disp_desired_rows = int(cfg["settings"]["display"]["desired_rows"])


# -- Function


def select_images_loader(src_data_type, src_data_path):
    if src_data_type == "video":
        images_loader = lib_images_io.ReadFromVideo(
            src_data_path,
            sample_interval=SRC_VIDEO_SAMPLE_INTERVAL)

    elif src_data_type == "folder":
        images_loader = lib_images_io.ReadFromFolder(
            folder_path=src_data_path)

    elif src_data_type == "webcam":
        if src_data_path == "":
            webcam_idx = 0
        elif src_data_path.isdigit():
            webcam_idx = int(src_data_path)
        else:
            webcam_idx = src_data_path
        images_loader = lib_images_io.ReadFromWebcam(
            SRC_WEBCAM_MAX_FPS, webcam_idx)
    return images_loader


class MultiPersonClassifier(object):
    ''' This is a wrapper around ClassifierOnlineTest
        for recognizing actions of multiple people.
    '''

    def __init__(self, model_path, classes):

        self.dict_id2clf = {}  # human id -> classifier of this person

        # Define a function for creating classifier for new people.
        self._create_classifier = lambda human_id: ClassifierOnlineTest(
            model_path, classes, WINDOW_SIZE, human_id)

    def classify(self, dict_id2skeleton):
        ''' Classify the action type of each skeleton in dict_id2skeleton '''

        # Clear people not in view
        old_ids = set(self.dict_id2clf)
        cur_ids = set(dict_id2skeleton)
        humans_not_in_view = list(old_ids - cur_ids)
        for human in humans_not_in_view:
            del self.dict_id2clf[human]

        # Predict each person's action
        id2label = {}
        for id, skeleton in dict_id2skeleton.items():

            if id not in self.dict_id2clf:  # add this new person
                self.dict_id2clf[id] = self._create_classifier(id)

            classifier = self.dict_id2clf[id]
            id2label[id] = classifier.predict(skeleton)  # predict label
            # print("\n\nPredicting label for human{}".format(id))
            # print("  skeleton: {}".format(skeleton))
            # print("  label: {}".format(id2label[id]))

        return id2label

    def get_classifier(self, id):
        ''' Get the classifier based on the person id.
        Arguments:
            id {int or "min"}
        '''
        if len(self.dict_id2clf) == 0:
            return None
        if id == 'min':
            id = min(self.dict_id2clf.keys())
        return self.dict_id2clf[id]


def remove_skeletons_with_few_joints(skeletons):
    ''' Remove bad skeletons before sending to the tracker '''
    good_skeletons = []
    for skeleton in skeletons:
        px = skeleton[2:2+13*2:2]
        py = skeleton[3:2+13*2:2]
        num_valid_joints = len([x for x in px if x != 0])
        num_leg_joints = len([x for x in px[-6:] if x != 0])
        total_size = max(py) - min(py)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # IF JOINTS ARE MISSING, TRY CHANGING THESE VALUES:
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if num_valid_joints >= 5 and total_size >= 0.1 and num_leg_joints >= 0:
            # add this skeleton only when all requirements are satisfied
            good_skeletons.append(skeleton)
    return good_skeletons


def draw_result_img(img_disp, ith_img, humans, dict_id2skeleton,
                    skeleton_detector, multiperson_classifier,
                    dict_id2label, scale_h=1.0):
    ''' Draw skeletons, labels, and prediction scores onto image for display '''

    # Resize to a proper size for display
    r, c = img_disp.shape[0:2]
    desired_cols = int(1.0 * c * (img_disp_desired_rows / r))
    img_disp = cv2.resize(img_disp,
                          dsize=(desired_cols, img_disp_desired_rows))

    # Draw all people's skeleton
    # skeleton_detector.draw(img_disp, humans, draw_pta=True)
    skeleton_detector.draw(img_disp, humans)

    # Draw bounding box and label of each person
    if len(dict_id2skeleton):
        for id, label in dict_id2label.items():
            skeleton = dict_id2skeleton[id]
            # scale the y data back to original
            skeleton[1::2] = skeleton[1::2] / scale_h
            # print("Drawing skeleton: ", dict_id2skeleton[id], "with label:", label, ".")
            lib_plot.draw_action_result(img_disp, id, skeleton, label)

    # Add blank to the left for displaying prediction scores of each class
    img_disp = lib_plot.add_white_region_to_left_of_image(img_disp)

    cv2.putText(img_disp, "Frame:" + str(ith_img),
                (20, 20), fontScale=1.5, fontFace=cv2.FONT_HERSHEY_PLAIN,
                color=(0, 0, 0), thickness=2)

    # Draw predicting score for only 1 person
    if len(dict_id2skeleton):
        classifier_of_a_person = multiperson_classifier.get_classifier(
            id='min')
        classifier_of_a_person.draw_scores_onto_image(img_disp)
    return img_disp


def get_the_skeleton_data_to_save_to_disk(dict_id2skeleton, dict_id2label):
    '''
    In each image, for each skeleton, save the:
        human_id, label, and the skeleton positions of length 18*2.
    So the total length per row is 2+36=38
    '''
    skels_to_save = []
    for human_id in dict_id2skeleton.keys():
        label = dict_id2label[human_id]
        skeleton = dict_id2skeleton[human_id]
        skels_to_save.append([[human_id, label] + skeleton.tolist()])
    return skels_to_save


def analyze_log(log_path, ith_img):
    ''' Analyze the log file '''

    predicted_label_cnt = dict.fromkeys(list(CLASSES) + ['None'], 0)

    with open(log_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith('predicted label is :'):
                continue
            words = line.split()
            # print(words)
            if words[-1] == ':':
                predicted_label_cnt['None'] += 1
            else:
                predicted_label_cnt[words[-1]] += 1
    print(f'\n\ntotal frames: {ith_img}')
    print(f'🟢 Predicted label count: {predicted_label_cnt}')


def init_log(log_path):
    ''' Initialize log file '''
    dst_folder = os.path.dirname(log_path)
    if not os.path.isdir(dst_folder):
        os.makedirs(dst_folder, exist_ok=True)
    with open(log_path, "w") as f:  # create log file
        pass


def append_log_and_print(log_path, text):
    ''' Append text to log file '''
    with open(log_path, "a") as f:
        f.write(text + "\n")
    print(text)


def is_in_area(attack_point, hit_area, threshold=0.5):
    ''' 
    Check if a attack point is in the pointing area 
    attack_point: (x, y)
    hit_area: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    '''
    if len(hit_area) != 4:
        return False
    x1, y1 = hit_area[0]
    x2, y2 = hit_area[1]
    x3, y3 = hit_area[2]
    x4, y4 = hit_area[3]
    x1 -= threshold
    x2 += threshold
    y1 -= threshold
    y4 += threshold
    if x1 <= attack_point[0] <= x2 and y1 <= attack_point[1] <= y4:
        return True
    return False

def is_hit(attack_point, hit_area, threshold=0.5):
    ''' 
    Check if a person hit the pointing area 
    attack_point: (x, y)
    hit_area: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    '''
    if len(hit_area) != 4:
        return False
    if is_in_area(attack_point, hit_area, threshold):
        return True
    return False    


def is_hit_pt(attack_point, hit_point, threshold=0.5):
    return np.linalg.norm(attack_point - hit_point) < threshold


def check_pointing_area(img_w, img_h, humans, dict_id2skeleton):
    ''' 
    Check if a person hit the pointing area 
    
    '''
    pt_list = []
    ret_list = []
    atk_name = ['r_wrist', 'l_wrist', 'r_andke', 'l_andke']
    for human_id, human in enumerate(humans):
        r_wrist = human.get_part_point(common.CocoPart.RWrist)
        l_wrist = human.get_part_point(common.CocoPart.LWrist)
        r_andke = human.get_part_point(common.CocoPart.RAnkle)
        l_andke = human.get_part_point(common.CocoPart.LAnkle)
        atk_pt = [r_wrist, l_wrist, r_andke, l_andke]
        hit_area = []
        for h_id, h in enumerate(humans):
            if h == human:
                continue
            hit_area.append([h_id, h.get_face_box_new(img_w, img_h), 
                             h.get_body_box_new(img_w, img_h)])

        for i, pt in enumerate(atk_pt):
            if pt is None:
                continue
            for j, area in enumerate(hit_area):
                if is_hit(pt, area[1]):
                    pt_list.append((human_id, atk_name[i], 'head'))
                if is_hit(pt, area[2]):
                    pt_list.append((human_id, atk_name[i], 'body'))

        if atk_pt[0] is not None and atk_pt[1] is not None:
            ret_list.append([human_id, is_hit_pt(atk_pt[0], atk_pt[1])])
    return pt_list


def s5_test_main(model_path=SRC_MODEL_PATH, data_type=SRC_DATA_TYPE, data_path=SRC_DATA_PATH, output_folder=args.output_folder, img_displayer_on=False):
    start = time.time()

    # img_displayer_on = True

    dst_folder_name = get_dst_folder_name(data_type, data_path)
    dst_folder = output_folder + "/" + dst_folder_name + "/"
    DST_VIDEO_NAME = dst_folder_name + ".avi"

    # log_path = DST_FOLDER + "log.txt"
    log_path = os.path.join(dst_folder, "log.txt")
    init_log(log_path)
    predicted_label_cnt = [dict.fromkeys(list(CLASSES) + ['None'], 0)] * 2
    append_log_and_print(log_path, f"🟢 Start processing {data_path} ...")

    # -- Detector, tracker, classifier

    skeleton_detector = SkeletonDetector(OPENPOSE_MODEL, OPENPOSE_IMG_SIZE)

    multiperson_tracker = Tracker()

    multiperson_classifier = MultiPersonClassifier(model_path, CLASSES)

    # -- Image reader and 
    images_loader = select_images_loader(data_type, data_path)
    print(f'{data_type=}\n{data_path=}\n{images_loader=}')
    append_log_and_print(log_path, '🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴')
    if img_displayer_on:
        img_displayer = lib_images_io.ImageDisplayer()

    # -- Init output

    # output folder
    # os.makedirs(DST_FOLDER, exist_ok=True)
    os.makedirs(dst_folder, exist_ok=True)
    # os.makedirs(DST_FOLDER + DST_SKELETON_FOLDER_NAME, exist_ok=True)
    os.makedirs(dst_folder + DST_SKELETON_FOLDER_NAME, exist_ok=True)

    # video writer
    DST_VIDEO_FPS = 30
    video_writer = lib_images_io.VideoWriter(
        dst_folder + DST_VIDEO_NAME, DST_VIDEO_FPS)  # video_writer = lib_images_io.VideoWriter(DST_FOLDER + DST_VIDEO_NAME, DST_VIDEO_FPS)

    # -- Read images and process
    try:
        ith_img = -1 + 1
        while images_loader.has_image():

            # -- Read image
            img = images_loader.read_image()
            if img is None and data_type != 'webcam':
                append_log_and_print(log_path, f"🔴 Error: {img} is None")
                break
            if img_displayer_on and cv2.waitKey(1) & 0xFF == ord('q'):
                break

            ith_img += 1
            img_disp = img.copy()
            append_log_and_print(
                log_path, f"\nProcessing {ith_img}th image ...")

            # -- Detect skeletons
            humans = skeleton_detector.detect(img)
            skeletons, scale_h = skeleton_detector.humans_to_skels_list(humans)
            skeletons = remove_skeletons_with_few_joints(skeletons)

            # -- Track people
            dict_id2skeleton = multiperson_tracker.track(
                skeletons)  # int id -> np.array() skeleton

            # -- Recognize action of each person
            if len(dict_id2skeleton):
                dict_id2label = multiperson_classifier.classify(
                    dict_id2skeleton)
            else:
                dict_id2label = {}

            # -- Draw
            img_disp = draw_result_img(img_disp, ith_img, humans, dict_id2skeleton,
                                       skeleton_detector, multiperson_classifier, dict_id2label, scale_h)

            # -- Check if a person hit the pointing area
            # (contestant_id, action, hit_area)
            pt_list = check_pointing_area(
                img.shape[1], img.shape[0], humans, dict_id2skeleton)
            if len(pt_list):
                append_log_and_print(log_path, f'\n🟢 {pt_list=}\n')
            else:
                append_log_and_print(log_path, f'\n🟡 {pt_list=} No one hit the pointing area\n')

            # Print label of a person
            if len(dict_id2skeleton):
                append_log_and_print(log_path, f'{dict_id2label=}\n')
                ccnt = 0
                for i in dict_id2label.keys():
                    ccnt += 1
                    if ccnt > 2:
                        break
                    append_log_and_print(log_path, f'frame {ith_img} skeleton {i} label: {dict_id2label[i]}')
                    # dict_id2label[i] is empty string
                    if len(dict_id2label[i]) == 0:
                        predicted_label_cnt[ccnt-1]['None'] += 1
                    else:
                        predicted_label_cnt[ccnt-1][dict_id2label[i]] += 1

            # -- Display image, and write to video.avi
            append_log_and_print(log_path, '🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴\n')
            if img_displayer_on:
                img_displayer.display(img_disp, wait_key_ms=1)
            if data_type != 'webcam':
                video_writer.write(img_disp)
            else:
                video_writer.write(img_disp)

            # -- Get skeleton data and save to file
            skels_to_save = get_the_skeleton_data_to_save_to_disk(
                dict_id2skeleton, dict_id2label)
            lib_commons.save_listlist(
                dst_folder + DST_SKELETON_FOLDER_NAME +
                SKELETON_FILENAME_FORMAT.format(ith_img),
                skels_to_save)  # lib_commons.save_listlist(DST_FOLDER + DST_SKELETON_FOLDER_NAME + SKELETON_FILENAME_FORMAT.format(ith_img), skels_to_save)
        # end while
    finally:
        video_writer.stop()
        # analyze_log(log_path)
        append_log_and_print(log_path, "Program ends")
        end = time.time()
        append_log_and_print(
            log_path, f"🟢 Time elapsed: {end - start} seconds")
        append_log_and_print(log_path, 'time spent: ' +
                             time.strftime("%H:%M:%S", time.gmtime(end-start)))
        append_log_and_print(
            log_path, f"🟢 Predicted label count: {predicted_label_cnt}")
        append_log_and_print(log_path, f'Predicted label percentage: ')
        for ith_human, plabel_cnt in enumerate(predicted_label_cnt):
            append_log_and_print(log_path, f'human {ith_human} total frames: {ith_img+1}')
            for label, count in plabel_cnt.items():
                append_log_and_print(
                    log_path, f'{label}: {count/(ith_img+1)*100:.2f}%')


# -- Main
if __name__ == "__main__":
    s5_test_main(SRC_MODEL_PATH, SRC_DATA_TYPE, SRC_DATA_PATH,
                 args.output_folder, img_displayer_on=False)


r'''
touch output/video-11m14s-31-x3htXTI7nDI/log.txt | \
    \
python src/s5_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type video \
    --data_path /home/training_data/web/'313 R16 M +80kg CHN MENG M CRO SAPINA I'/video-11m14s-31-x3htXTI7nDI.mp4 \
    --output_folder output | \
        \
    tee output/video-11m14s-31-x3htXTI7nDI/log.txt
'''
r'''
touch output/AxeKickLeft_1/log.txt | \
    \
python src/s5_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type video \
    --data_path /home/training_data/FHD-240FPS/cut/AxeKickLeft/AxeKickLeft_1.mp4 \
    --output_folder output | \
        \
    tee output/AxeKickLeft_1/log.txt
'''
r'''
python src/s5_test.py \
    --model_path model/trained_classifier.pickle \
    --data_type webcam \
    --data_path 'https://192.168.219.229:8080/video' \
    --output_folder output/webcam
'''
r'''
python src/s5_test.py `
    --model_path model/trained_classifier.pickle `
    --data_type video `
    --data_path "..\..\Taekwondo_media\self_rec\FHD-240FPS\cut\AxeKickLeft\AxeKickLeft_1.mp4" `
    --output_folder output
'''
r'''
python src/s5_test.py `
    --model_path model/trained_classifier.pickle `
    --data_type video `
    --data_path ..\..\Taekwondo_media\video\video-11m14s-31-x3htXTI7nDI.mp4 `
    --output_folder output
'''
r'''
python src/s5_test.py `
    --model_path model/trained_classifier.pickle `
    --data_type webcam `
    --data_path 'https://192.168.0.12:8080/video' `
    --output_folder output/webcam
'''
