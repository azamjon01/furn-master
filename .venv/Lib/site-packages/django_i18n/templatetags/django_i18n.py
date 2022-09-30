"""Translation tags"""
from ..tools import translate
from django import template

register = template.Library()

@register.simple_tag
def t(path, **args):
  """Translation tag"""
  return translate(path, **args)
