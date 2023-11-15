# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 8

from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bauiv1 as bui
from bauiv1lib import confirm, popup

if TYPE_CHECKING:
	pass


class ModInfo:
	cfgname = 'UIScale' # config name
	cfglist = {
		'scale': 'large',
	} # config list
	url = 'https://youtu.be/6j5dJDjrt3o' # video


class ModLang:
	lang = babase.app.lang.language
	if lang == 'Spanish':
		title = 'Escala de Juego'
		change = 'Tipo de Escala'
		large = 'Largo'
		medium = 'Mediano'
		small = 'Pequeño'
		enable = 'Habilitar Mod'
	else:
		title = 'Game Scale'
		change = 'Scale Type'
		large = 'Large'
		medium = 'Medium'
		small = 'Small'
		enable = 'Enable Mod'


class ModSettingsPopup(popup.PopupWindow):

	def __init__(self):
		uiscale = bui.app.ui_v1.uiscale
		self._transitioning_out = False
		self._width = 480
		self._height = 260
		bg_color = (0.4, 0.37, 0.49)

		# creates our _root_widget
		super().__init__(
			position=(0.0, 0.0),
			size=(self._width, self._height),
			scale=(
				2.06
				if uiscale is bui.UIScale.SMALL
				else 1.4
				if uiscale is bui.UIScale.MEDIUM
				else 1.0
			),
			bg_color=bg_color,
		)

		self._cancel_button = bui.buttonwidget(
			parent=self.root_widget,
			position=(34, self._height - 48),
			size=(50, 50),
			scale=0.7,
			label='',
			color=bg_color,
			on_activate_call=self._on_cancel_press,
			autoselect=True,
			icon=bui.gettexture('crossOut'),
			iconscale=1.2)
		bui.containerwidget(edit=self.root_widget,
						   cancel_button=self._cancel_button)

		if ModInfo.url != '':
			url_button = bui.buttonwidget(
				parent=self.root_widget,
				position=(self._width - 86, self._height - 51),
				size=(82, 82),
				scale=0.5,
				label='',
				color=(1.1, 0.0, 0.0),
				on_activate_call=self._youtube,
				autoselect=True,
				icon=bui.gettexture('startButton'),
				iconscale=1.83,
				icon_color=(1.3, 1.3, 1.3))

		title = bui.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.49, self._height - 27 - 5),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.0,
			text=ModLang.title,
			maxwidth=self._width * 0.6,
			color=bui.app.ui_v1.title_color)

		checkbox_size = (self._width * 0.72, 50)
		checkbox_maxwidth = 310
		checkbox_posx = self._width * 0.15
		checkbox_space = 52
		
		v = 0
		v += 132
		bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.265, self._height - v),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.0,
            text=ModLang.change,
            maxwidth=150,
            color=(0.8, 0.8, 0.8, 1.0))
		v += 23
		popup.PopupMenu(
			parent=self.root_widget,
			position=(self._width * 0.5, self._height - v),
			width=150,
			choices=['large', 'medium', 'small'],
			choices_display=[
				bui.Lstr(value=ModLang.large),
				bui.Lstr(value=ModLang.medium),
				bui.Lstr(value=ModLang.small),
			],
			current_choice=bui.app.config[ModInfo.cfgname]['scale'],
			on_value_change_call=self._set_uiscale,
		)

	def _set_uiscale(self, val: str) -> None:
		bui.app.config[ModInfo.cfgname]['scale'] = val
		bui.app.config.apply_and_commit()
		self._update_mod()
		print(babase.app.config[ModInfo.cfgname]['scale'])
		
	def _update_mod(self) -> None:
		cfg = babase.app.config[ModInfo.cfgname]
		if cfg['scale'] == 'large':
			uiscale = babase.UIScale.LARGE
		elif cfg['scale'] == 'medium':
			uiscale = babase.UIScale.MEDIUM
		else:
			uiscale = babase.UIScale.SMALL
		bui.app.ui_v1._uiscale = uiscale

	def _youtube(self) -> None:
		confirm.ConfirmWindow(
			ModLang.youtube,
			action=self._open_url,
			width=380,
			height=120,
		)

	def _open_url(self) -> None:
		bui.open_url(ModInfo.url)

	def _on_cancel_press(self) -> None:
		self._transition_out()

	def _transition_out(self) -> None:
		if not self._transitioning_out:
			self._transitioning_out = True
			bui.containerwidget(edit=self.root_widget, transition='out_scale')

	def on_popup_cancel(self) -> None:
		bui.getsound('swish').play()
		self._transition_out()


# ba_meta export plugin
class ModPlugin(babase.Plugin):

	def on_app_running(self) -> None:
		self.setup_config()
		self.custom_mod()

	def custom_mod(self) -> None:
		print(babase.app.config[ModInfo.cfgname]['scale'])
		cfg = babase.app.config[ModInfo.cfgname]
		if cfg['scale'] == 'large':
			uiscale = babase.UIScale.LARGE
		elif cfg['scale'] == 'medium':
			uiscale = babase.UIScale.MEDIUM
		else:
			uiscale = babase.UIScale.SMALL
		bui.app.ui_v1._uiscale = uiscale

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
		ModSettingsPopup()