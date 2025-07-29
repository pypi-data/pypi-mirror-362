Simple JWT
==========

.. image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband
.. image:: https://github.com/jazzband/djangorestframework-simplejwt/workflows/Test/badge.svg
   :target: https://github.com/jazzband/djangorestframework-simplejwt/actions
   :alt: GitHub Actions
.. image:: https://codecov.io/gh/jazzband/djangorestframework-simplejwt/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jazzband/djangorestframework-simplejwt
.. image:: https://img.shields.io/pypi/v/djangorestframework-simplejwt.svg
   :target: https://pypi.python.org/pypi/djangorestframework-simplejwt
.. image:: https://img.shields.io/pypi/pyversions/djangorestframework-simplejwt.svg
   :target: https://pypi.python.org/pypi/djangorestframework-simplejwt
.. image:: https://img.shields.io/pypi/djversions/djangorestframework-simplejwt.svg
   :target: https://pypi.python.org/pypi/djangorestframework-simplejwt
.. image:: https://readthedocs.org/projects/django-rest-framework-simplejwt/badge/?version=latest
   :target: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

Abstract
--------

Simple JWT is a JSON Web Token authentication plugin for the `Django REST
Framework <http://www.django-rest-framework.org/>`__.

For full documentation, visit `django-rest-framework-simplejwt.readthedocs.io
<https://django-rest-framework-simplejwt.readthedocs.io/en/latest/>`__.

二次开发的 Simple JWT
---------------------

Installation
------------

你可以使用以下命令安装这个包：

.. code-block:: bash

    pip3 install djangorestframework_simplejwt_captcha2


Usage
-----

在你的 Django 项目的 URL 配置中添加如下路径：

.. code-block:: python

    from rest_framework_simplejwt.views import captcha_verify, login_captcha_verify, token_refresh, token_verify, \
        token_obtain_pair

    urlpatterns = [
        path('api/token/', token_obtain_pair, name='token_pair'),
        path('api/token/refresh/', token_refresh, name='token_refresh'),
        path('api/token/verify/', token_verify, name='token_verify'),
        path('api/captcha/', captcha_verify, name='captcha'),
        path('api/login/', login_captcha_verify, name='login_captcha'),
    ]

- ``/api/captcha/`` 接口用于获取验证码图片（base64）和 UUID：

响应示例：

.. code-block:: json

    {
       "uuid": "",
       "img": ""
    }

- ``/api/token/`` 接口用于登录并获取 JWT：

需要传入四个参数：

- username
- password
- uuid          # 上一个接口返回的 uuid
- captcha       # 图片验证码

- ``/api/token/refresh/`` 接口用于刷新 token。


Settings
--------

在你的 Django 设置文件中配置 ``SIMPLE_JWT`` 参数，例如：

.. code-block:: python

    SIMPLE_JWT = {
        ...
        # 验证码类型支持 calculation、number 两种，
        # calculation 仅支持 + - * 不支持除法
        "CAPTCHA_TYPE": 'calculation',
        # 默认验证码有效期为 120 秒
        "CAPTCHA_CACHE_TIME": 120,
        # 仅在验证码类型为 number 时生效，默认长度为 4
        "CAPTCHA_LENGTH": 4,
        ...
    }


Translations
------------

