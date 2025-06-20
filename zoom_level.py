# -*- coding: utf-8 -*-
"""
ZoomLevel

 A QGIS plugin to display the zoom level of the map
                              -------------------
        updated              : 2025-03-21
        copyright            : (C) 2025 by Keith Jenkins
        email                : kgjenkins@gmail.com
 /***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QLabel

from .zoom_level_dockwidget import ZoomLevelDockWidget

from math import log2, floor
from . import resources
import os
from PyQt5.QtCore import QCoreApplication, QSettings, QTranslator, qVersion, QLocale
from qgis.core import QgsMessageLog
from qgis.utils import iface

class ZoomLevel:
    def tr(self, message):
        """
        This method is required to enable Qt internationalization.
        It is called by LUpdate and runTime when a translation is loaded.
        Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ZoomLevelDockWidget', message)

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.actions = []
        self.pluginIsActive = False
        self.dockwidget = None

        # Load translations
        locale = QSettings().value('locale/userLocale', QLocale.system().name())
        # 输出当前系统语言环境设置
        iface.messageBar().pushMessage("语言设置", f"当前语言设置: { locale }", level=0, duration=5)
                
        plugin_dir = os.path.dirname(__file__)
        locale_path = os.path.join(
            plugin_dir,
            'i18n',
            '{}.qm'.format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.tr("Zoom Level"),
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Add icon button to toolbar."""
        icon_path = ':/plugins/zoom_level/icon.png'
        self.add_action(
            icon_path,
            text = self.tr('Zoom Level'),
            callback = self.run,
            parent = self.iface.mainWindow()
        )
        if QSettings().value('plugins/zoom_level/pluginIsActive', True, type=bool):
            self.run()

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)
        self.pluginIsActive = False


    def unload(self):
        """Remove widget"""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr("Zoom Level"),
                action)
            self.iface.removeToolBarIcon(action)
        QSettings().setValue('plugins/zoom_level/pluginIsActive', self.pluginIsActive)

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True
            if self.dockwidget == None:
                self.dockwidget = ZoomLevelDockWidget()
                self.displayZoomLevel()

            # Display zoom level whenever the map scale changes
            self.iface.mapCanvas().scaleChanged.connect(self.displayZoomLevel)

            # Update map scale if user changes the zoom value
            self.dockwidget.zoomValue.valueChanged.connect(self.updateZoomLevel)
        
            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

    def updateZoomLevel(self):
        """Update the map scale based to match zoom level"""
        zoom = self.dockwidget.zoomValue.value()
        scale = 591658688 / pow(2, zoom)
        self.iface.mapCanvas().zoomScale(scale)

    def displayZoomLevel(self):
        """Display the current zoom level"""

        # Zoom level 1 scale "1:591658688" is the scale that QGIS reports
        # after "zoom to native resolution (100%)" when viewing OpenStreetMap
        # zoom level 1 tiles in EPSG:3857
        #
        # Other code such as https://github.com/qgis/QGIS/blob/f9d3ca3afe6529e9a4b6cbb1b8a2008e7103039e/src/core/vectortile/qgsvectortileutils.h#L72
        # uses the value 559082264.0287178 but it is not clear where that number
        # comes from.
        #
        # Interestingly, but perhaps coincidentally, the ratio between the two numbers is very close to the
        # ratio of 90 to 85.06 -- 85.06 degrees is the north/south limit of the EPSG:3857 CRS
        # (and the 85.06 value can also be calculated as 85.05112878)

        z1scale = 591658688
        mapScale = self.iface.mapCanvas().scale()
        zoom = log2(z1scale / mapScale)
        msg = '{:.2f}'.format(zoom)
        self.dockwidget.zoomValue.setValue(zoom)

        # estimate which XYZ zoom level would get requested
        msg = str(floor(zoom + 0.586))
        self.dockwidget.xyzValue.setText(msg)

        # estimate which vector tile zoom level would get requested
        msg = str(floor(zoom - 1))
        self.dockwidget.vectorValue.setText(msg)
        