
from django.conf import settings


BASE_RAID_IMAGE_URL = getattr(settings, 'RAIDIKALU_BASE_RAID_IMAGE_URL', 'https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/pokemon_icons/pokemon_icon_{:03d}_00.png')
GOOGLE_ANALYTICS_ID = getattr(settings, 'GOOGLE_ANALYTICS_ID', None)

#DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*']

SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_PRELOAD = False
SECURE_SSL_REDIRECT = False
