import csv
from collections import Counter
from collections import deque
from utils import CvFpsCalc
import numpy as np
import cv2
from PIL import Image, ImageFont, ImageDraw

import emoji
import mediapipe as mp 

from kazuhito import *
from model import KeyPointClassifier
from funcs import validate_facerect


# デコレーション基底クラス
class BaseDecoration():
    name = "Sample Name"
    description = "Sample Text."
    def decorate(self, input_image):
        return input_image

class MPFaceDecoration(BaseDecoration):
    name = "顔認識デコレーション MediaPipe版"
    description = "MediaPipeを用いて顔を検出し、アイコンを表示します。アイコンに用いる絵文字は自由に指定できます。"
    
    def __init__(self, args=dict()):
        mp_face_detection = mp.solutions.face_detection
        self.face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        
        # 絵文字画像を保存する
        img = Image.new("RGB", (134,126), (0,0,0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./fonts/NotoColorEmoji.ttf", size=109, layout_engine=ImageFont.LAYOUT_RAQM)
        # tick = str(emoji.emojize(':grinning_face:'))
        if 'symbol' in args.keys():
            tick = args['symbol']
        else:
            tick = str(emoji.emojize(':grinning_face:'))
        draw.text((0, 0), tick, fill="#faa2",font=font, embedded_color=True)
        img.save("images/emoji/face_icon.png")
        self.icon = img
        
        self.im_p = None
    
    def decorate(self, input_image: np.ndarray) -> np.ndarray:
        """Pillowを使って、顔画像を貼り付ける
        Args:
            input_image (np.ndarray): OpenCV image
        Returns:
            np.ndarray: OpenCV image
        """
        # 結果を格納する配列
        deco_image = np.zeros_like(input_image)
        # 結果を描画するPillowImage
        self.im_p = Image.fromarray(deco_image)
        
        # 顔検出
        # input_image.flags.writable = False
        # image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(input_image)
        
        # 検出した顔にあれする
        if results.detections:
            for detection in results.detections:
                x = detection.location_data.relative_bounding_box.xmin * self.im_p.width
                y = detection.location_data.relative_bounding_box.ymin * self.im_p.height
                h = detection.location_data.relative_bounding_box.height * self.im_p.height
                w = detection.location_data.relative_bounding_box.width * self.im_p.width
                x, y, h, w = validate_facerect(x, y, h, w)
                resized_icon = self.icon.resize((w, h))
                self.im_p.paste(resized_icon, (x, y))
                
        deco_image = np.array(self.im_p)
        return deco_image
    

class FruitLotteryDecoration(BaseDecoration):
    def __init__(self):
        self.use_brect = True
        # モデルロード #############################################################
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        self.keypoint_classifier = KeyPointClassifier()
        
        # フルーツ決定
        self.random_fruit()
        
        # ラベル読み込み ###########################################################
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [
                row[0] for row in self.keypoint_classifier_labels
            ]

    def decorate(self, input_image: np.ndarray) -> np.ndarray:
        # image = input_image
        input_image.flags.writeable = False
        results = self.hands.process(input_image)
        input_image.flags.writeable = True
        
        # 結果を描画する配列
        deco_image = np.zeros_like(input_image)
        # 結果を描画するPillowImage
        self.im_p = Image.fromarray(deco_image)
                
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # 外接矩形の計算
                brect = calc_bounding_rect(deco_image, hand_landmarks)
                # ランドマークの計算
                landmark_list = calc_landmark_list(deco_image, hand_landmarks)

                # 相対座標・正規化座標への変換
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)
                
                # ハンドサイン分類
                hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == 0:  # パー
                    x, y, h, w = validate_facerect(brect['x'], brect['y'], brect['h'], brect['w'], mode='fruit')
                    resized_fruit = self.fruit.resize((w, h))
                    self.im_p.paste(resized_fruit, (x, y))
                    
                elif hand_sign_id == 1:  # グー
                    self.random_fruit()

                # 描画
                # deco_image = draw_bounding_rect(self.use_brect, deco_image, brect)
                deco_image = draw_landmarks(deco_image, landmark_list)

        deco_image = np.array(self.im_p)
        return deco_image
    
    def random_fruit(self):
        # 絵文字画像を保存する
        img = Image.new("RGB", (134,126), (0,0,0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./fonts/NotoColorEmoji.ttf", size=109, layout_engine=ImageFont.LAYOUT_RAQM)
        # 表示する果物 ランダムで決まる
        fruits = list("🍇🍈🍉🍊🍋🍌🥭🍎🍏🍐🍑🍒🍓🥝🍅🍆🥔🥕🌽🌶🥦🧄🧅🍄")
        tick = fruits[np.random.randint(len(fruits))]
        
        draw.text((0, 0), tick, fill="#faa2",font=font, embedded_color=True)
        img.save("images/emoji/fruit.png")
        self.fruit = img
        
class FingerDrawingDecoration(BaseDecoration):
    def __init__(self):
        self.use_brect = True
        # モデルロード #############################################################
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        self.keypoint_classifier = KeyPointClassifier()
        # self.point_history_classifier = PointHistoryClassifier()
        
        # ラベル読み込み ###########################################################
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [
                row[0] for row in self.keypoint_classifier_labels
            ]

        # 座標履歴 #################################################################
        self.history_length = 64
        self.point_history = deque(maxlen=self.history_length)

        # フィンガージェスチャー履歴 ################################################
        self.finger_gesture_history = deque(maxlen=self.history_length)
        
    def decorate(self, input_image: np.ndarray) -> np.ndarray:
        # image = input_image
        input_image.flags.writeable = False
        results = self.hands.process(input_image)
        input_image.flags.writeable = True
        
        # 結果を描画する配列
        debug_image = np.zeros_like(input_image)
        
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # 外接矩形の計算
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                # ランドマークの計算
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                # 相対座標・正規化座標への変換
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)
                pre_processed_point_history_list = pre_process_point_history(
                    debug_image, self.point_history)

                # ハンドサイン分類
                hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
                if hand_sign_id == 2:  # 指差しサイン
                    self.point_history.append(landmark_list[8])  # 人差指座標
                else:
                    self.point_history.append([0, 0])

                # 描画
                # debug_image = draw_bounding_rect(self.use_brect, debug_image, brect)
                debug_image = draw_landmarks(debug_image, landmark_list)
        else:
            self.point_history.append([0, 0])

        debug_image = draw_point_history(debug_image, self.point_history)
        return debug_image