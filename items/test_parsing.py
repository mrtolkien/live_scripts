from bs4 import BeautifulSoup

field_name = "helloFriend"

soup = BeautifulSoup(f"<{field_name}>text</{field_name}>", "html.parser")

print(soup.findAll(field_name.lower()))
print(len(soup.findAll(field_name.lower())))
