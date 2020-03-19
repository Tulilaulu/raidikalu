"""
Import json gym data from URL to Database
DELETES ALL GYMS BEFORE REMAKING THEM FROM GOOGLE SHEET. Only use at night when there are no raids.
"""
import requests
import json
import os, sys

from raidikalu.models import Gym
from django.core.management.base import BaseCommand
from datetime import datetime

IMPORT_URL = 'https://spreadsheets.google.com/feeds/list/1umxfGu31a2YgKnjFEaCjhoyuxpeJVfQ-yszdXlMXJP0/od6/public/values?alt=json'

class Command(BaseCommand):
    def import_gym(self, data):
        name = data.get('gsx$name', None).get('$t', None)
        pogo_id = data.get('gsx$pogoid', None).get('$t', None)
        latitude = data.get('gsx$latitude', None).get('$t', None)
        longitude = data.get('gsx$longitude', None).get('$t', None)
        image_url = data.get('gsx$imageurl', None).get('$t', None)
        #is_park = data.get('gsx$ispark', False).get('$t', False)
        latest_ex_raid = data.get('gsx$latestexraidat', None).get('$t', None)
        is_ex_eligible = False
        if (latest_ex_raid != None):
            is_ex_eligible = True
        try: 
            gym, created = Gym.objects.get_or_create(
                latitude=latitude,
                longitude=longitude,
                defaults={
                    'name':name,
                    'pogo_id':pogo_id,
                    'image_url':image_url,
                    'is_ex_eligible':is_ex_eligible,
                    'is_active':True}
            )
            if created:
                print("\nGym "+name+" has been created.")
            else:
                gym.name=name
                gym.pogo_id=pogo_id
                gym.image_url=image_url
                gym.is_ex_eligible=is_ex_eligible
                gym.is_active=True
                print("Gym "+name+" already existed. It might have been updated.")
            gym.save()
        except Exception as ex:
            print(str(ex))
            msg = "\n\nSomething went wrong saving this gym: {}\n{}".format(name, str(ex))
            print(msg)

    def handle(self, *args, **options):
        headers = {'Content-Type': 'application/json'}
        response = requests.get(
        url=IMPORT_URL,
        headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        Gym.objects.all().delete()
        for entry in data['feed']['entry']:
            self.import_gym(entry)

