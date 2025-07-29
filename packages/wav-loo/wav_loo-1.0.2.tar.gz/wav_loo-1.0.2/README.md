# WAV Loo

版本：1.0.1

一个多功能Python命令行工具，支持查找WAV文件和常用运维/开发alias命令。

## 功能特性

- 查找WAV文件（本地/URL，递归）
- 集成多种常用命令行alias，方便日常运维和开发
- 一键安装，跨平台

## 安装

```bash
pip install wav-loo
```

## 命令行用法

### 1. 查找WAV文件

```bash
wav-loo find <路径或URL> [--output <文件>] [--verbose]
```
- 例：
  - `wav-loo find /path/to/audio`
  - `wav-loo find https://example.com/audio-files/`

### 2. 常用alias子命令

| 子命令   | 等价bash alias                                      | 说明 |
|----------|-----------------------------------------------------|------|
| kd       | kubectl delete pods                                 | 删除所有pods |
| kg       | kubectl get pods -o wide                            | 查看pods（详细） |
| kl       | kubectl logs                                        | 查看日志 |
| rs       | kubectl describe ResourceQuota -n ...                | 查看资源配额（需补参数） |
| kdn      | kubectl delete pods -n signal                       | 删除signal命名空间pods |
| kgn      | kubectl get pods -o wide -n signal                  | 查看signal命名空间pods |
| kln      | kubectl logs -n signal                              | 查看signal命名空间日志 |
| at       | atlasctl top node                                   | atlas节点监控 |
| ad       | atlasctl delete job                                 | 删除atlas作业 |
| atd      | atlasctl delete                                     | 删除atlas资源 |
| adp      | atlasctl delete job pytorchjob                      | 删除pytorch作业 |
| adn      | atlasctl delete job -n signal                       | 删除signal命名空间作业 |
| tb       | tensorboard --port=3027 --logdir=.                  | 启动tensorboard |
| ca       | conda activate <env>                                | 激活conda环境 |
| gp       | gpustat -i                                          | 查看GPU状态 |
| kgg      | kubectl get po --all-namespaces -o wide | grep ...  | 全局查找pod（需补参数） |
| uv       | uv pip install -i http://mirrors.unisound.ai/repository/pypi/simple <包>... | 使用unimirror安装PyPI包 |

#### 例子：
```bash
wav-loo kd
wav-loo kg
wav-loo kl
wav-loo rs mynamespace
wav-loo kdn
wav-loo kgn
wav-loo kln
wav-loo at
wav-loo ad
wav-loo atd
wav-loo adp
wav-loo adn
wav-loo tb
wav-loo ca myenv
wav-loo gp
wav-loo kgg mypod
wav-loo uv numpy pandas
```

## Python API

你也可以在Python中直接调用：

```python
from wav_loo import WavFinder
finder = WavFinder()
wavs = finder.find_wav_files('/path/to/audio')
print(wavs)
```

## 依赖
- Python 3.7+
- requests
- beautifulsoup4
- urllib3

## 许可证
MIT License 