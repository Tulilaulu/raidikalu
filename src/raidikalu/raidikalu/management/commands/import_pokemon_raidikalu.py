"""
Import raid data from Raidikalu (tampere) API to Datababse
"""
import requests
import json
import os, sys

from raidikalu.models import RaidType
from django.core.management.base import BaseCommand
from datetime import datetime

IMPORT_URL = 'https://raidikalu.herokuapp.com/api/1/raidtypes/'

class Command(BaseCommand):
    def import_pokemon(self, data):
        name = data.get('monster_name', None)
        number = data.get('monster_number', None)
        priority = data.get('priority', None)
        image_url = data.get('image_url', None)
        tier = data.get('tier', None)
        is_active = data.get('is_active', False)
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
        RaidType.objects.all().delete()
        for entry in data:
            self.import_pokemon(entry)

