with open('fixtures/tovari/cats.json', 'rb') as file:
    content = file.read().decode('windows-1251') 

with open('fixtures/tovari/cats.json', 'w', encoding='utf-8') as file:
    file.write(content)
