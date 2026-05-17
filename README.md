# hermes-platform-napcat

Hermes Agent 的 NapCat / OneBot v11 社区平台插件

## 安装方式

### 官方方式：Hermes 插件安装

Hermes 官方插件系统会从 `~/.hermes/plugins/<name>/plugin.yaml` 和 `__init__.py` 发现目录插件。第三方插件默认只发现不加载，需要加入 `plugins.enabled`，或安装时使用 `--enable`。

```bash
hermes plugins install ByteColtX/hermes-platform-napcat --enable
hermes plugins list
```

如果不想立即启用：

```bash
hermes plugins install ByteColtX/hermes-platform-napcat --no-enable
hermes plugins enable hermes-platform-napcat
```

### 其他安装方式

本地开发目录安装：

```bash
mkdir -p ~/.hermes/plugins
ln -s "$(pwd)" ~/.hermes/plugins/hermes-platform-napcat
hermes plugins enable hermes-platform-napcat
```

项目级插件安装，仅用于可信仓库：

```bash
mkdir -p .hermes/plugins
ln -s "$(pwd)" .hermes/plugins/hermes-platform-napcat
HERMES_ENABLE_PROJECT_PLUGINS=true hermes plugins list
```

pip / uv 开发安装会通过 `hermes_agent.plugins` 入口点被 Hermes 发现：

```bash
uv sync
uv pip install -e .
hermes plugins enable hermes-platform-napcat
```

## 配置方式

### 启用插件

`~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - hermes-platform-napcat
```

### NapCat 平台配置预留

以下配置面向后续适配器实现阶段。M0 骨架不会读取或连接这些值。

在 `~/.hermes/config.yaml` 中启用平台：

```yaml
gateway:
  platforms:
    napcat:
      enabled: true
      extra:
        ws_url: ws://127.0.0.1:3001
        http_url: http://127.0.0.1:3000
        access_token: your_access_token
        home_channel: group:123456789
```

`~/.hermes/.env`:

```dotenv
NAPCAT_WS_URL=ws://127.0.0.1:3001
NAPCAT_HTTP_URL=http://127.0.0.1:3000
NAPCAT_ACCESS_TOKEN=your_access_token
NAPCAT_HOME_CHANNEL=group:123456789
NAPCAT_ALLOWED_USERS=123456789,987654321
NAPCAT_ALLOW_ALL_USERS=false
```

Shell 环境变量：

```bash
export NAPCAT_WS_URL="ws://127.0.0.1:3001"
export NAPCAT_HTTP_URL="http://127.0.0.1:3000"
export NAPCAT_ACCESS_TOKEN="your_access_token"
export NAPCAT_HOME_CHANNEL="group:123456789"
export NAPCAT_ALLOWED_USERS="123456789,987654321"
export NAPCAT_ALLOW_ALL_USERS="false"
```
