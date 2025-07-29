操作步骤
- 修改代码
- 修改[setup.py](setup.py)中的版本号`version`
- 打包并上传至python中央仓库
```shell
pip install build
pip install twine
py -m build
py -m twine upload --repository secmind dist/* 或 twine upload dist/* 

```
- 提交git代码
- 打包Docker amd64 arm64镜像，地址http://git.wandoutech.com/xpam/delivery/pam-docker-images/-/tree/cicd/beta/build/pam-ruleworker
- 将Docker镜像上传至http://git.wandoutech.com/xpam/delivery/pam-docker-images/

直接使用：pip install secmind