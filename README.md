# 🌱 learn-seedphrase-generation-python

🔐 **Google Colab でシードフレーズを生成してみよう！**

実際に自分でエントロピー、シードフレーズ、シード、マスター秘密鍵、チェーンコード、BIP32ルート拡張鍵、P2PKHアドレス、秘密鍵を生成できます。

## 🔧 ステップ①：必要なライブラリをインストール

以下のURLから Google Colab にアクセスして Notebook を開いて、下のコマンドをコピー＆ペースト・実行して必要なライブラリをインストールしてください。

🔗 https://colab.google/

```python
!pip install mnemonic
!pip install pycryptodome
!pip install bip_utils
!pip install base58
!pip install ecdsa
```

## 🔧 ステップ②：english.txt をダウンロード＆アップロード

以下のリンクから english.txt をダウンロードしてください。

🔗 https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt

Google Colab上の Notebook の 左側「ファイル」タブ → 「ファイルをアップロード」でアップロードしてください。

## 🖋️ ステップ③：コードを Google Colab にコピー＆ペースト

generation_seed.py を Google Colab の Notebook にペーストして実行してください。

## 🎲 ステップ④：エントロピー（必要ならコピペ）を準備

コイントスでエントロピーを用意してください。表を1、裏を0 として 128回実行する必要があります。

もし、コイントスする時間がなければ以下の 128回分のコイントスの結果を利用できます。

```python
00011010110100001011000100010101010100010000001110010001000010001111010110110100101000000100001100111000111101101110010101100010
```

パスフレーズはあらかじめて記入してあるので変更したい場合はコードを編集して直接書き換える必要があります。

本プログラムのデフォルトでは"Buybitcoin"です。
