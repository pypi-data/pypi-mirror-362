import os
import re
from urllib.parse import urlparse
import requests
from ailice.modules.AScrollablePage import AScrollablePage

class ATextBrowser(AScrollablePage):
    def __init__(self, functions: dict[str, str]):
        super(ATextBrowser, self).__init__(functions=functions)
        self.path = None
        self.prompt = \
'''
The document is in editable mode. You can edit the content using the following functions:
#Replace the matching content within the current page. When regexMode==True, you can use regular expressions to represent the pattern and replacement. This function is a simple wrapper for re.sub() in this mode. When regexMode==False, pattern and replacement represent literal strings. Use triple quotes to represent pattern and replacement.
REPLACE<!|pattern: str, replacement: str, regexMode: bool, session: str|!> -> str
#Replace all matching content in the entire document. The parameters are the same as REPLACE.
REPLACE-ALL<!|pattern: str, replacement: str, regexMode: bool, session: str|!> -> str
#Save the modified content to a file. If the dstPath parameter is an empty string, save it to the original file.
SAVETO<!|dstPath: str, session: str|!> -> str

Example:
!REPLACE<!|"""Hello World!""", """Hello Python!""", False, "session_example"|!>
!SAVETO<!|"", "session_example"|!>
'''
        return
    
    def Browse(self, url: str) -> str:
        parsedURL = urlparse(url)
        
        if (parsedURL.scheme in ["file", ""]) and ("" == parsedURL.netloc):
            try:
                with open(parsedURL.path, 'r', encoding='utf-8') as f:
                    self.LoadPage(f.read(), "TOP")
                    self.path = None
                    return self()
            except Exception as e:
                self.LoadPage(f"Exception: {str(e)}.", "BOTTOM")
                return self()
        else:
            response = requests.get(url)
            if response.status_code != 200:
                return f"Error: can not download text file. HTTP err code: {response.status_code}"
            if 'text' not in response.headers.get('Content-Type', ''):
                return "The url returned non-text content and cannot be browsed."
            self.LoadPage(response.content, "TOP")
            return self()

    def Edit(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.LoadPage(f.read(), "TOP")
                self.path = path
                return self() + self.prompt
        except Exception as e:
            self.LoadPage(f"Exception: {str(e)}.", "BOTTOM")
            return self()
    
    def Replace(self, pattern: str, replacement: str, regexMode: bool) -> str:
        if regexMode:
            textNew = re.sub(pattern, replacement, self(prompt=False))
        else:
            textNew = self(prompt=False).replace(pattern, replacement)
        msg = "Pattern NOT FOUND in current visible page. Please check: 1. If the pattern you entered is correct, such as whether you forgot to properly escape characters within the quotes. 2. Ensure that the content to be replaced is within the currently visible page (you can use the SEARCHDOWN/SEARCHUP to locate it, or directly use the REPLACE-ALL to replace all matching content).\n\n"
        if (self(prompt=False) != textNew) or ("" == pattern):
            msg = "The matching contents has been replaced. \n\n"
        self.ReplaceText(textNew, replaceAll=False)
        return msg + self() + self.prompt
    
    def ReplaceAll(self, pattern: str, replacement: str, regexMode: bool) -> str:
        if regexMode:
            textNew = re.sub(pattern, replacement, self.txt)
        else:
            textNew = self.txt.replace(pattern, replacement)
        msg = "Pattern NOT FOUND in the entire document. Please check if the pattern you entered is correct, such as whether you forgot to properly escape characters within the quotes.\n\n"
        if (self.txt != textNew) or ("" == pattern):
            msg = "The matching contents has been replaced. \n\n"
        self.ReplaceText(textNew, replaceAll=True)
        return msg + self() + self.prompt
    
    def SaveTo(self, dstPath: str) -> str:
        try:
            dstPath = self.path if ((dstPath.strip() == "") and (self.path != None)) else dstPath
            d = os.path.dirname(dstPath)
            if d.strip() != "":
                os.makedirs(d, exist_ok=True)
            with open(dstPath, 'w') as f:
                f.write(self.txt)
            return f"File {dstPath} saved."
        except Exception as e:
            return f"Failed to save file {dstPath}, Exception: {str(e)}"

    def GetFullText(self) -> str:
        return self.txt if (self.txt != None) else ""
    
    def ScrollDown(self) -> str:
        return super(ATextBrowser, self).ScrollDown() + (self.prompt if self.path else "")
    
    def ScrollUp(self) -> str:
        return super(ATextBrowser, self).ScrollUp() + (self.prompt if self.path else "")

    def SearchDown(self, query: str) -> str:
        return super(ATextBrowser, self).SearchDown(query) + (self.prompt if self.path else "")
    
    def SearchUp(self, query: str) -> str:
        return super(ATextBrowser, self).SearchUp(query) + (self.prompt if self.path else "")
    
    def Destroy(self):
        return