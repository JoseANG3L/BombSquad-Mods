# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING

import babase
from baclassic._store import StoreSubsystem as store

if TYPE_CHECKING:
	from typing import Any


# ba_meta export babase.Plugin
class ModPlugin(babase.Plugin):

	def get_store_layout(self) -> dict[str, list[dict[str, Any]]]:
		"""Return what's available in the store at a given time.

		Categorized by tab and by section.
		"""
		plus = babase.app.plus
		classic = babase.app.classic

		assert classic is not None
		assert plus is not None

		if classic.store_layout is None:
			classic.store_layout = {
				'characters': [{'items': []}],
				'extras': [{'items': ['pro']}],
				'maps': [{'items': ['maps.lake_frigid']}],
				'minigames': [],
				'icons': [
					{
						'items': [
							'icons.mushroom',
							'icons.heart',
							'icons.eyeball',
							'icons.yinyang',
							'icons.hal',
							'icons.flag_us',
							'icons.flag_mexico',
							'icons.flag_germany',
							'icons.flag_brazil',
							'icons.flag_russia',
							'icons.flag_china',
							'icons.flag_uk',
							'icons.flag_canada',
							'icons.flag_india',
							'icons.flag_japan',
							'icons.flag_france',
							'icons.flag_indonesia',
							'icons.flag_italy',
							'icons.flag_south_korea',
							'icons.flag_netherlands',
							'icons.flag_uae',
							'icons.flag_qatar',
							'icons.flag_egypt',
							'icons.flag_kuwait',
							'icons.flag_algeria',
							'icons.flag_saudi_arabia',
							'icons.flag_malaysia',
							'icons.flag_czech_republic',
							'icons.flag_australia',
							'icons.flag_singapore',
							'icons.flag_iran',
							'icons.flag_poland',
							'icons.flag_argentina',
							'icons.flag_philippines',
							'icons.flag_chile',
							'icons.moon',
							'icons.fedora',
							'icons.spider',
							'icons.ninja_star',
							'icons.skull',
							'icons.dragon',
							'icons.viking_helmet',
							'icons.fireball',
							'icons.helmet',
							'icons.crown',
						]
					}
				],
			}
		store_layout = classic.store_layout
		store_layout['characters'] = [
			{
				'items': [
					'characters.kronk',
					'characters.zoe',
					'characters.jackmorgan',
					'characters.mel',
					'characters.snakeshadow',
					'characters.bones',
					'characters.bernard',
					'characters.agent',
					'characters.frosty',
					'characters.pascal',
					'characters.pixie',
				]
			}
		]
		store_layout['minigames'] = [
			{
				'items': [
					'games.ninja_fight',
					'games.meteor_shower',
					'games.target_practice',
				]
			}
		]
		store_layout['characters'][0]['items'].append('characters.wizard')
		store_layout['characters'][0]['items'].append('characters.cyborg')
		store_layout['characters'].append(
			{
				'title': 'store.holidaySpecialText',
				'items': [
					'characters.bunny',
					'characters.santa',
					'characters.taobaomascot',
				],
			}
		)
		store_layout['minigames'].append(
			{
				'title': 'store.holidaySpecialText',
				'items': ['games.easter_egg_hunt'],
			}
		)

		# This will cause merch to show only if the master-server has
		# given us a link (which means merch is available in our region).
		store_layout['extras'] = [{'items': ['pro']}]
		if babase.app.config.get('Merch Link'):
			store_layout['extras'][0]['items'].append('merch')
		return store_layout
	store.get_store_layout = get_store_layout
