from django import template

register = template.Library()

@register.simple_tag
def votes_per_user_and_choice(user, choice):
    print(choice.votes)
    return choice.num_votes_by_user(user)
