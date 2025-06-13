

```shell
$ python -m venv .venv
$ pip install PyQt5 PySide6 -i https://pypi.tuna.tsinghua.edu.cn/simple
$ pyrcc5 resources.qrc -o resources.py
# 生成多语言支持
# 简体中文
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/zh_CN.ts
# 繁体中文
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/zh_TW.ts
# 日本语
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/js.ts

# ko

# ar
# 编译多语言支持
$ mkdir i18n
$ pyside6-lrelease lang/zh_CN.ts -qm i18n/zh_CN.qm
$ pyside6-lrelease lang/zh_TW.ts -qm i18n/zh_TW.qm
$ pyside6-lrelease lang/ja.ts -qm i18n/ja.qm
$ pyside6-lrelease lang/ko.ts -qm i18n/ko.qm
# en_US
```