# Qumge — 为你的 Agent 找到能力

[English](README.md) | [简体中文](README.zh-CN.md)

给 Agent 一个任务，找到合适能力，先看交付内容和价格，再决定是否执行。

## 从这里开始：安装、确认、免费搜索

安装 skill 和搜索能力不需要 Qumge 账户、API 密钥或充值，也不会更换你现有的 Agent 或模型。

### 1. 在你的项目中安装

先准备支持 skill 的编程 Agent、[Node.js LTS](https://nodejs.org/)（含 npm/npx）和 [Git](https://git-scm.com/downloads)。可运行 `node --version`、`npx --version`、`git --version` 检查。在你使用 Agent 的**项目目录**中打开终端。

根据你的 Agent，**选择一条**命令：

**Codex**

```bash
npx skills add Qumge/qumge-skill --skill qumge --agent codex
```

**Claude Code**

```bash
npx skills add Qumge/qumge-skill --skill qumge --agent claude-code
```

**Cursor**

```bash
npx skills add Qumge/qumge-skill --skill qumge --agent cursor
```

其他兼容 Agent 可以使用原有命令，出现选择时选你正在使用的 Agent：

```bash
npx skills add Qumge/qumge-skill
```

首次运行 npx 可能询问是否下载包，确认包名是 `skills` 后继续。若找不到 npx，请先安装 Node.js 并重新打开终端。如果安装器询问范围，选择 **Project（当前项目）**，不要选 Global。按此流程只安装到当前项目；在其他项目使用时需要在那里安装。

只使用 ChatGPT 或 Claude 网页版？请使用 [MCP 连接器指南](https://qumge.com/zh/docs/connect)，不要在网页聊天框运行 npx。

### 2. 确认安装成功

安装器应显示 `Installation complete` 和 `qumge`。检查 `.agents/skills/qumge/SKILL.md` 或安装器提示的 Agent 专用位置是否存在。回到**同一个项目**的 Agent；如果看不到新技能，重新打开会话。Codex 可用 `$qumge` 显式选中它。

### 3. 免费找到第一个能力

在 Agent 聊天框说：

> 用 Qumge 找会议纪要能力，告诉我需要提供什么、交付什么和价格，先不要执行。

Agent 应给出合适能力及输入、完整交付和价格，或者明确说明没有合适结果。仅搜索无需登录或充值。比如，YouTube 内容概览需要受支持的公开视频链接；生成视频不能替代总结视频。

[浏览能力市场](https://qumge.com/zh/caps) · [分步安装指南](https://qumge.com/zh/docs/install)

## 还需要配置 MCP 吗？

**qumge skill** 是操作指引，**Qumge MCP** 是托管工具连接。支持 HTTP 工具的编程 Agent 可以按自带 HTTP 参考搜索，无需另配 MCP。希望使用原生 MCP 工具，或客户端没有 HTTP 工具时，再看 [MCP 接入说明](https://github.com/Qumge/qumge-mcp/blob/main/README.zh-CN.md)。安装 skill 不会自动修改 MCP 配置。

只有选好付费任务和预算后，Agent 才应请求登录授权及可用余额。两个 skill 的说明和面向用户的报告跟随用户语言，可使用中文或英文；命令、工具名与协议字段保持原样。

## 开发者：发布你自己的能力

| Skill | 适用人群 | 用途 |
|---|---|---|
| **qumge** | 能力使用者 | 查找和调用 Cap、安装目录中的 skill、发现模型、查询余额。 |
| **qumge-publish** | 能力提供方 | 分析项目、定义完整结果合同、预检、适配和部署，在授权范围内测试和发布。 |

需要发布时，再安装开发者入口：

```bash
npx skills add Qumge/qumge-skill --full-depth --skill qumge-publish
```

`--full-depth` 用于继续发现根目录 SKILL.md 以下的 skill。也可直接指定目录：

```bash
npx skills add https://github.com/Qumge/qumge-skill/tree/main/skills/qumge-publish
```

只查看两个入口：`npx skills add Qumge/qumge-skill --full-depth --list`。同时安装两个时，在原有命令后加 `--full-depth --skill qumge qumge-publish`。

两个 skill 共用同一账户与托管地址 `https://qumge.com/mcp`。开发者入口独立可用，其离线检查器需要 Python 3.10+；安装不会增加服务运行环境，也不会自动托管本地 CLI。模型推理走兼容模型 API，`list_models` 只用于发现。

## 发布流程包含什么

1. 检查现有 API、MCP 工具、业务函数或 CLI，以及原生任务系统。
2. 明确一种输入与一个完整、可用的结果；中间辅助步骤在提供方内部编排。
3. 仅在必要时生成或适配项目的 manifest 和轻量接口。
4. 运行附带的**离线就绪检查器**，保存可操作的本地 JSON 报告。
5. 使用项目已有工具部署，再通过 MCP 注册或更新草稿。
6. 运行平台检查，区分 fixture 与真实交付，在已有授权范围内发布。
7. 中断后先核对实际生效和待生效状态，再恢复流程，报告版本与阻塞项。

平台已有 `publish_cap`、`test_cap` 和 `submit_cap`。此 skill 不新建账户、钱包、订单系统、MCP 服务或通用云执行环境。

### 运行本地预检

在已安装的 **qumge-publish** 目录中运行：

```bash
python3 scripts/preflight.py /absolute/project/qumge.json \
  --slug your-cap-slug --report /absolute/project/.qumge/preflight-01.json
```

仅使用 Python 标准库，无需账户、密钥、额外依赖或网络。脚本读取 manifest，只创建指定的新报告文件，或向终端输出 JSON。

退出码 `0` 表示所列本地检查通过，`1` 表示存在阻塞，`2` 表示用法或报告写入错误。每次使用新的报告文件名；不会覆盖已有报告或 manifest。文件原始字节的指纹可用于判断本地内容是否变化。

它不替代完整 JSON Schema 或服务器验证，也不证明部署可用、价格已批准或真实交付完成；报告会将这些项目列为 `not_checked`。模板中的 example.com 地址是占位符，替换后才可能通过检查。样例价格不代表开发者已授权；未实现持久恢复时，不应声称具备原生幂等能力。

### 已有项目如何接入

- 已能交付完整结果的 API 或 MCP：复用接口，映射到托管执行。
- 多个局部工具：在服务端内部编排为完整结果操作。
- 只有 CLI 或函数：增加轻量 HTTPS 接口，并选择真实服务器或容器部署。
- 依赖桌面或 GPU：先确认目标环境能实际运行任务。

认证、异步任务读取、持久化请求去重与私有结果隔离，需要在提供方原生流程中验证。开发者适配参考中链接了维护中的 Ruby adapter 和隔离 fixture 合同包。它们是接入示例，不代表自动托管或已经生成真实业务结果。

## 常见问题

**需要同时安装两个 skill 吗？** 不需要。使用者安装 qumge，开发者可以单独安装 qumge-publish；两者使用同一个 MCP。

**预检通过就能上线吗？** 还需要部署、平台验证，以及相应的定价、付费测试和发布授权。不同验证阶段会分别报告。

**会自动上传密钥或发布本地项目吗？** 离线预检不联网、不读取凭据文件、不调用项目代码。后续部署和发布沿用已有授权，缺失的授权需补齐。

**中文用户需要另一份 SKILL.md 吗？** 不需要。Agent 按用户语言交流，机器协议和执行规范保持一份。

## 文件与维护

- [SKILL.md](SKILL.md)：原有使用者入口，名称 qumge。
- [API 参考](references/api-reference.md)：平台 HTTP 与工具参考。
- [qumge-publish](skills/qumge-publish/SKILL.md)：独立开发者 skill，包含检查器、模板和恢复指引。
- [旧接入指南入口](references/build-a-capability.md)：保留兼容路径，指向开发者 skill。
- [manifest 示例](references/qumge.example.json)：保留兼容路径，与 v2 模板同步。
- [marketplace.json](marketplace.json)：声明两个入口，无需新仓库或 MCP 服务。

本地检查：`python3 -m unittest discover -s tests -v`、`python3 scripts/check-package.py`。

线上元数据检查：`bash scripts/check-tools.sh`，不会调用付费或发布工具。

Qumge：https://qumge.com · Agent 索引：https://qumge.com/llms.txt

## 许可

MIT
