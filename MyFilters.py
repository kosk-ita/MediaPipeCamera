import numpy as np
import cv2
from scipy.interpolate import splrep, splev



# フィルター基底クラス
class BaseFilter():
    name = "Sample Name"
    description = "Sample Text."
    def filtering(self, input_image):
        return input_image
    

class LightSepiaFilter(BaseFilter):
    """フィルタークラス。
        このクラスを編集することで、様々なフィルタができる。
        基底クラスBaseFilterを継承している。
    """
    
    # 静的プロパティ
    name = 'ライトセピアフィルター'  # 名前
    description = 'セピアにするフィルターの簡易版'  # 説明
    
    def __init__(self):
        # フィルムテクスチャ
        film = cv2.imread('images/filter/1.jpg')
        self.film = cv2.cvtColor(film, cv2.COLOR_BGR2RGB)
    
    def filtering(self, input_image: np.ndarray) -> np.ndarray:
        """opencv画像(=numpy配列)を受け取って、フィルタリングしたものを返す。

        Args:
            input_image (np.ndarray): 

        Returns:
            np.ndarray: opencv画像(=numpy配列)
        """
        img = input_image
        #全画素についてB(青)の輝度を0.3倍、G(緑)の輝度を0.8倍、R(赤)の輝度はそのまま
        img[:, :, 0] = img[:, :, 0]
        img[:, :, 1] = (img[:, :, 1] * 0.8).astype(int)
        img[:, :, 2] = (img[:, :, 2] * 0.3).astype(int)
        
        self.film = cv2.resize(self.film, (img.shape[1], img.shape[0]))
        
        blended = cv2.addWeighted(src1=img, alpha=0.8, src2=self.film, beta=0.2, gamma=0)
        return blended
    

class SepiaFilter(BaseFilter):
    """フィルタークラス。
        このクラスを編集することで、様々なフィルタができる。
        基底クラスBaseFilterを継承している。
    """
    
    # 静的プロパティ
    name = 'セピアフィルター'  # 名前
    description = 'セピアにするフィルター'  # 説明
        
    def filtering(self, input_image: np.ndarray) -> np.ndarray:
        """opencv画像(=numpy配列)を受け取って、フィルタリングしたものを返す。

        Args:
            input_image (np.ndarray): 

        Returns:
            np.ndarray: opencv画像(=numpy配列)
        """
        img = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        h, w = gray.shape
        gauss = np.random.normal(0, 40, (h, w))
        gauss = gauss.reshape(h, w)
        gray = np.clip(gray + gauss, 0, 255).astype(np.uint8)
    
        xs = [0, 0.25, 0.5, 0.75, 1]
        ys = [0, 0.15, 0.5, 0.85, 0.99]
        gray = gray / 255
        tck = splrep(xs, ys)  # スプライン
        gray = splev(gray, tck)*255  # スプライン適用
    
        gray = self.peripheral_light_correct(gray, -0.4).astype(np.uint8)
    
        img_hsv = np.zeros_like(img)
        img_hsv[:, :, 0] = np.full_like(img_hsv[:, :, 0], 15, dtype=np.uint8)
        img_hsv[:, :, 1] = np.full_like(img_hsv[:, :, 1], 153, dtype=np.uint8)
        img_hsv[:, :, 2] = gray
        img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
        
        return img
    
    def peripheral_light_correct(self, img, gain_params):
        h, w = img.shape[:2]
        size = max([h, w])  # 幅、高の大きい方を確保
    
        # 1.画像の中心からの距離画像作成
        x = np.linspace(-w / size, w / size, w)
        y = np.linspace(-h / size, h / size, h)  # 長い方の辺が1になるように正規化
        xx, yy = np.meshgrid(x, y)
        r = np.sqrt(xx ** 2 + yy ** 2)
    
        # 2.距離画像にゲインを乗じ、ゲインマップを作製
        gainmap = gain_params * r + 1
    
        # 3.画像にゲインマップを乗じる
        return np.clip(img * gainmap, 0., 255)
    
class HSVFilter(BaseFilter):
    """フィルタークラス。
        このクラスを編集することで、様々なフィルタができる。
        基底クラスBaseFilterを継承している。
    """
    
    # 静的プロパティ
    name = '色調変換フィルター'  # 名前
    description = '色調を変えるフィルター'  # 説明
    
    def __init__(self):
        self.h_deg = np.random.randint(15, 166) #色相(Hue)の回転度数
        self.s_mag = 1.5 # 彩度(Saturation)の倍率
        self.v_mag = 1 # 明度(Value)の倍率
    
    def filtering(self, input_image: np.ndarray) -> np.ndarray:
        """opencv画像(=numpy配列)を受け取って、フィルタリングしたものを返す。"""

        img_hsv = cv2.cvtColor(input_image, cv2.COLOR_RGB2HSV) # 色空間をBGRからHSVに変換
        img_hsv = img_hsv.astype(np.uint16)
        
        img_hsv[:,:,(0)] = (img_hsv[:,:,0] + self.h_deg)%180 # 色相の計算
        img_hsv[:,:,(1)] = img_hsv[:,:,(1)] * self.s_mag # 彩度の計算
        img_hsv[:,:,(2)] = img_hsv[:,:,(2)] * self.v_mag # 明度の計算
        
        img_hsv = img_hsv.astype(np.uint8)
        img_rgb = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2RGB) # 色空間をHSVからrgbに変換
        
        return img_rgb
    
class PostarizationFilter(BaseFilter):
    """フィルタークラス。
        このクラスを編集することで、様々なフィルタができる。
        基底クラスBaseFilterを継承している。
    """
    
    # 静的プロパティ
    name = 'ポスタリゼーションフィルター'  # 名前
    description = 'ポスタリゼートするフィルター'  # 説明
    
    def filtering(self, input_image: np.ndarray) -> np.ndarray:
        """opencv画像(=numpy配列)を受け取って、フィルタリングしたものを返す。"""

        return (input_image // 64) * 64