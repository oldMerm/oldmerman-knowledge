--
-- PostgreSQL database dump
--

\restrict WpJ0vhycojqTI3LEYbZibPh7SZPFWLgcwhzqiCgivWAraUb0tfVKh7SGVOB6sfR

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: cache; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA cache;


ALTER SCHEMA cache OWNER TO postgres;

--
-- Name: SCHEMA cache; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA cache IS '缓存schema';


--
-- Name: langchain; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA langchain;


ALTER SCHEMA langchain OWNER TO postgres;

--
-- Name: SCHEMA langchain; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA langchain IS 'LangChain生产的相关表结构';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: summary_cache; Type: TABLE; Schema: cache; Owner: postgres
--

CREATE TABLE cache.summary_cache (
    id integer NOT NULL,
    article_id character varying(32) NOT NULL,
    article_name character varying(30) NOT NULL,
    article_summary text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE cache.summary_cache OWNER TO postgres;

--
-- Name: TABLE summary_cache; Type: COMMENT; Schema: cache; Owner: postgres
--

COMMENT ON TABLE cache.summary_cache IS '文章缓存表';


--
-- Name: COLUMN summary_cache.article_id; Type: COMMENT; Schema: cache; Owner: postgres
--

COMMENT ON COLUMN cache.summary_cache.article_id IS '文章唯一标识';


--
-- Name: COLUMN summary_cache.article_name; Type: COMMENT; Schema: cache; Owner: postgres
--

COMMENT ON COLUMN cache.summary_cache.article_name IS '文章名';


--
-- Name: COLUMN summary_cache.article_summary; Type: COMMENT; Schema: cache; Owner: postgres
--

COMMENT ON COLUMN cache.summary_cache.article_summary IS '文章摘要';


--
-- Name: COLUMN summary_cache.created_at; Type: COMMENT; Schema: cache; Owner: postgres
--

COMMENT ON COLUMN cache.summary_cache.created_at IS '创建时间';


--
-- Name: summary_cache_id_seq; Type: SEQUENCE; Schema: cache; Owner: postgres
--

CREATE SEQUENCE cache.summary_cache_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE cache.summary_cache_id_seq OWNER TO postgres;

--
-- Name: summary_cache_id_seq; Type: SEQUENCE OWNED BY; Schema: cache; Owner: postgres
--

ALTER SEQUENCE cache.summary_cache_id_seq OWNED BY cache.summary_cache.id;


--
-- Name: checkpoint_blobs; Type: TABLE; Schema: langchain; Owner: postgres
--

CREATE TABLE langchain.checkpoint_blobs (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    channel text NOT NULL,
    version text NOT NULL,
    type text NOT NULL,
    blob bytea
);


ALTER TABLE langchain.checkpoint_blobs OWNER TO postgres;

--
-- Name: checkpoint_migrations; Type: TABLE; Schema: langchain; Owner: postgres
--

CREATE TABLE langchain.checkpoint_migrations (
    v integer NOT NULL
);


ALTER TABLE langchain.checkpoint_migrations OWNER TO postgres;

--
-- Name: checkpoint_writes; Type: TABLE; Schema: langchain; Owner: postgres
--

CREATE TABLE langchain.checkpoint_writes (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    checkpoint_id text NOT NULL,
    task_id text NOT NULL,
    idx integer NOT NULL,
    channel text NOT NULL,
    type text,
    blob bytea NOT NULL,
    task_path text DEFAULT ''::text NOT NULL
);


ALTER TABLE langchain.checkpoint_writes OWNER TO postgres;

--
-- Name: checkpoints; Type: TABLE; Schema: langchain; Owner: postgres
--

CREATE TABLE langchain.checkpoints (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    checkpoint_id text NOT NULL,
    parent_checkpoint_id text,
    type text,
    checkpoint jsonb NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL
);


ALTER TABLE langchain.checkpoints OWNER TO postgres;

--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    filename character varying(30) NOT NULL,
    filesize integer NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    collection_name character varying(255) NOT NULL
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: COLUMN documents.collection_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.documents.collection_name IS '所属集合';


--
-- Name: model_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model_type (
    id integer NOT NULL,
    model_type_name character varying(20),
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.model_type OWNER TO postgres;

--
-- Name: COLUMN model_type.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.model_type.id IS '类型的唯一id';


--
-- Name: COLUMN model_type.model_type_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.model_type.model_type_name IS '模型分类名称';


--
-- Name: COLUMN model_type.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.model_type.created_at IS '创建时间';


--
-- Name: model_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.model_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.model_type_id_seq OWNER TO postgres;

--
-- Name: model_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.model_type_id_seq OWNED BY public.model_type.id;


--
-- Name: model_type_link; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.model_type_link (
    id integer NOT NULL,
    model_id integer NOT NULL,
    type_id integer NOT NULL
);


ALTER TABLE public.model_type_link OWNER TO postgres;

--
-- Name: TABLE model_type_link; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.model_type_link IS '模型，类型关联表';


--
-- Name: COLUMN model_type_link.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.model_type_link.id IS '唯一id';


--
-- Name: COLUMN model_type_link.model_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.model_type_link.model_id IS '模型id';


--
-- Name: COLUMN model_type_link.type_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.model_type_link.type_id IS '类型id';


--
-- Name: model_type_link_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.model_type_link_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.model_type_link_id_seq OWNER TO postgres;

--
-- Name: model_type_link_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.model_type_link_id_seq OWNED BY public.model_type_link.id;


--
-- Name: models_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.models_id_seq
    AS integer
    START WITH 1001
    INCREMENT BY 1
    MINVALUE 1001
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.models_id_seq OWNER TO postgres;

--
-- Name: models; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.models (
    id integer DEFAULT nextval('public.models_id_seq'::regclass) CONSTRAINT models_model_id_not_null NOT NULL,
    model_name character varying(50) NOT NULL,
    group_uuid uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid CONSTRAINT models_user_uuid_not_null NOT NULL,
    api_key character varying(255),
    base_url character varying(255),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.models OWNER TO postgres;

--
-- Name: TABLE models; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.models IS 'llm管理库';


--
-- Name: COLUMN models.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models.id IS '主键id';


--
-- Name: COLUMN models.model_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models.model_name IS '模型名称';


--
-- Name: COLUMN models.group_uuid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models.group_uuid IS 'llm所属分组id';


--
-- Name: COLUMN models.user_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models.user_id IS '添加该llm的用户唯一标识';


--
-- Name: COLUMN models.api_key; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models.api_key IS '大模型对应的api_key';


--
-- Name: COLUMN models.base_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models.base_url IS '大模型的base_url';


--
-- Name: COLUMN models.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models.created_at IS '创建时间';


--
-- Name: COLUMN models.updated_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models.updated_at IS '修改时间';


--
-- Name: models_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.models_group_id_seq
    AS integer
    START WITH 1001
    INCREMENT BY 1
    MINVALUE 1001
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.models_group_id_seq OWNER TO postgres;

--
-- Name: models_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.models_group (
    id integer DEFAULT nextval('public.models_group_id_seq'::regclass) CONSTRAINT model_group_id_not_null NOT NULL,
    group_uuid uuid DEFAULT gen_random_uuid() CONSTRAINT model_group_group_uuid_not_null NOT NULL,
    group_name character varying(50) CONSTRAINT model_group_group_name_not_null NOT NULL,
    group_attr character varying(255),
    created_at timestamp with time zone DEFAULT now(),
    api_key character varying(255),
    base_url character varying(255)
);


ALTER TABLE public.models_group OWNER TO postgres;

--
-- Name: TABLE models_group; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.models_group IS '大模型分组';


--
-- Name: COLUMN models_group.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models_group.id IS '主键id';


--
-- Name: COLUMN models_group.group_uuid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models_group.group_uuid IS '提供商唯一id';


--
-- Name: COLUMN models_group.group_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models_group.group_name IS '提供商名称';


--
-- Name: COLUMN models_group.group_attr; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models_group.group_attr IS '提供商图片';


--
-- Name: COLUMN models_group.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models_group.created_at IS '创建时间';


--
-- Name: COLUMN models_group.api_key; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models_group.api_key IS '提供商默认api-key';


--
-- Name: COLUMN models_group.base_url; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.models_group.base_url IS '公共的base_url';


--
-- Name: request_time_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.request_time_log (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    thread_id text NOT NULL,
    total_duration real NOT NULL,
    prompt text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    model_id integer NOT NULL
);


ALTER TABLE public.request_time_log OWNER TO postgres;

--
-- Name: COLUMN request_time_log.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.request_time_log.id IS 'log Id';


--
-- Name: COLUMN request_time_log.thread_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.request_time_log.thread_id IS '会话唯一标识';


--
-- Name: COLUMN request_time_log.total_duration; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.request_time_log.total_duration IS '响应总耗时';


--
-- Name: COLUMN request_time_log.prompt; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.request_time_log.prompt IS '调用提示词';


--
-- Name: COLUMN request_time_log.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.request_time_log.created_at IS '创建时间';


--
-- Name: COLUMN request_time_log.model_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.request_time_log.model_id IS '模型id';


--
-- Name: system_configs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.system_configs (
    id integer NOT NULL,
    config_key character varying(100) NOT NULL,
    config_value jsonb NOT NULL,
    description text,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_by character varying(40) NOT NULL
);


ALTER TABLE public.system_configs OWNER TO postgres;

--
-- Name: TABLE system_configs; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.system_configs IS '系统配置表';


--
-- Name: COLUMN system_configs.config_key; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.system_configs.config_key IS 'key描述';


--
-- Name: COLUMN system_configs.config_value; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.system_configs.config_value IS '配置信息';


--
-- Name: COLUMN system_configs.description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.system_configs.description IS '配置描述';


--
-- Name: system_configs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.system_configs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_configs_id_seq OWNER TO postgres;

--
-- Name: system_configs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.system_configs_id_seq OWNED BY public.system_configs.id;


--
-- Name: tokens_usage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tokens_usage (
    id integer CONSTRAINT table_usage_id_not_null NOT NULL,
    user_id character varying(36) CONSTRAINT table_usage_user_id_not_null NOT NULL,
    model_id integer CONSTRAINT table_usage_model_id_not_null NOT NULL,
    prompt_tokens integer DEFAULT 0 CONSTRAINT table_usage_prompt_tokens_not_null NOT NULL,
    completion_tokens integer DEFAULT 0 CONSTRAINT table_usage_completion_tokens_not_null NOT NULL,
    total_tokens integer CONSTRAINT table_usage_total_tokens_not_null NOT NULL,
    created_at timestamp with time zone DEFAULT now() CONSTRAINT table_usage_created_at_not_null NOT NULL
);


ALTER TABLE public.tokens_usage OWNER TO postgres;

--
-- Name: TABLE tokens_usage; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tokens_usage IS 'Token使用量统计';


--
-- Name: COLUMN tokens_usage.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tokens_usage.id IS '唯一id';


--
-- Name: COLUMN tokens_usage.user_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tokens_usage.user_id IS '调用方id';


--
-- Name: COLUMN tokens_usage.model_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tokens_usage.model_id IS '调用的模型id';


--
-- Name: COLUMN tokens_usage.prompt_tokens; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tokens_usage.prompt_tokens IS '提示的token消耗';


--
-- Name: COLUMN tokens_usage.completion_tokens; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tokens_usage.completion_tokens IS '补全的token消耗';


--
-- Name: COLUMN tokens_usage.total_tokens; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tokens_usage.total_tokens IS 'token总消耗量';


--
-- Name: COLUMN tokens_usage.created_at; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tokens_usage.created_at IS 'token消耗的时间';


--
-- Name: table_usage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.table_usage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.table_usage_id_seq OWNER TO postgres;

--
-- Name: table_usage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.table_usage_id_seq OWNED BY public.tokens_usage.id;


--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_sessions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id character varying(36) NOT NULL,
    thread_id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying(50) DEFAULT '新的会话'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    metadata jsonb NOT NULL
);


ALTER TABLE public.user_sessions OWNER TO postgres;

--
-- Name: TABLE user_sessions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.user_sessions IS '用户会话记录表';


--
-- Name: COLUMN user_sessions.thread_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_sessions.thread_id IS '会话标识';


--
-- Name: COLUMN user_sessions.title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_sessions.title IS '会话标题';


--
-- Name: COLUMN user_sessions.metadata; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_sessions.metadata IS '会话元数据';


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    user_uuid uuid DEFAULT gen_random_uuid() NOT NULL,
    ip_address inet,
    last_login_ip inet,
    username character varying(50),
    email character varying(100),
    phone character varying(20),
    password_hash character varying(255) NOT NULL,
    status smallint DEFAULT 1,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    last_login_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: vector_collection; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vector_collection (
    id integer NOT NULL,
    embedding_id integer,
    collection_name character varying(30) NOT NULL,
    collection_alias character varying(30),
    collection_description character varying(255) NOT NULL,
    items_number integer DEFAULT 0,
    created_at timestamp with time zone DEFAULT now(),
    dimensions integer DEFAULT 1024 NOT NULL
);


ALTER TABLE public.vector_collection OWNER TO postgres;

--
-- Name: COLUMN vector_collection.dimensions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.vector_collection.dimensions IS '存储向量的维度';


--
-- Name: vector_collection_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vector_collection_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vector_collection_id_seq OWNER TO postgres;

--
-- Name: vector_collection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vector_collection_id_seq OWNED BY public.vector_collection.id;


--
-- Name: vector_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vector_metadata (
    id uuid NOT NULL,
    content_hash character varying(64) NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    doc_id uuid NOT NULL,
    collection_name character varying(30) DEFAULT 'text_collection'::character varying NOT NULL
);


ALTER TABLE public.vector_metadata OWNER TO postgres;

--
-- Name: COLUMN vector_metadata.doc_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.vector_metadata.doc_id IS '所属文档的id';


--
-- Name: COLUMN vector_metadata.collection_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.vector_metadata.collection_name IS '所属集合';


--
-- Name: summary_cache id; Type: DEFAULT; Schema: cache; Owner: postgres
--

ALTER TABLE ONLY cache.summary_cache ALTER COLUMN id SET DEFAULT nextval('cache.summary_cache_id_seq'::regclass);


--
-- Name: model_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_type ALTER COLUMN id SET DEFAULT nextval('public.model_type_id_seq'::regclass);


--
-- Name: model_type_link id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.model_type_link ALTER COLUMN id SET DEFAULT nextval('public.model_type_link_id_seq'::regclass);


--
-- Name: system_configs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.system_configs ALTER COLUMN id SET DEFAULT nextval('public.system_configs_id_seq'::regclass);


--
-- Name: tokens_usage id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tokens_usage ALTER COLUMN id SET DEFAULT nextval('public.table_usage_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: vector_collection id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vector_collection ALTER COLUMN id SET DEFAULT nextval('public.vector_collection_id_seq'::regclass);