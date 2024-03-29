# al_tools

## インストール
以下のいずれかにより適切な方法を選ぶ
1. パッケージの中身には絶対に触らない場合（コード修正・改善・拡張には興味ない！という場合）
1. もしかするとコードを変更し，パッケージの改善に少しでも貢献するかもしれない場合

### 1. コードを変更しない場合
GitHubから`pip`を使って直接インストールする。
```Shell
pip install git+https://github.com/makutaga/al_tools.git
```
コード本体はユーザのパッケージの格納ディレクトリにインストールされる。
場合によってはシステム全体のパッケージディレクトリにインストールされる。
ただしインストール先については`pip`が勝手に善きにはからってくれるので気にすることはない。

### 2. コードを変更する可能性がある場合
ホームディレクトリ内の適当なディレクトリにパッケージを取得しておき，*editable mode* でインストールする。
自分の開発用のディレクトを決めておくと良い。例えばホームディレクトリ直下に`devel`というディレクトリを作って，その中に入れておくと良い。
パッケージのファイルを変更してもいちいち`pip install`でインストールする必要はない。

まずパッケージをGitHubから取得する。パッケージファイルを置いておくディレクトリで以下を実行する。
```
git clone https://github.com/makutaga/al_tools.git
```

カレントディレクトリ直下に以下のように`al_tools`というディレクトリが作成される。
```
al_tools
├── LICENSE
├── README.md
├── al_tools
│   ├── __init__.py
│   ├── plot_tools.py
│   └── utils.py
└── setup.py
```
（ファイル構成は変更の可能性あり）

`pip` を使ってeditable modeでインストール
```Shell
pip install -e al_tools
```

## パッケージファイルの更新
GitHubに置いてあるパッケージファイルが更新された場合，以下で手元のパッケージを更新できる。

### GitHubから直接インストールした場合
他の`pip`のパッケージと同様，以下で更新できる
```Shell
pip install -U git+https://github.com/makutaga/al_tools.git
```

### Editable modeでインストールした場合
`al_tools`を展開したディレクトリ内で，`git pull` で更新内容を取得する。
```Shell
git pull
```
それだけ。

## ドキュメント
docstringから生成されるドキュメントを以下で読める。
```Shell
pydoc al_tools
pydoc al_tools.utils
pydoc al_tools.plot_tools
```
