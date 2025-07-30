# lolicon-api

一个更简单的[lolicon API](https://docs.api.lolicon.app/#/setu)调用方法

## 安装

```bash
pip install lolicon-api
```

## 使用

本库十分简单，仅有两个主要函数：`fetch()`和`download_image()`。
```python
import lolicon_api

# 获取图片
data = lolicon_api.fetch(tags=[...], num=5)

# 下载图片
lolicon_api.download_image(data[0]['urls']['original'], save_path='path/to/save/image.jpg')
```

## 参数说明
几乎与文档参数保持一致，可以在[lolicon API文档](https://docs.api.lolicon.app/#/setu?id=%e8%af%b7%e6%b1%82)中找到。
