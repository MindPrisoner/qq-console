# QQ Console Agent

一个基于 **QQ 机器人 + OpenClaw + Codex** 的远程控制台原型项目。  
目标是：在手机 QQ 上发送命令，远程查看项目、启动任务、查看日志、停止任务，并把只读代码分析能力接到 Codex 上。

> 当前状态：**可用原型 / MVP**
>
> 已完成：
> - QQ 机器人单聊接入
> - 多文件结构重构
> - OpenClaw 控制台 agent（`qqconsole`）
> - 命令式控制台能力：`#help`、`#time`、`#pwd`、`#projects`
> - 后台任务能力：`#run`、`#ps`、`#logs`、`#stop`
> - 真实项目巡检任务：`webclean_snapshot`
> - Codex 只读分析命令：`#code <project> <prompt>`

---

## 1. 项目简介

这个项目不是普通聊天 bot，而是一个 **远程开发 / 实验控制台**：

- **QQ 机器人**：作为移动端入口
- **Python 桥接程序**：接收 QQ 消息并分发命令
- **OpenClaw**：作为 Agent / 工具调度层
- **Codex CLI**：作为代码分析层（当前为只读模式）

适合的使用场景：

- 上课或外出时，用手机 QQ 远程查看电脑上的项目状态
- 启动一个预设任务并查看日志
- 对指定项目进行快速只读分析
- 做 Agent / 自动化控制台的原型验证

---

## 2. 当前已支持能力

### 基础控制台命令
- `#help`：查看帮助
- `#time`：查看服务器时间
- `#pwd`：查看当前工作目录
- `#projects`：查看项目总目录内容

### 任务管理命令
- `#run <task_name>`：启动一个预设任务
- `#ps`：查看任务状态
- `#logs <task_name>`：查看任务日志
- `#stop <task_name>`：停止一个正在运行的任务

### Codex 命令
- `#code <project_name> <prompt>`：对指定项目执行 **只读分析**
  - 当前模式：`codex exec -s read-only`
  - 典型用途：总结结构、分析阅读顺序、解释模块职责

---

## 3. 当前项目结构

```text
qq_console/
├── __init__.py
├── main.py
├── config.py
├── commands/
│   ├── __init__.py
│   ├── basic.py
│   ├── router.py
│   ├── tasks.py
│   └── codex.py
├── qq/
│   ├── __init__.py
│   ├── client.py
│   ├── gateway.py
│   └── sender.py
├── services/
│   ├── __init__.py
│   ├── process_manager.py
│   ├── task_registry.py
│   └── codex_runner.py
├── storage/
│   ├── __init__.py
│   └── task_store.py
├── scripts/
│   ├── demo_task.py
│   └── project_snapshot.py
└── data/
    ├── tasks.json
    ├── logs/
    └── reports/
```

### 模块职责说明

#### `main.py`
项目入口。  
负责初始化任务存储，并启动 QQ 控制台客户端。

#### `config.py`
统一管理项目配置，例如：
- QQ 机器人凭证
- 项目路径映射
- 数据文件路径
- OpenClaw agent 名称
- 时区等

#### `qq/`
负责 **QQ 通信层**：

- `gateway.py`：获取 Access Token、获取 QQ Gateway 地址、构造 Identify、心跳
- `sender.py`：向 QQ 单聊回发消息
- `client.py`：接收 QQ 消息、调用命令路由、必要时调用 OpenClaw 或 Codex

#### `commands/`
负责 **命令解析层**：

- `basic.py`：固定基础命令（`#help`、`#time`、`#pwd`、`#projects`）
- `tasks.py`：任务类命令（`#run`、`#ps`、`#logs`、`#stop`）
- `codex.py`：Codex 命令（`#code`）
- `router.py`：总路由器，负责把命令分发到不同处理模块

#### `services/`
负责 **具体执行层**：

- `task_registry.py`：任务白名单 / 任务菜单定义
- `process_manager.py`：后台任务启动、状态判断、日志读取、停止任务
- `codex_runner.py`：调用 Codex CLI 执行只读分析

#### `storage/`
负责 **任务状态持久化**：

- `task_store.py`：读写 `tasks.json`

#### `scripts/`
放实际要执行的小脚本：

- `demo_task.py`：最小演示任务
- `project_snapshot.py`：真实项目巡检任务，生成项目快照报告

#### `data/`
存放运行过程中产生的数据：

- `tasks.json`：任务账本
- `logs/`：日志文件
- `reports/`：巡检报告

---

## 4. 已实现的真实任务

### `webclean_snapshot`
对 `webclean_mini` 项目做一次真实巡检，输出：
- 顶层目录结构
- README 检测结果
- 文件类型统计
- Markdown 报告路径

### `webclean_snapshot_slow`
与 `webclean_snapshot` 类似，但会故意慢速运行，便于测试 `#stop`

### `codex_test_snapshot`
对 `codex_test` 项目生成快照报告

---

## 5. 环境准备

### Python
推荐：
- Python 3.11+

### 依赖安装
```bash
pip install -r requirements.txt
```

### QQ 机器人配置
项目默认从 `.env.qqconsole` 读取控制台 QQ 机器人凭证：

```env
QQ_APP_ID=your_app_id
QQ_APP_SECRET=your_app_secret
```

> 注意：
> - 不要把真实的 `AppSecret` 提交到 GitHub
> - 建议把 `.env.qqconsole` 加入 `.gitignore`

---

## 6. OpenClaw 相关要求

本项目默认要求你本地已经正确安装并配置：

- OpenClaw
- 一个用于控制台的独立 agent：`qqconsole`
- 受限的 exec 策略 / 白名单
- 正常运行的 Gateway

项目当前默认使用：
- `OPENCLAW_AGENT = "qqconsole"`

### 推荐思路
把 OpenClaw 当成：
- Agent 路由层
- 工具调度层
- 命令式控制台的一部分

而不是普通聊天 bot。

---

## 7. Codex 相关要求

本项目当前已经支持通过 `#code` 调用 Codex CLI 做 **只读分析**。

### 当前模式
- `codex exec`
- `read-only sandbox`

### 已踩过的环境问题
如果系统里长期设置了：

```bash
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

可能会导致 Codex 被重定向到 DashScope 并出现 401。

### 当前解决方式
在 `codex_runner.py` 中调用 Codex 前，会临时移除：

- `OPENAI_BASE_URL`

这样不会影响 OpenClaw 的正常工作，同时 Codex 能恢复走自己的 OpenAI / ChatGPT 登录路径。

---

## 8. 启动方式

当前控制台启动命令：

```bash
python -m qq_console.main
```

启动后，QQ 机器人即可在单聊中接收命令。

---

## 9. 示例命令

### 基础命令
```text
#help
#time
#pwd
#projects
```

### 任务命令
```text
#run webclean_snapshot
#ps
#logs webclean_snapshot
#stop webclean_snapshot_slow
```

### Codex 命令
```text
#code webclean_mini 用中文一句话总结这个项目
#code codex_test 用中文简要说明这个项目适合从哪里开始阅读
```

---

## 10. 当前项目特点

### 优点
- 已经不是单文件脚本，而是清晰的多文件结构
- QQ 单聊入口已打通
- 可以远程启动真实任务并查看状态 / 日志
- 可以通过 Codex 做只读代码分析
- 已经具备“远程开发控制台”的雏形

### 当前限制
- `#code` 目前只做只读分析，不会修改代码
- 任务系统还是白名单任务，不支持任意任务自由执行
- 任务状态账本会保留历史记录，尚未做更精细的清理策略
- 还没有做权限分级、用户鉴权增强、任务并发控制
- 还没有正式接入 ACP 版 Codex / OpenClaw 多 agent 编排

---

## 11. 下一步可继续做的方向

后续继续开发时，可以优先做这些：

### 任务系统
- 更完善的任务生命周期管理
- 更好的日志切分与查询
- 任务历史清理策略
- 多任务并发管理

### Codex 集成
- `#code-plan`
- `#code-review`
- `#code-edit`（谨慎开放）
- 输出结果写入文件
- 更好的项目白名单与权限控制

### Agent 化增强
- 把部分复杂任务交给 OpenClaw 子 agent
- 引入 ACP 版 Codex
- 做更完整的开发控制台 / 实验管家

---

## 12. 免责声明

这是一个用于学习、测试和原型验证的远程控制台项目。  
在把它用于更真实的远程开发、任务调度或代码修改前，建议继续加强：

- 权限隔离
- 白名单控制
- 用户鉴权
- 日志审计
- 异常恢复
