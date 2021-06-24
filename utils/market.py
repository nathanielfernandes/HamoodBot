import json
import random
import os
from copy import copy
from discord.ext import commands, tasks
from datetime import datetime


class Market:
    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.every_item = json.load(open(f"{self.Hamood.filepath}/data/items.json"))

        self.variation = (
            lambda: random.uniform(0.1, 1)
            if random.randint(1, 10) < 7
            else random.uniform(1, 1.3)
        )

        self.all_items = {}
        self.shop = {}
        self.common_items = {}
        self.uncommon_items = {}
        self.rare_items = {}
        self.epic_items = {}
        self.legendary_items = {}
        self.dev_items = {}
        self.crates = {}

        self.last_refresh = datetime.now()

    @tasks.loop(hours=1, reconnect=True)
    async def update_items(self):
        self.all_items = {
            i: self.every_item[i]
            for i in self.every_item
            if self.every_item[i]["type"] not in ["crate", "claimable"]
        }

        for i in self.all_items:
            self.all_items[i]["price"] = round(
                self.all_items[i]["value"] * self.variation()
            )

        self.common_items = {
            i: self.all_items[i]
            for i in self.all_items
            if self.all_items[i]["rarity"] == "common"
        }

        self.uncommon_items = {
            i: self.all_items[i]
            for i in self.all_items
            if self.all_items[i]["rarity"] == "uncommon"
        }

        self.rare_items = {
            i: self.all_items[i]
            for i in self.all_items
            if self.all_items[i]["rarity"] == "rare"
        }

        self.epic_items = {
            i: self.all_items[i]
            for i in self.all_items
            if self.all_items[i]["rarity"] == "epic"
        }

        self.legendary_items = {
            i: self.all_items[i]
            for i in self.all_items
            if self.all_items[i]["rarity"] == "legendary"
        }

        self.blackmarket_items = {
            i: self.all_items[i]
            for i in self.all_items
            if self.all_items[i]["rarity"] == "blackmarket"
        }

        self.dev_items = {
            i: self.all_items[i]
            for i in self.all_items
            if self.all_items[i]["rarity"] == "dev"
        }

        self.crates = {
            i: self.every_item[i]
            for i in self.every_item
            if self.every_item[i]["type"] == "crate"
        }

        categs = [
            (self.common_items, random.randint(5, 8)),
            (self.uncommon_items, random.randint(4, 7)),
            (self.rare_items, random.randint(3, 6)),
            (self.epic_items, random.randint(2, 5)),
            (self.legendary_items, random.randint(0, 2)),
        ]

        self.shop = {}
        for cat in categs:
            for i in range(cat[1]):
                k, v = random.choice(list(cat[0].items()))
                self.shop[k] = v

        self.all_items = copy(self.every_item)
        self.last_refresh = datetime.now()
