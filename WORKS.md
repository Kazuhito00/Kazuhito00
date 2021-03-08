# WORKS
提供物、寄稿、公開リポジトリの内容をまとめています。

## Contribution
提供した情報等をまとめています。

<table>
    <tr>
        <th>
            提供先
        </th>
        <th>
            提供内容
        </th>
    </tr>
    <tr>
        <td>
            <a href="https://axross-recipe.com/recipes/136"><img src="https://user-images.githubusercontent.com/37477845/110350460-16634480-8077-11eb-8f12-91281d76af13.jpg" width="150px"></a>
        </td>
        <td>
            Axross様に<br>
            「MediaPipeを利用して簡単なジェスチャーを推定するレシピ」を寄稿しました。
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://amzn.to/3v5eEd7"><img src="https://user-images.githubusercontent.com/37477845/110343784-2f1c2c00-8070-11eb-91c5-ef8bdc5ae738.jpg" width="150px"></a>
        </td>
        <td>
             からあげさんの書籍「人気ブロガーからあげ先生のとにかく楽しいAI自作教室」<br>
            「2章：AIで画像認識」にて以下のリポジトリをご紹介いただきました。<br><br>
            ・TensorFlow Object Detection APIハンズオン資料<br>
            （<a href="https://github.com/Kazuhito00/Tensorflow2-ObjectDetectionAPI-Colab-Hands-On">Kazuhito00/Tensorflow2-ObjectDetectionAPI-Colab-Hands-On</a>）<br>
            ・データ拡張ライブラリAlbumentationsサンプル集<br>
            （<a href="https://github.com/Kazuhito00/albumentations-examples">Kazuhito00/albumentations-examples</a>）<br>
            ・Deep写輪眼<br>
            （<a href="https://github.com/Kazuhito00/NARUTO-HandSignDetection">Kazuhito00/NARUTO-HandSignDetection</a>）<br>
        </td>
    </tr>
</table>

## Repositories
リポジトリ数が増えてきたためカテゴリー分けしてまとめています。

#### LT資料
* [presentation-2021](https://github.com/Kazuhito00/presentation-2021)<br>LT資料をまとめたリポジトリ(2021年用)
* [presentation-2020](https://github.com/Kazuhito00/presentation-2020)<br>LT資料をまとめたリポジトリ(2020年用)
* [presentation-2019](https://github.com/Kazuhito00/presentation-2019)<br>LT資料をまとめたリポジトリ(2019年用)

#### Object Detection関連
* [NARUTO-HandSignDetection](https://github.com/Kazuhito00/NARUTO-HandSignDetection)<br>物体検出を用いてNARUTOの印(子～亥、壬、合掌)を検出するモデルとサンプルプログラム
* [Tensorflow2-ObjectDetectionAPI-Colab-Hands-On](https://github.com/Kazuhito00/Tensorflow2-ObjectDetectionAPI-Colab-Hands-On)<br>Tensorflow2 Object Detection APIのハンズオン用資料
* [FingerFrameDetection-TF2](https://github.com/Kazuhito00/FingerFrameDetection-TF2)<br>Finger Frame検出用のモデル(EfficientDetファインチューニング)
* [FingerFrameLens](https://github.com/Kazuhito00/FingerFrameLens)<br>FingerFrame検出を行った結果に対し、画像クラス分類を行うデモ
* [FaceDetection-Image-Overlay](https://github.com/Kazuhito00/FaceDetection-Image-Overlay)<br>顔検出を行い、検出した顔の上に画像を重ねるデモ(CenterFace, DBFace利用)
* [object-detection-bbox-art](https://github.com/Kazuhito00/object-detection-bbox-art)<br>OpenCVを用いたバウンディングボックス装飾の作例集

##### MediaPipe関連
* [mediapipe-python-sample](https://github.com/Kazuhito00/mediapipe-python-sample)<br>MediaPipeのPythonパッケージのサンプル
* [hand-gesture-recognition-using-mediapipe](https://github.com/Kazuhito00/hand-gesture-recognition-using-mediapipe)<br>MediaPipe(Python版)を用いて手の姿勢推定を行い、検出したキーポイントを用いて、<br>簡易なMLPでハンドサインとフィンガージェスチャーを認識するサンプル
* [iris-detection-using-py-mediapipe](https://github.com/Kazuhito00/iris-detection-using-py-mediapipe)<br>MediaPipeのIris(虹彩検出)をPythonで動作させるデモ

#### TensorFlow 2.x関連
* [tensorflow2-keras-learn](https://github.com/Kazuhito00/tensorflow2-keras-learn)<br>Tensorflow2のkerasの勉強の記録(社内向けハンズオン資料等)
* [ImageDataGenerator-examples](https://github.com/Kazuhito00/ImageDataGenerator-examples)<br>Tensorflow2(Keras)のImageDataGeneratorのJupyter上での実行例
* [tf2-keras-explain-examples](https://github.com/Kazuhito00/tf2-keras-explain-examples)<br>Tensorflowの可視化解釈ライブラリ(tf-explain、Grad-CAM等)のJupyter上での実行例。
* [mnist-sample-using-tf-simple-metric-learning](https://github.com/Kazuhito00/mnist-sample-using-tf-simple-metric-learning)<br>tf-simple-metric-learning を用いてMNISTで距離学習を実施するサンプル

#### 機械学習関連
* [albumentations-examples](https://github.com/Kazuhito00/albumentations-examples)<br>画像データ拡張ライブラリAlbumentationsのJupyter上での実行例
* [mixup](https://github.com/Kazuhito00/mixup)<br>Tensorflow2/KerasのImageDataGenerator向けのmixupの実装
* [cutmix](https://github.com/Kazuhito00/cutmix)<br>Tensorflow2/KerasのImageDataGenerator向けのcutmixの実装
* [nlpaug-examples](https://github.com/Kazuhito00/nlpaug-examples)<br>自然言語処理データ拡張ライブラリnlpaugのJupyter上での実行例

#### OpenCV関連
###### ユーティリティ
* [cvdrawtext](https://github.com/Kazuhito00/cvdrawtext)<br>OpenCV上でフォントを指定して文字を描画するクラス
* [cvoverlayimg](https://github.com/Kazuhito00/cvoverlayimg)<br>OpenCVで透過PNGを画像の上に重ね合わせるクラス
* [cvfpscalc](https://github.com/Kazuhito00/cvfpscalc)<br>OpenCVのgetTickFrequency()を利用したFPS計測クラス
* [cvui-py-two-knob-trackbar](https://github.com/Kazuhito00/cvui-py-two-knob-trackbar)<br>CVUIを用いた、上限下限指定が可能なトラックバーのお試し実装(Python)
* [cv-picture-in-picture-window](https://github.com/Kazuhito00/cv-picture-in-picture-window)<br>OpenCVでピクチャーインピクチャーのように表示するサンプル
* [cv-comparison-slider-window](https://github.com/Kazuhito00/cv-comparison-slider-window)<br>2枚の画像を重ね合わせて、マウススライドで比較するウィンドウのサンプル
###### 画像フィルタ
* [Kuwahara-Filter](https://github.com/Kazuhito00/Kuwahara-Filter)<br>Kuwahara filterのお試し実装
* [Polygon-Filter](https://github.com/Kazuhito00/Polygon-Filter)<br>ポリゴン化 filterのお試し実装
* [XDoG-OpenCV-Sample](https://github.com/Kazuhito00/XDoG-OpenCV-Sample)<br>XDoG(Extended Difference of Gaussians)アルゴリズムを用いた線画抽出のサンプル
* [color-equalize-hist-sample](https://github.com/Kazuhito00/color-equalize-hist-sample)<br>カラー画像に対するヒストグラム平坦化のOpenCVサンプル
###### 機械学習 データ作成向けツール
* [movie2jpg](https://github.com/Kazuhito00/movie2jpg)<br>Webカメラ、動画を連番jpgとして保存。および、連番jpgから動画を作成するツール
* [hsv-mask-extracter](https://github.com/Kazuhito00/hsv-mask-extracter)<br>HSV閾値でのマスク画像生成プログラム
* [image-mask-replace](https://github.com/Kazuhito00/image-mask-replace)<br>マスク画像を用いて2枚の画像を合成するプログラム(データ拡張用)
###### 実装例
* [OpenCV-readNetFromTensorflow-sample](https://github.com/Kazuhito00/OpenCV-readNetFromTensorflow-sample)<br>OpenCV 4.X系のreadNetFromTensorflow()の動作サンプル
* [click-warp-perspective](https://github.com/Kazuhito00/click-warp-perspective)<br>マウスクリックで指定した座標を矩形に射影変換するプログラム
* [cv-warpPolar-example](https://github.com/Kazuhito00/cv-warpPolar-example)<br>cv-warpPolar-exampleは、OpenCVでの極座標変換/逆変換の実行例
###### その他
* [desktopdraw-use-dxlib](https://github.com/Kazuhito00/desktopdraw-use-dxlib)<br>デスクトップ上に図形やテキストを重畳表示 ※DXライブラリ(C# DLL版)をPythonから利用

#### Qiita関連
* [Qiita-AdventCalendar-20201212-OpenCV](https://github.com/Kazuhito00/Qiita-AdventCalendar-20201212-OpenCV)<br>Qiita OpenCV アドベントカレンダー(2020年12月12日)の投稿用のサンプル集

#### Unity関連
* [Unity-Quad-Shader-Learn](https://github.com/Kazuhito00/Unity-Quad-Shader-Learn)<br>Unity平面シェーダーの勉強の記録
* [Unity-WebCamTexture-WebGL-Sample](https://github.com/Kazuhito00/Unity-WebCamTexture-WebGL-Sample)<br>UnityのWebカメラ入力をWebGLビルドしたサンプル
* [Unity-VideoPlayer-WebGL-Sample](https://github.com/Kazuhito00/Unity-VideoPlayer-WebGL-Sample)<br>Unityの動画再生をWebGLビルドしたサンプル
* [Unity-MousePaint-WebGL-Sample](https://github.com/Kazuhito00/Unity-MousePaint-WebGL-Sample)<br>Unityでのテクスチャお絵描きをWebGLビルドしたサンプル
* [Unity-Barracuda-MNIST-WebGL-Sample](https://github.com/Kazuhito00/Unity-Barracuda-MNIST-WebGL-Sample)<br>Unity Barracudaを用いてMNIST(手書き数字認識)をWebGL上で推論するサンプル
* [Unity-Barracuda-MobileNet-WebGL-Sample](https://github.com/Kazuhito00/Unity-Barracuda-MobileNet-WebGL-Sample)<br>Unity Barracudaを用いてMobileNet(画像クラス分類)をWebGL上で推論するサンプル
* [Unity-Barracuda-TinyYoloV2-WebGL-Sample](https://github.com/Kazuhito00/Unity-Barracuda-TinyYoloV2-WebGL-Sample)<br>Unity Barracudaを用いてTinyYoloV2をWebGL上で推論するサンプル
* [Unity-MediaPipeJs-SendMessage-WebGL-Sample](https://github.com/Kazuhito00/Unity-MediaPipeJs-SendMessage-WebGL-Sample)<br>ブラウザ上でMediaPipeを動かし、推論結果をJavaScript→Unity WebGL連携で表示するサンプル
* [Unity-Barracuda-Reversi-WebGL-Sample](https://github.com/Kazuhito00/Unity-Barracuda-Reversi-WebGL-Sample)<br>Unity Barracudaを用いてリバーシAI(簡易なMLP)をWebGL上で推論するサンプル ※リバーシ用のモデルは教師有り学習で作成したもの

#### WebSlides関連
* [opencv2eel-sample](https://github.com/Kazuhito00/opencv2eel-sample)<br>
* [opencv2webslides-sample](https://github.com/Kazuhito00/opencv2webslides-sample)<br>

#### Jupyte Notebook関連
* [Jupyter-VideoCapture-Demo](https://github.com/Kazuhito00/Jupyter-VideoCapture-Demo)<br>

#### Julia関連
* [Google-Colab-Julia](https://github.com/Kazuhito00/Google-Colab-Julia)<br>

#### TensorFlow 1.x関連
* [hand-detection-3class-MobilenetV2-SSDLite](https://github.com/Kazuhito00/hand-detection-3class-MobilenetV2-SSDLite)<br>
* [hand-detection-2class-MobilenetV1-SSD](https://github.com/Kazuhito00/hand-detection-2class-MobilenetV1-SSD)<br>

#### Kaggle関連
* [kaggle-memo](https://github.com/Kazuhito00/kaggle-memo)<br>

#### その他
* [PyCaret-Learn](https://github.com/Kazuhito00/PyCaret-Learn)<br>
* [pyboy-gbdk-examples](https://github.com/Kazuhito00/pyboy-gbdk-examples)<br>
* [SendGrid-Colaboratory](https://github.com/Kazuhito00/SendGrid-Colaboratory)<br>

<!--
|01：3連通信リング|02：和風 黒円|
:---:|:---:
|![01](https://user-images.githubusercontent.com/37477845/75368668-6ad0d180-5905-11ea-93c0-635ba29a2a05.gif)|![02](https://user-images.githubusercontent.com/37477845/75368708-77edc080-5905-11ea-9c11-f80373aa9ec2.gif)|
-->
