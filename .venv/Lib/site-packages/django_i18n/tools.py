"""Translations loader"""
from .loader import TranslationLoader
import json

loader = TranslationLoader()

def translate(path, **args):
  """Translation handler"""

  return loader.translate(path, **args)

def set_locale(locale, fallback = 'en'):
  """Set new locale and fallback"""

  loader.set_locale(locale=locale, fallback=fallback)

def handle_orm_errors(list_errors = None, as_json = False):
  """ORM errors handler"""
  result = {}

  if list_errors is None:
    return {}

  list_errors = json.loads(list_errors.as_json())

  for key in list_errors:
    result[key] = []

    for i in range(len(list_errors[key])):
      code = list_errors[key][i]['code']
      result[key].append(translate("errors.{}".format(code)))

  if as_json:
    return json.dumps(result)
  
  return result
