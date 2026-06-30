# PhD Deep Read 工作流

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/phd-deepread-workflow.svg)](https://pypi.org/project/phd-deepread-workflow/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Skill-6E56CF)](https://claude.com/claude-code)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-000000)](https://openai.com/codex)
[![English](https://img.shields.io/badge/README-English-blue)](README.md)

> 将学术 PDF 转化为结构化的 Obsidian 文献笔记和批判性思维画布。

---

> *"人类的心智……通过联想运作。当它掌握一个项目时，会瞬间跳转到联想链中的下一个。"*
> — Vannevar Bush, *As We May Think*, 1945

Bush 在 1945 年就设想了这样一张书桌——你所有的阅读内容都脱离了原始容器，随时可以建立关联路径。这就是本工作流的目标。

**第一步：** 将 PDF 转换为 Markdown。知识从冻结的 PDF 中解放出来，成为你可以随时返回、搜索和连接的内容——今天、下个月、明年都可以。

**第二步：** 随时回来提取当前所需的内容。跨论文连接想法。在 Obsidian 画布中并排可视化论点、证据和假设。文献笔记记录内容，画布让你将其与其他已知内容一起审视。

---

## 前置条件

你需要同时具备：

- **支持技能的 AI 编程助手** — **Claude Code**（[在此下载](https://claude.com/claude-code)）或 **Codex**。此工作流会作为技能安装到你所使用的助手中。
- **Obsidian** — [在此下载](https://obsidian.md)。最终输出是 JSON 画布文件，仅在 Obsidian 中渲染。

如果你只需要 AI 帮助阅读 PDF，不需要此工作流。将 PDF 拖入任何 AI 聊天窗口直接提问即可。此工作流是为需要结构化文献笔记和批判性思维画布、以便在 Obsidian 中反复查阅的人设计的。

---

## 30 秒安装

将此粘贴到 **Claude Code** 或 **Codex** 中：

```
Install this skill for me: https://github.com/heleninsights-dot/phd-deepread-workflow
```

你的助手会自动安装技能、Python CLI 及所有依赖。技能会安装到该助手的技能目录（Claude Code 为 `~/.claude/skills/`，Codex 为 `~/.codex/skills/`）——如有提示请重启助手。完成。将 PDF 拖入并说 **"phd-deepread read this paper"**。

### 可选：Tesseract OCR

仅当你处理扫描版 PDF（基于图像，文本不可选中）时需要：

```bash
brew install tesseract          # macOS
sudo apt install tesseract-ocr  # Ubuntu/Debian
```

---

## 使用工作流

### 一篇论文

将 PDF 拖入 Claude Code 或 Codex 并说：

> **phd-deepread read this paper**

你的助手会提取文本，撰写结构化文献笔记，并创建 9 节点批判性思维画布——一步完成。在 Obsidian 中打开 `.canvas` 文件，并排可视化论点、证据、假设和空白。

你也可以请求特定步骤：*"phd-deepread extract this PDF, but just give me the prompt — I'll write the note myself."*

### 一个文件夹的论文

将文件夹拖入 Claude Code 或 Codex 并说：

> **phd-deepread read this folder**

你的助手会批量处理文件夹中的每个 PDF——提取文本、为每篇撰写结构化文献笔记、创建画布模板。已处理的论文自动跳过。与单篇论文一样，只是处理整个文件夹。

---

## 你能得到什么

每篇 PDF 处理后生成三个文件：

| 输出 | 说明 |
|--------|-----------|
| `paper.md` | PDF 全文，转换为 Markdown |
| `paper_literature_note.md` | 结构化文献笔记 — 见下方详细说明 |
| `paper.canvas` | 9 节点批判性思维画布 — **在 Obsidian 中打开**即可并排可视化论点、证据、假设和空白 |

### 文献笔记提取的内容

笔记不做摘要——它提取你在研究中实际需要的具体数据：

| 类别 | 提取内容 |
|----------|-------------|
| **研究发现** | 每项关键结果的方向、效应量、p 值、置信区间、效应大小及来源表/图 |
| **方法学** | 研究设计、样本量及流失率、纳入/排除标准、每项仪器/检测/软件的名称 |
| **批判评估** | 映射到效度类型（内部、外部、建构、统计结论）的局限性，以及作者未讨论的局限 |
| **知识连接** | 广泛的方法、蛋白质、基因、疾病、概念的 [[维基链接]]——将论文与你已有的笔记连接 |
| **行动项目** | 具体的、可执行的后续步骤，无需重新阅读论文即可执行 |
| **综合评估** | 创新性、证据强度和实践潜力——每项均有具体理由，而非仅仅打分 |

---

## CLI 参考

你的助手（Claude Code 或 Codex）会为你调用这些命令——你无需手动输入：

| 命令 | 功能 |
|---------|-------------|
| `doctor` | 检查所有依赖是否已安装 |
| `extract <pdf>` | 从 PDF 中提取文本和图像 |
| `generate <dir>` | 根据提取的文本构建文献笔记提示词 |
| `canvas -o <file> [--from-note <md>]` | 创建 9 节点画布；使用 `--from-note` 从已有笔记填充 |
| `run <pdf>` | 完整流程：提取 → 生成提示词 → 画布 |
| `batch <dir>` | 批量处理文件夹中的所有 PDF |
| `verify <dir>` | 质量检查输出文件 |

---

## 与 Obsidian 和 Zotero 的集成

**Obsidian：** 笔记使用 YAML 前置元数据和兼容 Dataview 的标注块。画布文件通过 Obsidian Canvas 插件打开。维基链接可连接到你现有的笔记。

**Zotero：** 将你的 Zotero 引用键用作生成笔记中的 `citekey` 字段。在运行工作流之前，从 Zotero 导出 PDF 到处理文件夹。

---

## 故障排查

**"command not found: phd-deepread"** — 终端找不到安装位置。打开新的终端窗口。如果仍然缺失，将 `~/.local/bin` 添加到 PATH：

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

**"Tesseract not found"** — 仅影响扫描版 PDF：

```bash
brew install tesseract          # macOS
sudo apt install tesseract-ocr  # Ubuntu/Debian
```

**安装后出现"Template not found"** — 升级到最新版本：

```bash
pip install --upgrade phd-deepread-workflow
```

**使用虚拟环境（最干净的安装方式）**

```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# 或：venv\Scripts\activate   # Windows
pip install phd-deepread-workflow
```

---

## 贡献

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/my-feature`
3. 提交并推送，然后发起 Pull Request

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

## 支持

- 问题反馈：[GitHub Issues](https://github.com/heleninsights-dot/phd-deepread-workflow/issues)
- 电子邮件：[heleninsights@gmail.com](mailto:heleninsights@gmail.com)

---

<div align="center">
  <p>为学术社区倾心打造</p>
  <p>如果此工作流对你的研究有帮助，请在 GitHub 上给它一颗星！</p>
</div>
