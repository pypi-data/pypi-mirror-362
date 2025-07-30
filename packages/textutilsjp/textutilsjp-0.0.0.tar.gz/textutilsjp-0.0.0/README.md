# textutilsjp

日本語テキストの整形・抽出・要約・解析に役立つPythonライブラリです。

## 主な機能

- 全角⇔半角変換
- ひらがな⇔カタカナ変換
- メールアドレス・URLの抽出
- テキストクリーニング（改行・空白の統一、不要文字の削除など）
- 文章の要約（シンプルな1行要約）
- キーワード抽出、単語頻度解析

## インストール

```bash
pip install .
```

## 使い方

```python
from textutilsjp import (
    to_hankaku, to_zenkaku,
    hira_to_kata, kata_to_hira,
    extract_emails, extract_urls,
    clean_text, summarize,
    extract_keywords, word_count
)

text = "ＡＢＣ　１２３ test@example.com https://example.com"
print(to_hankaku(text))
# => ABC 123 test@example.com https://example.com

print(hira_to_kata("こんにちは"))
# => コンニチハ

print(kata_to_hira("テスト"))
# => てすと

print(extract_emails("連絡先: info@example.com, test@sample.jp"))
# => ['info@example.com', 'test@sample.jp']

print(extract_urls("公式: https://example.com/info 参考: http://ex.jp"))
# => ['https://example.com/info', 'http://ex.jp']

print(clean_text("  こんにちは。\n\n世界！\t  "))
# => こんにちは。\n世界！

print(summarize("今日は晴れです。明日は雨でしょう。"))
# => 今日は晴れです

print(extract_keywords("テスト テスト python python コード", topn=2))
# => ['テスト', 'python']

print(word_count("テスト テスト python コード コード"))
# => {'テスト': 2, 'python': 1, 'コード': 2}
```

## ライセンス

MIT
