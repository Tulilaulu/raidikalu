"""
Import json data from URL to Datababse
"""
import requests
import json
import os, sys

from raidikalu.models import RaidType
from django.core.management.base import BaseCommand
from datetime import datetime

IMPORT_URL = 'https://spreadsheets.google.com/feeds/list/19BNyX86PB-EuBPDp5IERqEq94QZR8cR8c1OaMMKux6k/od6/public/values?alt=json'

class Command(BaseCommand):
    def import_pokemon(self, data):
        name = data.get('gsx$monstername', None).get('$t', None)
        number = data.get('gsx$monsternumber', None).get('$t', None)
        priority = data.get('gsx$priority', None).get('$t', None)
        image_url = data.get('gsx$imageurl', None).get('$t', None)
        tier = data.get('gsx$tier', None).get('$t', None)
        is_active = data.get('gsx$isactive', False).get('$t', False)
        if (is_active == 'TRUE'):
            is_active = True
        if (is_active == 'FALSE'):
            is_active = False
        try: 
            raidType, created = RaidType.objects.get_or_create(
                monster_name=name,
                monster_number=number,
                defaults={
                    'tier': tier,
                    'priority': priority,
                    'image_url': image_url,
                    'is_active': is_active}
            )
            if created:
                print("\nRaid type "+name+" has been created.")
            else: 
                raidType.tier = tier
                raidType.priority = priority
                raidType.image_url = image_url
                raidType.is_active = is_active
                print("\nRaid type "+name+" already existed. It might have been updated.")
            raidType.save()
        except Exception as ex:
            print(str(ex))
            msg = "\n\nSomething went wrong saving this raid type: {}\n{}".format(name, str(ex))
            print(msg)

    def handle(self, *args, **options):
        headers = {'Content-Type': 'application/json'}
        response = requests.get(
        url=IMPORT_URL,
        headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        #RaidType.objects.all().delete()
        for entry in data['feed']['entry']:
            self.import_pokemon(entry)

