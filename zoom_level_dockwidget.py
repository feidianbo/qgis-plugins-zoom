# -*- coding: utf-8 -*-
"""
/***************************************************************************
        updated              : 2025-03-21
        copyright            : (C) 2025 Keith Jenkins
        email                : kgjenkins@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QWidget, QDockWidget, QGridLayout, QLabel, QDoubleSpinBox


class ZoomLevelDockWidget(QDockWidget):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(ZoomLevelDockWidget, self).__init__(parent)

        self.setWindowTitle(self.tr("Zoom Level plugin"))
        self.setObjectName('zoom-level-plugin-dock')
        # 设置固定高度
        self.setFixedHeight(120)
        self.dockWidgetContents = QWidget(self)
        self.setWidget(self.dockWidgetContents)
        self.gridLayout = QGridLayout()
        self.dockWidgetContents.setLayout(self.gridLayout)

        self.zoomLabel = QLabel(self.dockWidgetContents)
        self.zoomLabel.setText(self.tr('Zoom Level'))

        self.zoomValue = QDoubleSpinBox()
        self.zoomValue.setDecimals(2)
        self.zoomValue.setSingleStep(1)

        self.xyzLabel = QLabel(self.dockWidgetContents)
        self.xyzLabel.setText(self.tr('XYZ tile requests'))
        self.xyzValue = QLabel(self.dockWidgetContents)

        self.vectorLabel = QLabel(self.dockWidgetContents)
        self.vectorLabel.setText(self.tr('Vector tile requests'))
        self.vectorValue = QLabel(self.dockWidgetContents)

        self.dockWidgetContents.layout().addWidget(self.zoomLabel, 0, 0)
        self.dockWidgetContents.layout().addWidget(self.zoomValue, 0, 1)
        self.dockWidgetContents.layout().addWidget(self.xyzLabel, 1, 0)
        self.dockWidgetContents.layout().addWidget(self.xyzValue, 1, 1)
        self.dockWidgetContents.layout().addWidget(self.vectorLabel, 2, 0)
        self.dockWidgetContents.layout().addWidget(self.vectorValue, 2, 1)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
