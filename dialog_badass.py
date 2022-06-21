# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DialogBADASS
                                 A QGIS plugin
 Extention permettant l'accès à l'interface BADASS
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-04-12
        git sha              : $Format:%H$
        copyright            : (C) 2021-2022 by Alexandre Humeau, Alex Baiet
        email                : alexandre.humeau1@gmail.com, alex.baiet3@gmail.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsMessageLog, Qgis
import os.path
# Initialize Qt resources from file resources.py
# from .resources import *
from .py.home import Home
from .py.modify_db import ModifyDB
from .py.create_db import CreateDB
from .py import helper

class DialogBADASS:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DialogBADASS_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Dialog BADASS')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('DialogBADASS', message)


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
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = helper.get_file_path("file/icon.png")
        self.add_action(
            icon_path,
            text=self.tr(u'BADASS Extension'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Dialog BADASS'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            # Page d'accueil
            self.home_win = Home()
            # Page de création de bdd
            self.create_win = CreateDB()
            # Page de modification de bdd
            self.modify_win = ModifyDB()
            
            # Création de toutes les actionsw onClick
            self.home_win.btnCreate.clicked.connect(self.load_create_db_ui)
            self.home_win.btnModify.clicked.connect(self.load_modify_db_ui)
            self.home_win.btnClose.clicked.connect(self.home_win.close)
            
            self.create_win.btnBack.clicked.connect(self.load_home_ui)
            
            self.modify_win.btnBack.clicked.connect(self.load_home_ui)

        # QgsMessageLog.logMessage(helper.get_file_path("logo_full.png"), "test")

        # show the dialog
        self.current_win = self.home_win
        self.current_win.show()
        
        # Run the dialog event loop
        result = self.home_win.exec_()
        
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass


    def load_home_ui(self):
        """Ouvre la fenêtre d'accueil."""
        self.current_win.close()
        self.current_win = self.home_win
        self.current_win.show()


    def load_create_db_ui(self):
        """Ouvre la fenêtre de création de base de données."""
        self.current_win.close()
        self.current_win = self.create_win
        self.current_win.show()


    def load_modify_db_ui(self):
        """Ouvre la fenêtre de modification de base de données."""
        self.current_win.close()
        self.current_win = self.modify_win
        self.current_win.show()
        
