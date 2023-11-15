# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 8

from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import random
import bauiv1 as bui
import bascenev1 as bs
from bascenev1lib.actor import playerspaz
from bascenev1lib.actor import bomb as stdbomb
from bascenev1lib.actor.spaz import BombDiedMessage
from bauiv1lib import popup

if TYPE_CHECKING:
	pass


class ModInfo:
	cfgname = 'Random Bomb' # config name
	cfglist = {
		'enable_mod': True,
		'ice': True,
		'impact': True,
		'land_mine': True,
		'normal': True,
		'sticky': True,
		'tnt': True,
		'enable': True,
	} # config list
	url = 'https://youtu.be/rz14ioyaopI' # video


class ModLang:
	lang = babase.app.lang.language
	if lang == 'Spanish':
		title = 'Bomba Aleatoria'
		enable = 'Habilitar'
		ice = 'Bomba de Hielo'
		impact = 'Insta-Bomba'
		land_mine = 'Mina Terrestre'
		normal = 'Bomba Normal'
		sticky = 'Bomba Pegajosa'
		tnt = 'Caja de TNT'
	else:
		title = 'Random Bomb'
		enable = 'Enable'
		ice = 'Ice Bomb'
		impact = 'Impact Bomb'
		land_mine = 'Land Mine'
		normal = 'Normal Bomb'
		sticky = 'Sticky Bomb'
		tnt = 'TNT Box'



class ModSettingsPopup(popup.PopupWindow):

	def __init__(self):
		uiscale = bui.app.ui_v1.uiscale
		self._transitioning_out = False
		self._width = 480
		self._height = 320
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
		
		self._scroll_width = self._width - 65
		self._scroll_height = self._height - 85
		self._sub_width = self._scroll_width * 0.95
		self._sub_height = 400

		self._scrollwidget = bui.scrollwidget(
			parent=self.root_widget,
			position=(35, 35),
			highlight=False,
			size=(self._scroll_width, self._scroll_height),
			selection_loops_to_parent=True,
		)

		self._subcontainer = bui.containerwidget(
			parent=self._scrollwidget,
			size=(self._sub_width, self._sub_height),
			background=False,
			selection_loops_to_parent=True,
		)

		v = 0
		v += 60
		bui.checkboxwidget(
			parent=self._subcontainer,
			position=(self._sub_width * 0.08, self._sub_height - v),
			size=(self._sub_width * 0.9, 50),
			autoselect=True,
			maxwidth=self._sub_width * 0.68,
			scale=0.9,
			textcolor=(0.8, 0.8, 0.8),
			value=babase.app.config[ModInfo.cfgname]['enable'],
			text=ModLang.enable,
			on_value_change_call=self._enable_mod,
		)
		v += 15
		bui.textwidget(
			parent=self._subcontainer,
			position=(self._sub_width * 0.5, self._sub_height - v),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=0.8,
			text='- - - - - - - - - - - - - - - - - - - - - - - - - - - - -',
			color=bui.app.ui_v1.title_color)

		bomb_type_list = [
			(ModLang.ice, 'ice', self.change_ice),
			(ModLang.impact, 'impact', self.change_impact),
			(ModLang.land_mine, 'land_mine', self.change_land_mine),
			(ModLang.normal, 'normal', self.change_normal),
			(ModLang.sticky, 'sticky', self.change_sticky),
			(ModLang.tnt, 'tnt', self.change_tnt),
		]
		v += 15
		for i in bomb_type_list:
			v += 50
			bui.checkboxwidget(
				parent=self._subcontainer,
				position=(self._sub_width * 0.08, self._sub_height - v),
				size=(self._sub_width * 0.9, 50),
				autoselect=True,
				maxwidth=self._sub_width * 0.68,
				scale=0.9,
				textcolor=(0.8, 0.8, 0.8),
				value=babase.app.config[ModInfo.cfgname][i[1]],
				text=i[0],
				on_value_change_call=i[2],
			)

	def _enable_mod(self, val: bool) -> None:
		bui.app.config[ModInfo.cfgname]['enable_mod'] = val
		bui.app.config.apply_and_commit()

	def change_ice(self, val: bool) -> None:
		cfg = babase.app.config
		cfg[ModInfo.cfgname]['ice'] = val
		cfg.apply_and_commit()

	def change_impact(self, val: bool) -> None:
		cfg = babase.app.config
		cfg[ModInfo.cfgname]['impact'] = val
		cfg.apply_and_commit()

	def change_land_mine(self, val: bool) -> None:
		cfg = babase.app.config
		cfg[ModInfo.cfgname]['land_mine'] = val
		cfg.apply_and_commit()

	def change_normal(self, val: bool) -> None:
		cfg = babase.app.config
		cfg[ModInfo.cfgname]['normal'] = val
		cfg.apply_and_commit()

	def change_sticky(self, val: bool) -> None:
		cfg = babase.app.config
		cfg[ModInfo.cfgname]['sticky'] = val
		cfg.apply_and_commit()

	def change_tnt(self, val: bool) -> None:
		cfg = babase.app.config
		cfg[ModInfo.cfgname]['tnt'] = val
		cfg.apply_and_commit()

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
		class NewPlayerSpaz(playerspaz.PlayerSpaz):
			def drop_bomb(self) -> stdbomb.Bomb | None:
				if (self.land_mine_count <= 0 and self.bomb_count <= 0) or self.frozen:
					return None
				assert self.node
				pos = self.node.position_forward
				vel = self.node.velocity

				if self.land_mine_count > 0:
					dropping_bomb = False
					self.set_land_mine_count(self.land_mine_count - 1)
					bomb_type = 'land_mine'
				else:
					dropping_bomb = True
					bomb_type = self.bomb_type

				# custom
				blist = [
					'ice',
					'impact',
					'land_mine',
					'normal',
					'sticky',
					'tnt',
				]
				bomb_type_list = []
				for i in blist:
					if babase.app.config[ModInfo.cfgname][i]:
						bomb_type_list.append(i)

				if len(bomb_type_list) <= 0:
					return
				random_bomb_type = random.choice(bomb_type_list)

				bomb = stdbomb.Bomb(
					position=(pos[0], pos[1] - 0.0, pos[2]),
					velocity=(vel[0], vel[1], vel[2]),
					bomb_type=random_bomb_type,
					blast_radius=self.blast_radius,
					source_player=self.source_player,
					owner=self.node,
				).autoretain()

				assert bomb.node
				if dropping_bomb:
					self.bomb_count -= 1
					bomb.node.add_death_action(
						bs.WeakCall(self.handlemessage, BombDiedMessage())
					)
				self._pick_up(bomb.node)

				for clb in self._dropped_bomb_callbacks:
					clb(self, bomb)

				return bomb
		playerspaz.PlayerSpaz = NewPlayerSpaz

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
