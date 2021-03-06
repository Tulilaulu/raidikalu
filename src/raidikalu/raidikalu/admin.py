from django.contrib import admin
from django.utils.html import format_html
from raidikalu.models import InfoBox, Gym, GymNickname, RaidType, Raid, DataSource, RaidVote, Attendance


def make_active(modeladmin, request, queryset):
  queryset.update(is_active=True)
make_active.short_description = 'Mark selected as active'


def make_inactive(modeladmin, request, queryset):
  queryset.update(is_active=False)
make_inactive.short_description = 'Mark selected as not active'


def make_ex_eligible(modeladmin, request, queryset):
  queryset.update(is_ex_eligible=True)
make_ex_eligible.short_description = 'Mark selected as EX eligible'


def make_ex_ineligible(modeladmin, request, queryset):
  queryset.update(is_ex_eligible=False)
make_ex_ineligible.short_description = 'Mark selected as not EX eligible'


class GymAdmin(admin.ModelAdmin):
  list_display = ('name', 'is_ex_eligible', 'is_active')
  list_filter = ('is_ex_eligible', 'is_active')
  search_fields = ('name',)
  actions = [make_active, make_inactive, make_ex_eligible, make_ex_ineligible]


class RaidTypeAdmin(admin.ModelAdmin):
  list_display = ('monster_name', 'image_tag', 'get_tier_display', 'monster_number', 'is_active')
  list_filter = ('tier', 'is_active')
  actions = [make_active, make_inactive]
  ordering = ['-tier', '-priority']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    RaidType.get_tier_display.short_description = 'Tier'

  def image_tag(self, obj):
    return format_html('<img src="%s" width="32" height="32" style="margin: -8px 0;" />' % obj.get_image_url()) if obj.get_image_url() else ''
  image_tag.short_description = 'Image'


admin.site.register(InfoBox)
admin.site.register(Gym, GymAdmin)
admin.site.register(GymNickname)
admin.site.register(RaidType, RaidTypeAdmin)
admin.site.register(Raid)
admin.site.register(DataSource)
admin.site.register(RaidVote)
admin.site.register(Attendance)
