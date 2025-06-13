

```shell
$ python -m venv .venv
$ pip install PyQt5 PySide6 -i https://pypi.tuna.tsinghua.edu.cn/simple
$ pyrcc5 resources.qrc -o resources.py
# 生成多语言支持
# 中文
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/zh.ts
# 日文
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/js.ts
# 编译多语言支持
$ mkdir i18n
$ pyside6-lrelease lang/zh.ts -qm i18n/zh.qm
$ pyside6-lrelease lang/ja.ts -qm i18n/ja.qm
```