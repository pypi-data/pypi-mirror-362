# TongfuJigsaw - 综合工具包集合

> **包含 wecomutils & omzutils 两个核心工具包**

`tongfujigsaw` 是一个综合性的 Python 工具包集合，专为企业微信集成和通用工具功能设计。

## 📦 包含的工具包

### wecomutils - 企业微信工具包
专门用于企业微信（WeChat Work/WeCom）的集成开发，提供API调用、消息加密解密、令牌管理等功能。

### omzutils - 通用工具包  
提供数据库管理、存储服务、函数计算等通用工具功能。

## 🚀 安装

```bash
pip install tongfujigsaw
```

## Usage

### Using WeChat Work/WeCom features
```python
from wecomutils.wecom import WXApiBase
```

### Using general utilities
```python
# Direct import from omzutils
from omzutils.db_manager import DBManager
from omzutils.storage import StorageService
from omzutils.fc_service import FCService


```

## License

MIT