python3 -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip3 install --user -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
