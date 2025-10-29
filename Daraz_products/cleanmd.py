import re

with open("single_url.md","r",encoding="utf-8") as f:
    raw_md=f.read()

# Removing image markdown like(!)
clean_md=re.sub(r"!\[.*?\]\(.*?\)","",raw_md)
#Removing markdown headers
clean_md=re.sub(r"#+\s*", "", clean_md)
#Removing bullets at gthe start of the line
clean_md=re.sub(r"^[*\-•]\s*", "", clean_md, flags=re.MULTILINE)
#Removing excessive whitespace and empty lines
clean_md=re.sub(r"\n\s*\n", "\n\n", clean_md)
clean_md=clean_md.strip()

with open("single_url_clean.md","w",encoding="utf-8") as f:
    f.write(clean_md)

print("Cleaned product description saved to single_url_clean.md")