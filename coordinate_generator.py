# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoordinateGenerator
                                 A QGIS plugin
 This plugin generates coordinate files from selected polygons.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-09-18
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Hiago Cardoso Arquitetura e Urbanismo
        email                : hiagocardoso.arq@gmail.com
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

# QSettings: Used to store persistent user settings
# QTranslator: Used to manage translations, allowing the plugin to support multiple languages
# QCoreApplication: Base class for all Qt applications
# QIcon e QAction: Used to create icons and actions (such as menu items or buttons)
# s
# QSettings: Usada para armazenar configurações de usuário persistentes
# QTranslator: Usada para gerenciar traduções, permitindo que o plugin suporte múltiplos idiomas
# QCoreApplication: Classe base para todas as aplicações Qt
# QIcon e QAction: Usados para criar ícones e ações (como itens de menu ou botões)
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
# 
# Inicializa recursos Qt do arquivo resources.py
from .resources import *

# Import the code for the dialog (graphical interface)
# 
# Importa o código para a caixa de diálogo (interface gráfica)
from .coordinate_generator_dialog import CoordinateGeneratorDialog

# Library used for file path manipulations
# 
# Biblioteca usada para manipulações de caminho de arquivos
import os.path

# Core logic of the plugin and how it interacts with the QGIS interface
# 
# Lógica principal do plugin e como ele interage com a interface do QGIS
class CoordinateGenerator:
    """QGIS Plugin Implementation."""

    # Creates a new instance of the CoordinateGenerator class
    # 
    # Cria uma nova instância da classe CoordinateGenerator
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        # iface parameter is the QGIS interface instance
        # Allows the plugin to interact with the QGIS application in real time
        # 
        # Parâmetro iface é a instância da interface QGIS
        # Permite que o plugin interaja com a aplicação QGIS em tempo real
        self.iface = iface

        # Gets the directory of the plugin's Python file
        # Useful for assembling resource paths or other plugin dependencies
        # 
        # Obtém o c
        # Útil para montar caminhos de recursos ou outras dependências do plugin
        self.plugin_dir = os.path.dirname(__file__)

        # Gets the user's locale setting
        # Gets the first two characters of the locale code
        # ("pt" for Portuguese or "en" for English, for example)
        # 
        # Obtém a configuração de localidade do usuário
        # Obtém os dois primeiros caracteres do código da localidade
        # ("pt" para Português ou "en" para Inglês, por exemplo)
        locale = QSettings().value('locale/userLocale')[0:2]

        # Mount the translation file path using the plugin directory
        # 
        # Monta o caminho do arquivo de tradução usando o diretório do plugin
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CoordinateGenerator_{}.qm'.format(locale))

        # Checks if the translation file exists
        # 
        # Verifica se o arquivo de tradução existe
        if os.path.exists(locale_path):

            # Load the translation
            # 
            # Carrega a tradução
            self.translator = QTranslator()
            self.translator.load(locale_path)

            # Install the translation in the application
            # 
            # Instala a tradução no aplicativo
            QCoreApplication.installTranslator(self.translator)

        # Declares list that can be used to store actions (such as menu items) that the plugin creates
        # 
        # Declara lista que pode ser usada para armazenar ações (como itens de menu) que o plugin cria
        self.actions = []

        # Declares the menu text where the plugin will be listed
        # The self.tr() method marks the string for translation
        # 
        # Declara o texto do menu onde o plugin será listado
        # O método self.tr() marca a string para tradução
        self.menu = self.tr(u'&Coordinate Generator')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() method to survive plugin reloads
        # 
        # Verifique se o plugin foi iniciado pela primeira vez na sessão atual do QGIS
        # Pode ser configurado em um método initGui() para sobreviver às recargas do plugin
        self.first_start = None

    # Method to translate strings within the plugin
    # Uses the Qt translation system
    # 
    # Método para traduzir strings dentro do plugin
    # Utiliza o sistema de tradução do Qt
    #
    # 
    # Warning that an instance method is not using self
    # Suggests that the method can be defined as a static method
    #
    # Aviso de que um método de instância não está usando self
    # Sugere que o método pode ser definido como um método estático
    
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
        return QCoreApplication.translate('CoordinateGenerator', message)


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

        icon_path = ':/plugins/coordinate_generator/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Generate coordinates'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Coordinate Generator'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = CoordinateGeneratorDialog(self.iface) # Passa iface como argumento

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
