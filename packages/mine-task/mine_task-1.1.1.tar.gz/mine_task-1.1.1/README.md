# magic_api 使用说明

本库为 API Server 的 Python 客户端，支持用户注册、登录、定时任务管理、用户注销等功能。
本库目前支持用户定时推送自定义消息。
本库主要为了方便用户使用api服务，从简构建，未来将支持更多类型的任务，包括但不限于“自动推送订阅文章”、“自动推送频道内容”等等。

## 安装依赖

请先安装依赖：

```bash
pip install mine-task
```

## 快速开始

### 1. 导入库
```python
from mine_task import connect_session, create_normal_task
```

### 2. 注册新用户，获取 API 密钥，<b>若已注册过的用户，此步骤可以跳过</b>
```python
session = connect_session()
api_key = session.create_user("terminal")  # 直接在控制台输出密钥
# 或保存到本地 json 文件
# json_path = session.create_user("json")
# print(json_path)  控制台会输出包含密钥的json文件的路径
print(api_key)
```
**输出示例：**
```
your key: 12345678-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 3. 登录服务
```python
server = session.login_server(api_key)
if server.status == 'ok':
    print("服务连接成功")
else:
    print("服务连接失败")
```
**输出示例：**
```
服务连接成功
```

### 4. 创建定时任务
这里使用create_normal_task方法，参数分别是“任务标题”，“任务消息的内容”，“是否每天执行”
```python
task = create_normal_task("Morning Notice", "Good morning! Have a nice day.", everyday=True)
status = server.sub(task, email="your@email.com")  # 提交任务需要“任务”、“用户的邮箱”两个参数
print(status)
```
**输出示例：**
```
Business creation completed
```

### 5. 查看任务状态
```python
# 查看简略的任务信息
server.task.status(detail=False)
# 查看详细的任务信息
server.task.status(detail=True)
```
**简略输出示例：**
```
[0] Morning Notice | Running: True
```
**详细输出示例：**
```
========================================
Index:        0
Title:        Morning Notice
Content:      Good morning! Have a nice day.
Email:        your@email.com
Cron:         0 8 * * *
Everyday:     True
Running:      True
Next Run:     2025-07-16 08:00:00
Job ID:       1234abcd-xxxx-xxxx-xxxx-xxxxxxxxxxxx
========================================
```

### 6. 修改任务
支持修改任务的任意参数：任务标题、任务内容、任务执行时间、是否每天执行
```python
server.task.modify("Morning Notice", new_content="新的内容", everyday=False)
server.task.modify(0, new_title="New Title", new_time="30 8 * * *")
```
**输出示例：**
```
Task updated
```

### 7. 删除任务
```python
server.task.rm("Morning Notice")  # 支持删除单任务
server.task.rm("Morning Notice", is_all=True)  # 支持删除同名的任务
server.task.rm(0)  # 支持根据索引删除任务
server.task.rm(["Morning Notice", "Another Task"])  # 支持删除多任务，需要输入列表类型
```
**输出示例：**
（无输出，删除成功）

### 8. 注销用户
```python
result = session.destroy_user(api_key)
print(result)
```
**输出示例：**
```
User unregistered and all tasks deleted.
```

## 其他说明
- 每个 API key 独立管理自己的任务，互不干扰。
- 任务类型目前仅支持 normal（普通定时任务）。
- 任务通知方式目前仅支持邮箱推送。
- 所有数据均在服务端加密存储。

如需更多帮助或定制功能，请联系开发者。 