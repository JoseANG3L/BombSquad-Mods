# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING, override

import babase
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib import popup
from bauiv1lib import confirm
from bascenev1lib.actor.spaz import Spaz

if TYPE_CHECKING:
	from typing import Any


class ModInfo:
	cfgname = 'Epic Elimination' # config name
	cfglist = {
		'time': 0.6,
		'fall': True,
		'enable_mod': True,
	} # config list
	url = 'https://youtu.be/rz14ioyaopI' # video


class ModLang:
	def __init__(self) -> None:
		lang = bs.app.lang.language
		spanish = ['Spanish', 'SpanishLatinAmerica', 'SpanishSpain']
		portuguese = ['Portuguese', 'PortugueseBrazil']
		french = ['French', 'FrenchCanada']
		russian = ['Russian']
		chinese = ['Chinese', 'ChineseSimplified', 'ChineseTraditional']
		if lang in spanish:
			self.title = 'Opciones del Mod'
			self.youtube = (
				'¿Estás seguro?\n'
				'Te llevará a un vídeo de YouTube.'
			)
			self.enable = 'Habilitar Mod'
			self.fall = 'Habilitar al caer del mapa'
			self.time = 'Tiempo Épico'
			self.slowest = 'Más Lento'
			self.slow = 'Lento'
			self.normal = 'Normal'
			self.fast = 'Rápido'
			self.faster = 'Más Rápido'
		elif lang in portuguese:
			self.title = 'Opções de Mod'
			self.youtube = (
				'Tem certeza?\n'
				'Ele o levará a um vídeo do YouTube.'
			)
			self.enable = 'Ativar Mod'
			self.fall = 'Habilitar ao cair do mapa'
			self.time = 'Tempo épico'
			self.slowest = 'Mais Devagar'
			self.slow = 'Lento'
			self.normal = 'Normal'
			self.fast = 'Rápido'
			self.faster = 'Mais Rápido'
		elif lang in french:
			self.title = 'Options de Modules'
			self.youtube = (
				'Tu es sûr?\n'
				'Cela vous amènera à une vidéo YouTube.'
			)
			self.enable = 'Activer le module'
			self.fall = 'Activer lors de la chute de la carte'
			self.time = 'Temps Épique'
			self.slowest = 'Ralentissez'
			self.slow = 'Lent'
			self.normal = 'Normal'
			self.fast = 'Rapide'
			self.faster = 'Plus Rapide'
		elif lang in chinese:
			self.title = '模组设置'
			self.youtube = (
				'你确定吗？\n'
				'它将带您观看 YouTube 视频。'
			)
			self.enable = '启用模组'
			self.fall = '从地图上掉下来时启用'
			self.time = '史诗般的时光'
			self.slowest = '最慢的'
			self.slow = '慢的'
			self.normal = '普通的'
			self.fast = '快速地'
			self.faster = '快点'
		elif lang in russian:
			self.title = 'Настройки мода'
			self.youtube = (
				'Вы уверены?\n'
				'Это приведет вас к видео на YouTube.'
			)
			self.enable = 'Включить мод'
			self.fall = 'Включить при падении c карты'
			self.time = 'Эпическое время'
			self.slowest = 'Самый медленный'
			self.slow = 'Медленный'
			self.normal = 'Нормальный'
			self.fast = 'Быстрый'
			self.faster = 'Быстрее'
		else:
			self.title = 'Mod Settings'
			self.youtube = (
				'Are you sure?\n'
				'It will take you to a YouTube video.'
			)
			self.enable = 'Enable Mod'
			self.fall = 'Enable when falling from the map'
			self.time = 'Epic Time'
			self.slowest = 'Slowest'
			self.slow = 'Slow'
			self.normal = 'Normal'
			self.fast = 'Fast'
			self.faster = 'Faster'
		

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
				on_activate_call=self._youtube,
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
			text=ModLang().title,
			maxwidth=self._width * 0.6,
			color=bui.app.ui_v1.title_color)

		checkbox_size = (self._width * 0.72, 50)
		checkbox_maxwidth = 310
		
		v = 0
		v += 106
		bui.textwidget(
			parent=self._root_widget,
			position=(self._width * 0.265, self._height - v),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.0,
			text=ModLang().time,
			maxwidth=150,
			color=(0.8, 0.8, 0.8, 1.0),
		)
		v += 22
		popup.PopupMenu(
			parent=self._root_widget,
			position=(self._width * 0.5, self._height - v),
			width=150,
			choices=[1.0, 0.8, 0.6, 0.4, 0.2],
			choices_display=[
				bs.Lstr(value=ModLang().slowest),
				bs.Lstr(value=ModLang().slow),
				bs.Lstr(value=ModLang().normal),
				bs.Lstr(value=ModLang().fast),
				bs.Lstr(value=ModLang().faster),
			],
			current_choice=bui.app.config[ModInfo.cfgname]['time'],
			on_value_change_call=self._set_time,
		)
		v += 60
		bui.checkboxwidget(
			parent=self._root_widget,
			position=(self._width * 0.14, self._height - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=bui.app.config[ModInfo.cfgname]['fall'],
			text=ModLang().fall,
			on_value_change_call=self._fall,
		)
		v += 46
		bui.checkboxwidget(
			parent=self._root_widget,
			position=(self._width * 0.14, self._height - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=bui.app.config[ModInfo.cfgname]['enable_mod'],
			text=ModLang().enable,
			on_value_change_call=self._enable_mod,
		)

	def _set_time(self, val: float) -> None:
		bui.app.config[ModInfo.cfgname]['time'] = val
		bui.app.config.apply_and_commit()

	def _fall(self, val: bool) -> None:
		bui.app.config[ModInfo.cfgname]['fall'] = val
		bui.app.config.apply_and_commit()

	def _enable_mod(self, val: bool) -> None:
		bui.app.config[ModInfo.cfgname]['enable_mod'] = val
		bui.app.config.apply_and_commit()

	def _youtube(self) -> None:
		confirm.ConfirmWindow(
			ModLang().youtube,
			action=self._open_url,
			width=380,
			height=120,
		)

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

			
class CustomMod:
	def __init__(self) -> None:
		Spaz.oldhandlemessage = Spaz.handlemessage
		def handlemessage(self, msg: Any) -> Any:
			if isinstance(msg, bs.DieMessage):
				self.oldhandlemessage(msg)
				if not self.node:
					return
				if not babase.app.config[ModInfo.cfgname]['enable_mod']:
					return
				fall = babase.app.config[ModInfo.cfgname]['fall']
				if msg.how is bs.DeathType.FALL and not fall:
					return
				gnode = bs.getactivity().globalsnode
				def stopsm():
					gnode.slow_motion = False
				gnode.slow_motion = True
				time = babase.app.config[ModInfo.cfgname]['time']
				bs.timer(time, stopsm)
			else:
				self.oldhandlemessage(msg)
		Spaz.handlemessage = handlemessage


# ba_meta export babase.Plugin
class ModPlugin(babase.Plugin):

	def on_app_running(self) -> None:
		self.setup_config()
		self.custom_mod()

	def custom_mod(self) -> None:
		CustomMod()

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