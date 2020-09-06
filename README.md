# Bluepetit-alpha

PC から Nintendo Switch 上の　SmileBASIC 4 に Bluetooth 経由でデータを送信する試み。


## 動作確認環境

1. VirutalBox 6.1.12
    - ホスト OS : Windows 10 Home バージョン 1909 ビルド 18363.1016 (64 ビット)
    - ゲスト OS : Ubuntu 20.04.1 LTS (64 ビット)

Linux のみで動作します。Windows では上記の通り VirtualBox 上にインストールした Ubuntu で動作を確認しています。


## 使用方法

リポジトリをクローンします。

```bash
sudo apt install git
git clone https://github.com/rtanpo440/bluepetit-alpha.git
cd bluepetit-alpha
```

`setup.sh` というスクリプトを実行して必要なパッケージやライブラリをインストールします。

```bash
sudo ./setup.sh
```

コントローラーを登録するために、一度だけ `pair.sh` を実行します。  
先に Nintendo Switch のホーム画面から "コントローラー" > "持ちかた/順番を変える" を選択してコントローラーの接続画面を出しておきます。

成功すると、画面に MAC アドレスが表示されるので、これを控えて以下のように保存します。

```bash
sudo ./pair.sh
./macaddress "xx:xx:xx:xx:xx:xx"
```

これで準備が整います。`sendstring.sh` で文字列を送信できます。

```bash
sudo ./sendstring "This is a test message sent from PC. かなや漢字もおっけー!"
```

Nintendo Switch 上での操作は [こちら](http://wiki.hosiken.jp/petc4/?Toukou/bluepetit-alpha) を参照。


## ライセンス

MIT License. See `LICENSE`.

