# yaml2py

將 YAML 配置檔案轉換為型態安全的 Python 類別，支援巢狀結構、列表和完整的型態提示。


## 特色功能

- 🎯 **自動生成型態提示的 Python 類別** - 從 YAML 檔案生成完整的型態安全配置類別
- 🔄 **支援巢狀結構** - 完美處理 YAML 的巢狀字典和物件
- 📝 **智慧型態推斷** - 自動識別 int、float、bool、str、list、dict 等型態
- 🔥 **熱重載支援** - 檔案變更時自動重新載入配置
- 🔒 **敏感資料保護** - 自動遮罩密碼、API 金鑰等敏感資訊
- 🔍 **智慧路徑探測** - 自動尋找專案中的配置檔案
- 💡 **IDE 友好** - 完整的自動完成和型態檢查支援
- 🎨 **單例模式** - 確保全域只有一個配置實例

## 安裝

```bash
pip install yaml2py
```

或從原始碼安裝：

```bash
git clone https://github.com/joneshong/yaml2py.git
cd yaml2py
pip install .
```

## 快速開始

### 1. 準備 YAML 配置檔案

建立 `config.yaml`：

```yaml
app:
  name: MyApplication
  version: 1.0.0
  debug: true
  
database:
  host: localhost
  port: 5432
  username: admin
  password: secret123
  options:
    pool_size: 10
    timeout: 30
    
features:
  - name: feature_a
    enabled: true
    config:
      threshold: 0.8
  - name: feature_b
    enabled: false
    config:
      threshold: 0.5
```

### 2. 生成配置類別

```bash
yaml2py --config config.yaml --output ./src/config
```

或使用互動模式（自動探測檔案）：

```bash
yaml2py
```

### 3. 在程式碼中使用

```python
from src.config.manager import ConfigManager

# 建立配置管理器（單例模式）
config = ConfigManager()

# 使用型態安全的配置
print(config.app.name)                    # MyApplication
print(config.app.debug)                   # True
print(config.database.host)               # localhost
print(config.database.options.pool_size) # 10

# 存取列表結構
for feature in config.features:
    print(f"{feature.name}: {feature.enabled}")
    
# 敏感資料自動遮罩
print(config.database.password)  # ********
```

## 進階功能

### 巢狀結構支援

yaml2py 完美支援 YAML 的巢狀結構：

```yaml
cache:
  enabled: true
  providers:
    redis:
      host: 127.0.0.1
      port: 6379
    memory:
      max_size: 1024
```

生成的程式碼支援鏈式存取：

```python
config.cache.providers.redis.host  # 完整的型態提示！
```

### 列表處理

自動為物件列表生成對應的型態：

```yaml
endpoints:
  - path: /users
    method: GET
    auth_required: true
  - path: /login
    method: POST
    auth_required: false
```

```python
for endpoint in config.api.endpoints:
    # endpoint 有完整的型態提示
    print(f"{endpoint.method} {endpoint.path}")
```

### 熱重載

當配置檔案變更時自動重新載入：

```python
# 配置會自動更新，無需重啟程式
config = ConfigManager()
# 修改 config.yaml...
# config 的值會自動更新！
```

### 型態安全

所有配置都有正確的型態：

```python
config.app.debug         # bool
config.database.port     # int
config.app.version       # str
config.features          # List[FeatureSchema]
```

## CLI 選項

```bash
yaml2py --help

選項：
  -c, --config PATH   輸入的 YAML 檔案路徑
  -o, --output PATH   生成檔案的輸出目錄
  --help             顯示說明訊息
```

## 生成的檔案結構

```
output_dir/
├── __init__.py      # 模組初始化
├── schema.py        # 配置類別定義
└── manager.py       # 配置管理器（含熱重載）
```


## 開發指南

### 執行測試

```bash
python -m pytest tests/
```

### 程式碼品質

```bash
make lint    # 執行 linting
make format  # 格式化程式碼
make test    # 執行測試
```

## 授權

MIT License - 詳見 [LICENSE](LICENSE) 檔案


## 貢獻

歡迎提交 Pull Request！請確保：

1. 更新相關測試
2. 執行 `make format` 格式化程式碼
3. 執行 `make lint` 確保無錯誤
4. 更新文件（如需要）