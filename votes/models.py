from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_all_friends(self: User):
    teams_pk = self.teams.values_list('pk', flat=True)
    members_pk = Team.objects.filter(pk__in=teams_pk).values_list('members', flat=True).distinct()
    return User.objects.filter(pk__in=members_pk)


User.add_to_class("friends", get_all_friends)


class Decision(models.Model):
    subject = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='decisions', on_delete=models.SET_NULL, null=True)
    voters = models.ManyToManyField(User, related_name='elections', blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject}"

    def pending_voters(self):
        voters = []
        for user in self.voters.all():
            votes = Vote.objects.filter(user=user, option__in=self.options.all())
            if not votes.count():
                voters.append(user)

        return voters

    def state(self):
        now = timezone.now()

        if not self.pending_voters():
            # all voters have voted
            return {
                'code': "closed",
                'color': "danger",
                'icon': "fas fa-lock",
            }

        if now < self.start:
            # voting not started
            return {
                'code': "pending",
                'color': "warning",
                'icon': "fas fa-clock",
            }

        if self.start <= now < self.end:
            # voting possible
            return {
                'code': "open",
                'color': "success",
                'icon': "fas fa-vote-yea",
            }

        # voting closed
        return {
            'code': "closed",
            'color': "danger",
            'icon': "fas fa-lock",
        }


class Option(models.Model):
    decision = models.ForeignKey(Decision, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.text}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(Option, related_name='votes', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'option'], name='unique_vote'),
        ]


class Team(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    members = models.ManyToManyField(User, related_name='teams', through='Membership')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    token = models.SlugField(unique=True)
    teams = models.ManyToManyField(Team, related_name='invitations')
    expiry = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invitation = models.ForeignKey(Invitation, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'user'], name='unique_member'),
        ]
