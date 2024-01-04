import os
import re
import pandas as pd
import shutil
import wave
import azure.cognitiveservices.speech as speechsdk
wkdir = os.getcwd()
juqing = r"ArknightsGameData\zh_CN\gamedata\story\activities"
guanqia = r"ArknightsGameData\zh_CN\gamedata\story\[uc]info\activities"
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
id = 'act28side'

# 清理temp文件夹，不然会一直append
if os.path.exists(os.path.join(wkdir, 'temp')):
    # delete temp folder
    shutil.rmtree(os.path.join(wkdir, 'temp'))
    # create temp folder
    os.makedirs(os.path.join(wkdir, 'temp'))
else:
    os.makedirs(os.path.join(wkdir, 'temp'))

# 先把文件写到一起，操作一个文件要方便一些
def formattext(id):
    # 手动建立一个同名csv文件，第一个是顺序，因为游戏资源里面的文件名不是按照顺序排列的，第二个是文件名+后缀(要path.join用)
    df = pd.read_csv(os.path.join(wkdir,'scripts', id+'.txt'), index_col=0, header=0)
    # for循环，把所有文件写到一起
    with open(os.path.join(wkdir, 'temp', id+'.txt'), 'a', encoding='utf-8') as a:
        for i in range(len(df)):
            with open(os.path.join(wkdir, guanqia, id, df['filename'][i+1]), 'r', encoding='utf-8') as f:
                text = f.read()
                # append text to file
                a.write(text)
            with open(os.path.join(wkdir, juqing, id, df['filename'][i+1]), 'r', encoding='utf-8') as f:
                text = f.read()
                a.write(text)

# 第一次简单清洗，把不需要的行删掉
# header太多了，建立了一个txt文件，把header写进去，然后用这个函数清理
# file即为header.txt，text即为要清理的文本
def clear(file, text):
    import re
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if text.strip().lower().startswith(line.strip().lower()):
                text = ''
            # elif text not containes Chinese characters, remove it
            elif not re.search(r'[\u4e00-\u9fa5]', text):
                text = ''
    # if text contains 'text="', keep between 'text="' and '",'
    if re.search(r'text="', text):
        text = re.search(r'text="(.*)",', text).group(1)
        # keep <i>(.*)</i>
        text = re.sub(r'<i>(.*)</i>', r'\1', text)
        # keep <color*>(.*)</color
        text = re.sub(r'<color.*>(.*)</color.*', r'\1', text)
        # delete from '", ' to the end
        text = re.sub(r'", .*', '', text)
        text = text + '\n'
    # if text contains '[HEADER', remove from '[HEADER' to the end
    if re.search(r'\[HEADER', text):
        text = re.sub(r'\[HEADER.*', '', text)
    # if text contains 'Dr.{@nickname}', replace it with '博士'
    if re.search(r'Dr.{@nickname}', text):
        text = re.sub(r'Dr.{@nickname}', '博士', text)
    return text

# copilot写的，基本上就是判断这两行是不是同一个说话人，如果是的话就合并
# 这个function在clearline(id)用到
# 这个地方本来是想写成把整个文本读进去，但是不太成功，所以就先这样了
def process_lines(lines, i, pattern):
    try:
        name1 = re.search(pattern, lines[i]).group(1) if re.search(pattern, lines[i]) else ''
    except:
        name1 = ''
    try:
        name2 = re.search(pattern, lines[i+1]).group(1) if re.search(pattern, lines[i+1]) else ''
    except:
        name2 = ''
    if name1 == name2:
        lines[i] = lines[i].replace('\n', '')
        lines[i+1] = re.sub(pattern, '', lines[i+1])
    return lines

# 这个是要执行的function
# 我也不想function套function
# 下次再改吧
def clearline(id):
    # 先根据header清理一下
    with open(os.path.join(wkdir, 'temp', id+'.bak.txt'), 'w', encoding='utf-8') as b:
        with open(os.path.join(wkdir, 'temp', id+'.txt'), 'r', encoding='utf-8') as a:
            for line in a:
                # header是基本固定的，如果出现问题也要根据实际情况写一下header
                b.write(clear(os.path.join(wkdir, 'scripts\header.txt'), line))
    # 再把同一个人的对话合并一下
    with open(os.path.join(wkdir, 'temp', id+'.xml'), 'w', encoding='utf-8') as f:
        with open(os.path.join(wkdir, 'temp', id+'.bak.txt'), 'r', encoding='utf-8') as a:
            lines = a.readlines()
            # 分成两种情况，一种是[name=，一种是[multiline
            # 但是还有一种是玩家选择的，没有做，从实际情况来讲这行去掉了也不影响阅读体验，下次再补充
            for i in range(len(lines)):
                if lines[i].startswith('[name='):
                    lines = process_lines(lines, i, r'\[name="(.*)"\]')
                if lines[i].startswith('[multiline'):
                    lines = process_lines(lines, i, r'\[multiline.*name="(.*)".*\]')
                # write to file
                f.write(lines[i])
    # repeat the above process until id_xml.txt not changed
    while True:
        with open(os.path.join(wkdir, 'temp', id+'.bak.txt'), 'w', encoding='utf-8') as b:
            with open(os.path.join(wkdir, 'temp', id+'.xml'), 'r', encoding='utf-8') as a:
                lines = a.readlines()
                for i in range(len(lines)):
                    if lines[i].startswith('[name='):
                        lines = process_lines(lines, i, r'\[name="(.*)"\]')
                    if lines[i].startswith('[multiline'):
                        lines = process_lines(lines, i, r'\[multiline.*name="(.*)".*\]')
                    # write to file
                    b.write(lines[i])
        # if id_xml.txt.bak and id_xml.txt are the same, break
        if open(os.path.join(wkdir, 'temp', id+'.bak.txt'), 'r', encoding='utf-8').read() == open(os.path.join(wkdir, 'temp', id+'.xml'), 'r', encoding='utf-8').read():
            break
        else:
            # if not the same, copy id_xml.txt.bak to id_xml.txt
            with open(os.path.join(wkdir, 'temp', id+'.bak.txt'), 'r', encoding='utf-8') as b:
                with open(os.path.join(wkdir, 'temp', id+'.xml'), 'w', encoding='utf-8') as a:
                    a.write(b.read())


# azure ssml的要求是45段话，所以要把文件分成45段话
# 如果需要的话根据这里调整一下
def split_file(filename, lines_per_file=45):
    i = 0
    with open(filename, 'r', encoding="utf8") as src_file:
        while True:
            lines = [src_file.readline() for _ in range(lines_per_file)]
            if not lines[0]:  # End of file
                break
            with open(f'{os.path.splitext(filename)[0]}_{i:02d}.txt', 'w', encoding="utf8") as dst_file:
                dst_file.writelines(lines)
            i += 1

def tossml(text):
    import xml.etree.cElementTree as ET
    import pandas as pd
    # <speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
    header = ET.Element('speak', {'version': '1.0', 'xmlns': 'https://www.w3.org/2001/10/synthesis', 'xml:lang': 'zh-CN'})
    char2voicename = pd.read_csv(os.path.join(wkdir, 'scripts', 'char2voicename.csv'), header=0, index_col=0)
    # for each line
    for line in text:
        # if line not start with '[', delete newline
        if not line.startswith('['):
            char = 'narration'
            line = line.replace('\n', '')
            ET.SubElement(header, 'voice', name=char2voicename.loc[char][0]).text = line
        if line.startswith('[name='):
            char = line.split('"')[1]
            line = line.split('"]')[1]
            # line delete newline
            line = line.replace('\n', '')
            # if line == '......', skip
            if line == '......':
                continue
            ET.SubElement(header, 'voice', name=char2voicename.loc[char][0]).text = line
        if line.startswith('[multiline'):
            char = line.split('"')[1]
            line = line.split(']')[1]
            # line delete newline
            line = line.replace('\n', '')
            # if line == '......', skip
            if line == '......':
                continue
            ET.SubElement(header, 'voice', name=char2voicename.loc[char][0]).text = line
        if line.startswith('[Image]') or line.startswith('[image'):
            line = line.split(']')[1]
            # line delete newline
            line = line.replace('\n', '')
            char = 'narration'
            ET.SubElement(header, 'voice', name=char2voicename.loc[char][0]).text = line
    # write to file
    tree = ET.ElementTree(header)
    return tree

# function to convert txt to xml
def txt2xml(txtfile, xmlfile):
    with open(txtfile, 'r', encoding='utf-8') as f:
        tree = tossml(f)
        tree.write(xmlfile, encoding='utf-8', xml_declaration=True)
    # format xml
    import xml.dom.minidom as minidom
    dom = minidom.parse(xmlfile)
    with open(xmlfile, 'w', encoding='utf-8') as f:
        f.write(dom.toprettyxml(indent='    '))

def tts(xmlpath, wavpath):
    ssml_string = open(xmlpath, "r", encoding="utf-8-sig").read()
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()
    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file(os.path.join(os.path.dirname(xmlpath), wavpath))

def combine_wav(wavdir, wavname):
    wavfiles = []
    for wav in os.listdir(wavdir):
        if wav.endswith(".wav"):
            wavfiles.append(os.path.join(wavdir, wav))
    with wave.open(os.path.join(wavdir, wavname), 'wb') as output:
        for wav in wavfiles:
            with wave.open(wav, 'rb') as w:
                if not output.getnframes():
                    output.setparams(w.getparams())
                output.writeframes(w.readframes(w.getnframes()))

# function都在上面了，下面开始执行
# 生成单独一个文件
formattext(id)
clearline(id)
# 到文件夹里面
if not os.path.exists(os.path.join(wkdir, 'temp', id)):
    os.makedirs(os.path.join(wkdir, 'temp', id))
shutil.copyfile(os.path.join(wkdir, 'temp', id+'.xml'), os.path.join(wkdir, 'temp', id, id + '.xml'))
split_file(os.path.join(wkdir, 'temp', id, id+'.xml'))

# 再次清理，每行开头需要为中文字符
for xml in os.listdir(os.path.join(wkdir, 'temp', id)):
    if xml.endswith(".txt"):
        with open(os.path.join(wkdir, 'temp', id, xml), 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(os.path.join(wkdir, 'temp', id, xml), 'w', encoding='utf-8') as f:
            for line in lines:
                if re.search(r'[\u4e00-\u9fa5]', line):
                    f.write(line)

# 转换xml
for xml in os.listdir(os.path.join(wkdir, 'temp', id)):
    if xml.endswith(".txt"):
        txt2xml(os.path.join(wkdir, 'temp', id, xml), os.path.join(wkdir, 'temp', id, xml.replace(".txt", ".xml")))
        # wait until xml file is created
        while not os.path.exists(os.path.join(wkdir, 'temp', id, xml.replace(".txt", ".xml"))):
            pass
        # delete txt file
        os.remove(os.path.join(wkdir, 'temp', id, xml))

os.remove(os.path.join(wkdir, 'temp', id, id+'.xml'))
# xml to wav
'''
for xml in os.listdir(os.path.join(wkdir, 'temp', id)):
    if xml.endswith(".xml"):
        # if same name wav was already created, skip
        if os.path.exists(os.path.join(wkdir, 'temp', id, xml.replace(".xml", ".wav"))):
            continue
        wav = xml.replace(".xml", ".wav")
        tts(os.path.join(wkdir, 'temp', id, xml), wav)
        # wait until wav file is created
        while not os.path.exists(os.path.join(wkdir, 'temp', id, wav)):
            pass
'''
# combine all wav files into one in the folder
# combine_wav(os.path.join(wkdir, 'temp', id), id+'.wav')