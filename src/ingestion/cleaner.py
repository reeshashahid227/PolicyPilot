import re

def clean_text(text):
    text=re.sub("\r\n"," ",text)
    text=re.sub(r"[ \t]+"," ",text)
    text=re.sub(r"\n{3,}"," ",text)
    text=text.strip()

    return text