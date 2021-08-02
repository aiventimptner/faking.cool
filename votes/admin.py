from django.contrib import admin

from .models import Decision, Option, Vote, Team, Invitation, Membership


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    pass


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('team', 'user', 'invitation')
    list_filter = ('team', )
