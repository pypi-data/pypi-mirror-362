import unittest

from jinnang.io.file import (
    is_bad_llm_caption,
    is_bad_folder_name
)


class TestFileIO(unittest.TestCase):
    def test_is_bad_llm_caption(self):
        # Test valid captions (3 or fewer question marks)
        self.assertFalse(is_bad_llm_caption("This is a normal caption."))
        self.assertFalse(is_bad_llm_caption("Is this a question?"))
        self.assertFalse(is_bad_llm_caption("Is this a question? Yes it is. Another question?"))
        self.assertFalse(is_bad_llm_caption("Is this a question? Yes it is. Another question? Yes."))
        
        # Test invalid captions (more than 3 question marks)
        self.assertTrue(is_bad_llm_caption("Is this a question? What about this? And this? And one more?"))
        self.assertTrue(is_bad_llm_caption("????? Multiple question marks"))

    def test_is_bad_folder_name_with_whitespace(self):
        # Test case for folder names with leading/trailing whitespace
        self.assertTrue(is_bad_folder_name(" foldername"))
        self.assertTrue(is_bad_folder_name("foldername "))
        self.assertTrue(is_bad_folder_name(" foldername "))

    def test_is_bad_folder_name_empty_or_whitespace(self):
        # Test case for empty string or string with only whitespace
        self.assertTrue(is_bad_folder_name(""))
        self.assertTrue(is_bad_folder_name("   "))
        # Test with Chinese question marks
        self.assertFalse(is_bad_llm_caption("这是一个问题？"))
        self.assertFalse(is_bad_llm_caption("这是一个问题？这是另一个问题？这是第三个问题？"))
        self.assertTrue(is_bad_llm_caption("这是一个问题？这是另一个问题？这是第三个问题？这是第四个问题？"))
        
        # Test with mixed question marks
        self.assertFalse(is_bad_llm_caption("Is this a question? 这是一个问题？ Another one?"))
        self.assertFalse(is_bad_llm_caption("Is this a question? 这是一个问题？ Another one? 这是另一个问题？"))
        
        # Test with empty string
        self.assertFalse(is_bad_llm_caption(""))
        
        # Test with no question marks
        self.assertFalse(is_bad_llm_caption("This caption has no question marks."))
    
    def test_is_bad_folder_name(self):
        # Test valid folder names
        self.assertFalse(is_bad_folder_name("valid folder"))
        self.assertFalse(is_bad_folder_name("folder-with-hyphens"))
        self.assertFalse(is_bad_folder_name("folder123"))
        self.assertFalse(is_bad_folder_name("简体中文"))  # Chinese characters
        self.assertFalse(is_bad_folder_name("日本語"))    # Japanese characters
        
        # Test invalid folder names - None or empty
        self.assertTrue(is_bad_folder_name(None))
        self.assertTrue(is_bad_folder_name(""))
        self.assertTrue(is_bad_folder_name("   "))  # Whitespace only
        
        # Test invalid folder names - forbidden ASCII characters
        self.assertTrue(is_bad_folder_name("folder{bracket}"))
        self.assertTrue(is_bad_folder_name("folder<angle>"))
        self.assertTrue(is_bad_folder_name("folder:colon"))
        self.assertTrue(is_bad_folder_name('folder"quotes"'))
        self.assertTrue(is_bad_folder_name("folder/slash"))
        self.assertTrue(is_bad_folder_name("folder\\backslash"))
        self.assertTrue(is_bad_folder_name("folder|pipe"))
        self.assertTrue(is_bad_folder_name("folder?question"))
        self.assertTrue(is_bad_folder_name("folder*asterisk"))
        self.assertTrue(is_bad_folder_name("folder_underscore"))
        self.assertTrue(is_bad_folder_name("folder.dot"))
        
        # Test invalid folder names - Chinese/Japanese punctuation
        self.assertTrue(is_bad_folder_name("folder，comma"))
        self.assertTrue(is_bad_folder_name("folder。period"))
        self.assertTrue(is_bad_folder_name("folder？question"))
        self.assertTrue(is_bad_folder_name("folder、slash"))
        self.assertTrue(is_bad_folder_name("folder『bracket』"))
        self.assertTrue(is_bad_folder_name("folder【bracket】"))
        
        # Test invalid folder names - forbidden words
        self.assertTrue(is_bad_folder_name("未知"))
        self.assertTrue(is_bad_folder_name("未提"))
        self.assertTrue(is_bad_folder_name("图中"))
        self.assertTrue(is_bad_folder_name("unknown"))
        self.assertTrue(is_bad_folder_name("none"))
        self.assertTrue(is_bad_folder_name("null"))
        self.assertTrue(is_bad_folder_name("folder with unknown in it"))
        
        # Test invalid folder names - Windows reserved names
        self.assertTrue(is_bad_folder_name("CON"))
        self.assertTrue(is_bad_folder_name("PRN"))
        self.assertTrue(is_bad_folder_name("AUX"))
        self.assertTrue(is_bad_folder_name("NUL"))
        self.assertTrue(is_bad_folder_name("COM1"))
        self.assertTrue(is_bad_folder_name("LPT1"))
        self.assertTrue(is_bad_folder_name("con"))  # Case insensitive
        
        # Test invalid folder names - structural problems
        self.assertTrue(is_bad_folder_name(" leadingSpace"))
        self.assertTrue(is_bad_folder_name("trailingSpace "))
        self.assertTrue(is_bad_folder_name(".leadingDot"))
        self.assertTrue(is_bad_folder_name("trailingDot."))
        self.assertTrue(is_bad_folder_name("a" * 51))  # Too long (> 50 chars)
        
        # Test invalid folder names - control characters
        self.assertTrue(is_bad_folder_name("folder\nwith\nnewlines"))
        self.assertTrue(is_bad_folder_name("folder\twith\ttabs"))
        self.assertTrue(is_bad_folder_name("folder\rwith\rreturns"))
        
        # Test invalid folder names - temporary files
        self.assertTrue(is_bad_folder_name("~$tempfile"))
        
        # Test invalid folder names - emoji and unusual Unicode
        self.assertTrue(is_bad_folder_name("folder📁with📂emoji"))
        self.assertTrue(is_bad_folder_name("folder★with☆symbols"))
        
        # Test with non-string input
        self.assertTrue(is_bad_folder_name(123))
        self.assertTrue(is_bad_folder_name(["list"]))
        self.assertTrue(is_bad_folder_name({"dict": "value"}))


if __name__ == "__main__":
    unittest.main()