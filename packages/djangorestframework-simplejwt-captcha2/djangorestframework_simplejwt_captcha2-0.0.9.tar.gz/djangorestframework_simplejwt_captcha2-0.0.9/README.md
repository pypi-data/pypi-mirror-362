# Simple JWT with Captcha2

[![Jazzband](https://jazzband.co/static/img/badge.svg) ](https://gitee.com/link?target=https%3A%2F%2Fjazzband.co%2F)[![GitHub Actions](https://github.com/jazzband/djangorestframework-simplejwt/workflows/Test/badge.svg) ](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fjazzband%2Fdjangorestframework-simplejwt%2Factions)[![img](https://codecov.io/gh/jazzband/djangorestframework-simplejwt/branch/master/graph/badge.svg) ](https://gitee.com/link?target=https%3A%2F%2Fcodecov.io%2Fgh%2Fjazzband%2Fdjangorestframework-simplejwt)[![img](https://img.shields.io/pypi/v/djangorestframework-simplejwt.svg) ](https://gitee.com/link?target=https%3A%2F%2Fpypi.python.org%2Fpypi%2Fdjangorestframework-simplejwt)[![img](https://img.shields.io/pypi/pyversions/djangorestframework-simplejwt.svg) ](https://gitee.com/link?target=https%3A%2F%2Fpypi.python.org%2Fpypi%2Fdjangorestframework-simplejwt)[![img](https://img.shields.io/pypi/djversions/djangorestframework-simplejwt.svg) ](https://gitee.com/link?target=https%3A%2F%2Fpypi.python.org%2Fpypi%2Fdjangorestframework-simplejwt)[![https://readthedocs.org/projects/django-rest-framework-simplejwt/badge/?version=latest](https://readthedocs.org/projects/django-rest-framework-simplejwt/badge/?version=latest)](https://gitee.com/link?target=https%3A%2F%2Fdjango-rest-framework-simplejwt.readthedocs.io%2Fen%2Flatest%2F)

## Abstract

Simple JWT with Captcha2 是对 djangorestframework-simplejwt 的二次开发版本，在原有 JWT
登录认证基础上，增加了图形验证码（CAPTCHA）验证逻辑，用于增强登录安全性。

它适用于需要在登录时加入验证码验证的 Django REST Framework 项目。

## Installation

使用 pip 安装：

```
pip install djangorestframework_simplejwt_captcha2
```

## Usage

在你的 Django 设置文件中配置 `INSTALLED_APPS` 参数，例如：

```
INSTALLED_APPS = [
    'rest_framework_simplejwt',
]
```

在你的 Django 项目的 URL 配置中添加如下路径：

```
from rest_framework_simplejwt.views import (
    captcha_verify,
    login_captcha_verify,
    token_refresh,
    token_verify,
    token_obtain_pair
)

urlpatterns = [
    path('api/token/', token_obtain_pair, name='token_pair'),
    path('api/token/refresh/', token_refresh, name='token_refresh'),
    path('api/token/verify/', token_verify, name='token_verify'),
    path('api/captcha/', captcha_verify, name='captcha'),
    path('api/login/', login_captcha_verify, name='login_captcha'),
]
```

接口说明：

- `/api/captcha/`：获取验证码图片（Base64）和唯一标识 UUID。

  响应示例：

  ```
  {
     "uuid": "abc123xyz",
     "img": "data:image/png;base64,iVBORw0KG..."
  }
  ```

- `/api/token/`：普通登录接口，返回 JWT Token（当不需要验证码时使用）。

  请求参数：

  ```
  {
      "username": "your_username",
      "password": "your_password"
  }
  ```

- `/api/login/`：带验证码的登录接口，需传入用户名、密码、UUID 和 Base64 图片内容。

  请求参数：

  ```
  {
      "username": "your_username",
      "password": "your_password",
      "uuid": "abc123xyz",
      "img": "data:image/png;base64,iVBORw0KG..."
  }
  ```

- `/api/token/refresh/`：刷新 Access Token。

  请求参数：

  ```
  {
      "refresh": "your_refresh_token"
  }
  ```

- `/api/token/verify/`：验证 Token 是否有效。

  请求参数：

  ```
  {
      "token": "your_access_token"
  }
  ```

## Settings

**(可选)** 在你的 Django 设置文件中配置 `SIMPLE_JWT` 参数，例如：

```
SIMPLE_JWT = {
    # ...其他配置...

    # 验证码类型支持 'calculation' 或 'number'
    # calculation 仅支持 + - * 运算
    "CAPTCHA_TYPE": "calculation",

    # 验证码过期时间（秒），默认为 120 秒
    "CAPTCHA_CACHE_TIME": 120,

    # 仅在 CAPTCHA_TYPE 为 'number' 时生效，默认长度为 4
    "CAPTCHA_LENGTH": 4,

    # 验证码默认宽度 185
    "CAPTCHA_WIDTH": 185,

    # 验证码默认高度 40
    "CAPTCHA_HEIGHT": 40,

    # ...其他配置...
}
```

## Translations

本项目支持多语言翻译，可通过 Django 的 i18n 功能进行扩展。

## Documentation

完整文档请访问：

🔗 [https://django-rest-framework-simplejwt-captcha2.readthedocs.io/en/latest/](https://gitee.com/link?target=https%3A%2F%2Fdjango-rest-framework-simplejwt-captcha2.readthedocs.io%2Fen%2Flatest%2F)

## License

MIT License.

## Source Code

GitHub
地址：🔗 [https://github.com/yaohua1179/djangorestframework_simplejwt_captcha2](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fyaohua1179%2Fdjangorestframework_simplejwt_captcha2)