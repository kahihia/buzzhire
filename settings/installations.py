from .project import ProjectConfiguration
from configurations_seddonym.utils import classproperty
import os


class Local(ProjectConfiguration):
    DEBUG = True
    DOMAIN = 'buzzhire.localhost'
    PROJECT_ROOT = '/home/david/www/buzzhire'
    MANAGERS = ADMINS = (
        ('David Seddon', 'david@seddonym.me'),
    )

    @classproperty
    def BASE_URL(cls):
        return '%s://%s' % (cls.PROTOCOL, cls.DOMAIN)

    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    @classmethod
    def get_static_root(cls):
        return ''

    @classproperty
    def STATICFILES_DIRS(cls):
        return (os.path.join(cls.get_setting('PROJECT_ROOT'), 'static'),)

    STATIC_ROOT = ''

    @classproperty
    def LOG_PATH(cls):
        return os.path.join('/var/log/django', cls.PROJECT_NAME)


class Dev(ProjectConfiguration):
    DEBUG = True
    DOMAIN = 'dev.buzzhire.co'
    WEBFACTION_USER = 'buzzhire'
    WEBFACTION_APPNAME = 'dev'

    @classproperty
    def PROJECT_ROOT(cls):
        return '/home/%s/webapps/%s/project' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    MANAGERS = ADMINS = (
        ('David Seddon', 'david@seddonym.me'),
    )

    @classproperty
    def BASE_URL(cls):
        return '%s://%s' % (cls.PROTOCOL, cls.DOMAIN)

    ACCOUNT_PASSWORD_MIN_LENGTH = 1

    @classproperty
    def STATICFILES_DIRS(cls):
        return (os.path.join(cls.get_setting('PROJECT_ROOT'), 'static'),)

    @classmethod
    def get_static_root(cls):
        return '/home/%s/webapps/%s/static' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classmethod
    def get_media_root(cls):
        return '/home/%s/webapps/%s/uploads' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classproperty
    def LOG_PATH(cls):
        return '/home/%s/logs/user/%s/' % (cls.WEBFACTION_USER, cls.WEBFACTION_APPNAME)

    @classmethod
    def get_default_database_name(cls):
        return '%s_%s' % (cls.get_setting('PROJECT_NAME'),
                          cls.get_setting('WEBFACTION_APPNAME'))

    @classmethod
    def get_default_database_user(cls):
        return cls.get_default_database_name()


class Live(Dev):
    DEBUG = False
    DOMAIN = 'buzzhire.co'
    WEBFACTION_APPNAME = 'live'

    ACCOUNT_PASSWORD_MIN_LENGTH = 6
