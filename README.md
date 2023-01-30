# eegtools

## インストール

### github からパッケージを取得

```
git clone https://github.com/makutaga/eegtools.git
```
カレントディレクトリ直下に```eegtools```というディレクトリが作成される。

### Editable で使う

上記で作成された ```eegtools``` にディレクトリを変更し，```pip``` を使ってEditableとしてインストール
```
cd eegtools
pip install -e .
```

githubのリポジトリが更新されたら，ディレクトリ```eegtools```で
```
git pull
```

## ドキュメント
docstringから生成されるドキュメントを以下で読める。
```
pydoc eegtools
pydoc eegtools.utils
pydoc eegtools.plot_tools
```
