# GDPU_zfjw
广东药科大学正方教务系统

使用方法
---
1.安装依赖

```shell
pip install -r requirements.txt
```

2.<code>config.yml</code>填写学号等信息，cookie项不用填

3.获取登录cookie

```shell
python login.py
```

---
获取课程表,课程表原始数据保存在<code>table.yml</code>

```shell
python timetable.py
```

---
计划实现功能

✅模拟登录

✅获取课程表

✅格式化输出课程表

❎抢课

---
登录密码RSA加密参考https://github.com/hibiscustoyou/pyrsa