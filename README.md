# NPC-JSON

## 自动化测试

安装依赖

```bash
pip install pytest pytest-watch pytest-testmon
```

执行以下命令, 当文件修改之后, 自动运行所有测试

```bash
ptw --runner "pytest --testmon -v"
```
