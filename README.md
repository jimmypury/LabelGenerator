# LabelGenerator

一个标签生成器，使用python写的，原本是一个闭源模块，给一个小公司生成资产管理标签，现在将其简化版本开源。

## 特性

- 支持生成各种大小和格式的标签
- 支持添加文本、条形码和二维码元素
- 提供灵活的字体管理系统，支持系统和自定义字体
- 灵活的坐标系统，可精确定位各元素位置
- 全面的日志记录功能
- 兼容各种操作系统

## 安装

目前没有提交pypi，只能从源码安装：

```bash
git clone https://github.com/jimmyho/labelgenerator.git
cd labelgenerator
pip install -e .
```

## 使用方法

### 基本用法

```python
from LabelGenerator import LabelDocument, LabelPage, LabelText

# 创建文档
doc = LabelDocument()

# 创建页面
page = LabelPage()
page.set_size(100, 50)  # 设置页面大小（毫米）

# 添加文本元素
text = LabelText()
text.set_location(10, 10)  # 设置位置（点）
text.set_text("Hello World")
text.set_font("Arial", 12)
page.add_element(text)

# 将页面添加到文档
doc.add_page(page)

# 导出PDF
doc.export_pdf("label.pdf")
```

### 添加条形码

```python
from LabelGenerator import LabelBarcode

# 创建条形码
barcode = LabelBarcode()
barcode.set_location(10, 30)
barcode.set_size(80, 20)
barcode.set_data("1234567890")
barcode.set_barcode_type("code128")
barcode.enable_text(True)
page.add_element(barcode)
```

### 添加二维码

```python
from LabelGenerator import LabelQRCode

# 创建二维码
qrcode = LabelQRCode()
qrcode.set_location(10, 60)
qrcode.set_size(30, 30)
qrcode.set_data("https://example.com")
page.add_element(qrcode)
```

### 批量生成标签

查看 `examples/assets/template.py` 获取从CSV数据批量生成标签的示例。

## API 文档

### LabelDocument

标签文档类，用于创建和管理PDF标签文档。

### LabelPage

标签页类，用于创建和管理PDF页面。

### LabelText

文本元素类，用于创建和管理标签中的文本。

### LabelBarcode

条形码元素类，用于创建和管理标签中的条形码。

### LabelQRCode

二维码元素类，用于创建和管理标签中的二维码。

### FontManager

字体管理类，用于查找和注册系统字体。

## 许可证

MIT License
