# AudioZEN

## Prerequisites

```bash
# Install uv for speed up virtual environment creation and management
uv venv -p 3.12 venv/torch251_cu124_py312
source venv/torch251_cu124_py312/bin/activate

# Install the package
uv pip install -e .

# cd to the model directory
uv pip install -r /path/to/requirements.txt
```

## Features

- [x] Gradient accumulation
- [x] Multi-node training
- [x] BF16 support
- [x] Learning rate warmup
- [x] Learning rate decay
  - [x] Linear decay

## Prerequisites

```shell
rsync -avPxH --no-g --chmod=Dg+ /home/xhao/proj/audiozen xhao@10.21.4.91:/home/xhao/proj/audiozen --exclude="*.git" --exclude="*.egg-info" --exclude="*.egg" --exclude="*.pyc" --exclude="*.log" --exclude="*.npy"
```

- How to split the repo into read-only standalone repos? Check out [Monorepo-Management](https://github.com/haoxiangsnr/audiozen/wiki/Monorepo-Management)

## Tips

### Release Package

Check out [Release Package](./docs/release.md) for more details.

### Git LFS

我们尽量不实用 Git LFS，因为 GitHub 给 LFS 提供的存储和带宽是有限的。对于大文件，我们可以考虑使用其他方式存储：
- For ipynb files, we don't need to track them as they are not large files and they are not changed frequently.
- 优先考虑将数据上传到 Github Release

## How to Process Data Files

1. 优先考虑将数据上传到 Github Release，然后在 `/path/to/local/data` 目录中下载数据
2. 在 `/path/to/local/data` 目录中创建 `README.md` 文件，描述数据的来源和下载位置

### 如何命名实验运行脚本

经过较长时间的实践，我们发现实验脚本的管理是一个比较复杂的问题。在过程，我曾经尝试过每个实验对应一个 yaml 文件，但这样会带来
问题，即配置文件毕竟是固定格式的文件，难以区分训练和测试，不方便记录实验的结果。当有环境变量要设置的时候，yaml 文件就显得
更加不方便了，每次都需要在命令行中来设置。用户还需要学习 yaml 文件和配置文件之间的映射关系。运行参数和实验参数分离后，运行参数
便需要通过命令行的历史记录来查找，或者通过文档来存储，这样就会带来另一个问题，即文档和实际运行可能不一致。

我有时候会觉得在使用 yaml 设置 `eval`/`train` 比较麻烦，每次都要修改 yaml 文件，于是额外增加了一个 `run.sh` 脚本，这样
就可以直接在命令行中设置环境变量，但这样又会带来另一个问题，即每次运行实验要考虑两个层次的问题，即命令行和 yaml 文件。

而 shell 脚本则不同，它本身是完备的脚本语言，可以方便的设置环境变量，可以方便的设置参数，可以方便的设置输出文件，符合
Unix 的 KISS 原则。因此，我们决定使用 shell 脚本来管理实验的运行。

当然，一切的前提是，即使整理废弃的实验脚本，并且保证你的 python 脚本是干净的，不要冲突。