# WAV Loo

一个多功能Python工具，支持查找WAV文件和常用命令行alias（如kgn、gp、uv等）。

## 功能特性

- 查找WAV文件（本地/URL，递归）
- 支持命令行子命令：
  - `find`：查找WAV文件
  - `kgn`：kubectl get pods -o wide -n signal
  - `gp`：gpustat -i
  - `uv`：uv pip install -i http://mirrors.unisound.ai/repository/pypi/simple ...

## 安装

```bash
pip install wav-loo
```

## 使用方法

### 查找WAV文件

```bash
wav-loo find /path/to/audio
wav-loo find https://example.com/audio-files/
```

### 常用alias子命令

```bash
wav-loo kgn
wav-loo gp
wav-loo uv numpy pandas
```

## 依赖

- Python 3.7+
- requests
- beautifulsoup4
- urllib3

## 许可证

MIT License 