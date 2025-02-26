如果你本地已经安装了 Python 依赖，并且希望让团队或其他设备同步相同的依赖项，你需要使用 pip freeze 将依赖保存到 requirements.txt，然后在其他环境中用它来安装。

步骤 1：导出依赖
在 Python 虚拟环境（.venv）激活的情况下运行：

bash
Copy
Edit
pip freeze > requirements.txt

当其他人克隆你的 Git 仓库时，他们可以运行：

bash
Copy
Edit
python -m venv .venv # 创建虚拟环境
source .venv/bin/activate # Linux/Mac 启动虚拟环境

# Windows 使用: .venv\Scripts\activate

pip install -r requirements.txt # 安装依赖
