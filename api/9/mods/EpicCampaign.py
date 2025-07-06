# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 9

from __future__ import annotations
import random

from typing import TYPE_CHECKING, override

import babase
import bascenev1 as bs
from bascenev1lib.game.onslaught import OnslaughtGame
from bascenev1lib.game.football import FootballCoopGame
from bascenev1lib.game.runaround import RunaroundGame
from bauiv1lib.coop import browser
import bauiv1 as bui
from bauiv1lib import popup

if TYPE_CHECKING:
	from typing import Sequence


class ModInfo:
	cfgname = 'Epic Campaign' # config name
	cfglist = {
		'enable_mod': True,
	} # config list
	url = 'https://youtu.be/tUz1vH6JJjo?si=FE7zCsi5XsxR6E-c' # video


class ModLang:
	lang = bs.app.lang.language
	spanish = ['Spanish', 'SpanishLatinAmerica', 'SpanishSpain']
	chinese = ['Chinese', 'ChineseSimplified', 'ChineseTraditional']
	if lang in spanish:
		title = 'Opciones del Mod'
		enable = 'Habilitar Mod'
		epic = 'Modo Épico'
	elif lang in chinese:
		title = '模组设置'
		enable = '启用模组'
		epic = '史诗模式'
	else:
		title = 'Mod Settings'
		enable = 'Enable Mod'
		epic = 'Epic Mode'


class ModSettingsWindow(bui.MainWindow):

	def __init__(self, transition= 'in_right', origin_widget: bui.Widget | None = None):
		uiscale = bui.app.ui_v1.uiscale
		self._transitioning_out = False
		self._width = 480
		self._height = 260
		bg_color = (0.4, 0.37, 0.49)

		# creates our _root_widget
		super().__init__(
			root_widget=bui.containerwidget(
				size=(self._width, self._height),
				scale=(
					2.06
					if uiscale is bui.UIScale.SMALL
					else 1.4
					if uiscale is bui.UIScale.MEDIUM
					else 1.0
				),
			),
			transition=transition,
			origin_widget=origin_widget,
		)

		self._cancel_button = bui.buttonwidget(
			parent=self._root_widget,
			position=(34, self._height - 48),
			size=(50, 50),
			scale=0.7,
			label='',
			color=bg_color,
			on_activate_call=self.main_window_back,
			autoselect=True,
			icon=bui.gettexture('crossOut'),
			iconscale=1.2)
		bui.containerwidget(edit=self._root_widget,
						   cancel_button=self._cancel_button)

		if ModInfo.url != '':
			url_button = bui.buttonwidget(
				parent=self._root_widget,
				position=(self._width - 86, self._height - 51),
				size=(82, 82),
				scale=0.5,
				label='',
				color=(1.1, 0.0, 0.0),
				on_activate_call=self._open_url,
				autoselect=True,
				icon=bui.gettexture('startButton'),
				iconscale=1.83,
				icon_color=(1.3, 1.3, 1.3))

		title = bui.textwidget(
			parent=self._root_widget,
			position=(self._width * 0.49, self._height - 27 - 5),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.0,
			text=ModLang.title,
			maxwidth=self._width * 0.6,
			color=bui.app.ui_v1.title_color)

		checkbox_size = (self._width * 0.7, 50)
		checkbox_maxwidth = 250
		
		v = 0
		v += 165
		bui.checkboxwidget(
			parent=self._root_widget,
			position=(self._width * 0.155, self._height - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=bui.app.config[ModInfo.cfgname]['enable_mod'],
			text=ModLang.enable,
			on_value_change_call=self._enable_mod,
		)

	def _enable_mod(self, val: bool) -> None:
		bui.app.config[ModInfo.cfgname]['enable_mod'] = val
		bui.app.config.apply_and_commit()

	def _open_url(self) -> None:
		bui.open_url(ModInfo.url)

	@override
	def get_main_window_state(self) -> bui.MainWindowState:
		# Support recreating our window for back/refresh purposes.
		cls = type(self)
		return bui.BasicMainWindowState(
			create_call=lambda transition, origin_widget: cls(
				transition=transition, origin_widget=origin_widget
			)
		)


# ba_meta export babase.Plugin
class ModPlugin(babase.Plugin):

	def on_app_running(self) -> None:
		self.setup_config()
		self.custom_mod()
		
	def custom_mod(self) -> None:
		OnslaughtGame.old_oti = OnslaughtGame.on_transition_in
		def og_on_transition_in(self) -> None:
			self.old_oti()
			gnode = bs.getactivity().globalsnode
			gnode.slow_motion = babase.app.config[ModInfo.cfgname]['enable_mod']
		OnslaughtGame.on_transition_in = og_on_transition_in

		FootballCoopGame.old_oti = FootballCoopGame.on_transition_in
		def fcg_on_transition_in(self) -> None:
			self.old_oti()
			gnode = bs.getactivity().globalsnode
			gnode.slow_motion = babase.app.config[ModInfo.cfgname]['enable_mod']
		FootballCoopGame.on_transition_in = fcg_on_transition_in

		RunaroundGame.old_oti = RunaroundGame.on_transition_in
		def rg_on_transition_in(self) -> None:
			self.old_oti()
			gnode = bs.getactivity().globalsnode
			gnode.slow_motion = babase.app.config[ModInfo.cfgname]['enable_mod']
		RunaroundGame.on_transition_in = rg_on_transition_in

		class CoopBrowserWindow(browser.CoopBrowserWindow):
			def __init__(
				self,
				transition: str | None = 'in_right',
				origin_widget: bui.Widget | None = None,
			):
				super().__init__(transition,origin_widget)
				uiscale = bui.app.ui_v1.uiscale
				position = (
					(self._width * 0.38, 2020)
					if uiscale is bui.UIScale.SMALL
					else (self._width * 0.67, 2020)
				)
				self._epic_button = bui.buttonwidget(
					parent=self._subcontainer,
					position=position,
					size=(200, 60),
					autoselect=True,
					scale=1.0,
					color=(0.45, 0.4, 0.5),
					textcolor=(0.8, 0.8, 0.8),
					label=ModLang.epic,
					on_activate_call=self.epic_mode,
				)
				self.update_epic_mode()

			def epic_mode(self) -> None:
				if bui.app.config[ModInfo.cfgname]['enable_mod']:
					val = False
				else:
					val = True
				bui.app.config[ModInfo.cfgname]['enable_mod'] = val
				bui.app.config.apply_and_commit()
				self.update_epic_mode()

			def update_epic_mode(self) -> None:
				if bui.app.config[ModInfo.cfgname]['enable_mod']:
					color = (0.2, 0.6, 0.8)
					textcolor = (0.9, 0.9, 0.9)
				else:
					color = (0.45, 0.4, 0.5)
					textcolor = (0.5, 0.5, 0.5)
				bui.buttonwidget(
					edit=self._epic_button,
					color=color,
					textcolor=textcolor,
				)

		browser.CoopBrowserWindow = CoopBrowserWindow
		

	def installcfg(self) -> None:
		babase.app.config[ModInfo.cfgname] = ModInfo.cfglist
		babase.app.config.apply_and_commit()

	def setup_config(self) -> None:
		if ModInfo.cfgname in babase.app.config:
			for key in ModInfo.cfglist.keys():
				if not key in babase.app.config[ModInfo.cfgname]:
					self.installcfg()
					break
		else:
			self.installcfg()

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: babase.Widget | None) -> None:
		bs.app.ui_v1.get_main_window().main_window_replace(
			ModSettingsWindow(origin_widget=source_widget)
		)