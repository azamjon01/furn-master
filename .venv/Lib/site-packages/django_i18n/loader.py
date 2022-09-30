"""Loader class"""
import yaml, io, os
from django.conf import settings

class DefaultTranslations:
  """Default translations"""

  def __init__(self):
    """Constructor"""

    # All commented lines means work to do
    # All comments after the translation is "little" issues related to form validators

    self.default = {
      'required': 'Is required',
      'max_length': 'Is too long', # Must have less than %{length} characters
      'min_length': 'Is too short', # Must have at least %{length} characters
      'invalid_choice': 'Has invalid choice',
      'invalid': 'Has invalid',
      'max_value': 'Is too long',
      'min_value': 'Is too short',
      # 'max_digits': '',
      # 'max_decimal_places': '',
      # 'max_whole_digits': '',
      'overflow': 'Is too long', # Cannot exceed %{duration}
      'missing': 'Missing image',
      'empty': 'Cannot be empty',
      'invalid_image': 'Invalid image',
      'invalid_list': 'Invalid list',
      'incomplete': 'Incomplete',
      'invalid_date': 'Invalid date',
      'invalid_time': 'Invalid time',
      'invalid_pk_value': 'Invalid primary key value',
      # 'list': '',
    }

  def get_default(self):
    """GEt default translations"""
    return self.default

class TranslationLoaderErrors:
  """Translations error"""

  def __init__(self, message):
    """Constructor"""
    self.message = message

  def __repr__(self):
    """Readable property"""
    return "Translation Loader Error: {}".format(self.message)

  def __str__(self):
    """Readable property"""
    return "Translation Loader Error: {}".format(self.message)

class TranslationLoader:
  """Loader class"""

  def __init__(self):
    """Initializer"""

    self.translations = {}
  
    for i in range(len(settings.LOCALES)):  
      with io.open(os.path.join(settings.LOCALES_PATH, "{filename}.yml".format(filename=settings.LOCALES[i])), 'r') as stream:
        self.__convert_to_path(yaml.safe_load(stream))

    if not hasattr(settings, 'LOCALE'):
      self.locale = 'en'
      settings.LOCALE = 'en'
    elif settings.LOCALE in settings.LOCALES:
      self.locale = settings.LOCALE
    else:
      raise TranslationLoaderErrors('Fallback language has invalid language')

    if not hasattr(settings, 'LOCALE_FALLBACK'):
      self.fallback = ''
      settings.LOCALE_FALLBACK = ''
    elif settings.LOCALE_FALLBACK in settings.LOCALES:
      self.fallback = settings.LOCALE_FALLBACK
    else:
      raise TranslationLoaderErrors('Fallback language has invalid language')

    self.__assign_default_errors()

  def __assign_default_errors(self):
    """Assign default errors"""
    default = DefaultTranslations().get_default()

    for key in default:
      finder = "en.errors.{}".format(key)

      if not finder in self.translations:
        self.translations[finder] = default[key]

  def __read_down(self, key, value):
    """Read down method"""
    if type(value) == list:
      for i in range(len(value)):
        val = value[i]
        k = "{key}.{i}".format(key=key, i=i)

        if type(val) == dict or type(val) == list:
          self.__read_down(k, val)
        else:
          self.translations[k] = val

    else:
      for i in value:
        val = value[i]
        k = "{key}.{i}".format(key=key, i=i)

        if type(val) == dict or type(val) == list:
          self.__read_down(k, val)
        else:
          self.translations[k] = val

  def __convert_to_path(self, payload):
    """Convert to path"""
    for key in payload:
      value = payload[key]

      if type(value) == dict or type(value) == list:
        self.__read_down(key, value)
      else:
        self.translations[key] = value

  def set_locale(self, locale, fallback):
    """Set locale"""
    if locale is None:
      raise TranslationLoaderErrors('Fallback language has invalid language')

    if locale in settings.LOCALES:
      self.locale = locale
      settings.LOCALE = locale

    else:
      raise TranslationLoaderErrors('Fallback language has invalid language')

    if fallback is None:
      self.fallback = ''
      settings.LOCALE_FALLBACK = ''
    elif fallback in settings.LOCALES:
      self.fallback = fallback
      settings.LOCALE_FALLBACK = fallback
    else:
      raise TranslationLoaderErrors('Fallback language has invalid language')

  def translate(self, path, **args):
    """Translate"""
    key = "{locale}.{path}".format(locale=self.locale, path=path)

    if key in self.translations:
      response = self.translations[key]

      for sub_key in args:
        response = response.replace("%{" + str(sub_key) + "}", args[sub_key])

      return response

    if self.fallback != '':
      new_key = "{locale}.{path}".format(locale=self.fallback, path=path)
      
      if new_key in self.translations:
        response = "Fallback: {message}".format(message=self.translations[new_key])

        for sub_key in args:
          response = response.replace("%{" + str(sub_key) + "}", args[sub_key])

        return response

    return "Translation missing {key}".format(key=key)