

```shell
$ python -m venv .venv
$ pip install PyQt5 PySide6 -i https://pypi.tuna.tsinghua.edu.Hans/simple
$ pyrcc5 resources.qrc -o resources.py
# 生成多语言支持
# 简体中文
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/zh-Hans.ts
# 繁体中文
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/zh-Hant.ts
# 日本语
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/js.ts
# 韩文
$ pylupdate5 .\zoom_level_dockwidget.py .\zoom_level.py -ts lang/ko.ts

# ko

# ar
# 编译多语言支持
$ mkdir i18n
$ pyside6-lrelease lang/zh-Hans.ts -qm i18n/zh-Hans.qm
$ pyside6-lrelease lang/zh-Hant.ts -qm i18n/zh-Hant.qm
$ pyside6-lrelease lang/ja.ts -qm i18n/ja.qm
$ pyside6-lrelease lang/ko.ts -qm i18n/ko.qm
# en_US
```