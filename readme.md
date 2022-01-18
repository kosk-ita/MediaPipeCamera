# MediaPipeCamera

## 概要

Webカメラの映像から顔検出やハンドサイン推定をして映像に装飾を加える機能を持つカメラアプリです。Googleの提供するMediaPipe( https://google.github.io/mediapipe/ )を利用しています。

ハンドサイン推定においてはKazuhito00氏の公開しているソースコード（ https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe ）を大変参考にさせていただきました。

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



## 工夫点

1. Googleが公開しているMediaPipeのPython版ライブラリを使用することで、高い性能の機械学習モデルを比較的簡単に利用することができた。
    MediaPipe: https://google.github.io/mediapipe/
2. ハンドサイン推定の学習を、画像ではなく手のランドマーク座標（MediaPipeによる推定）を基に行うことで、少ないデータ（ハンドポーズごとに1500件程度）で高い精度を出すことができた。
   （前述のKazuhito00氏の公開するプログラムに則ったものです）
3. ボタンのアイコンを自作し、直感的なUIにこだわった。



## 今後の課題

1. 初期段階のアイディアであった、機械学習を取り入れたフィルター機能（鼻だけを検出して大きくする等）は実現することができなかった。鼻や目の位置を検出することはできても、画像に繋がりを持たせたまま一部を拡大縮小するのが難しく、断念した。
2. ニューラルネットワーク等はKazuhito00氏が公開しているものを使わせていただいたが、識別するべきハンドポーズの種類が増えると性能が悪くなることが確認されたので、今後機能を拡張していくならそれに合わせてネットワーク構造や学習方法も見直す必要が出てくる。