
# requests session extension for flask

requests session


## 安装

```sh
poetry add flask-requests-session
```

## 用法

```py
from flask_requests_session import RequestsSession

rs = RequestsSession()

rs.init_app(app)
```
