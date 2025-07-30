# 前端开发提示词智能助手 MCP

## 项目简介

这是一个专为前端开发团队设计的Model Context Protocol (MCP)服务器，主要功能包括：

1. **智能提示词管理**：管理和应用标准化的开发提示词
2. **Vue组件生成**：基于团队编码规范生成标准组件
3. **组件复用助手**：快速定位和复用项目中的现有组件
4. **使用效果追踪**：记录AI工具使用情况和效果反馈

## 🚀 快速开始 (推荐)

### 1. 安装

```bash
# 从Git仓库直接安装
pip install git+https://github.com/ursazoo/frontend-dev-assistant-mcp.git
```

如果遇到权限问题，可以尝试用户模式安装:

```bash
pip install --user git+https://github.com/ursazoo/frontend-dev-assistant-mcp.git
```

### 2. 配置

在你的项目根目录或全局`~/.cursor`目录下，创建`mcp.json`文件：

```json
{
  "mcpServers": {
    "frontend-dev-assistant": {
      "command": "frontend-dev-assistant"
    }
  }
}
```

### 3. 使用

重启Cursor后，即可在聊天中使用。例如：

- `"请帮我获取git_commit提示词模板"`
- `"帮我生成一个Vue3的用户表格组件"`

### 4. 更新

```bash
# 获取最新版本
pip install --upgrade git+https://github.com/ursazoo/frontend-dev-assistant-mcp.git
```

## 📁 项目结构

项目遵循标准的Python包布局。

- `src/frontend_dev_assistant`: 核心源代码
- `docs`: 详细文档
- `scripts`: 辅助脚本
- `tests`: 测试文件

## 🧪 功能测试

```bash
# 运行功能测试 (确保已安装依赖)
python tests/test_server.py
```

## ✨ 主要功能

### 提示词模板

- **代码提交助手**：智能分批次提交代码
- **Code Review**：基于团队规范进行代码审查
- **组件复用**：快速定位和复用现有组件
- **Vue组件生成**：基于编码规范生成标准组件

### 组件生成器

支持生成以下类型的Vue组件：

- 表单、表格、弹窗、通用业务组件

### 使用统计

- 工具使用频率统计
- 团队成员活跃度分析
- 使用效果反馈收集

## 📚 详细文档

更详细的说明、配置和使用示例，请查看`docs`目录下的相关文档：

- **[团队分发指南.md](docs/团队分发指南.md)**: 如何将此工具分发给团队。
- **[MCP使用手册.md](docs/MCP使用手册.md)**: MCP协议和工具的详细用法。

## 📞 技术支持

- **命令找不到?**: 确认pip安装路径在系统PATH中，或使用`python -m frontend_dev_assistant`。
- **其他问题**: 请在项目的GitHub Issues中提出。
