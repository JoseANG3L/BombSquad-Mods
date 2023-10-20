# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 8

from __future__ import annotations
import random

from typing import TYPE_CHECKING

import babase
import bascenev1 as bs
from bascenev1lib.actor.powerupbox import PowerupBox
import bauiv1 as bui
from bauiv1lib import popup
from bascenev1lib.mainmenu import MainMenuSession
from bascenev1._gameactivity import GameActivity
from bascenev1lib.actor import playerspaz
from bascenev1lib.actor.bomb import Bomb

if TYPE_CHECKING:
	from typing import Sequence


class ModInfo:
	cfgname = 'Day Night' # config name
	cfglist = {
		'enable_mod': True,
	} # config list
	url = 'https://youtu.be/rz14ioyaopI' # video


class ModLang:
	lang = babase.app.lang.language
	if lang == 'Spanish':
		title = 'Opciones del Mod'
		enable = 'Habilitar Mod'
	elif lang == 'Chinese':
		title = '模组设置'
		enable = '启用模组'
	else:
		title = 'Mod Settings'
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
				on_activate_call=self._open_url,
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

		checkbox_size = (self._width * 0.7, 50)
		checkbox_maxwidth = 250
		
		v = 0
		v += 165
		bui.checkboxwidget(
			parent=self.root_widget,
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
		GameActivity.old_on_transition_in = GameActivity.on_transition_in
		def on_transition_in(self) -> None:
			self.old_on_transition_in()
			if babase.app.config[ModInfo.cfgname]['enable_mod']:
				day_color = (1, 1, 1)
				night_color = (0.4, 0.4, 0.4)
				gnode = bs.getactivity().globalsnode
				bs.animate_array(gnode, 'tint', 3, {
					0: day_color,
					5: night_color,
					8: night_color,
					13: day_color,
					16: day_color,
				}, loop=True)
				self.mode_day = True

				light_pos = [
					(0, 5, -8.5),

					(-6.5, 3, -4),
					(6.5, 3, -4),

					(-6.5, 3, -0.5),
					(6.5, 3, -0.5),

					(-4.2, 3, -6.6),
					(4.2, 3, -6.6),

					(-4.2, 3, 2.5),
					(4.2, 3, 2.5),
				]
				class RandomLight:
					def __init__(self, pos: Sequence(float) = (0, 0 ,0)) -> None:
						light = bs.newnode(
							'light',
							attrs={
								'position': pos,
								'radius': 0.5,
								'intensity': 0.6,
								'height_attenuated': False,
								'color': (0, 1, 1)
							})
						bs.animate(light, 'intensity', {
							0: 0,
							5: 0.8,
							8: 0.8,
							13: 0,
							16: 0,
						}, loop=True)
						def rcolor():
							bs.animate_array(light, 'color', 3, {
								0: (random.random(), random.random(), random.random()),
								0.1: (random.random(), random.random(), random.random()),
							})
						bs.timer(0.1, rcolor, repeat=True)

				for i in light_pos:
					RandomLight(i)

				def remitfx():
					bs.emitfx(
						position=(-6 + random.random() * 12, 15, -1),
						velocity=(0, -1, 0),
						count=10,
						spread=5,
						scale=0.5,
						chunk_type='ice',
					)
					bs.emitfx(
						position=(-6 + random.random() * 12, 15, -1),
						velocity=(0, -1, 0),
						count=10,
						spread=5,
						scale=0.5,
						chunk_type='spark',
					)
				bs.timer(0.1, remitfx, repeat=True)
					
		GameActivity.on_transition_in = on_transition_in
			# if self.map.name in [
			# 		'Monkey Face', 'Rampage', 'Roundabout',
			# 		'Step Right Up', 'Tip Top', 'Zigzag', 'The Pad']:
			# 	gnode.tint = (0.5, 0.5, 0.5)
			# elif self.map.name in [
			# 		'Big G', 'Bridgit', 'Courtyard',
			# 		'Crag Castle', 'Doom Shroom',
			# 		'Football Stadium', 'Happy Thoughts',
			# 		'Hockey Stadium']:
			# 	gnode.tint = (0.6, 0.6, 0.6)
			# else:
			# 	gnode.tint = (0.4, 0.4, 0.4)
		# GameActivity.on_transition_in = on_transition_in
		class NewPlayerSpaz(playerspaz.PlayerSpaz):
			def __init__(self, **kwargs):
				super().__init__(**kwargs)
				if babase.app.config[ModInfo.cfgname]['enable_mod']:
					light = bs.newnode(
						'light',
						owner=self.node,
						attrs={
							'radius': 0.3,
							'intensity': 0.0,
							'height_attenuated': False,
							'color': self.node.color
						})
					self.node.connectattr(
						'position', light, 'position')
					day_color = 0
					night_color = 0.6
					bs.animate(light, 'intensity', {
						0: day_color,
						5: night_color,
						8: night_color,
						13: day_color,
						16: day_color,
					}, loop=True)
		playerspaz.PlayerSpaz = NewPlayerSpaz
		# Bomb.oldinit = Bomb.__init__
		# def __bomb_init__(
		# 	self,
		# 	position: Sequence[float] = (0.0, 1.0, 0.0),
		# 	velocity: Sequence[float] = (0.0, 0.0, 0.0),
		# 	bomb_type: str = 'normal',
		# 	blast_radius: float = 2.0,
		# 	bomb_scale: float = 1.0,
		# 	source_player: bs.Player | None = None,
		# 	owner: bs.Node | None = None,
		# ):
		# 	self.oldinit(
		# 		position,
		# 		velocity,
		# 		bomb_type,
		# 		blast_radius,
		# 		bomb_scale,
		# 		source_player,
		# 		owner,
		# 	)
		# 	if babase.app.config[ModInfo.cfgname]['enable_mod']:
		# 		if self.bomb_type == 'ice':
		# 			color = (0.4, 1, 1)
		# 		elif self.bomb_type == 'impact':
		# 			color = (0.4, 0.4, 0.4)
		# 		elif self.bomb_type == 'land_mine':
		# 			color = (0.2, 0.6, 0.4)
		# 		elif self.bomb_type == 'normal':
		# 			color = (0.5, 0.5, 0.5)
		# 		elif self.bomb_type == 'sticky':
		# 			color = (0.2, 0.9, 0.3)
		# 		elif self.bomb_type == 'tnt':
		# 			color = (0.8, 0.8, 0.6)
		# 		else:
		# 			color = (0.8, 0.8, 0.8)
		# 		light = bs.newnode(
		# 			'light',
		# 			owner=self.node,
		# 			attrs={
		# 				'radius': 0.3,
		# 				'intensity': 0.4,
		# 				'height_attenuated': False,
		# 				'color': color,
		# 			})
		# 		self.node.connectattr(
		# 			'position', light, 'position')
		# Bomb.__init__ = __bomb_init__
		# PowerupBox.oldinit = PowerupBox.__init__
		# def __pw_init__(
		# 	self,
		# 	position: Sequence[float] = (0.0, 1.0, 0.0),
		# 	poweruptype: str = 'triple_bombs',
		# 	expire: bool = True,
		# ):
		# 	self.oldinit(
		# 		position,
		# 		poweruptype,
		# 		expire,
		# 	)
		# 	if babase.app.config[ModInfo.cfgname]['enable_mod']:
		# 		if self.poweruptype == 'triple_bombs':
		# 			color = (0.8, 0.8, 0.5)
		# 		elif self.poweruptype == 'punch':
		# 			color = (1, 0.2, 0.2)
		# 		elif self.poweruptype == 'ice_bombs':
		# 			color = (0.4, 1, 1)
		# 		elif self.poweruptype == 'impact_bombs':
		# 			color = (0.4, 0.4, 0.4)
		# 		elif self.poweruptype == 'land_mines':
		# 			color = (0.4, 0.8, 0.6)
		# 		elif self.poweruptype == 'sticky_bombs':
		# 			color = (0.2, 0.9, 0.3)
		# 		elif self.poweruptype == 'shield':
		# 			color = (0.8, 0, 1)
		# 		elif self.poweruptype == 'health':
		# 			color = (1.1, 1.1, 0.7)
		# 		elif self.poweruptype == 'curse':
		# 			color = (0.6, 0.2, 0.7)
		# 		else:
		# 			color = (0.8, 0.8, 0.8)
		# 		light = bs.newnode(
		# 			'light',
		# 			owner=self.node,
		# 			attrs={
		# 				'radius': 0.3,
		# 				'intensity': 0.6,
		# 				'height_attenuated': False,
		# 				'color': color,
		# 			})
		# 		self.node.connectattr(
		# 			'position', light, 'position')
		# PowerupBox.__init__ = __pw_init__

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
