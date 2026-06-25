# oldmerman-knowledge

**快速了解**：鱼人知识库是老鱼人的第二个**开源的前后端分离项目**，定位是一个**轻量级的个人知识库系统**，并为**鱼人博客**提供API服务。


**项目愿景**：
* 持续集成各类国内外的各类模型，虽然老鱼人更倾向于廉价，把性价比提上来，集成适合的模型，用适合的价格，最大化的提高模型输出的准确性。
* 如果你也追求性价比，希望物尽其用，不妨花时间浏览下这个项目，期待您宝贵的建议！ 

![img.png](img.png)

基于如下技术栈实现：
Python + FastAPI + PostgreSQL + ChromaDB(前端见仓库：https://github.com/oldMerm/oldmerman-assistant)

## 快速了解项目

**1**.目录结构

| 目录名称       | 作用概述                   |
|:----------:|:----------------------:|
| main.py    | 程序主入口，配置路由，中间件         |
| agents     | Agent核心部件，prompt，tool等 |
| common     | Web统一响应封装              |
| config     | 项目部分配置(数据库连接参数等)       |
| db         | 数据库连接池，dao，数据库实体       |
| middleware | Web端的中间件               |
| routes     | Web路由                  |
| services   | Web业务层代码               |
| utils      | 项目使用的工具包               |

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
4. 支持文档重排序(目前只支持智谱，后续会加入更多Rerank模型)，不考虑本地部署(追求系统的轻量化)
5. 文档整体的管理，支持根据文档记录删除向量库中的所有文档条目(不会支持单独删除切分后的单条记录，若文档修改，需重新向量化入库)
6. 为**鱼人博客**提供第一个API服务，流式生成文章摘要

## 未来要实现的功能

1. 主页面历史多轮对话
2. 更好的提示词工程，和Agent工作流搭建
3. 各种多模态功能

## 大模型集成列表
**chat**: DeepSeek
**embedding**: BigModel(智谱)，Alibaba
**rerank**: BigModel

有优秀，廉价的模型也可以向老鱼人反馈~

## email

鄙人不才，望共勉之~~您的⭐和反馈是老鱼人最大的动力和财富！！！


**outlook**: `oldmerman@outlook.com`


**qq**: `oldmerman@qq.com`(使用较多)
