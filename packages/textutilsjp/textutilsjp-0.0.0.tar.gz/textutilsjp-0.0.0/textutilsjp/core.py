import re

def to_hankaku(text: str) -> str:
    """全角→半角変換（一部記号と数字・英字対応）"""
    import unicodedata
    return unicodedata.normalize('NFKC', text)

def to_zenkaku(text: str) -> str:
    """半角→全角変換（一部記号と数字・英字対応）"""
    # Python標準では難しいため、外部ライブラリjaconvに依存も可
    try:
        import jaconv
        return jaconv.h2z(text, kana=False, digit=True, ascii=True)
    except ImportError:
        # jaconvがなければnormalizeで最低限
        return text

def hira_to_kata(text: str) -> str:
    """ひらがな→カタカナ変換"""
    return "".join([chr(ord(ch) + 0x60) if 'ぁ' <= ch <= 'ゖ' else ch for ch in text])

def kata_to_hira(text: str) -> str:
    """カタカナ→ひらがな変換"""
    return "".join([chr(ord(ch) - 0x60) if 'ァ' <= ch <= 'ヶ' else ch for ch in text])

def extract_emails(text: str) -> list:
    """テキストからメールアドレスを抽出"""
    return re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)

def extract_urls(text: str) -> list:
    """テキストからURLを抽出"""
    return re.findall(r'https?://[^\s]+', text)

def clean_text(text: str) -> str:
    """改行・空白の統一、不要空白除去"""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

def summarize(text: str) -> str:
    """文章の1行要約（最長文、または先頭文抽出）"""
    sentences = re.split(r'[。．.!?！？]\s*', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return ""
    # 最も長い文、なければ先頭文
    return max(sentences, key=len)

def extract_keywords(text: str, topn: int = 5) -> list:
    """頻出単語の上位を抽出（日本語は形態素解析も考慮、ここでは単純分割）"""
    words = re.findall(r'\w+', text.lower())
    from collections import Counter
    freq = Counter(words)
    return [w for w, _ in freq.most_common(topn)]

def word_count(text: str) -> dict:
    """単語頻度カウント"""
    words = re.findall(r'\w+', text.lower())
    from collections import Counter
    return dict(Counter(words))
