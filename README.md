# Windows_JRA_download
同じくJRA55のダウンロードの自動化をwindowsでも行う

# Discription
JRA55(気象庁)データはブラウザでダウンロードする際、1ファイルごとに利用規約をクリックする必要があり、手作業で行うと大幅な時間を費やすこととなる。公式側がpython2のダウンロードスクリプトを出しているが、python3での動作や任意の日時や物理用のデータ取得が難しい。  
またダウンロード後には、データサーバへの一斉送信という作業も行う必要がある。  
そのため今回はこの2つの作業を一つのシェルスクリプトの実行で実現できるようなプログラムを制作した。  

# Requirement
## remote(データサーバ)側
- centOS6
- python3.8以上(今回はanacondaベース)
python3ならおそらく動く（確認は取れていない）
- ssh-sever

## local側
- Windows10以降
- python3.8以上(remote同様 anacondaベース)
今回seleniumモジュールが必要なため、Anaconda Promptで下記をインストール。
```
conda install selenium
```
- Git Bash
- Linuxコマンドjq(Windows版)
- Linuxコマンドmake(Windows版)
- Linuxコマンドwgrib(Windows版)
- Google Chrome(最新バージョン)
- Chromedriver(Google Chromeのバージョンと一致しているもの)
- ssh-client

# Usage
ローカル側の環境依存性が極めて高く、現時点では同研究室のメンバーしか需要がないため、使い方は割愛。  
現在、ローカル側の環境依存性を低くするためにコンテナ技術を導入中。
また、取得できるデータの種類や、ローカル・サーバ側の詳細設定を増やす予定。
