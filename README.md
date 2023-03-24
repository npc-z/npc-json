# NPC-JSON

## 支持特性

- 注释, 从 `//` 起始至行尾
- 尾部元素带 `,`
  ```
  [1, 2,]
  ```

## 自动化测试

安装依赖

```bash
pip install pytest pytest-watch pytest-testmon
```

执行以下命令, 当文件修改之后, 自动运行所有测试

```bash
ptw --runner "pytest --testmon -v"
```
