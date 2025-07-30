# PyPI 发布指南

本指南将帮助您将 agentrix 项目发布到 PyPI。

## 准备工作

### 1. 注册 PyPI 账户

1. 访问 [PyPI](https://pypi.org/account/register/) 注册账户
2. 访问 [TestPyPI](https://test.pypi.org/account/register/) 注册测试账户

### 2. 创建 API Token

1. 登录 PyPI，进入 "Account settings" → "API tokens"
2. 点击 "Add API token"
3. 选择 "Entire account (all projects)" 或 "Scope to specific project"
4. 复制生成的 token（格式：`pypi-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

### 3. 配置认证

创建 `~/.pypirc` 文件（或复制 `.pypirc.template` 并重命名）：

```bash
cp .pypirc.template ~/.pypirc
```

编辑 `~/.pypirc` 文件，替换为您的实际 token：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-actual-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

## 发布步骤

### 方法一：使用自动化脚本（推荐）

```bash
# 给脚本执行权限
chmod +x scripts/publish.py

# 运行发布脚本
python scripts/publish.py
```

脚本会引导您完成以下步骤：
1. 清理旧的构建文件
2. 检查包配置
3. 构建包
4. 选择是否先上传到 TestPyPI
5. 上传到正式 PyPI

### 方法二：手动发布

#### 1. 清理构建文件

```bash
rm -rf build/ dist/ *.egg-info/
```

#### 2. 检查包配置

```bash
uv check
```

#### 3. 构建包

```bash
uv build
```

#### 4. 上传到 TestPyPI（可选，推荐）

```bash
uv publish --index testpypi
```

检查 TestPyPI：https://test.pypi.org/project/agentrix/

#### 5. 上传到正式 PyPI

```bash
uv publish
```

检查 PyPI：https://pypi.org/project/agentrix/

## 版本管理

### 更新版本号

编辑 `src/agentrix/__init__.py` 文件中的 `__version__`：

```python
__version__ = "0.1.1"  # 从 0.1.0 更新到 0.1.1
```

### 版本号规范

遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)：

- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

## 常见问题

### 1. 包名冲突

如果 `agentrix` 包名已被占用，需要修改 `pyproject.toml` 中的 `name` 字段：

```toml
name = "agentrix-mcp"  # 或其他可用名称
```

### 2. 认证失败

检查 `~/.pypirc` 文件：
- 确保 token 正确
- 确保文件权限正确（600）
- 确保没有多余的空格或换行

### 3. 构建失败

检查项目结构：
- 确保所有必要的文件都在 `src/agentrix/` 目录下
- 确保 `__init__.py` 文件存在
- 确保依赖项在 `pyproject.toml` 中正确声明

### 4. 上传失败

常见原因：
- 网络连接问题
- PyPI 服务暂时不可用
- 包名已被占用
- 版本号已存在

## 发布后验证

### 1. 安装测试

```bash
# 从 TestPyPI 安装（如果使用了）
pip install --index-url https://test.pypi.org/simple/ agentrix

# 从正式 PyPI 安装
pip install agentrix
```

### 2. 功能测试

```bash
# 测试 CLI 命令
agentrix --help

# 测试基本功能
agentrix search test
```

### 3. 检查 PyPI 页面

访问 https://pypi.org/project/agentrix/ 确认：
- 包信息正确显示
- 描述和文档链接正确
- 依赖项列表正确

## 维护

### 更新包

1. 修改代码
2. 更新版本号
3. 更新 CHANGELOG.md（如果有）
4. 运行发布流程

### 删除包

⚠️ **注意**：删除包是不可逆操作，请谨慎操作。

```bash
# 删除特定版本
uv publish --delete 0.1.0

# 删除整个包（需要联系 PyPI 管理员）
```

## 相关链接

- [PyPI 官方文档](https://packaging.python.org/tutorials/packaging-projects/)
- [TestPyPI 文档](https://test.pypi.org/help/)
- [语义化版本控制](https://semver.org/lang/zh-CN/)
- [Python 打包用户指南](https://packaging.python.org/guides/) 