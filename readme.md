# MediaPipeCamera

## 概要

Webカメラの映像から顔検出やハンドポーズ推定をして映像に装飾を加える機能を持つカメラアプリです。Googleの提供するMediaPipe( https://google.github.io/mediapipe/ )を利用しています。

ハンドポーズ推定においてはKazuhito00氏の公開しているソースコード（ https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe ）を大変参考にさせていただきました。

## 実行方法
MediaPipeCameraフォルダをカレントディレクトリに設定し、`app.py`を実行する。

必要環境
- Python 3.8
- MediaPipe
- OpenCV
- TensorFlow
- scikit-learn

## ディレクトリ構成
```
MediaPipeCamera/       
    fonts/
    images/
        emoji/         : 絵文字を画像化したものを保存
        filter/        : フィルター機能に用いる画像を保存
        gui/           : ボタン用の画像などを保存
    model/             : データセットや学習モデル等が配置されている
    snapshots/                     
    utils/
    app.py             : GUIを記述。メインプログラムも兼ねる
    camera_model.py    : フィルタ機能とデコレーション機能を備えたカメラ機能を提供
    funcs.py           : 関数群
    MyDecorations.py   : デコレーションクラスを記述
    MyFilters.py       : フィルタークラスを記述
    readme.py          : このファイル

```



## スクリーンショット



![screenshot_new](https://user-images.githubusercontent.com/71445661/148839276-43848225-bccb-4e5c-9a21-91a0fb4e3884.png)







