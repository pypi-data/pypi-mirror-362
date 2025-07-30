import unittest
from textutilsjp.core import (
    to_hankaku, to_zenkaku,
    hira_to_kata, kata_to_hira,
    extract_emails, extract_urls,
    clean_text, summarize,
    extract_keywords, word_count
)

class TestTextUtilsJP(unittest.TestCase):
    def test_to_hankaku(self):
        self.assertEqual(to_hankaku('ＡＢＣ！　１２３'), 'ABC! 123')
        self.assertEqual(to_hankaku('テスト１２３'), 'テスト123')

    def test_to_zenkaku(self):
        # jaconvがなければ元テキストを返す（例として簡単なチェック）
        out = to_zenkaku('ABC! 123')
        self.assertTrue(isinstance(out, str))

    def test_hira_to_kata(self):
        self.assertEqual(hira_to_kata('あいうえお'), 'アイウエオ')
        self.assertEqual(hira_to_kata('こんにちは'), 'コンニチハ')

    def test_kata_to_hira(self):
        self.assertEqual(kata_to_hira('アイウエオ'), 'あいうえお')
        self.assertEqual(kata_to_hira('コンニチハ'), 'こんにちは')

    def test_extract_emails(self):
        t = "お問い合わせはinfo@example.comまたはtest123@sample.co.jpまで"
        self.assertIn('info@example.com', extract_emails(t))
        self.assertIn('test123@sample.co.jp', extract_emails(t))

    def test_extract_urls(self):
        t = "公式サイトはhttps://example.comとhttp://test.co.jpです"
        urls = extract_urls(t)
        self.assertIn('https://example.com', urls)
        self.assertIn('http://test.co.jp', urls)

    def test_clean_text(self):
        t = "  こんにちは。\r\n\n  \n世界！\t \n\n"
        self.assertEqual(clean_text(t), "こんにちは。\n世界！")

    def test_summarize(self):
        t = "今日はいい天気です。明日は雨が降るでしょう。"
        self.assertEqual(summarize(t), "今日はいい天気です")
        t2 = ""
        self.assertEqual(summarize(t2), "")

    def test_extract_keywords(self):
        t = "テスト テスト python python コード"
        kws = extract_keywords(t, topn=2)
        self.assertTrue('テスト' in kws or 'python' in kws)

    def test_word_count(self):
        t = "test test code python python python"
        counts = word_count(t)
        self.assertEqual(counts.get('python', 0), 3)
        self.assertEqual(counts.get('test', 0), 2)
        self.assertEqual(counts.get('code', 0), 1)

if __name__ == '__main__':
    unittest.main()
