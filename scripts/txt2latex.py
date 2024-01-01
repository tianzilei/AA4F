# txt to latex style
import os

def convspeak(content):
    # standard [name="{who}}"]{content}”
    # to \speak{who} content
    for i in range(len(content)):
        if content[i][0] == '[':
            content[i] = content[i].replace('[name="', '\\speak{')
            content[i] = content[i].replace('"]', '} ')
    return content

dir = 'Z:/Zilei_Tian/Arknights_Books/CW'
for txtfile in os.listdir(dir):
    if txtfile.endswith('.txt'):
        # read txtfile
        with open(os.path.join(dir, txtfile), 'r', encoding='utf-8') as f:
            content = f.readlines()
            convspeak(content)
        # write to txtfile_changed
        txtfile_changed = txtfile.replace('.txt', '_changed.txt')
        with open(os.path.join(dir, txtfile_changed), 'w', encoding='utf-8') as f:
            f.writelines(content)
