# oldmerman-knowledge

鱼人知识库是老鱼人的第二个**开源的前后端分离项目**，其目标为实现主流个人知识库系统的功能，并为**鱼人博客**提供API服务。

![img.png](img.png)

基于如下技术栈实现：
前端(90%vibecoding + 10%微调)：Vue3 + TypeScript(仓库见：https://github.com/oldMerm/oldmerman-assistant)
后端(几乎都在古法)：Python + FastAPI + PostgreSQL + ChromaDB + ....

## 快速了解项目

**1**.目录结构

| 目录名称 | 作用概述 |
|:----------:|:----------------------:|
| main.py | 程序主入口，配置路由，中间件 |
| agents | Agent核心部件，prompt,tool等 |
| common | Web统一响应封装 |
| config | 项目部分配置(数据库连接参数等)    |
| db | 数据库连接池，dao，数据库实体 |
| middleware | Web端的中间件 |
| routes | Web路由 |
| services | Web业务层代码 |
| utils | 项目使用的工具包 |

**2**.环境变量文件(目前)
```dotenv
# Environment /production/test/development
# production -> 持久化日志到LOGGIN_PATH
ENVIRONMENT=development
LOGGING_PATH=/oldk/logs

# Database
DATABASE_URL=postgresql://postgres:123456@localhost:5432/o_knowledge

# Secret Key
JWT_SECRET=your-jwt-secret
AES_SECRET_KEY=your-aes-secret
SYSTEM_REGISTER_SECRET=用于注册的系统凭证

# API-KEY
XX_API_KEY=用于调试Agent

```

## 主要功能

1. 简单的用户鉴权(控制台管理员)，通过环境变量设置**标志值**，可创建管理员账户操作控制台内容。
2. 模型注册功能，支持提供商注册，模型注册，与模型分类，可为每个模型配置单独的API-KEY(不推荐，建议为提供商提供统一KEY)
3. ChromaDB实现持久化的向量数据库，配合向量模型进行检索，切分策略使用LangChain中的`RecursiveCharacterTextSplitter`
4. 文档整体的管理，暂不支持删除向量库中详细的文档，但可以通过删除整个文档以删除其在向量库内的所有chunk
5. 为**鱼人博客**提供第一个API服务，流式生成文章摘要(缓存7天)

## 未来要实现的功能

1. 更细粒度的文档管理，细分到每个chunk
2. 添加**重排序rerank**，以增加向量检索精准度
3. 主页面历史多轮对话
4. 更好的提示词工程，和Agent工作流搭建
5. 各种多模态功能

## email

鄙人不才，望共勉之~~你的一个⭐是我最大的动力😏！！！
outlook: `oldmerman@outlook.com`
qq: `oldmerman@qq.com`(使用较多)
