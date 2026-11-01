# Qumge Skills

[English](README.md) | [简体中文](README.zh-CN.md)

两个 skill，共用一个托管 MCP：使用现有能力，或将自己项目中的工作流发布为能力。

| Skill | 适用人群 | Agent 做什么 |
|---|---|---|
| **qumge** | 能力买家与模型用户 | 查找和调用付费 Cap、安装目录中的 skill、接入模型客户端、查询消费余额。 |
| **qumge-publish** | 开发者与能力提供方 | 分析项目、准备完整结果合同、运行离线预检、适配和部署、测试、发布或管理已有 Cap。 |

## 安装

原有使用者入口及安装命令保持兼容：

```bash
npx skills add Qumge/qumge-skill
```

单独安装开发者 skill：

```bash
npx skills add Qumge/qumge-skill --full-depth --skill qumge-publish
```

`--full-depth` 很重要：安装器可能在找到根目录的 SKILL.md 后停止继续发现，只显示 qumge。也可以直接指定开发者 skill 所在目录：

```bash
npx skills add https://github.com/Qumge/qumge-skill/tree/main/skills/qumge-publish
```

只查看两个入口，不安装：

```bash
npx skills add Qumge/qumge-skill --full-depth --list
```

同时安装两个：

```bash
npx skills add Qumge/qumge-skill --full-depth --skill qumge qumge-publish
```

需要支持 SKILL 格式的 Agent。开发者 skill 附带的离线检查器需要 Python 3.10+。安装 skill 不会安装服务运行环境，也不会自动托管本地 CLI。

## 使用 Qumge

客户端支持 MCP 时，连接现有服务：

```bash
claude mcp add --transport http qumge https://qumge.com/mcp
```

其他客户端配置见 [Qumge MCP 中文说明](https://github.com/Qumge/qumge-mcp/blob/main/README.zh-CN.md)。两个 skill 共用同一个服务地址、账户和密钥。优先使用 MCP；开发者 skill 自带 HTTP 与认证参考，无需先安装使用者 skill。

使用者可以这样说：

> 帮我找一个能总结这个视频的能力，先告诉我交付内容和价格。

Agent 会在付费调用前读取实际交付内容、计价方式和消费授权范围。模型推理走兼容的模型 API；`list_models` 用于发现模型，不通过 MCP 执行推理。

开发者可以这样说：

> 分析这个项目，准备一个交付完整结果的 Cap。先做本地预检；沿用我已有的部署和发布授权，只询问缺少的定价或访问权限。

两个 skill 的说明、提问与面向用户的报告跟随用户语言，可使用中文或英文。工具名、命令、标识符、JSON 字段及协议值保持原样。SKILL.md 与技术参考保留英文规范，避免两套执行规则产生偏差。

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
