# learn-seedphrase-generation-python

Google Colabで実行してください。

https://colab.google/


これらのコマンドを先に実行してください。

!pip install mnemonic

!pip install pycryptodome

!pip install bip_utils

!pip install base58

!pip install ecdsa


ここからenglish.txtをダウンロードしてGoogle Colabのフォルダにアップロード

https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt

次にgenerate_seed.pyをGoogle Colabにコピーペーストして実行してください。

エントロピーは自分でダイスロールして表を1、裏を0として128回入力しても良いですが、よければこちらのエントロピーをどうぞ。

00011010110100001011000100010101010100010000001110010001000010001111010110110100101000000100001100111000111101101110010101100010
