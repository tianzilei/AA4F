# AA4F
    Arknights Audiobook for SLEEP (aka 舟游沙雕动画)
    如果不能自动化，那就手动 -> 反正也要手动，干脆完全手动。

## Aims
1. ~~从ArknightsGameData获得文本~~
2. ~~大清洗~~
3. ~~先tts转一波 -> 发布（发布到森空岛了，B不让发）~~
4. 先进行LLM的复写：可用模型RWKV-4-Novel-7B、chatglm3
5. 自动生成文本对应顺序（大概是从prts.wiki获取）
4. 从prts.wiki获得语音、炼VITS（优先级下降）
6. 再洗图片、自动化视频制作 -> 发布（优先级下降）

## 正在进行的内容
1. ArknightsGameData （完成）
    `scripts\formatText.py`，详情请看usage节

    |文件夹|剧集名|剧集类型|文件数量|
    |---|---|---|---|
    |a001|骑兵与猎人|支线|20|
    |act1bossrush|引航者试炼|引航者试炼|1|
    |act1lock|荷谟伊智境|联锁竞赛|3+subfolder|
    |act1sandbox|沙中之火|生息演算|4+subfolder*3|
    |act3d0|火蓝之心|支线|25|
    |act3fun|《狂弹要塞！罗德大兵集结》||2+subfolder|
    |act4d0|战地秘闻|剧情|7|

2. 重写自动化（进行中）

## Usage
- 设置env(SPEECH_KEY和SPEECH_REGION)
- requirements.txt没写，好像只有个pandas和azure的包
- 先git clone https://github.com/Kengxxiao/ArknightsGameData 到根文件夹
- 在根文件夹`python scripts\formatText.py`，因为要读取ArknightsGameData的内容
- 执行过程中会出现各种报错，先看temp文件夹中的对应文件夹内容
- 如果报错出现了名字，如`Ace`那么就是`scripts\char2voicename.csv`里面没有这个人对应的tts[设置](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)

## 关于本仓库
- 完全没有版权，不提供任何文本
- 全靠copilot编，到处都是特性

## 额外产出
1. 电子书
    既然我都要出audiobook了，纸质版打出来才叫健全

## 相关项目
> https://learn.microsoft.com/en-us/azure/ai-services/speech-service
> https://github.com/Kengxxiao/ArknightsGameData