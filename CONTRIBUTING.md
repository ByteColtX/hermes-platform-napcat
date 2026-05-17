# Contributing to hermes-platform-napcat

感谢你的贡献！以下是开发、测试和提交的完整指南。

---

## 目录

1. [开发环境搭建](#开发环境搭建)
2. [运行测试](#运行测试)
3. [代码规范](#代码规范)
4. [项目结构](#项目结构)
5. [提交规范](#提交规范)
6. [Pull Request 流程](#pull-request-流程)
7. [常见问题](#常见问题)

---

## 开发环境搭建

### 前置要求

| 工具 | 版本 | 说明 |
| :- | :- | :- |
| Python | >= 3.11 | 运行时 |
| uv | 最新稳定版 | Python 包管理与虚拟环境 |
| git | 任意 | 版本管理 |
| NapCat | v4.18.2+ | 本地测试（可选） |

### 克隆与初始化

```bash
git clone https://github.com/ByteColtX/hermes-platform-napcat.git
cd hermes-platform-napcat

# 安装 uv（如本机尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境并同步依赖
uv sync

# 安装 git pre-commit 钩子（首次克隆后执行一次即可）
uv run pre-commit install
```

> 不需要安装完整的 Hermes Agent。项目测试通过 `conftest.py` 中的 gateway stub 隔离所有 gateway 依赖，可独立运行。

---

## Pre-commit 钩子

每次 `git commit` 时自动执行三项检查，与 CI 保持一致：

| 钩子 | 作用 |
| :- | :- |
| `ruff (lint)` | 检查代码错误、未使用导入、风格问题 |
| `ruff (format)` | 检查代码格式是否统一（不自动修改，需手动运行 `ruff format .`） |
| `pytest` | 运行全部单元测试，**测试失败则拒绝提交** |

```bash
# 手动对所有文件运行全部钩子（等价于 CI 检查）
pre-commit run --all-files

# 只运行某一项
pre-commit run ruff-lint --all-files
pre-commit run pytest --all-files

# 修复 ruff 可自动修复的问题
ruff check --fix .

# 格式化所有文件
ruff format .

# 跳过钩子提交（紧急情况，不推荐）
git commit --no-verify -m "message"
```

---

## 运行测试

测试使用 `pytest` + `pytest-asyncio`，通过 `uv` 运行，确保使用项目声明的开发依赖。

```bash
# 运行全部测试
uv run pytest

# 运行详细输出
uv run pytest -v

# 只运行某个模块
uv run pytest tests/test_<module>.py -v

# 只运行某个测试用例
uv run pytest tests/test_<module>.py::test_<case> -v

# 运行带覆盖率报告
uv add --dev pytest-cov
uv run pytest --cov=napcat_platform --cov-report=term-missing
```

后续新增测试统一放在 `tests/` 目录，文件命名为 `test_<module>.py`。

### 新增测试

1. 在 `tests/test_<module>.py` 文件中追加测试类或函数
2. 异步测试用 `@pytest.mark.asyncio` 装饰
3. Mock 网络请求用 `unittest.mock.AsyncMock`，不要发真实网络请求

---

## 代码规范

### Python 版本与风格

- 目标 Python **3.11+**，可使用 `match`、`tomllib`、`Self` 等新特性
- 遵循 **PEP 8**，行宽上限 **100** 字符，以 `ruff` 检查结果为准
- 所有公共函数、方法、类必须有 **docstring**，格式参见下方
- 所有函数参数和返回值必须有 **类型注解**

### Docstring 格式

使用 **Google 风格**：

模块文件头可以用简短 docstring 说明模块职责；只写真实边界，不重复文件名。

```python
"""解析 NapCat / OneBot v11 入站事件。"""
```

```python
def example(param1: str, param2: int = 0) -> str | None:
    """单行摘要，不超过 79 字符。

    可选的多行详细说明。说明设计决策、边界条件、
    或与外部协议的关联。

    Args:
        param1: 参数说明。
        param2: 参数说明，含默认值语义。

    Returns:
        返回值说明。为 ``None`` 时的条件也要写清楚。

    Raises:
        ValueError: 说明何时抛出。
        OneBotAPIError: 说明何时抛出。
    """
```

私有函数（`_` 前缀）可以只写单行摘要。

### 异常处理规范

- **不要**裸 `except:` 或无日志的 `except Exception: pass`
- 捕获具体异常类型（`httpx.HTTPError`、`asyncio.TimeoutError` 等）优先于 `Exception`
- 意料外的 `except Exception` 必须用 `logger.error(..., exc_info=True)` 记录完整堆栈
- 已知的、可降级的失败用 `logger.warning`

### 常量管理

- 避免在逻辑中散落魔法数字和字符串，优先提取为模块级常量
- 跨模块共享的常量再集中到 `constants.py`，命名全大写 + 下划线

### 导入顺序

导入顺序由 `ruff` 自动检查和修复，分组如下：

```python
# 1. __future__
from __future__ import annotations

# 2. 标准库
import asyncio
import json

# 3. 第三方库
import httpx
import websockets

# 4. 本地相对导入
from .constants import API_TIMEOUT
from .utils import OneBotAPIError
```

---

## 项目结构

```text
hermes-platform-napcat/
├── napcat_platform/        # Python 包入口
│   ├── __init__.py         # 包导出与命令入口预留
│   └── adapter.py          # NapCat 平台适配器预留
│
├── tests/                  # 单元测试目录
│   └── conftest.py         # pytest 共享配置预留
│
├── docs/                   # 架构、环境、功能规划文档
├── plugin.yaml             # Hermes 目录插件清单
├── pyproject.toml          # 包元数据、依赖与工具配置
├── uv.lock                 # uv 锁文件
├── .env.example            # 环境变量示例
├── .python-version         # 本地 Python 版本提示
│
├── CONTRIBUTING.md         # 本文件
├── LICENSE
└── README.md
```

### 模块职责边界

| 模块 | 职责 | 禁止 |
| :- | :- | :- |
| `napcat_platform/__init__.py` | 包导出、插件入口和命令入口 | NapCat 网络连接与业务逻辑 |
| `napcat_platform/adapter.py` | 平台适配器实现预留 | 文档规划、安装脚本逻辑 |
| `plugin.yaml` | Hermes 目录插件清单 | Python 运行逻辑 |
| `pyproject.toml` | 包元数据、依赖、ruff / pytest 等工具配置 | 业务配置和密钥 |
| `tests/` | 单元测试与测试共享配置 | 真实 NapCat / QQ 网络调用 |

---

## 提交规范

遵循 [**Conventional Commits**](https://www.conventionalcommits.org/)：

```text
<type>(<scope>): <subject>

[可选 body]

[可选 footer]
```

| Type | 含义 |
| :- | :- |
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 仅文档变更 |
| `test` | 测试相关 |
| `refactor` | 重构（非 feat / fix） |
| `perf` | 性能优化 |
| `chore` | 构建、依赖等杂项 |

示例：

```text
fix(utils): use `or` instead of `and` in API error detection

api_call raised OneBotAPIError only when BOTH retcode != 0 AND
status != "ok". A response with retcode=100 but status="ok" was
silently accepted as success. The condition is now an `or`.
```

---

## Pull Request 流程

1. **Fork** 仓库，基于 `main` 新建分支：

   ```bash
   git checkout -b fix/your-fix-name
   ```

2. **写代码** — 遵循上方规范

3. **补测试** — 新功能必须附带测试，Bug 修复必须附带回归测试

4. **本地检查**：

   ```bash
   uv run ruff check .
   uv run pytest
   ```

5. **提交**：使用 Conventional Commits 格式

6. **发起 PR**：
   - 标题与 commit 格式一致
   - 描述中说明：改了什么、为什么改、如何验证
   - 如果当前没有测试用例，在描述中写明 `pytest` 的实际输出

7. **代码审查**：响应 review 意见，并继续推送到同一分支

---

## 常见问题
