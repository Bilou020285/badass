# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DialogBADASSDialog
                                 A QGIS plugin
 Extention permettant l'accès à l'interface BADASS
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2021-04-12
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Alexandre Humeau
        email                : alexandre.humeau1@gmail.com
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

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from .expression import *
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'form4_entitearcheo3.ui'))


class DialogBADASSForm4Entitearcheo3(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self,donnees=None, parent=None):
        """Constructor."""
        super(DialogBADASSForm4Entitearcheo3, self).__init__(parent)
        #
        self.donnees= donnees
        self.setupUi(self)
        #fenetre expression
        self.rechercher.clicked.connect(lambda: expression_dialog(self,iface))
