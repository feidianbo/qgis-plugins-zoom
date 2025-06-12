

```shell
$ pip install PyQt5 PySide6 -i https://pypi.tuna.tsinghua.edu.cn/simple
$ pyrcc5 resources.qrc -o resources.py
# 生成多语言支持
$ pylupdate5 .\zoom_level_dockwidget.py -ts lang/zh.ts
# 编译多语言支持
$ mkdir i18n
$ pyside6-lrelease lang/zh.ts -qm i18n/zoom_level_zh.qm
```