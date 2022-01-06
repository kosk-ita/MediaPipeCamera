import numpy as np

from MyFilters import *
from MyDecorations import *

class CameraModel():
    def __init__(self, args=None):
        self.filter = BaseFilter()
        self.decorations = []  # 適用するデコレーションのリスト
        # フィルター
        self.filter_dict = {
            'None': BaseFilter,
            'LightSepia': LightSepiaFilter,
            'Sepia': SepiaFilter,
            'ColorShift': HSVFilter,
            'Postarization': PostarizationFilter,
        }
        # デコレーション
        self.decoration_dict = {
            'Face MediaPipe': MPFaceDecoration(),
            'Fruits Lottery': FruitLotteryDecoration(),
            'Finger Drawing': FingerDrawingDecoration(),
        }
        
    def process(self, input_image: np.ndarray) -> np.ndarray:
        """画像を受け取り、フィルタリングとデコレーションをして返す

        Args:
            input_image (np.ndarray): OpenCV Image RGB形式

        Returns:
            np.ndarray: OpenCV Image RGB形式
        """
        # フィルター
        filtered_image = self.filter.filtering(copy.deepcopy(input_image))
        
        processed_image = filtered_image
        
        # デコレーション
        for name in self.decorations:
            decoration = self.decoration_dict[name]
            deco_image = decoration.decorate(input_image)
            mask = np.where(np.all(deco_image == 0, axis=-1), 0, 1)  # マスク
            # 合成
            processed_image[mask == 1] = deco_image[mask == 1]
        
        return processed_image
    
    def change_filter(self, filter_name):
        # クラスを受け取ってインスタンス化
        self.filter = self.filter_dict[filter_name]()
    
    def change_decorations(self, decoration_name):
        # 名前を受け取ってリストに追加したり削除したり
        if decoration_name not in self.decorations:
            self.decorations.append(decoration_name)
        else:
            self.decorations.remove(decoration_name)