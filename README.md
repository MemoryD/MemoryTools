## Memory Tools V1.6.0

> 2020/3/26 更新

---

#### 软件功能

- **复制翻译**：翻译剪切板的文本，并弹框显示结果。
    - **中文-->英文**：中文翻译成英文，如果复制的文本英文的比例过高，则不会翻译。
    - **英文-->中文**：英文翻译成中文，如果复制的文本中文的比例过高，则不会翻译。
    - **英文 <-> 中文**：中英互译，检测复制的文本是哪种语言，然后翻译成另一种语言。
    - **去除换行**：如果是从pdf上复制，则每一行末尾都会加入换行，结果就不准确，开启去除换行可以避免。
    - **严格模式**：默认使用语言自动检测，如果开启严格模式，则将设置源语言。（可以在谷歌翻译上试一下，在中英文混排时可能有一点差异）

- **OCR识别**：对剪切板中的图片进行OCR识别，并弹框显示。
    - **识别：文本**：识别普通的文本。
    - **识别：公式**：可以识别公式，并转换成 Latex 代码。（准确率emmm...）
    - **去除换行**：是否去除识别后文本中的换行。识别公式时，此项不起作用。

- **休息提醒**：在你工作一段时间以后，提醒你该休息了。
    - **更改时间**：提醒时间默认90分钟，可以自己更改。

---

#### 软件说明

1. 每次退出会保存程序的配置，下次启动时自动载入。
2. 复制翻译使用谷歌翻译的接口。
3. 如果翻译后的结果与未翻译时一样，则不会显示。
4. OCR使用百度AI开放平台的接口，每天有一定的次数限制。
5. 当OCR设置为识别公式时，仍然可以识别文本，但是可能会发生意料之外的错误。
6. 请按时休息 :smile:。

---

#### 关于作者

1. 作者：Memory
2. 邮箱：memory_d@foxmail.com