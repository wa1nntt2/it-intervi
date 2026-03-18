--
-- PostgreSQL database dump
--

\restrict OWmUZvUx9fAnbsvZEuVhXVFdwZK6KEJf0tJYFwZ1SO42RimiG0EYKdff35SKbJb

-- Dumped from database version 15.17
-- Dumped by pg_dump version 15.17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: achievements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.achievements (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    icon character varying NOT NULL,
    xp_reward integer,
    requirement_type character varying NOT NULL,
    requirement_value integer NOT NULL,
    category character varying
);


ALTER TABLE public.achievements OWNER TO postgres;

--
-- Name: achievements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.achievements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.achievements_id_seq OWNER TO postgres;

--
-- Name: achievements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.achievements_id_seq OWNED BY public.achievements.id;


--
-- Name: answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.answers (
    id integer NOT NULL,
    question_id integer NOT NULL,
    user_id integer,
    selected_option integer,
    selected_order json,
    is_correct boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.answers OWNER TO postgres;

--
-- Name: answers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.answers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answers_id_seq OWNER TO postgres;

--
-- Name: answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.answers_id_seq OWNED BY public.answers.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    profession_id integer NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: interview_configs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.interview_configs (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    profession_id integer NOT NULL,
    user_id integer,
    difficulty character varying,
    category_configs json NOT NULL,
    is_public boolean,
    is_default boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.interview_configs OWNER TO postgres;

--
-- Name: interview_configs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.interview_configs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.interview_configs_id_seq OWNER TO postgres;

--
-- Name: interview_configs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.interview_configs_id_seq OWNED BY public.interview_configs.id;


--
-- Name: ordering_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ordering_items (
    id integer NOT NULL,
    question_id integer NOT NULL,
    item_text character varying NOT NULL,
    correct_position integer NOT NULL
);


ALTER TABLE public.ordering_items OWNER TO postgres;

--
-- Name: ordering_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ordering_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ordering_items_id_seq OWNER TO postgres;

--
-- Name: ordering_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ordering_items_id_seq OWNED BY public.ordering_items.id;


--
-- Name: professions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.professions (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text
);


ALTER TABLE public.professions OWNER TO postgres;

--
-- Name: professions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.professions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.professions_id_seq OWNER TO postgres;

--
-- Name: professions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.professions_id_seq OWNED BY public.professions.id;


--
-- Name: question_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question_categories (
    question_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.question_categories OWNER TO postgres;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    text text NOT NULL,
    question_type character varying NOT NULL,
    profession_id integer NOT NULL,
    difficulty character varying,
    options json NOT NULL,
    correct_option integer,
    correct_order json,
    explanation text
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.questions_id_seq OWNER TO postgres;

--
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    id integer NOT NULL,
    profession_id integer NOT NULL,
    user_id integer,
    question_ids json NOT NULL,
    status character varying,
    score integer,
    mode character varying,
    time_limit integer,
    created_at timestamp without time zone,
    completed_at timestamp without time zone
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sessions_id_seq OWNER TO postgres;

--
-- Name: sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sessions_id_seq OWNED BY public.sessions.id;


--
-- Name: user_achievements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_achievements (
    id integer NOT NULL,
    user_id integer NOT NULL,
    achievement_id integer NOT NULL,
    unlocked_at timestamp without time zone
);


ALTER TABLE public.user_achievements OWNER TO postgres;

--
-- Name: user_achievements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_achievements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_achievements_id_seq OWNER TO postgres;

--
-- Name: user_achievements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_achievements_id_seq OWNED BY public.user_achievements.id;


--
-- Name: user_progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_progress (
    id integer NOT NULL,
    user_id integer NOT NULL,
    xp integer,
    level integer,
    total_sessions integer,
    completed_sessions integer,
    total_correct_answers integer,
    total_questions_answered integer,
    best_streak integer,
    current_streak integer,
    created_at timestamp without time zone,
    last_session_at timestamp without time zone,
    title character varying,
    badges json
);


ALTER TABLE public.user_progress OWNER TO postgres;

--
-- Name: user_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_progress_id_seq OWNER TO postgres;

--
-- Name: user_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_progress_id_seq OWNED BY public.user_progress.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_admin boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: achievements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.achievements ALTER COLUMN id SET DEFAULT nextval('public.achievements_id_seq'::regclass);


--
-- Name: answers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers ALTER COLUMN id SET DEFAULT nextval('public.answers_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: interview_configs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interview_configs ALTER COLUMN id SET DEFAULT nextval('public.interview_configs_id_seq'::regclass);


--
-- Name: ordering_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordering_items ALTER COLUMN id SET DEFAULT nextval('public.ordering_items_id_seq'::regclass);


--
-- Name: professions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.professions ALTER COLUMN id SET DEFAULT nextval('public.professions_id_seq'::regclass);


--
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- Name: sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions ALTER COLUMN id SET DEFAULT nextval('public.sessions_id_seq'::regclass);


--
-- Name: user_achievements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_achievements ALTER COLUMN id SET DEFAULT nextval('public.user_achievements_id_seq'::regclass);


--
-- Name: user_progress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_progress ALTER COLUMN id SET DEFAULT nextval('public.user_progress_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: achievements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.achievements (id, name, description, icon, xp_reward, requirement_type, requirement_value, category) FROM stdin;
\.


--
-- Data for Name: answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.answers (id, question_id, user_id, selected_option, selected_order, is_correct, created_at) FROM stdin;
1	68	1	1	\N	t	2026-03-18 20:20:19.204333
2	15	1	1	\N	t	2026-03-18 20:30:48.998133
3	41	1	1	\N	t	2026-03-18 20:30:49.049812
4	50	1	0	\N	t	2026-03-18 20:30:49.06402
5	1	1	2	\N	t	2026-03-18 20:30:49.075974
6	51	1	0	\N	t	2026-03-18 20:30:49.089251
7	32	1	2	\N	t	2026-03-18 20:30:49.101001
8	27	1	2	\N	f	2026-03-18 20:30:49.111449
9	42	1	2	\N	t	2026-03-18 20:30:49.1219
10	9	1	2	\N	t	2026-03-18 20:30:49.133068
11	6	1	2	\N	t	2026-03-18 20:30:49.143771
12	4	1	2	\N	t	2026-03-18 20:30:49.15522
13	2	1	1	\N	t	2026-03-18 20:30:49.166111
14	36	1	2	\N	t	2026-03-18 20:30:49.177172
15	35	1	1	\N	t	2026-03-18 20:30:49.18801
16	10	1	1	\N	f	2026-03-18 20:30:49.198365
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name, description, profession_id) FROM stdin;
1	HTML & CSS	Вопросы по теме HTML & CSS	1
2	JavaScript	Вопросы по теме JavaScript	1
3	React	Вопросы по теме React	1
4	Vue	Вопросы по теме Vue	1
5	Angular	Вопросы по теме Angular	1
6	TypeScript	Вопросы по теме TypeScript	1
7	CSS Frameworks	Вопросы по теме CSS Frameworks	1
8	Build Tools	Вопросы по теме Build Tools	1
9	Python	Вопросы по теме Python	2
10	Базы данных	Вопросы по теме Базы данных	2
11	API Design	Вопросы по теме API Design	2
12	Архитектура	Вопросы по теме Архитектура	2
13	Безопасность	Вопросы по теме Безопасность	2
14	Кэширование	Вопросы по теме Кэширование	2
15	Микросервисы	Вопросы по теме Микросервисы	2
16	Тестирование	Вопросы по теме Тестирование	2
17	Frontend + Backend	Вопросы по теме Frontend + Backend	3
18	Архитектура приложений	Вопросы по теме Архитектура приложений	3
19	Базы данных	Вопросы по теме Базы данных	3
20	DevOps основы	Вопросы по теме DevOps основы	3
21	API Integration	Вопросы по теме API Integration	3
22	Аутентификация	Вопросы по теме Аутентификация	3
23	Deployment	Вопросы по теме Deployment	3
24	Производительность	Вопросы по теме Производительность	3
25	Linux	Вопросы по теме Linux	4
26	Docker	Вопросы по теме Docker	4
27	Kubernetes	Вопросы по теме Kubernetes	4
28	CI/CD	Вопросы по теме CI/CD	4
29	Infrastructure as Code	Вопросы по теме Infrastructure as Code	4
30	Мониторинг	Вопросы по теме Мониторинг	4
31	Сети	Вопросы по теме Сети	4
32	Безопасность	Вопросы по теме Безопасность	4
33	Git	Вопросы по теме Git	4
34	Scripting	Вопросы по теме Scripting	4
\.


--
-- Data for Name: interview_configs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.interview_configs (id, name, description, profession_id, user_id, difficulty, category_configs, is_public, is_default, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: ordering_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ordering_items (id, question_id, item_text, correct_position) FROM stdin;
\.


--
-- Data for Name: professions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.professions (id, name, description) FROM stdin;
1	Frontend	Разработка клиентской части веб-приложений (HTML, CSS, JavaScript, React, Vue, Angular)
2	Backend	Разработка серверной части веб-приложений (Python, Java, Node.js, базы данных, API)
3	Fullstack	Универсальная разработка веб-приложений (Frontend + Backend)
4	DevOps	Автоматизация развертывания, CI/CD, контейнеризация, мониторинг (Docker, Kubernetes, Jenkins)
\.


--
-- Data for Name: question_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.question_categories (question_id, category_id) FROM stdin;
1	25
2	25
3	29
4	25
5	25
6	25
7	25
9	25
10	25
11	25
12	25
14	31
14	34
15	25
16	25
18	31
19	31
20	25
20	31
21	31
22	31
23	31
24	31
25	33
26	25
26	33
27	25
28	33
29	25
30	33
31	33
32	25
32	33
33	26
34	26
35	26
36	25
36	26
37	25
37	26
90	27
38	27
39	27
41	28
42	28
47	28
48	25
49	26
50	25
50	26
51	26
52	25
52	26
53	26
54	25
54	26
55	26
56	26
57	25
57	26
59	25
59	33
60	25
62	25
62	33
63	25
64	29
65	25
66	25
67	25
68	25
68	31
68	34
69	25
70	25
71	25
75	31
77	26
80	33
81	33
82	25
82	26
83	26
84	26
85	26
86	27
87	27
88	27
89	27
92	27
93	28
94	28
95	25
95	28
95	33
96	28
96	33
97	29
98	29
99	29
100	25
100	32
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (id, text, question_type, profession_id, difficulty, options, correct_option, correct_order, explanation) FROM stdin;
1	Что такое DevOps?	mcq	4	intern	["\\u041a\\u043e\\u043d\\u043a\\u0440\\u0435\\u0442\\u043d\\u044b\\u0439 \\u0438\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442 \\u0434\\u043b\\u044f \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438 \\u0442\\u0435\\u0441\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f", "\\u041e\\u0442\\u0434\\u0435\\u043b\\u044c\\u043d\\u0430\\u044f \\u0434\\u043e\\u043b\\u0436\\u043d\\u043e\\u0441\\u0442\\u044c, \\u043a\\u043e\\u0442\\u043e\\u0440\\u0430\\u044f \\u0437\\u0430\\u043d\\u0438\\u043c\\u0430\\u0435\\u0442\\u0441\\u044f \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u043d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u043e\\u0439 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432", "\\u041a\\u0443\\u043b\\u044c\\u0442\\u0443\\u0440\\u0430, \\u043d\\u0430\\u0431\\u043e\\u0440 \\u043f\\u0440\\u0430\\u043a\\u0442\\u0438\\u043a \\u0438 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u043e\\u0432 \\u0434\\u043b\\u044f \\u043e\\u0431\\u044a\\u0435\\u0434\\u0438\\u043d\\u0435\\u043d\\u0438\\u044f \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438 (Dev) \\u0438 \\u044d\\u043a\\u0441\\u043f\\u043b\\u0443\\u0430\\u0442\\u0430\\u0446\\u0438\\u0438 (Ops)", "\\u041c\\u0435\\u0442\\u043e\\u0434\\u043e\\u043b\\u043e\\u0433\\u0438\\u044f \\u0443\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u044f \\u043f\\u0440\\u043e\\u0435\\u043a\\u0442\\u0430\\u043c\\u0438, \\u043f\\u043e\\u0445\\u043e\\u0436\\u0430\\u044f \\u043d\\u0430 Waterfall"]	2	null	DevOps — это прежде всего философия, направленная на устранение барьеров между командами, автоматизацию и повышение скорости и надежности поставки ПО.
2	Основная цель внедрения DevOps?	mcq	4	intern	["\\u041f\\u043e\\u043b\\u043d\\u043e\\u0441\\u0442\\u044c\\u044e \\u0437\\u0430\\u043c\\u0435\\u043d\\u0438\\u0442\\u044c \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u0447\\u0438\\u043a\\u043e\\u0432 \\u0430\\u0434\\u043c\\u0438\\u043d\\u0438\\u0441\\u0442\\u0440\\u0430\\u0442\\u043e\\u0440\\u0430\\u043c\\u0438", "\\u0423\\u0441\\u043a\\u043e\\u0440\\u0435\\u043d\\u0438\\u0435 \\u0438 \\u043f\\u043e\\u0432\\u044b\\u0448\\u0435\\u043d\\u0438\\u0435 \\u043d\\u0430\\u0434\\u0435\\u0436\\u043d\\u043e\\u0441\\u0442\\u0438 \\u0434\\u043e\\u0441\\u0442\\u0430\\u0432\\u043a\\u0438 \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u0435\\u0441\\u043f\\u0435\\u0447\\u0435\\u043d\\u0438\\u044f", "\\u0423\\u0432\\u0435\\u043b\\u0438\\u0447\\u0435\\u043d\\u0438\\u0435 \\u043a\\u043e\\u043b\\u0438\\u0447\\u0435\\u0441\\u0442\\u0432\\u0430 \\u0434\\u043e\\u043a\\u0443\\u043c\\u0435\\u043d\\u0442\\u0430\\u0446\\u0438\\u0438", "\\u041f\\u0435\\u0440\\u0435\\u0441\\u0442\\u0430\\u0442\\u044c \\u0438\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u044c \\u0442\\u0435\\u0441\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435"]	1	null	DevOps стремится к более частым и стабильным релизам. Это достигается за счет автоматизации (CI/CD), мониторинга и тесного сотрудничества команд.
3	Что такое Infrastructure as Code (IaC)?	mcq	4	intern	["\\u0423\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u0435 \\u0438\\u043d\\u0444\\u0440\\u0430\\u0441\\u0442\\u0440\\u0443\\u043a\\u0442\\u0443\\u0440\\u043e\\u0439 (\\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0430\\u043c\\u0438, \\u0441\\u0435\\u0442\\u044f\\u043c\\u0438) \\u0447\\u0435\\u0440\\u0435\\u0437 \\u043e\\u043f\\u0438\\u0441\\u0430\\u043d\\u0438\\u0435 \\u0432 \\u0444\\u0430\\u0439\\u043b\\u0430\\u0445 \\u043a\\u043e\\u043d\\u0444\\u0438\\u0433\\u0443\\u0440\\u0430\\u0446\\u0438\\u0438, \\u043a\\u0430\\u043a \\u043a\\u043e\\u0434\\u043e\\u043c", "\\u0417\\u0430\\u043f\\u0443\\u0441\\u043a \\u043a\\u043e\\u0434\\u0430 \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u044f \\u043d\\u0430 \\u0444\\u0438\\u0437\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438\\u0445 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0430\\u0445 \\u0431\\u0435\\u0437 \\u0432\\u0438\\u0440\\u0442\\u0443\\u0430\\u043b\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438", "\\u041d\\u0430\\u043f\\u0438\\u0441\\u0430\\u043d\\u0438\\u0435 \\u043a\\u043e\\u0434\\u0430 \\u043d\\u0430 \\u044f\\u0437\\u044b\\u043a\\u0430\\u0445 \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u043d\\u0438\\u0437\\u043a\\u043e\\u0433\\u043e \\u0443\\u0440\\u043e\\u0432\\u043d\\u044f \\u0434\\u043b\\u044f BIOS", "\\u0420\\u0443\\u0447\\u043d\\u043e\\u0435 \\u0438\\u0437\\u043c\\u0435\\u043d\\u0435\\u043d\\u0438\\u0435 \\u043a\\u043e\\u043d\\u0444\\u0438\\u0433\\u0443\\u0440\\u0430\\u0446\\u0438\\u0438 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432 \\u0447\\u0435\\u0440\\u0435\\u0437 SSH"]	0	null	IaC позволяет хранить конфигурацию инфраструктуры в Git, применять к ней контроль версий, ревью и автоматически разворачивать идентичные окружения.
4	Что означает термин "Automation" в контексте DevOps?	mcq	4	intern	["\\u0410\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u043e\\u0435 \\u043d\\u0430\\u043f\\u0438\\u0441\\u0430\\u043d\\u0438\\u0435 \\u043a\\u043e\\u0434\\u0430 \\u043d\\u0435\\u0439\\u0440\\u043e\\u0441\\u0435\\u0442\\u044f\\u043c\\u0438", "\\u0423\\u0432\\u043e\\u043b\\u044c\\u043d\\u0435\\u043d\\u0438\\u0435 \\u0432\\u0441\\u0435\\u0445 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u043d\\u044b\\u0445 \\u0430\\u0434\\u043c\\u0438\\u043d\\u0438\\u0441\\u0442\\u0440\\u0430\\u0442\\u043e\\u0440\\u043e\\u0432", "\\u0410\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0437\\u0430\\u0446\\u0438\\u044f \\u0440\\u0443\\u0442\\u0438\\u043d\\u043d\\u044b\\u0445 \\u0437\\u0430\\u0434\\u0430\\u0447: \\u0441\\u0431\\u043e\\u0440\\u043a\\u0438, \\u0442\\u0435\\u0441\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f, \\u0440\\u0430\\u0437\\u0432\\u0435\\u0440\\u0442\\u044b\\u0432\\u0430\\u043d\\u0438\\u044f, \\u043d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0438 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432", "\\u0410\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0430\\u044f \\u043e\\u0442\\u043f\\u0440\\u0430\\u0432\\u043a\\u0430 \\u043f\\u0438\\u0441\\u0435\\u043c \\u0441 \\u043e\\u0442\\u0447\\u0435\\u0442\\u0430\\u043c\\u0438"]	2	null	Автоматизация снижает риск человеческой ошибки и освобождает время команды для решения более сложных задач.
5	Зачем в DevOps нужна культура сотрудничества (Collaboration)?	mcq	4	intern	["\\u0427\\u0442\\u043e\\u0431\\u044b \\u0432\\u043c\\u0435\\u0441\\u0442\\u0435 \\u0445\\u043e\\u0434\\u0438\\u0442\\u044c \\u043d\\u0430 \\u043e\\u0431\\u0435\\u0434", "\\u0427\\u0442\\u043e\\u0431\\u044b \\u0431\\u044b\\u043b\\u043e \\u043a\\u043e\\u043c\\u0443 \\u043f\\u0435\\u0440\\u0435\\u043b\\u043e\\u0436\\u0438\\u0442\\u044c \\u0432\\u0438\\u043d\\u0443 \\u0437\\u0430 \\u0441\\u0431\\u043e\\u0439", "\\u0427\\u0442\\u043e\\u0431\\u044b \\u0440\\u0430\\u0437\\u0440\\u0443\\u0448\\u0438\\u0442\\u044c \\"\\u0441\\u0442\\u0435\\u043d\\u044b\\" \\u043c\\u0435\\u0436\\u0434\\u0443 Dev \\u0438 Ops, \\u0441\\u0434\\u0435\\u043b\\u0430\\u0432 \\u043a\\u043e\\u043c\\u0430\\u043d\\u0434\\u044b \\u043e\\u0442\\u0432\\u0435\\u0442\\u0441\\u0442\\u0432\\u0435\\u043d\\u043d\\u044b\\u043c\\u0438 \\u0437\\u0430 \\u043f\\u0440\\u043e\\u0434\\u0443\\u043a\\u0442 \\u0446\\u0435\\u043b\\u0438\\u043a\\u043e\\u043c", "\\u042d\\u0442\\u043e \\u043f\\u0440\\u043e\\u0441\\u0442\\u043e \\u043c\\u043e\\u0434\\u043d\\u043e\\u0435 \\u0441\\u043b\\u043e\\u0432\\u043e, \\u043d\\u0430 \\u043f\\u0440\\u0430\\u043a\\u0442\\u0438\\u043a\\u0435 \\u043d\\u0435 \\u0440\\u0430\\u0431\\u043e\\u0442\\u0430\\u0435\\u0442"]	2	null	Когда разработчик понимает, как его код будет работать на проде, а администратор участвует в планировании фич — продукт становится качественнее.
6	Какой командой можно посмотреть список запущенных процессов в реальном времени?	mcq	4	intern	["ls", "df -h", "top (\\u0438\\u043b\\u0438 htop)", "echo"]	2	null	`top` показывает динамический список процессов и потребление ресурсов. `htop` — более продвинутая и удобная версия.
7	Как проверить, сколько свободного места на диске в Linux?	mcq	4	intern	["free -m", "df -h", "du -sh", "ps aux"]	1	null	`df` (disk free) с флагом `-h` (human-readable) показывает занятое и свободное место на всех смонтированных файловых системах.
8	Как узнать размер папки `/var/log`?	mcq	4	intern	["df -h /var/log", "du -sh /var/log", "ls -lh /var/log", "cat /var/log"]	1	null	`du` (disk usage) с флагом `-s` (summary) и `-h` покажет общий размер указанной директории.
9	Какая команда используется для просмотра содержимого файла (например, лога) в реальном времени, по мере его дополнения?	mcq	4	intern	["cat file.log", "head -f file.log", "tail -f file.log", "less file.log"]	2	null	`tail -f` (follow) незаменима для наблюдения за растущими логами.
10	Как в текстовом файле найти все строки, содержащие слово "error", не учитывая регистр?	mcq	4	intern	["cat file \\\\| wc -l error", "find . -name \\"error\\"", "grep -i error file.log", "sed 's/error//g' file.log"]	2	null	`grep` (global regular expression print) с флагом `-i` (ignore case) ищет строки, соответствующие шаблону.
11	Как посмотреть переменные окружения в Linux?	mcq	4	intern	["ls env", "echo $VAR", "env \\u0438\\u043b\\u0438 printenv", "export"]	2	null	Команда `env` выводит список всех установленных переменных окружения.
12	Что сделает команда `ping -c 4 google.com`?	mcq	4	intern	["\\u041e\\u0442\\u043f\\u0440\\u0430\\u0432\\u0438\\u0442 4 \\u043f\\u0430\\u043a\\u0435\\u0442\\u0430 \\u043d\\u0430 \\u0433\\u0443\\u0433\\u043b \\u0438 \\u0437\\u0430\\u0432\\u0435\\u0440\\u0448\\u0438\\u0442\\u0441\\u044f", "\\u0411\\u0443\\u0434\\u0435\\u0442 \\u043f\\u0438\\u043d\\u0433\\u043e\\u0432\\u0430\\u0442\\u044c \\u0431\\u0435\\u0441\\u043a\\u043e\\u043d\\u0435\\u0447\\u043d\\u043e", "\\u041f\\u043e\\u043a\\u0430\\u0436\\u0435\\u0442 \\u043c\\u0430\\u0440\\u0448\\u0440\\u0443\\u0442 \\u0434\\u043e \\u0433\\u0443\\u0433\\u043b\\u0430", "\\u041f\\u0440\\u043e\\u0432\\u0435\\u0440\\u0438\\u0442, \\u043e\\u0442\\u043a\\u0440\\u044b\\u0442 \\u043b\\u0438 \\u043f\\u043e\\u0440\\u0442 80"]	0	null	Флаг `-c` (count) задает количество отправляемых пакетов.
13	Как создать нового пользователя с именем `john`?	mcq	4	intern	["useradd john", "adduser john", "newuser john", "\\u0412\\u0441\\u0435 \\u0432\\u0430\\u0440\\u0438\\u0430\\u043d\\u0442\\u044b \\u0432\\u0435\\u0440\\u043d\\u044b (useradd/adduser, \\u0432 \\u0437\\u0430\\u0432\\u0438\\u0441\\u0438\\u043c\\u043e\\u0441\\u0442\\u0438 \\u043e\\u0442 \\u0434\\u0438\\u0441\\u0442\\u0440\\u0438\\u0431\\u0443\\u0442\\u0438\\u0432\\u0430)"]	3	null	`useradd` — базовая утилита, `adduser` — более дружелюбный скрипт-обертка (обычно в Debian/Ubuntu). Оба создают пользователя.
14	Как сделать скрипт `my_script.py` исполняемым?	mcq	4	intern	["./my_script.py", "python my_script.py", "chmod +x my_script.py", "execute my_script.py"]	2	null	`chmod +x` добавляет флаг исполнения (execute) для владельца, группы и остальных.
15	Что покажет команда `whoami`?	mcq	4	intern	["\\u0421\\u043f\\u0438\\u0441\\u043e\\u043a \\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u0435\\u0439 \\u0432 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u0435", "\\u0418\\u043c\\u044f \\u0442\\u0435\\u043a\\u0443\\u0449\\u0435\\u0433\\u043e \\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044f", "IP-\\u0430\\u0434\\u0440\\u0435\\u0441 \\u0442\\u0435\\u043a\\u0443\\u0449\\u0435\\u0433\\u043e \\u0445\\u043e\\u0441\\u0442\\u0430", "\\u0422\\u0435\\u043a\\u0443\\u0449\\u0443\\u044e \\u0434\\u0438\\u0440\\u0435\\u043a\\u0442\\u043e\\u0440\\u0438\\u044e"]	1	null	Буквально: "кто я?".
16	Как вывести первые 10 строк файла?	mcq	4	intern	["tail file.txt", "cat -10 file.txt", "head file.txt", "less file.txt"]	2	null	По умолчанию `head` выводит первые 10 строк, `tail` — последние 10.
17	Что произойдет, когда вы введете google.com в браузере?	mcq	4	intern	["\\u0411\\u0440\\u0430\\u0443\\u0437\\u0435\\u0440 \\u0441\\u0440\\u0430\\u0437\\u0443 \\u043e\\u0442\\u043f\\u0440\\u0430\\u0432\\u0438\\u0442 \\u0437\\u0430\\u043f\\u0440\\u043e\\u0441 \\u043d\\u0430 IP 8.8.8.8", "\\u0411\\u0440\\u0430\\u0443\\u0437\\u0435\\u0440 \\u043f\\u0440\\u043e\\u0432\\u0435\\u0440\\u0438\\u0442 \\u043a\\u044d\\u0448, \\u0437\\u0430\\u0442\\u0435\\u043c DNS, \\u0443\\u0441\\u0442\\u0430\\u043d\\u043e\\u0432\\u0438\\u0442 TCP-\\u0441\\u043e\\u0435\\u0434\\u0438\\u043d\\u0435\\u043d\\u0438\\u0435, \\u043e\\u0442\\u043f\\u0440\\u0430\\u0432\\u0438\\u0442 HTTP-\\u0437\\u0430\\u043f\\u0440\\u043e\\u0441, \\u043f\\u043e\\u043b\\u0443\\u0447\\u0438\\u0442 \\u043e\\u0442\\u0432\\u0435\\u0442 \\u0438 \\u043e\\u0442\\u0440\\u0435\\u043d\\u0434\\u0435\\u0440\\u0438\\u0442 \\u0441\\u0442\\u0440\\u0430\\u043d\\u0438\\u0446\\u0443", "\\u0421\\u043d\\u0430\\u0447\\u0430\\u043b\\u0430 \\u0441\\u0440\\u0430\\u0431\\u043e\\u0442\\u0430\\u0435\\u0442 \\u043f\\u0440\\u043e\\u0442\\u043e\\u043a\\u043e\\u043b FTP", "\\u0411\\u0443\\u0434\\u0435\\u0442 \\u043e\\u0442\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d ICMP ping"]	1	null	Классический вопрос для проверки понимания веб-стека: DNS -> TCP (3-way handshake) -> TLS (если HTTPS) -> HTTP Request -> HTTP Response.
18	Что такое DNS?	mcq	4	intern	["\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430 \\u0434\\u043b\\u044f \\u0434\\u0438\\u043d\\u0430\\u043c\\u0438\\u0447\\u0435\\u0441\\u043a\\u043e\\u0439 \\u043c\\u0430\\u0440\\u0448\\u0440\\u0443\\u0442\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438 \\u043f\\u0430\\u043a\\u0435\\u0442\\u043e\\u0432", "\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430 \\u0434\\u043e\\u043c\\u0435\\u043d\\u043d\\u044b\\u0445 \\u0438\\u043c\\u0435\\u043d (Domain Name System), \\u043f\\u0440\\u0435\\u043e\\u0431\\u0440\\u0430\\u0437\\u0443\\u044e\\u0449\\u0430\\u044f \\u0438\\u043c\\u0435\\u043d\\u0430 \\u0445\\u043e\\u0441\\u0442\\u043e\\u0432 (google.com) \\u0432 IP-\\u0430\\u0434\\u0440\\u0435\\u0441\\u0430", "\\u041f\\u0440\\u043e\\u0442\\u043e\\u043a\\u043e\\u043b \\u0434\\u043b\\u044f \\u043e\\u0442\\u043f\\u0440\\u0430\\u0432\\u043a\\u0438 \\u043f\\u043e\\u0447\\u0442\\u044b", "\\u0422\\u0438\\u043f \\u0441\\u0435\\u0442\\u0435\\u0432\\u043e\\u0433\\u043e \\u044d\\u043a\\u0440\\u0430\\u043d\\u0430"]	1	null	DNS — это "телефонная книга" интернета.
19	Какой порт используется по умолчанию для HTTP?	mcq	4	intern	["22", "443", "80", "25"]	2	null	HTTP — 80, HTTPS — 443, SSH — 22, DNS — 53.
20	Какой протокол используется для безопасной передачи гипертекста (HTTPS)?	mcq	4	intern	["HTTP + FTP", "HTTP + TLS/SSL", "HTTP + SMTP", "HTTP + SNMP"]	1	null	HTTPS — это обычный HTTP, работающий поверх шифрованного TLS (ранее SSL) соединения.
21	Что такое IP-адрес?	mcq	4	intern	["\\u0423\\u043d\\u0438\\u043a\\u0430\\u043b\\u044c\\u043d\\u043e\\u0435 \\u0438\\u043c\\u044f \\u043a\\u043e\\u043c\\u043f\\u044c\\u044e\\u0442\\u0435\\u0440\\u0430 \\u0432 \\u0441\\u0435\\u0442\\u0438", "\\u0423\\u043d\\u0438\\u043a\\u0430\\u043b\\u044c\\u043d\\u044b\\u0439 \\u0447\\u0438\\u0441\\u043b\\u043e\\u0432\\u043e\\u0439 \\u0438\\u0434\\u0435\\u043d\\u0442\\u0438\\u0444\\u0438\\u043a\\u0430\\u0442\\u043e\\u0440 \\u0443\\u0441\\u0442\\u0440\\u043e\\u0439\\u0441\\u0442\\u0432\\u0430 \\u0432 \\u043a\\u043e\\u043c\\u043f\\u044c\\u044e\\u0442\\u0435\\u0440\\u043d\\u043e\\u0439 \\u0441\\u0435\\u0442\\u0438", "\\u0410\\u0434\\u0440\\u0435\\u0441 \\u044d\\u043b\\u0435\\u043a\\u0442\\u0440\\u043e\\u043d\\u043d\\u043e\\u0439 \\u043f\\u043e\\u0447\\u0442\\u044b", "MAC-\\u0430\\u0434\\u0440\\u0435\\u0441 \\u0441\\u0435\\u0442\\u0435\\u0432\\u043e\\u0439 \\u043a\\u0430\\u0440\\u0442\\u044b"]	1	null	IP (Internet Protocol) адрес — это логический адрес устройства в сети (например, 192.168.1.1).
22	В чем разница между публичным (белым) и приватным (серым) IP-адресом?	mcq	4	intern	["\\u041f\\u0440\\u0438\\u0432\\u0430\\u0442\\u043d\\u044b\\u0435 \\u0430\\u0434\\u0440\\u0435\\u0441\\u0430 \\u0438\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u0443\\u044e\\u0442\\u0441\\u044f \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0432\\u043d\\u0443\\u0442\\u0440\\u0438 \\u043b\\u043e\\u043a\\u0430\\u043b\\u044c\\u043d\\u044b\\u0445 \\u0441\\u0435\\u0442\\u0435\\u0439 \\u0438 \\u043d\\u0435 \\u043c\\u0430\\u0440\\u0448\\u0440\\u0443\\u0442\\u0438\\u0437\\u0438\\u0440\\u0443\\u044e\\u0442\\u0441\\u044f \\u0432 \\u0438\\u043d\\u0442\\u0435\\u0440\\u043d\\u0435\\u0442\\u0435", "\\u041f\\u0443\\u0431\\u043b\\u0438\\u0447\\u043d\\u044b\\u0435 \\u0430\\u0434\\u0440\\u0435\\u0441\\u0430 \\u0431\\u044b\\u0441\\u0442\\u0440\\u0435\\u0435", "\\u041f\\u0440\\u0438\\u0432\\u0430\\u0442\\u043d\\u044b\\u0435 \\u0430\\u0434\\u0440\\u0435\\u0441\\u0430 \\u043d\\u0430\\u0447\\u0438\\u043d\\u0430\\u044e\\u0442\\u0441\\u044f \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0441 8.8.8.8", "\\u0420\\u0430\\u0437\\u043d\\u0438\\u0446\\u044b \\u043d\\u0435\\u0442"]	0	null	Приватные диапазоны: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Устройства с такими адресами выходят в интернет через NAT (например, роутер).
23	Что такое HTTP-метод GET?	mcq	4	intern	["\\u0417\\u0430\\u043f\\u0440\\u043e\\u0441 \\u043d\\u0430 \\u0443\\u0434\\u0430\\u043b\\u0435\\u043d\\u0438\\u0435 \\u0440\\u0435\\u0441\\u0443\\u0440\\u0441\\u0430", "\\u0417\\u0430\\u043f\\u0440\\u043e\\u0441 \\u043d\\u0430 \\u043f\\u043e\\u043b\\u0443\\u0447\\u0435\\u043d\\u0438\\u0435 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445 \\u0441 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0430", "\\u0417\\u0430\\u043f\\u0440\\u043e\\u0441 \\u043d\\u0430 \\u043e\\u0442\\u043f\\u0440\\u0430\\u0432\\u043a\\u0443 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445 \\u043d\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440 (\\u043d\\u0430\\u043f\\u0440\\u0438\\u043c\\u0435\\u0440, \\u0444\\u043e\\u0440\\u043c\\u044b)", "\\u0417\\u0430\\u043f\\u0440\\u043e\\u0441 \\u043d\\u0430 \\u043e\\u0431\\u043d\\u043e\\u0432\\u043b\\u0435\\u043d\\u0438\\u0435 \\u0440\\u0435\\u0441\\u0443\\u0440\\u0441\\u0430"]	1	null	GET — самый распространенный метод. Он не должен изменять состояние сервера (идемпотентен).
24	Какой HTTP-статус означает "Успешно" (OK)?	mcq	4	intern	["404", "200", "500", "301"]	1	null	200 OK — стандартный ответ на успешный GET-запрос. 404 — не найдено, 500 — внутренняя ошибка сервера, 301 — перемещено навсегда (редирект).
25	Для чего нужна система контроля версий (VCS), такая как Git?	mcq	4	intern	["\\u0414\\u043b\\u044f \\u043e\\u0431\\u0449\\u0435\\u043d\\u0438\\u044f \\u0432 \\u043a\\u043e\\u043c\\u0430\\u043d\\u0434\\u0435", "\\u0414\\u043b\\u044f \\u043e\\u0442\\u0441\\u043b\\u0435\\u0436\\u0438\\u0432\\u0430\\u043d\\u0438\\u044f \\u0438\\u0437\\u043c\\u0435\\u043d\\u0435\\u043d\\u0438\\u0439 \\u0432 \\u043a\\u043e\\u0434\\u0435, \\u0432\\u043e\\u0437\\u0432\\u0440\\u0430\\u0442\\u0430 \\u043a \\u0441\\u0442\\u0430\\u0440\\u044b\\u043c \\u0432\\u0435\\u0440\\u0441\\u0438\\u044f\\u043c \\u0438 \\u0441\\u043e\\u0432\\u043c\\u0435\\u0441\\u0442\\u043d\\u043e\\u0439 \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b", "\\u0414\\u043b\\u044f \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u043e\\u0433\\u043e \\u0434\\u0435\\u043f\\u043b\\u043e\\u044f \\u043a\\u043e\\u0434\\u0430 \\u043d\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440", "\\u0414\\u043b\\u044f \\u043a\\u043e\\u043c\\u043f\\u0438\\u043b\\u044f\\u0446\\u0438\\u0438 \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c"]	1	null	Git сохраняет всю историю проекта. Можно увидеть, кто, когда и зачем изменил любую строку.
26	Какая команда Git используется для сохранения изменений в локальный репозиторий?	mcq	4	intern	["git push", "git fetch", "git commit", "git pull"]	2	null	`git commit` создает "снимок" (snapshot) состояния проекта на текущий момент в локальной истории.
27	Какая команда загружает изменения из удаленного репозитория в локальный и сразу сливает их с текущей веткой?	mcq	4	intern	["git fetch", "git pull", "git push", "git merge"]	1	null	`git pull = git fetch + git merge`. `git fetch` просто скачивает новые данные, но не применяет их к вашим рабочим файлам.
28	Что такое ветка (branch) в Git?	mcq	4	intern	["\\u0421\\u043a\\u043e\\u043f\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u044b\\u0439 \\u0440\\u0435\\u043f\\u043e\\u0437\\u0438\\u0442\\u043e\\u0440\\u0438\\u0439", "\\u041b\\u0435\\u0433\\u043a\\u043e\\u0432\\u0435\\u0441\\u043d\\u044b\\u0439 \\u0443\\u043a\\u0430\\u0437\\u0430\\u0442\\u0435\\u043b\\u044c \\u043d\\u0430 \\u043e\\u043f\\u0440\\u0435\\u0434\\u0435\\u043b\\u0435\\u043d\\u043d\\u044b\\u0439 \\u043a\\u043e\\u043c\\u043c\\u0438\\u0442, \\u043f\\u043e\\u0437\\u0432\\u043e\\u043b\\u044f\\u044e\\u0449\\u0438\\u0439 \\u0432\\u0435\\u0441\\u0442\\u0438 \\u043f\\u0430\\u0440\\u0430\\u043b\\u043b\\u0435\\u043b\\u044c\\u043d\\u0443\\u044e \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0443", "\\u041d\\u0430\\u0437\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0443\\u0434\\u0430\\u043b\\u0435\\u043d\\u043d\\u043e\\u0433\\u043e \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0430", "\\u041a\\u043e\\u043d\\u0444\\u043b\\u0438\\u043a\\u0442 \\u0432 \\u043a\\u043e\\u0434\\u0435"]	1	null	Ветки позволяют разрабатывать фичи независимо друг от друга, не мешая основной линии разработки (обычно `main` или `master`).
29	Вы хотите создать новую ветку `feature` и сразу переключиться на нее. Какая команда это сделает?	mcq	4	intern	["git branch feature", "git checkout feature", "git checkout -b feature", "git switch feature (\\u0431\\u0435\\u0437 \\u0444\\u043b\\u0430\\u0433\\u043e\\u0432)"]	2	null	`git checkout -b` создает ветку и переключается на нее. `git switch -c` делает то же самое в более новом синтаксисе.
30	Как отправить свои локальные коммиты в удаленный репозиторий (например, на GitHub)?	mcq	4	intern	["git pull", "git commit", "git push", "git fetch"]	2	null	`git push origin branch-name` отправляет изменения из вашей локальной ветки в ветку `branch-name` на удаленном сервере `origin`.
31	Что такое .gitignore?	mcq	4	intern	["\\u041a\\u043e\\u043c\\u0430\\u043d\\u0434\\u0430 \\u0434\\u043b\\u044f \\u0443\\u0434\\u0430\\u043b\\u0435\\u043d\\u0438\\u044f \\u0440\\u0435\\u043f\\u043e\\u0437\\u0438\\u0442\\u043e\\u0440\\u0438\\u044f", "\\u0424\\u0430\\u0439\\u043b, \\u0432 \\u043a\\u043e\\u0442\\u043e\\u0440\\u043e\\u043c \\u043f\\u0435\\u0440\\u0435\\u0447\\u0438\\u0441\\u043b\\u0435\\u043d\\u044b \\u0438\\u043c\\u0435\\u043d\\u0430 \\u0438 \\u043f\\u0430\\u043f\\u043a\\u0438, \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0435 Git \\u0434\\u043e\\u043b\\u0436\\u0435\\u043d \\u0438\\u0433\\u043d\\u043e\\u0440\\u0438\\u0440\\u043e\\u0432\\u0430\\u0442\\u044c (\\u043d\\u0435 \\u043e\\u0442\\u0441\\u043b\\u0435\\u0436\\u0438\\u0432\\u0430\\u0442\\u044c)", "\\u0424\\u0430\\u0439\\u043b \\u0441 \\u0438\\u0441\\u0442\\u043e\\u0440\\u0438\\u0435\\u0439 \\u043a\\u043e\\u043c\\u043c\\u0438\\u0442\\u043e\\u0432", "\\u041a\\u043e\\u043d\\u0444\\u0438\\u0433\\u0443\\u0440\\u0430\\u0446\\u0438\\u043e\\u043d\\u043d\\u044b\\u0439 \\u0444\\u0430\\u0439\\u043b \\u0441\\u0430\\u043c\\u043e\\u0433\\u043e Git"]	1	null	Туда помещают временные файлы, секреты (пароли), папки `node_modules`, чтобы не засорять репозиторий.
32	Для чего нужна команда `git log`?	mcq	4	intern	["\\u0414\\u043b\\u044f \\u0432\\u0445\\u043e\\u0434\\u0430 \\u0432 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u0443", "\\u0414\\u043b\\u044f \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u044f \\u043d\\u043e\\u0432\\u043e\\u0439 \\u0432\\u0435\\u0442\\u043a\\u0438", "\\u0414\\u043b\\u044f \\u043f\\u0440\\u043e\\u0441\\u043c\\u043e\\u0442\\u0440\\u0430 \\u0438\\u0441\\u0442\\u043e\\u0440\\u0438\\u0438 \\u043a\\u043e\\u043c\\u043c\\u0438\\u0442\\u043e\\u0432", "\\u0414\\u043b\\u044f \\u0443\\u0434\\u0430\\u043b\\u0435\\u043d\\u0438\\u044f \\u0444\\u0430\\u0439\\u043b\\u043e\\u0432"]	2	null	`git log` показывает список коммитов с их хешами, авторами и датами.
33	В чем ключевое отличие контейнера от виртуальной машины?	mcq	4	intern	["\\u041a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440 \\u0438\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u0443\\u0435\\u0442 \\u044f\\u0434\\u0440\\u043e \\u0445\\u043e\\u0441\\u0442\\u043e\\u0432\\u043e\\u0439 \\u041e\\u0421 \\u0438 \\u0438\\u0437\\u043e\\u043b\\u0438\\u0440\\u0443\\u0435\\u0442 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u044b, VM \\u0441\\u043e\\u0434\\u0435\\u0440\\u0436\\u0438\\u0442 \\u043f\\u043e\\u043b\\u043d\\u0443\\u044e \\u0433\\u043e\\u0441\\u0442\\u0435\\u0432\\u0443\\u044e \\u041e\\u0421 \\u0441\\u043e \\u0441\\u0432\\u043e\\u0438\\u043c \\u044f\\u0434\\u0440\\u043e\\u043c", "\\u041a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u044b \\u0440\\u0430\\u0431\\u043e\\u0442\\u0430\\u044e\\u0442 \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0432 Windows", "\\u0412\\u0438\\u0440\\u0442\\u0443\\u0430\\u043b\\u044c\\u043d\\u044b\\u0435 \\u043c\\u0430\\u0448\\u0438\\u043d\\u044b \\u0431\\u044b\\u0441\\u0442\\u0440\\u0435\\u0435 \\u0437\\u0430\\u043f\\u0443\\u0441\\u043a\\u0430\\u044e\\u0442\\u0441\\u044f", "\\u041a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u044b \\u043d\\u0435 \\u043c\\u043e\\u0433\\u0443\\u0442 \\u0432\\u044b\\u0445\\u043e\\u0434\\u0438\\u0442\\u044c \\u0432 \\u0438\\u043d\\u0442\\u0435\\u0440\\u043d\\u0435\\u0442"]	0	null	VM тяжелее (гигабайты), контейнеры легкие (мегабайты) и запускаются за секунды, так как не нужно грузить ОС.
34	Что такое Docker-образ (image)?	mcq	4	intern	["\\u0417\\u0430\\u043f\\u0443\\u0449\\u0435\\u043d\\u043d\\u044b\\u0439 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u0430", "\\u041d\\u0435\\u0438\\u0437\\u043c\\u0435\\u043d\\u044f\\u0435\\u043c\\u044b\\u0439 \\u0448\\u0430\\u0431\\u043b\\u043e\\u043d (\\u0441\\u043b\\u0435\\u043f\\u043e\\u043a) \\u0444\\u0430\\u0439\\u043b\\u043e\\u0432\\u043e\\u0439 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u044b \\u0434\\u043b\\u044f \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u044f \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u043e\\u0432", "\\u041b\\u043e\\u0433\\u0438 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u0430", "Docker-\\u0440\\u0435\\u043f\\u043e\\u0437\\u0438\\u0442\\u043e\\u0440\\u0438\\u0439"]	1	null	Образ — это как "класс" в ООП, а контейнер — "экземпляр" этого класса. Образы состоят из слоев.
35	Что такое Docker-контейнер?	mcq	4	intern	["\\u0424\\u0430\\u0439\\u043b \\u0441 \\u043d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0430\\u043c\\u0438 Docker", "\\u0417\\u0430\\u043f\\u0443\\u0449\\u0435\\u043d\\u043d\\u044b\\u0439 \\u044d\\u043a\\u0437\\u0435\\u043c\\u043f\\u043b\\u044f\\u0440 Docker-\\u043e\\u0431\\u0440\\u0430\\u0437\\u0430 (\\u0438\\u0437\\u043e\\u043b\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u044b\\u0439 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441)", "\\u0423\\u0442\\u0438\\u043b\\u0438\\u0442\\u0430 \\u0434\\u043b\\u044f \\u0441\\u0431\\u043e\\u0440\\u043a\\u0438 \\u043e\\u0431\\u0440\\u0430\\u0437\\u043e\\u0432", "\\u0413\\u0440\\u0430\\u0444\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438\\u0439 \\u0438\\u043d\\u0442\\u0435\\u0440\\u0444\\u0435\\u0439\\u0441 \\u0434\\u043b\\u044f Docker"]	1	null	Контейнер — это живая, работающая среда, созданная из образа.
36	Для чего нужен файл Dockerfile?	mcq	4	intern	["\\u0414\\u043b\\u044f \\u0437\\u0430\\u043f\\u0443\\u0441\\u043a\\u0430 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u043e\\u0432", "\\u0414\\u043b\\u044f \\u0445\\u0440\\u0430\\u043d\\u0435\\u043d\\u0438\\u044f \\u043b\\u043e\\u0433\\u043e\\u0432", "\\u0414\\u043b\\u044f \\u043e\\u043f\\u0438\\u0441\\u0430\\u043d\\u0438\\u044f \\u0438\\u043d\\u0441\\u0442\\u0440\\u0443\\u043a\\u0446\\u0438\\u0439 \\u043f\\u043e \\u0441\\u0431\\u043e\\u0440\\u043a\\u0435 Docker-\\u043e\\u0431\\u0440\\u0430\\u0437\\u0430", "\\u0414\\u043b\\u044f \\u043d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0438 \\u0441\\u0435\\u0442\\u0435\\u0439 \\u0432 Docker"]	2	null	Dockerfile содержит команды `FROM`, `RUN`, `COPY`, `CMD` и т.д., которые выполняются для создания образа.
37	Какая команда используется для запуска контейнера из образа?	mcq	4	intern	["docker build", "docker stop", "docker run", "docker commit"]	2	null	`docker run nginx` скачает образ (если его нет) и запустит контейнер с nginx.
90	Что такое namespace в Kubernetes?	mcq	4	junior	["\\u041d\\u0430\\u0437\\u0432\\u0430\\u043d\\u0438\\u0435 \\u043a\\u043b\\u0430\\u0441\\u0442\\u0435\\u0440\\u0430", "\\u041f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441 \\u043d\\u0430 \\u043d\\u043e\\u0434\\u0435", "\\u0421\\u043f\\u043e\\u0441\\u043e\\u0431 \\u043b\\u043e\\u0433\\u0438\\u0447\\u0435\\u0441\\u043a\\u043e\\u0433\\u043e \\u0440\\u0430\\u0437\\u0434\\u0435\\u043b\\u0435\\u043d\\u0438\\u044f \\u0440\\u0435\\u0441\\u0443\\u0440\\u0441\\u043e\\u0432 \\u043a\\u043b\\u0430\\u0441\\u0442\\u0435\\u0440\\u0430 \\u043c\\u0435\\u0436\\u0434\\u0443 \\u0440\\u0430\\u0437\\u043d\\u044b\\u043c\\u0438 \\u043a\\u043e\\u043c\\u0430\\u043d\\u0434\\u0430\\u043c\\u0438 \\u0438\\u043b\\u0438 \\u043f\\u0440\\u043e\\u0435\\u043a\\u0442\\u0430\\u043c\\u0438", "\\u0422\\u0438\\u043f \\u043f\\u043e\\u0434\\u0430"]	2	null	Позволяет иметь несколько "виртуальных кластеров" внутри одного физического. Например, namespace "dev" и "prod".
38	Что такое Kubernetes (K8s)?	mcq	4	intern	["\\u0415\\u0449\\u0435 \\u043e\\u0434\\u0438\\u043d \\u0438\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442 \\u0434\\u043b\\u044f \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438, \\u043a\\u0430\\u043a Docker", "\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430 \\u0434\\u043b\\u044f \\u043a\\u043e\\u043d\\u0442\\u0440\\u043e\\u043b\\u044f \\u0432\\u0435\\u0440\\u0441\\u0438\\u0439", "\\u041f\\u043b\\u0430\\u0442\\u0444\\u043e\\u0440\\u043c\\u0430 \\u0434\\u043b\\u044f \\u043e\\u0440\\u043a\\u0435\\u0441\\u0442\\u0440\\u0430\\u0446\\u0438\\u0438 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u043e\\u0432: \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438 \\u0440\\u0430\\u0437\\u0432\\u0435\\u0440\\u0442\\u044b\\u0432\\u0430\\u043d\\u0438\\u044f, \\u043c\\u0430\\u0441\\u0448\\u0442\\u0430\\u0431\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u0438 \\u0443\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u044f", "\\u041e\\u0431\\u043b\\u0430\\u0447\\u043d\\u044b\\u0439 \\u043f\\u0440\\u043e\\u0432\\u0430\\u0439\\u0434\\u0435\\u0440"]	2	null	Если Docker — это "кирпичи" (контейнеры), то Kubernetes — это "прораб", который управляет этими кирпичами на множестве машин.
39	Что значит декларативный подход в Kubernetes?	mcq	4	intern	["\\u0412\\u044b \\u043f\\u0438\\u0448\\u0435\\u0442\\u0435 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442 \\u0441 \\u043f\\u043e\\u0441\\u043b\\u0435\\u0434\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044c\\u043d\\u043e\\u0441\\u0442\\u044c\\u044e \\u0434\\u0435\\u0439\\u0441\\u0442\\u0432\\u0438\\u0439", "\\u0412\\u044b \\u043e\\u043f\\u0438\\u0441\\u044b\\u0432\\u0430\\u0435\\u0442\\u0435 \\u0436\\u0435\\u043b\\u0430\\u0435\\u043c\\u043e\\u0435 \\u0441\\u043e\\u0441\\u0442\\u043e\\u044f\\u043d\\u0438\\u0435 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u044b (YAML-\\u0444\\u0430\\u0439\\u043b), \\u0430 Kubernetes \\u0441\\u0430\\u043c \\u0440\\u0435\\u0448\\u0430\\u0435\\u0442, \\u043a\\u0430\\u043a \\u043a \\u043d\\u0435\\u043c\\u0443 \\u043f\\u0440\\u0438\\u0439\\u0442\\u0438", "\\u0412\\u044b \\u0432\\u0440\\u0443\\u0447\\u043d\\u0443\\u044e \\u0432\\u044b\\u043f\\u043e\\u043b\\u043d\\u044f\\u0435\\u0442\\u0435 \\u043a\\u043e\\u043c\\u0430\\u043d\\u0434\\u044b \\u043d\\u0430 \\u043a\\u0430\\u0436\\u0434\\u043e\\u043c \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0435", "\\u0418\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0438\\u043c\\u043f\\u0435\\u0440\\u0430\\u0442\\u0438\\u0432\\u043d\\u044b\\u0445 \\u043a\\u043e\\u043c\\u0430\\u043d\\u0434 \\u0442\\u0438\\u043f\\u0430 `kubectl run`"]	1	null	Декларативный подход — основа Kubernetes. Вы говорите "хочу 5 копий", а не "запусти контейнер, потом проверь, запусти еще один".
40	Что такое Continuous Integration (CI)?	mcq	4	intern	["\\u0410\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438\\u0439 \\u0434\\u0435\\u043f\\u043b\\u043e\\u0439 \\u043a\\u043e\\u0434\\u0430 \\u0432 \\u043f\\u0440\\u043e\\u0434", "\\u0420\\u0443\\u0447\\u043d\\u043e\\u0435 \\u0442\\u0435\\u0441\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 \\u043a\\u043e\\u0434\\u0430 \\u043f\\u0435\\u0440\\u0435\\u0434 \\u0440\\u0435\\u043b\\u0438\\u0437\\u043e\\u043c", "\\u0427\\u0430\\u0441\\u0442\\u0430\\u044f \\u0438\\u043d\\u0442\\u0435\\u0433\\u0440\\u0430\\u0446\\u0438\\u044f \\u043a\\u043e\\u0434\\u0430 \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u0447\\u0438\\u043a\\u043e\\u0432 \\u0432 \\u043e\\u0431\\u0449\\u0443\\u044e \\u0432\\u0435\\u0442\\u043a\\u0443 \\u0441 \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u043e\\u0439 \\u0441\\u0431\\u043e\\u0440\\u043a\\u043e\\u0439 \\u0438 \\u0437\\u0430\\u043f\\u0443\\u0441\\u043a\\u043e\\u043c \\u0442\\u0435\\u0441\\u0442\\u043e\\u0432", "\\u041d\\u0430\\u043f\\u0438\\u0441\\u0430\\u043d\\u0438\\u0435 \\u043a\\u043e\\u0434\\u0430 \\u0431\\u0435\\u0437 \\u043f\\u0435\\u0440\\u0435\\u0440\\u044b\\u0432\\u0430"]	2	null	Цель CI — быстро найти и исправить проблемы при слиянии кода от разных разработчиков.
41	Что такое CI/CD пайплайн?	mcq	4	intern	["\\u0413\\u0440\\u0443\\u043f\\u043f\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432, \\u043d\\u0430 \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0445 \\u0440\\u0430\\u0431\\u043e\\u0442\\u0430\\u0435\\u0442 CI", "\\u0410\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0437\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u0430\\u044f \\u043f\\u043e\\u0441\\u043b\\u0435\\u0434\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044c\\u043d\\u043e\\u0441\\u0442\\u044c \\u0448\\u0430\\u0433\\u043e\\u0432 (\\u0441\\u0442\\u0430\\u0434\\u0438\\u0439), \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0435 \\u043a\\u043e\\u0434 \\u043f\\u0440\\u043e\\u0445\\u043e\\u0434\\u0438\\u0442 \\u043e\\u0442 \\u043a\\u043e\\u043c\\u043c\\u0438\\u0442\\u0430 \\u0434\\u043e \\u0434\\u0435\\u043f\\u043b\\u043e\\u044f (\\u043d\\u0430\\u043f\\u0440\\u0438\\u043c\\u0435\\u0440: \\u0441\\u0431\\u043e\\u0440\\u043a\\u0430 -> \\u0442\\u0435\\u0441\\u0442\\u044b -> \\u0434\\u0435\\u043f\\u043b\\u043e\\u0439 \\u043d\\u0430 staging -> \\u0434\\u0435\\u043f\\u043b\\u043e\\u0439 \\u0432 \\u043f\\u0440\\u043e\\u0434)", "\\u0412\\u0438\\u0437\\u0443\\u0430\\u043b\\u044c\\u043d\\u043e\\u0435 \\u043e\\u0442\\u043e\\u0431\\u0440\\u0430\\u0436\\u0435\\u043d\\u0438\\u0435 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u043e\\u0432 \\u0432 \\u043e\\u0444\\u0438\\u0441\\u0435", "\\u0421\\u043f\\u0438\\u0441\\u043e\\u043a \\u0431\\u0430\\u0433\\u043e\\u0432 \\u0432 \\u043a\\u043e\\u0434\\u0435"]	1	null	Пайплайн описывает жизненный цикл кода.
42	Что обычно происходит на стадии "сборка" (build) в CI/CD?	mcq	4	intern	["\\u041e\\u0442\\u043f\\u0440\\u0430\\u0432\\u043a\\u0430 \\u0443\\u0432\\u0435\\u0434\\u043e\\u043c\\u043b\\u0435\\u043d\\u0438\\u0439 \\u0432 Telegram", "\\u041d\\u0430\\u043f\\u0438\\u0441\\u0430\\u043d\\u0438\\u0435 \\u043a\\u043e\\u0434\\u0430", "\\u041a\\u043e\\u043c\\u043f\\u0438\\u043b\\u044f\\u0446\\u0438\\u044f \\u043a\\u043e\\u0434\\u0430 (\\u0435\\u0441\\u043b\\u0438 \\u043d\\u0443\\u0436\\u043d\\u043e), \\u0443\\u043f\\u0430\\u043a\\u043e\\u0432\\u043a\\u0430 \\u0435\\u0433\\u043e \\u0432 \\u0430\\u0440\\u0442\\u0435\\u0444\\u0430\\u043a\\u0442 (\\u043d\\u0430\\u043f\\u0440\\u0438\\u043c\\u0435\\u0440, JAR, WAR, Docker-\\u043e\\u0431\\u0440\\u0430\\u0437)", "\\u041f\\u0440\\u043e\\u0432\\u0435\\u0440\\u043a\\u0430 \\u043a\\u043e\\u0434\\u0430 \\u043b\\u0438\\u043d\\u0442\\u0435\\u0440\\u043e\\u043c"]	2	null	Результат сборки — артефакт, готовый к развертыванию.
43	Зачем запускать автотесты в CI?	mcq	4	intern	["\\u0427\\u0442\\u043e\\u0431\\u044b \\u0437\\u0430\\u043d\\u044f\\u0442\\u044c \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u043e\\u0440", "\\u042d\\u0442\\u043e \\u043d\\u0435\\u043e\\u0431\\u044f\\u0437\\u0430\\u0442\\u0435\\u043b\\u044c\\u043d\\u043e", "\\u0427\\u0442\\u043e\\u0431\\u044b \\u0441\\u0440\\u0430\\u0437\\u0443 \\u043e\\u0431\\u043d\\u0430\\u0440\\u0443\\u0436\\u0438\\u0442\\u044c \\u043e\\u0448\\u0438\\u0431\\u043a\\u0438 \\u0438\\u043b\\u0438 \\u0440\\u0435\\u0433\\u0440\\u0435\\u0441\\u0441\\u0438\\u044e \\u043f\\u043e\\u0441\\u043b\\u0435 \\u0441\\u043b\\u0438\\u044f\\u043d\\u0438\\u044f \\u043a\\u043e\\u0434\\u0430, \\u043d\\u0435 \\u0434\\u043e\\u043f\\u0443\\u0441\\u043a\\u0430\\u044f \\u0438\\u0445 \\u0434\\u043e \\u043f\\u0440\\u043e\\u0434\\u0430\\u043a\\u0448\\u0435\\u043d\\u0430", "\\u0414\\u043b\\u044f \\u0433\\u0435\\u043d\\u0435\\u0440\\u0430\\u0446\\u0438\\u0438 \\u043e\\u0442\\u0447\\u0435\\u0442\\u043e\\u0432 \\u0434\\u043b\\u044f \\u043c\\u0435\\u043d\\u0435\\u0434\\u0436\\u0435\\u0440\\u043e\\u0432"]	2	null	Автоматические тесты — основа уверенности в качестве кода.
44	Что такое облачные провайдеры (Cloud Providers)?	mcq	4	intern	["\\u041a\\u043e\\u043c\\u043f\\u0430\\u043d\\u0438\\u0438, \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0435 \\u043f\\u0440\\u0435\\u0434\\u043e\\u0441\\u0442\\u0430\\u0432\\u043b\\u044f\\u044e\\u0442 \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f \\u0432 \\u0438\\u043d\\u0442\\u0435\\u0440\\u043d\\u0435\\u0442", "\\u041a\\u043e\\u043c\\u043f\\u0430\\u043d\\u0438\\u0438 (AWS, Google Cloud, Azure, Yandex Cloud), \\u043f\\u0440\\u0435\\u0434\\u043e\\u0441\\u0442\\u0430\\u0432\\u043b\\u044f\\u044e\\u0449\\u0438\\u0435 \\u0432\\u044b\\u0447\\u0438\\u0441\\u043b\\u0438\\u0442\\u0435\\u043b\\u044c\\u043d\\u044b\\u0435 \\u0440\\u0435\\u0441\\u0443\\u0440\\u0441\\u044b (\\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u044b, \\u0411\\u0414, \\u0445\\u0440\\u0430\\u043d\\u0438\\u043b\\u0438\\u0449\\u0430) \\u043f\\u043e \\u0437\\u0430\\u043f\\u0440\\u043e\\u0441\\u0443 \\u0447\\u0435\\u0440\\u0435\\u0437 \\u0438\\u043d\\u0442\\u0435\\u0440\\u043d\\u0435\\u0442", "\\u041f\\u0440\\u043e\\u0438\\u0437\\u0432\\u043e\\u0434\\u0438\\u0442\\u0435\\u043b\\u0438 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u043e\\u0440\\u043e\\u0432", "\\u0425\\u043e\\u0441\\u0442\\u0438\\u043d\\u0433-\\u043f\\u0440\\u043e\\u0432\\u0430\\u0439\\u0434\\u0435\\u0440\\u044b, \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0435 \\u0441\\u0434\\u0430\\u044e\\u0442 \\u0441\\u0442\\u043e\\u0439\\u043a\\u0438 \\u0441 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0430\\u043c\\u0438"]	1	null	Главная фишка облаков — "pay-as-you-go" (плати только за то, что используешь) и масштабирование по запросу.
45	Что такое AWS EC2?	mcq	4	intern	["\\u0421\\u0435\\u0440\\u0432\\u0438\\u0441 \\u0434\\u043b\\u044f \\u043e\\u0442\\u043f\\u0440\\u0430\\u0432\\u043a\\u0438 email", "\\u0412\\u0438\\u0440\\u0442\\u0443\\u0430\\u043b\\u044c\\u043d\\u044b\\u0435 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u044b \\u0432 \\u043e\\u0431\\u043b\\u0430\\u043a\\u0435 Amazon", "\\u041e\\u0431\\u044a\\u0435\\u043a\\u0442\\u043d\\u043e\\u0435 \\u0445\\u0440\\u0430\\u043d\\u0438\\u043b\\u0438\\u0449\\u0435 (\\u043a\\u0430\\u043a \\u0434\\u0438\\u0441\\u043a)", "\\u0423\\u043f\\u0440\\u0430\\u0432\\u043b\\u044f\\u0435\\u043c\\u0430\\u044f \\u0431\\u0430\\u0437\\u0430 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445"]	1	null	EC2 (Elastic Compute Cloud) — основа вычислительных мощностей AWS.
46	Что такое AWS S3?	mcq	4	intern	["\\u0421\\u0435\\u0440\\u0432\\u0438\\u0441 DNS", "\\u0411\\u0430\\u0437\\u0430 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "\\u041e\\u0431\\u044a\\u0435\\u043a\\u0442\\u043d\\u043e\\u0435 \\u0445\\u0440\\u0430\\u043d\\u0438\\u043b\\u0438\\u0449\\u0435 (\\u0434\\u043b\\u044f \\u0445\\u0440\\u0430\\u043d\\u0435\\u043d\\u0438\\u044f \\u0444\\u0430\\u0439\\u043b\\u043e\\u0432, \\u0441\\u0442\\u0430\\u0442\\u0438\\u043a\\u0438, \\u0431\\u044d\\u043a\\u0430\\u043f\\u043e\\u0432)", "\\u0421\\u0435\\u0440\\u0432\\u0438\\u0441 \\u043c\\u043e\\u043d\\u0438\\u0442\\u043e\\u0440\\u0438\\u043d\\u0433\\u0430"]	2	null	S3 (Simple Storage Service) хранит файлы в "бакетах" (bucket). Очень надежное и дешевое хранилище.
47	Как безопасно хранить пароли и ключи API в коде или CI/CD?	mcq	4	intern	["\\u0412 \\u043e\\u0442\\u043a\\u0440\\u044b\\u0442\\u043e\\u043c \\u0432\\u0438\\u0434\\u0435 \\u043f\\u0440\\u044f\\u043c\\u043e \\u0432 \\u043a\\u043e\\u0434\\u0435", "\\u0412 \\u043a\\u043e\\u043c\\u043c\\u0435\\u043d\\u0442\\u0430\\u0440\\u0438\\u044f\\u0445", "\\u0418\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u044c \\u0441\\u0435\\u043a\\u0440\\u0435\\u0442\\u044b (Secrets) \\u0432 CI/CD, HashiCorp Vault, \\u0438\\u043b\\u0438 \\u0437\\u0430\\u0448\\u0438\\u0444\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u044b\\u0435 \\u043f\\u0435\\u0440\\u0435\\u043c\\u0435\\u043d\\u043d\\u044b\\u0435 \\u043e\\u043a\\u0440\\u0443\\u0436\\u0435\\u043d\\u0438\\u044f", "\\u0412 \\u0438\\u043c\\u0435\\u043d\\u0438 \\u0444\\u0430\\u0439\\u043b\\u0430"]	2	null	Никогда не коммитьте секреты в Git. Для этого есть специальные инструменты.
48	Что такое DevOps? (копия)	mcq	4	intern	["\\u041a\\u043e\\u043d\\u043a\\u0440\\u0435\\u0442\\u043d\\u044b\\u0439 \\u0438\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442 \\u0434\\u043b\\u044f \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438 \\u0442\\u0435\\u0441\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f", "\\u041e\\u0442\\u0434\\u0435\\u043b\\u044c\\u043d\\u0430\\u044f \\u0434\\u043e\\u043b\\u0436\\u043d\\u043e\\u0441\\u0442\\u044c, \\u043a\\u043e\\u0442\\u043e\\u0440\\u0430\\u044f \\u0437\\u0430\\u043d\\u0438\\u043c\\u0430\\u0435\\u0442\\u0441\\u044f \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u043d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u043e\\u0439 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432", "\\u041a\\u0443\\u043b\\u044c\\u0442\\u0443\\u0440\\u0430, \\u043d\\u0430\\u0431\\u043e\\u0440 \\u043f\\u0440\\u0430\\u043a\\u0442\\u0438\\u043a \\u0438 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u043e\\u0432 \\u0434\\u043b\\u044f \\u043e\\u0431\\u044a\\u0435\\u0434\\u0438\\u043d\\u0435\\u043d\\u0438\\u044f \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438 (Dev) \\u0438 \\u044d\\u043a\\u0441\\u043f\\u043b\\u0443\\u0430\\u0442\\u0430\\u0446\\u0438\\u0438 (Ops)", "\\u041c\\u0435\\u0442\\u043e\\u0434\\u043e\\u043b\\u043e\\u0433\\u0438\\u044f \\u0443\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u044f \\u043f\\u0440\\u043e\\u0435\\u043a\\u0442\\u0430\\u043c\\u0438, \\u043f\\u043e\\u0445\\u043e\\u0436\\u0430\\u044f \\u043d\\u0430 Waterfall"]	2	null	\N
49	Что такое контейнеризация?	mcq	4	intern	["\\u0423\\u043f\\u0430\\u043a\\u043e\\u0432\\u043a\\u0430 \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u044f \\u0441\\u043e \\u0437\\u0430\\u0432\\u0438\\u0441\\u0438\\u043c\\u043e\\u0441\\u0442\\u044f\\u043c\\u0438 \\u0432 \\u0438\\u0437\\u043e\\u043b\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u043d\\u0443\\u044e \\u0441\\u0440\\u0435\\u0434\\u0443", "\\u0421\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u0435 \\u0432\\u0438\\u0440\\u0442\\u0443\\u0430\\u043b\\u044c\\u043d\\u044b\\u0445 \\u043c\\u0430\\u0448\\u0438\\u043d \\u0441 \\u043f\\u043e\\u043b\\u043d\\u043e\\u0439 \\u041e\\u0421", "\\u0420\\u0435\\u0437\\u0435\\u0440\\u0432\\u043d\\u043e\\u0435 \\u043a\\u043e\\u043f\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "\\u041c\\u043e\\u043d\\u0438\\u0442\\u043e\\u0440\\u0438\\u043d\\u0433 \\u043f\\u0440\\u043e\\u0438\\u0437\\u0432\\u043e\\u0434\\u0438\\u0442\\u0435\\u043b\\u044c\\u043d\\u043e\\u0441\\u0442\\u0438 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432"]	0	null	Контейнеризация — технология виртуализации на уровне ОС. Преимущества: изоляция приложений, быстрый запуск, переносимость, эффективное использование ресурсов. Инструменты: Docker, Podman, containerd.
50	Какая команда Docker используется для запуска контейнера?	mcq	4	intern	["docker run", "docker start", "docker create", "docker exec"]	0	null	docker run — основная команда для запуска контейнеров. Примеры: docker run nginx, docker run -d nginx (фоновый режим), docker run -p 8080:80 nginx (маппинг порта).
51	Что такое Docker Image?	mcq	4	intern	["\\u0428\\u0430\\u0431\\u043b\\u043e\\u043d \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0434\\u043b\\u044f \\u0447\\u0442\\u0435\\u043d\\u0438\\u044f \\u0434\\u043b\\u044f \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u044f \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u043e\\u0432", "\\u0417\\u0430\\u043f\\u0443\\u0449\\u0435\\u043d\\u043d\\u044b\\u0439 \\u044d\\u043a\\u0437\\u0435\\u043c\\u043f\\u043b\\u044f\\u0440 \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u044f", "\\u0424\\u0430\\u0439\\u043b \\u0441 \\u043b\\u043e\\u0433\\u0430\\u043c\\u0438 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u0430", "\\u0421\\u043a\\u0440\\u0438\\u043f\\u0442 \\u0434\\u043b\\u044f \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438 \\u0440\\u0430\\u0437\\u0432\\u0451\\u0440\\u0442\\u044b\\u0432\\u0430\\u043d\\u0438\\u044f"]	0	null	Docker Image — шаблон только для чтения для создания контейнеров. Содержит приложение и зависимости, имеет слоистую структуру, неизменяемый, хранится в реестре (Docker Hub).
52	Что делает команда `docker ps`?	mcq	4	intern	["\\u041f\\u043e\\u043a\\u0430\\u0437\\u044b\\u0432\\u0430\\u0435\\u0442 \\u0441\\u043f\\u0438\\u0441\\u043e\\u043a \\u0437\\u0430\\u043f\\u0443\\u0449\\u0435\\u043d\\u043d\\u044b\\u0445 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u043e\\u0432", "\\u041e\\u0441\\u0442\\u0430\\u043d\\u0430\\u0432\\u043b\\u0438\\u0432\\u0430\\u0435\\u0442 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u044b", "\\u0421\\u043e\\u0437\\u0434\\u0430\\u0451\\u0442 \\u043d\\u043e\\u0432\\u044b\\u0439 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440", "\\u0423\\u0434\\u0430\\u043b\\u044f\\u0435\\u0442 \\u0441\\u0442\\u0430\\u0440\\u044b\\u0435 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u044b"]	0	null	docker ps — показывает список запущенных контейнеров. Опции: docker ps -a (все), docker ps -l (последний).
53	Что такое Dockerfile?	mcq	4	intern	["\\u0422\\u0435\\u043a\\u0441\\u0442\\u043e\\u0432\\u044b\\u0439 \\u0444\\u0430\\u0439\\u043b \\u0441 \\u0438\\u043d\\u0441\\u0442\\u0440\\u0443\\u043a\\u0446\\u0438\\u044f\\u043c\\u0438 \\u0434\\u043b\\u044f \\u0441\\u0431\\u043e\\u0440\\u043a\\u0438 Docker \\u043e\\u0431\\u0440\\u0430\\u0437\\u0430", "\\u0421\\u043a\\u0440\\u0438\\u043f\\u0442 \\u0434\\u043b\\u044f \\u0437\\u0430\\u043f\\u0443\\u0441\\u043a\\u0430 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u0430", "\\u0424\\u0430\\u0439\\u043b \\u043a\\u043e\\u043d\\u0444\\u0438\\u0433\\u0443\\u0440\\u0430\\u0446\\u0438\\u0438 Docker daemon", "\\u041b\\u043e\\u0433 \\u0441\\u0431\\u043e\\u0440\\u043a\\u0438 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u0430"]	0	null	Dockerfile — текстовый файл с инструкциями для сборки Docker образа. Основные инструкции: FROM, WORKDIR, COPY, RUN, CMD, EXPOSE.
54	Какая команда используется для остановки контейнера?	mcq	4	intern	["docker stop", "docker pause", "docker kill", "docker down"]	0	null	docker stop — корректная остановка контейнера. Также: docker start (запуск), docker restart (перезапуск), docker kill (принудительно).
55	Что такое Docker Hub?	mcq	4	intern	["\\u041e\\u0431\\u043b\\u0430\\u0447\\u043d\\u044b\\u0439 \\u0440\\u0435\\u0435\\u0441\\u0442\\u0440 \\u0434\\u043b\\u044f \\u0445\\u0440\\u0430\\u043d\\u0435\\u043d\\u0438\\u044f Docker \\u043e\\u0431\\u0440\\u0430\\u0437\\u043e\\u0432", "\\u0418\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442 \\u0434\\u043b\\u044f \\u043c\\u043e\\u043d\\u0438\\u0442\\u043e\\u0440\\u0438\\u043d\\u0433\\u0430 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u043e\\u0432", "\\u0421\\u0440\\u0435\\u0434\\u0430 \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438 \\u0434\\u043b\\u044f Docker", "\\u041f\\u0430\\u043d\\u0435\\u043b\\u044c \\u0443\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u044f Docker daemon"]	0	null	Docker Hub — облачный реестр для хранения и распространения Docker образов. Поддерживает публичные и приватные репозитории, автоматическую сборку из GitHub.
56	Что означает директива FROM в Dockerfile?	mcq	4	intern	["\\u0423\\u043a\\u0430\\u0437\\u044b\\u0432\\u0430\\u0435\\u0442 \\u0431\\u0430\\u0437\\u043e\\u0432\\u044b\\u0439 \\u043e\\u0431\\u0440\\u0430\\u0437 \\u0434\\u043b\\u044f \\u0441\\u0431\\u043e\\u0440\\u043a\\u0438", "\\u041e\\u043f\\u0440\\u0435\\u0434\\u0435\\u043b\\u044f\\u0435\\u0442 \\u043a\\u043e\\u043c\\u0430\\u043d\\u0434\\u0443 \\u0437\\u0430\\u043f\\u0443\\u0441\\u043a\\u0430", "\\u041a\\u043e\\u043f\\u0438\\u0440\\u0443\\u0435\\u0442 \\u0444\\u0430\\u0439\\u043b\\u044b \\u0432 \\u043e\\u0431\\u0440\\u0430\\u0437", "\\u0423\\u0441\\u0442\\u0430\\u043d\\u0430\\u0432\\u043b\\u0438\\u0432\\u0430\\u0435\\u0442 \\u043f\\u0435\\u0440\\u0435\\u043c\\u0435\\u043d\\u043d\\u044b\\u0435 \\u043e\\u043a\\u0440\\u0443\\u0436\\u0435\\u043d\\u0438\\u044f"]	0	null	FROM — указывает базовый образ для сборки. Должна быть первой инструкцией, может использоваться несколько раз (multi-stage).
57	Какая команда показывает логи контейнера?	mcq	4	intern	["docker logs", "docker inspect", "docker events", "docker stats"]	0	null	docker logs — вывод логов контейнера. Опции: -f (follow), --tail (последние N строк), --since (за время).
58	Какой порт используется по умолчанию для SSH?	mcq	4	intern	["22", "80", "8080", "443"]	0	null	Порт 22 — стандартный порт для SSH. Популярные порты: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3306 (MySQL), 5432 (PostgreSQL), 6379 (Redis).
59	Что делает команда `git clone`?	mcq	4	intern	["\\u041a\\u043e\\u043f\\u0438\\u0440\\u0443\\u0435\\u0442 \\u0443\\u0434\\u0430\\u043b\\u0451\\u043d\\u043d\\u044b\\u0439 \\u0440\\u0435\\u043f\\u043e\\u0437\\u0438\\u0442\\u043e\\u0440\\u0438\\u0439 \\u043d\\u0430 \\u043b\\u043e\\u043a\\u0430\\u043b\\u044c\\u043d\\u0443\\u044e \\u043c\\u0430\\u0448\\u0438\\u043d\\u0443", "\\u0421\\u043e\\u0437\\u0434\\u0430\\u0451\\u0442 \\u043d\\u043e\\u0432\\u0443\\u044e \\u0432\\u0435\\u0442\\u043a\\u0443", "\\u041e\\u0442\\u043f\\u0440\\u0430\\u0432\\u043b\\u044f\\u0435\\u0442 \\u0438\\u0437\\u043c\\u0435\\u043d\\u0435\\u043d\\u0438\\u044f \\u043d\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440", "\\u041f\\u043e\\u043a\\u0430\\u0437\\u044b\\u0432\\u0430\\u0435\\u0442 \\u0438\\u0441\\u0442\\u043e\\u0440\\u0438\\u044e \\u043a\\u043e\\u043c\\u043c\\u0438\\u0442\\u043e\\u0432"]	0	null	git clone — копирует удалённый репозиторий на локальную машину. Примеры: git clone <url>, git clone --depth 1 (shallow), git clone --branch name.
60	Какая команда показывает текущую директорию в Linux?	mcq	4	intern	["pwd", "cd", "ls", "dir"]	0	null	pwd (print working directory) — показывает полный путь к текущей директории. Смежные команды: cd (перейти), ls (список файлов).
61	Что такое переменная окружения?	mcq	4	intern	["\\u0418\\u043c\\u0435\\u043d\\u043e\\u0432\\u0430\\u043d\\u043d\\u043e\\u0435 \\u0437\\u043d\\u0430\\u0447\\u0435\\u043d\\u0438\\u0435, \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u043d\\u043e\\u0435 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u0430\\u043c \\u0432 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c\\u0435", "\\u0413\\u043b\\u043e\\u0431\\u0430\\u043b\\u044c\\u043d\\u0430\\u044f \\u043f\\u0435\\u0440\\u0435\\u043c\\u0435\\u043d\\u043d\\u0430\\u044f \\u0432 \\u043a\\u043e\\u0434\\u0435 \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c\\u044b", "\\u041d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0430 \\u043a\\u043e\\u043d\\u0444\\u0438\\u0433\\u0443\\u0440\\u0430\\u0446\\u0438\\u0438 Git", "\\u041f\\u0430\\u0440\\u0430\\u043c\\u0435\\u0442\\u0440 \\u043a\\u043e\\u043c\\u0430\\u043d\\u0434\\u043d\\u043e\\u0439 \\u0441\\u0442\\u0440\\u043e\\u043a\\u0438"]	0	null	Переменная окружения — именованное значение, доступное процессам в системе. Примеры: PATH, HOME, USER, DATABASE_URL, API_KEY.
62	Какая команда используется для создания новой ветки в Git?	mcq	4	intern	["git branch", "git commit", "git merge", "git push"]	0	null	git branch — создание и управление ветками. Также: git checkout -b name (создать и переключиться), git switch -c name (новая команда).
63	Чем DevOps отличается от Agile?	mcq	4	junior	["\\u042d\\u0442\\u043e \\u043e\\u0434\\u043d\\u043e \\u0438 \\u0442\\u043e \\u0436\\u0435", "Agile \\u043a\\u0430\\u0441\\u0430\\u0435\\u0442\\u0441\\u044f \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0434\\u0438\\u0437\\u0430\\u0439\\u043d\\u0430, DevOps \\u2014 \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f", "Agile \\u0444\\u043e\\u043a\\u0443\\u0441\\u0438\\u0440\\u0443\\u0435\\u0442\\u0441\\u044f \\u043d\\u0430 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u0435 \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438 \\u0438 \\u0432\\u0437\\u0430\\u0438\\u043c\\u043e\\u0434\\u0435\\u0439\\u0441\\u0442\\u0432\\u0438\\u0438 \\u0441 \\u0437\\u0430\\u043a\\u0430\\u0437\\u0447\\u0438\\u043a\\u043e\\u043c, DevOps \\u2014 \\u043d\\u0430 \\u0434\\u043e\\u0441\\u0442\\u0430\\u0432\\u043a\\u0435 \\u0438 \\u044d\\u043a\\u0441\\u043f\\u043b\\u0443\\u0430\\u0442\\u0430\\u0446\\u0438\\u0438", "DevOps \\u2014 \\u044d\\u0442\\u043e \\u043d\\u0435\\u043d\\u043e\\u0440\\u043c\\u0430\\u0442\\u0438\\u0432\\u043d\\u0430\\u044f \\u043b\\u0435\\u043a\\u0441\\u0438\\u043a\\u0430"]	2	null	Agile отвечает на вопрос "как быстро мы можем разработать и изменить продукт?", а DevOps — "как быстро и надежно мы доставим эти изменения пользователю и будем их поддерживать?".
64	Какие инструменты относятся к категории IaC?	mcq	4	junior	["Jira \\u0438 Confluence", "Terraform \\u0438 Ansible", "Git \\u0438 GitHub", "Docker \\u0438 Kubernetes"]	1	null	Terraform (для создания ресурсов) и Ansible (для настройки ПО) — классические примеры. Пулл-реквесты здесь проходят не на код фичи, а на изменение инфраструктуры.
65	Что из перечисленного НЕ является целью DevOps?	mcq	4	junior	["\\u0423\\u0432\\u0435\\u043b\\u0438\\u0447\\u0435\\u043d\\u0438\\u0435 \\u0447\\u0430\\u0441\\u0442\\u043e\\u0442\\u044b \\u0440\\u0435\\u043b\\u0438\\u0437\\u043e\\u0432", "\\u0421\\u043e\\u043a\\u0440\\u0430\\u0449\\u0435\\u043d\\u0438\\u0435 \\u0432\\u0440\\u0435\\u043c\\u0435\\u043d\\u0438 \\u043e\\u0442 \\u043a\\u043e\\u043c\\u043c\\u0438\\u0442\\u0430 \\u0434\\u043e \\u0434\\u0435\\u043f\\u043b\\u043e\\u044f", "\\u0423\\u043c\\u0435\\u043d\\u044c\\u0448\\u0435\\u043d\\u0438\\u0435 \\u043a\\u043e\\u043b\\u0438\\u0447\\u0435\\u0441\\u0442\\u0432\\u0430 \\u043e\\u0448\\u0438\\u0431\\u043e\\u043a \\u043d\\u0430 \\u043f\\u0440\\u043e\\u0434\\u0435", "\\u0423\\u0432\\u0435\\u043b\\u0438\\u0447\\u0435\\u043d\\u0438\\u0435 \\u0432\\u0440\\u0435\\u043c\\u0435\\u043d\\u0438 \\u043f\\u043e\\u0441\\u0442\\u0430\\u0432\\u043a\\u0438 \\u0438\\u0437\\u043c\\u0435\\u043d\\u0435\\u043d\\u0438\\u0439 (Lead Time)"]	3	null	DevOps стремится сократить Lead Time (время от появления идеи до ее реализации в продукте), а не увеличить его.
66	Что такое "Shift Left" в контексте DevOps и безопасности (DevSecOps)?	mcq	4	junior	["\\u041f\\u0435\\u0440\\u0435\\u043d\\u043e\\u0441 \\u043a\\u043e\\u0434\\u0430 \\u0441 \\u043e\\u0434\\u043d\\u043e\\u0433\\u043e \\u044f\\u0437\\u044b\\u043a\\u0430 \\u043d\\u0430 \\u0434\\u0440\\u0443\\u0433\\u043e\\u0439", "\\u041f\\u0435\\u0440\\u0435\\u043d\\u043e\\u0441 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u043e\\u0432 \\u0442\\u0435\\u0441\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u0438 \\u0431\\u0435\\u0437\\u043e\\u043f\\u0430\\u0441\\u043d\\u043e\\u0441\\u0442\\u0438 \\u043d\\u0430 \\u0440\\u0430\\u043d\\u043d\\u0438\\u0435 \\u044d\\u0442\\u0430\\u043f\\u044b \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438", "\\u041c\\u0438\\u0433\\u0440\\u0430\\u0446\\u0438\\u044f \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432 \\u0432 \\u043b\\u0435\\u0432\\u044b\\u0439 \\u0434\\u0430\\u0442\\u0430-\\u0446\\u0435\\u043d\\u0442\\u0440", "\\u0423\\u0434\\u0430\\u043b\\u0435\\u043d\\u0438\\u0435 \\u043d\\u0435\\u0438\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u0443\\u0435\\u043c\\u043e\\u0433\\u043e \\u043a\\u043e\\u0434\\u0430"]	1	null	"Сдвиг влево" означает, что мы проверяем безопасность и качество не в конце, когда все готово, а сразу, как только написан код. Это дешевле и быстрее.
67	Как найти все файлы с расширением `.conf` в директории `/etc`?	mcq	4	junior	["grep \\".conf\\" /etc", "ls /etc/*.conf", "find /etc -name \\"*.conf\\"", "whereis .conf"]	2	null	`find` — мощная команда для поиска файлов по различным критериям. `ls /etc/*.conf` тоже сработает, но только на один уровень вложенности. `find` ищет рекурсивно.
68	Что означает команда `chmod 755 script.sh`?	mcq	4	junior	["\\u0417\\u0430\\u043f\\u0440\\u0435\\u0442\\u0438\\u0442\\u044c \\u0432\\u044b\\u043f\\u043e\\u043b\\u043d\\u0435\\u043d\\u0438\\u0435 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442\\u0430 \\u0432\\u0441\\u0435\\u043c", "\\u0412\\u043b\\u0430\\u0434\\u0435\\u043b\\u044c\\u0446\\u0443 \\u043c\\u043e\\u0436\\u043d\\u043e \\u0432\\u0441\\u0451, \\u0433\\u0440\\u0443\\u043f\\u043f\\u0435 \\u0438 \\u043e\\u0441\\u0442\\u0430\\u043b\\u044c\\u043d\\u044b\\u043c \\u2014 \\u0447\\u0438\\u0442\\u0430\\u0442\\u044c \\u0438 \\u0432\\u044b\\u043f\\u043e\\u043b\\u043d\\u044f\\u0442\\u044c", "\\u0421\\u0434\\u0435\\u043b\\u0430\\u0442\\u044c \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442 \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u043d\\u044b\\u043c \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0434\\u043b\\u044f \\u0447\\u0442\\u0435\\u043d\\u0438\\u044f \\u0432\\u0441\\u0435\\u043c", "\\u0423\\u0434\\u0430\\u043b\\u0438\\u0442\\u044c \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442"]	1	null	7 (rwx) для владельца, 5 (r-x) для группы и остальных. Это стандартные права для исполняемых файлов.
69	Что такое Load Average (средняя нагрузка) в Linux?	mcq	4	junior	["\\u041f\\u0440\\u043e\\u0446\\u0435\\u043d\\u0442 \\u0437\\u0430\\u043d\\u044f\\u0442\\u043e\\u0439 \\u043e\\u043f\\u0435\\u0440\\u0430\\u0442\\u0438\\u0432\\u043d\\u043e\\u0439 \\u043f\\u0430\\u043c\\u044f\\u0442\\u0438", "\\u041e\\u0431\\u0449\\u0435\\u0435 \\u043a\\u043e\\u043b\\u0438\\u0447\\u0435\\u0441\\u0442\\u0432\\u043e \\u0437\\u0430\\u043f\\u0443\\u0449\\u0435\\u043d\\u043d\\u044b\\u0445 \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u043e\\u0432", "\\u0421\\u0440\\u0435\\u0434\\u043d\\u0435\\u0435 \\u043a\\u043e\\u043b\\u0438\\u0447\\u0435\\u0441\\u0442\\u0432\\u043e \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441\\u043e\\u0432, \\u043d\\u0430\\u0445\\u043e\\u0434\\u044f\\u0449\\u0438\\u0445\\u0441\\u044f \\u0432 \\u043e\\u0447\\u0435\\u0440\\u0435\\u0434\\u0438 \\u043d\\u0430 \\u0432\\u044b\\u043f\\u043e\\u043b\\u043d\\u0435\\u043d\\u0438\\u0435 \\u0438\\u043b\\u0438 \\u043e\\u0436\\u0438\\u0434\\u0430\\u044e\\u0449\\u0438\\u0445 \\u0432\\u0432\\u043e\\u0434\\u0430-\\u0432\\u044b\\u0432\\u043e\\u0434\\u0430, \\u0437\\u0430 1, 5 \\u0438 15 \\u043c\\u0438\\u043d\\u0443\\u0442", "\\u0421\\u043a\\u043e\\u0440\\u043e\\u0441\\u0442\\u044c \\u0438\\u043d\\u0442\\u0435\\u0440\\u043d\\u0435\\u0442-\\u0441\\u043e\\u0435\\u0434\\u0438\\u043d\\u0435\\u043d\\u0438\\u044f"]	2	null	Важно понимать: высокий Load Average не всегда означает 100% CPU. Процессы могут ждать диска (I/O).
70	Какой сигнал по умолчанию посылает команда `kill PID`?	mcq	4	junior	["SIGKILL (9)", "SIGTERM (15)", "SIGHUP (1)", "SIGSTOP (19)"]	1	null	SIGTERM — это "вежливый" запрос на завершение. Процесс может его перехватить и корректно закрыть файлы. SIGKILL убивает процесс принудительно.
71	Для чего нужна команда `ssh-keygen`?	mcq	4	junior	["\\u0414\\u043b\\u044f \\u0448\\u0438\\u0444\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u0434\\u0438\\u0441\\u043a\\u0430", "\\u0414\\u043b\\u044f \\u0433\\u0435\\u043d\\u0435\\u0440\\u0430\\u0446\\u0438\\u0438 \\u043f\\u0430\\u0440\\u044b \\u043f\\u0443\\u0431\\u043b\\u0438\\u0447\\u043d\\u043e\\u0433\\u043e \\u0438 \\u043f\\u0440\\u0438\\u0432\\u0430\\u0442\\u043d\\u043e\\u0433\\u043e SSH-\\u043a\\u043b\\u044e\\u0447\\u0435\\u0439", "\\u0414\\u043b\\u044f \\u043f\\u043e\\u0434\\u043a\\u043b\\u044e\\u0447\\u0435\\u043d\\u0438\\u044f \\u043a \\u0443\\u0434\\u0430\\u043b\\u0435\\u043d\\u043d\\u043e\\u043c\\u0443 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0443", "\\u0414\\u043b\\u044f \\u0441\\u043c\\u0435\\u043d\\u044b \\u043f\\u0430\\u0440\\u043e\\u043b\\u044f"]	1	null	SSH-ключи используются для безопасного подключения к серверам без ввода пароля.
72	Что такое символическая ссылка (symlink)?	mcq	4	junior	["\\u041a\\u043e\\u043f\\u0438\\u044f \\u0444\\u0430\\u0439\\u043b\\u0430", "\\u0421\\u043f\\u0435\\u0446\\u0438\\u0430\\u043b\\u044c\\u043d\\u044b\\u0439 \\u0444\\u0430\\u0439\\u043b, \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0439 \\u0443\\u043a\\u0430\\u0437\\u044b\\u0432\\u0430\\u0435\\u0442 \\u043d\\u0430 \\u0434\\u0440\\u0443\\u0433\\u043e\\u0439 \\u0444\\u0430\\u0439\\u043b \\u0438\\u043b\\u0438 \\u0434\\u0438\\u0440\\u0435\\u043a\\u0442\\u043e\\u0440\\u0438\\u044e", "\\u0421\\u0436\\u0430\\u0442\\u0430\\u044f \\u0432\\u0435\\u0440\\u0441\\u0438\\u044f \\u0444\\u0430\\u0439\\u043b\\u0430", "\\u0424\\u0430\\u0439\\u043b \\u0441 \\u0440\\u0430\\u0441\\u0448\\u0438\\u0440\\u0435\\u043d\\u0438\\u0435\\u043c .sym"]	1	null	Симлинки — это как "ярлыки" в Windows. Они позволяют иметь доступ к файлу из разных мест без дублирования.
73	Какой сигнал нельзя перехватить и обработать в приложении?	mcq	4	junior	["SIGTERM", "SIGINT", "SIGKILL", "SIGHUP"]	2	null	SIGKILL (9) убивает процесс принудительно на уровне ядра, процесс не может его игнорировать.
74	Что такое stdin, stdout, stderr?	mcq	4	junior	["\\u041d\\u0430\\u0437\\u0432\\u0430\\u043d\\u0438\\u044f \\u0434\\u0438\\u0441\\u0442\\u0440\\u0438\\u0431\\u0443\\u0442\\u0438\\u0432\\u043e\\u0432 Linux", "\\u0422\\u0438\\u043f\\u044b \\u0444\\u0430\\u0439\\u043b\\u043e\\u0432\\u044b\\u0445 \\u0441\\u0438\\u0441\\u0442\\u0435\\u043c", "\\u0421\\u0442\\u0430\\u043d\\u0434\\u0430\\u0440\\u0442\\u043d\\u044b\\u0435 \\u043f\\u043e\\u0442\\u043e\\u043a\\u0438 \\u0432\\u0432\\u043e\\u0434\\u0430, \\u0432\\u044b\\u0432\\u043e\\u0434\\u0430 \\u0438 \\u043e\\u0448\\u0438\\u0431\\u043e\\u043a", "\\u041a\\u043e\\u043c\\u0430\\u043d\\u0434\\u044b \\u0434\\u043b\\u044f \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 \\u0441\\u0435\\u0442\\u044c\\u044e"]	2	null	Все программы в Linux работают с этими потоками. Можно перенаправлять `stdout` одного процесса в `stdin` другого с помощью пайпа (`\\|`).
75	Что такое TCP и UDP? В чем разница?	mcq	4	junior	["TCP \\u2014 \\u043d\\u0430\\u0434\\u0435\\u0436\\u043d\\u044b\\u0439 \\u043f\\u0440\\u043e\\u0442\\u043e\\u043a\\u043e\\u043b \\u0441 \\u0443\\u0441\\u0442\\u0430\\u043d\\u043e\\u0432\\u043a\\u043e\\u0439 \\u0441\\u043e\\u0435\\u0434\\u0438\\u043d\\u0435\\u043d\\u0438\\u044f (\\u043a\\u0430\\u043a \\u0437\\u0432\\u043e\\u043d\\u043e\\u043a), UDP \\u2014 \\u0431\\u044b\\u0441\\u0442\\u0440\\u044b\\u0439, \\u043d\\u043e \\u0431\\u0435\\u0437 \\u0433\\u0430\\u0440\\u0430\\u043d\\u0442\\u0438\\u0438 \\u0434\\u043e\\u0441\\u0442\\u0430\\u0432\\u043a\\u0438 (\\u043a\\u0430\\u043a \\u043f\\u0438\\u0441\\u044c\\u043c\\u043e \\u0432 \\u0431\\u0443\\u0442\\u044b\\u043b\\u043a\\u0435)", "\\u042d\\u0442\\u043e \\u0442\\u0438\\u043f\\u044b IP-\\u0430\\u0434\\u0440\\u0435\\u0441\\u043e\\u0432", "\\u042d\\u0442\\u043e \\u043d\\u0430\\u0437\\u0432\\u0430\\u043d\\u0438\\u044f \\u0441\\u0435\\u0442\\u0435\\u0432\\u044b\\u0445 \\u043a\\u0430\\u0440\\u0442", "TCP \\u0434\\u043b\\u044f Windows, UDP \\u0434\\u043b\\u044f Linux"]	0	null	TCP гарантирует доставку и порядок пакетов (используется для веб, почты). UDP быстрее (используется для видео, DNS, игр).
76	Для чего нужен протокол ICMP?	mcq	4	junior	["\\u0414\\u043b\\u044f \\u043f\\u0435\\u0440\\u0435\\u0434\\u0430\\u0447\\u0438 \\u0432\\u0435\\u0431-\\u0441\\u0442\\u0440\\u0430\\u043d\\u0438\\u0446", "\\u0414\\u043b\\u044f \\u0448\\u0438\\u0444\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "\\u0414\\u043b\\u044f \\u0434\\u0438\\u0430\\u0433\\u043d\\u043e\\u0441\\u0442\\u0438\\u043a\\u0438 \\u0441\\u0435\\u0442\\u0438 \\u0438 \\u0441\\u043e\\u043e\\u0431\\u0449\\u0435\\u043d\\u0438\\u0439 \\u043e\\u0431 \\u043e\\u0448\\u0438\\u0431\\u043a\\u0430\\u0445 (\\u0438\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u0443\\u0435\\u0442\\u0441\\u044f \\u0443\\u0442\\u0438\\u043b\\u0438\\u0442\\u043e\\u0439 ping)", "\\u0414\\u043b\\u044f \\u043d\\u0430\\u0437\\u043d\\u0430\\u0447\\u0435\\u043d\\u0438\\u044f IP-\\u0430\\u0434\\u0440\\u0435\\u0441\\u043e\\u0432"]	2	null	ICMP (Internet Control Message Protocol) — служебный протокол. `ping` отправляет ICMP Echo Request.
77	Что такое NAT (Network Address Translation)?	mcq	4	junior	["\\u041f\\u0440\\u043e\\u0442\\u043e\\u043a\\u043e\\u043b \\u0448\\u0438\\u0444\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u0442\\u0440\\u0430\\u0444\\u0438\\u043a\\u0430", "\\u041c\\u0435\\u0445\\u0430\\u043d\\u0438\\u0437\\u043c, \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0439 \\u043f\\u043e\\u0434\\u043c\\u0435\\u043d\\u044f\\u0435\\u0442 IP-\\u0430\\u0434\\u0440\\u0435\\u0441\\u0430 \\u0432 \\u043f\\u0430\\u043a\\u0435\\u0442\\u0430\\u0445 (\\u043e\\u0431\\u044b\\u0447\\u043d\\u043e \\u043f\\u0440\\u0438\\u0432\\u0430\\u0442\\u043d\\u044b\\u0439 \\u043d\\u0430 \\u043f\\u0443\\u0431\\u043b\\u0438\\u0447\\u043d\\u044b\\u0439) \\u0434\\u043b\\u044f \\u0432\\u044b\\u0445\\u043e\\u0434\\u0430 \\u0432 \\u0438\\u043d\\u0442\\u0435\\u0440\\u043d\\u0435\\u0442", "\\u0410\\u043d\\u0442\\u0438\\u0432\\u0438\\u0440\\u0443\\u0441\\u043d\\u0430\\u044f \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c\\u0430", "\\u0422\\u0438\\u043f \\u043a\\u0430\\u0431\\u0435\\u043b\\u044f"]	1	null	Благодаря NAT ваш домашний роутер с одним белым IP-адресом может раздавать интернет десятку устройств.
78	Как проверить, открыт ли порт 80 на удаленном хосте example.com?	mcq	4	junior	["ping example.com", "telnet example.com 80 \\u0438\\u043b\\u0438 nc -zv example.com 80", "ssh example.com 80", "curl example.com:80"]	1	null	`telnet` или `netcat (nc)` — классические утилиты для проверки доступности портов. `curl` тоже покажет ответ, если там HTTP-сервер.
79	Что такое прокси-сервер?	mcq	4	junior	["\\u0421\\u0435\\u0440\\u0432\\u0435\\u0440 \\u0434\\u043b\\u044f \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u043a\\u0438 \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u0439", "\\u041f\\u043e\\u0441\\u0440\\u0435\\u0434\\u043d\\u0438\\u043a \\u043c\\u0435\\u0436\\u0434\\u0443 \\u043a\\u043b\\u0438\\u0435\\u043d\\u0442\\u043e\\u043c \\u0438 \\u0434\\u0440\\u0443\\u0433\\u0438\\u043c\\u0438 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0430\\u043c\\u0438, \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0439 \\u043c\\u043e\\u0436\\u0435\\u0442 \\u043a\\u044d\\u0448\\u0438\\u0440\\u043e\\u0432\\u0430\\u0442\\u044c \\u0434\\u0430\\u043d\\u043d\\u044b\\u0435, \\u0444\\u0438\\u043b\\u044c\\u0442\\u0440\\u043e\\u0432\\u0430\\u0442\\u044c \\u0442\\u0440\\u0430\\u0444\\u0438\\u043a \\u0438\\u043b\\u0438 \\u0441\\u043a\\u0440\\u044b\\u0432\\u0430\\u0442\\u044c \\u043a\\u043b\\u0438\\u0435\\u043d\\u0442\\u0430", "\\u0422\\u043e \\u0436\\u0435 \\u0441\\u0430\\u043c\\u043e\\u0435, \\u0447\\u0442\\u043e \\u0438 VPN", "\\u0421\\u0435\\u0440\\u0432\\u0435\\u0440 \\u0431\\u0430\\u0437 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445"]	1	null	Прокси бывают прямыми (для клиентов) и обратными (для серверов, как nginx).
80	Что такое конфликт слияния (merge conflict)?	mcq	4	junior	["\\u041e\\u0448\\u0438\\u0431\\u043a\\u0430 \\u0432 \\u043a\\u043e\\u0434\\u0435 \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c\\u044b", "\\u0421\\u0438\\u0442\\u0443\\u0430\\u0446\\u0438\\u044f, \\u043a\\u043e\\u0433\\u0434\\u0430 Git \\u043d\\u0435 \\u043c\\u043e\\u0436\\u0435\\u0442 \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438 \\u043e\\u0431\\u044a\\u0435\\u0434\\u0438\\u043d\\u0438\\u0442\\u044c \\u0438\\u0437\\u043c\\u0435\\u043d\\u0435\\u043d\\u0438\\u044f \\u0438\\u0437 \\u0434\\u0432\\u0443\\u0445 \\u0432\\u0435\\u0442\\u043e\\u043a, \\u043f\\u043e\\u0442\\u043e\\u043c\\u0443 \\u0447\\u0442\\u043e \\u043e\\u043d\\u0438 \\u0437\\u0430\\u0442\\u0440\\u0430\\u0433\\u0438\\u0432\\u0430\\u044e\\u0442 \\u043e\\u0434\\u043d\\u0438 \\u0438 \\u0442\\u0435 \\u0436\\u0435 \\u0441\\u0442\\u0440\\u043e\\u043a\\u0438 \\u0444\\u0430\\u0439\\u043b\\u0430", "\\u041e\\u0442\\u0441\\u0443\\u0442\\u0441\\u0442\\u0432\\u0438\\u0435 \\u0438\\u043d\\u0442\\u0435\\u0440\\u043d\\u0435\\u0442\\u0430 \\u043f\\u0440\\u0438 push'\\u0435", "\\u0423\\u0434\\u0430\\u043b\\u0435\\u043d\\u0438\\u0435 \\u0432\\u0435\\u0442\\u043a\\u0438"]	1	null	Конфликт решается вручную разработчиком, нужно выбрать, какие изменения оставить.
81	Что такое `origin` в Git?	mcq	4	junior	["\\u041d\\u0430\\u0437\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0433\\u043b\\u0430\\u0432\\u043d\\u043e\\u0439 \\u0432\\u0435\\u0442\\u043a\\u0438", "\\u041f\\u0441\\u0435\\u0432\\u0434\\u043e\\u043d\\u0438\\u043c (\\u0430\\u043b\\u0438\\u0430\\u0441) \\u043f\\u043e \\u0443\\u043c\\u043e\\u043b\\u0447\\u0430\\u043d\\u0438\\u044e \\u0434\\u043b\\u044f \\u0443\\u0434\\u0430\\u043b\\u0435\\u043d\\u043d\\u043e\\u0433\\u043e \\u0440\\u0435\\u043f\\u043e\\u0437\\u0438\\u0442\\u043e\\u0440\\u0438\\u044f, \\u0441 \\u043a\\u043e\\u0442\\u043e\\u0440\\u043e\\u0433\\u043e \\u0431\\u044b\\u043b \\u0441\\u0434\\u0435\\u043b\\u0430\\u043d \\u043a\\u043b\\u043e\\u043d", "\\u041a\\u043e\\u043c\\u0430\\u043d\\u0434\\u0430 \\u0434\\u043b\\u044f \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u044f \\u0440\\u0435\\u043f\\u043e\\u0437\\u0438\\u0442\\u043e\\u0440\\u0438\\u044f", "\\u0418\\u043c\\u044f \\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044f"]	1	null	Когда вы клонируете репозиторий, Git автоматически дает имя `origin` тому серверу, откуда вы клонировали.
82	Что делает команда `docker build -t my-app:1.0 .`?	mcq	4	junior	["\\u0417\\u0430\\u043f\\u0443\\u0441\\u043a\\u0430\\u0435\\u0442 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440 my-app", "\\u0421\\u043e\\u0431\\u0438\\u0440\\u0430\\u0435\\u0442 Docker-\\u043e\\u0431\\u0440\\u0430\\u0437 \\u0438\\u0437 Dockerfile \\u0432 \\u0442\\u0435\\u043a\\u0443\\u0449\\u0435\\u0439 \\u0434\\u0438\\u0440\\u0435\\u043a\\u0442\\u043e\\u0440\\u0438\\u0438 \\u0438 \\u043f\\u0440\\u0438\\u0441\\u0432\\u0430\\u0438\\u0432\\u0430\\u0435\\u0442 \\u0435\\u043c\\u0443 \\u0442\\u0435\\u0433 my-app:1.0", "\\u0423\\u0434\\u0430\\u043b\\u044f\\u0435\\u0442 \\u0432\\u0441\\u0435 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u044b", "\\u041f\\u0443\\u0448\\u0438\\u0442 \\u043e\\u0431\\u0440\\u0430\\u0437 \\u0432 Docker Hub"]	1	null	Флаг `-t` задает имя и тег образу. Точка в конце — это путь к контексту сборки (где искать Dockerfile).
83	Что такое Docker Compose?	mcq	4	junior	["\\u041f\\u043b\\u0430\\u0433\\u0438\\u043d \\u0434\\u043b\\u044f \\u043c\\u043e\\u043d\\u0438\\u0442\\u043e\\u0440\\u0438\\u043d\\u0433\\u0430", "\\u0418\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442 \\u0434\\u043b\\u044f \\u043e\\u043f\\u0440\\u0435\\u0434\\u0435\\u043b\\u0435\\u043d\\u0438\\u044f \\u0438 \\u0437\\u0430\\u043f\\u0443\\u0441\\u043a\\u0430 \\u043c\\u043d\\u043e\\u0433\\u043e\\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u043d\\u044b\\u0445 \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u0439 (\\u0447\\u0435\\u0440\\u0435\\u0437 YAML-\\u0444\\u0430\\u0439\\u043b)", "\\u0410\\u043b\\u044c\\u0442\\u0435\\u0440\\u043d\\u0430\\u0442\\u0438\\u0432\\u0430 Docker", "\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430 \\u043e\\u0440\\u043a\\u0435\\u0441\\u0442\\u0440\\u0430\\u0446\\u0438\\u0438, \\u043a\\u0430\\u043a Kubernetes"]	1	null	Compose позволяет одной командой `docker-compose up` поднять, например, приложение, базу данных и redis.
84	Для чего нужна директива `EXPOSE` в Dockerfile?	mcq	4	junior	["\\u041f\\u0440\\u043e\\u043f\\u0438\\u0441\\u0430\\u0442\\u044c \\u043f\\u0430\\u0440\\u043e\\u043b\\u044c", "\\u0417\\u0430\\u043f\\u0443\\u0441\\u0442\\u0438\\u0442\\u044c \\u043f\\u0440\\u043e\\u0446\\u0435\\u0441\\u0441 \\u0432\\u043d\\u0443\\u0442\\u0440\\u0438 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u0430", "\\u0423\\u043a\\u0430\\u0437\\u0430\\u0442\\u044c, \\u0447\\u0442\\u043e \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440 \\u0441\\u043b\\u0443\\u0448\\u0430\\u0435\\u0442 \\u043e\\u043f\\u0440\\u0435\\u0434\\u0435\\u043b\\u0435\\u043d\\u043d\\u044b\\u0439 \\u043f\\u043e\\u0440\\u0442 (\\u044d\\u0442\\u043e \\u0434\\u043e\\u043a\\u0443\\u043c\\u0435\\u043d\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u0435, \\u0430 \\u043d\\u0435 \\u043f\\u0443\\u0431\\u043b\\u0438\\u043a\\u0430\\u0446\\u0438\\u044f \\u043f\\u043e\\u0440\\u0442\\u0430 \\u043d\\u0430\\u0440\\u0443\\u0436\\u0443)", "\\u0421\\u043e\\u0437\\u0434\\u0430\\u0442\\u044c \\u0442\\u043e\\u043c \\u0434\\u043b\\u044f \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445"]	2	null	`EXPOSE 80` не делает порт доступным с хоста. Чтобы опубликовать порт наружу, нужно использовать флаг `-p` при запуске (`docker run -p 8080:80`).
85	Как сохранить данные, созданные в контейнере (например, в базе данных), чтобы они не пропали после удаления контейнера?	mcq	4	junior	["\\u041d\\u0438\\u043a\\u0430\\u043a, \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u044b \\u0432\\u0441\\u0435\\u0433\\u0434\\u0430 \\u0443\\u0434\\u0430\\u043b\\u044f\\u044e\\u0442\\u0441\\u044f \\u0441 \\u0434\\u0430\\u043d\\u043d\\u044b\\u043c\\u0438", "\\u0418\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u044c `docker commit`", "\\u0418\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u044c Docker volumes (\\u0442\\u043e\\u043c\\u0430)", "\\u0417\\u0430\\u043f\\u0438\\u0441\\u0430\\u0442\\u044c \\u0434\\u0430\\u043d\\u043d\\u044b\\u0435 \\u0432 \\u043e\\u0431\\u0440\\u0430\\u0437"]	2	null	Volume — это специальная директория на хосте, которую можно смонтировать внутрь контейнера. Данные в volume живут отдельно от контейнера.
86	Что такое Pod в Kubernetes?	mcq	4	junior	["\\u0413\\u0440\\u0443\\u043f\\u043f\\u0430 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u043e\\u0432", "\\u0412\\u0438\\u0440\\u0442\\u0443\\u0430\\u043b\\u044c\\u043d\\u0430\\u044f \\u043c\\u0430\\u0448\\u0438\\u043d\\u0430", "\\u041d\\u0430\\u0438\\u043c\\u0435\\u043d\\u044c\\u0448\\u0430\\u044f \\u0438 \\u043f\\u0440\\u043e\\u0441\\u0442\\u0435\\u0439\\u0448\\u0430\\u044f \\u0435\\u0434\\u0438\\u043d\\u0438\\u0446\\u0430 \\u0432 Kubernetes, \\u043a\\u043e\\u0442\\u043e\\u0440\\u0430\\u044f \\u043f\\u0440\\u0435\\u0434\\u0441\\u0442\\u0430\\u0432\\u043b\\u044f\\u0435\\u0442 \\u0441\\u043e\\u0431\\u043e\\u0439 \\u0433\\u0440\\u0443\\u043f\\u043f\\u0443 \\u0438\\u0437 \\u043e\\u0434\\u043d\\u043e\\u0433\\u043e \\u0438\\u043b\\u0438 \\u043d\\u0435\\u0441\\u043a\\u043e\\u043b\\u044c\\u043a\\u0438\\u0445 \\u043a\\u043e\\u043d\\u0442\\u0435\\u0439\\u043d\\u0435\\u0440\\u043e\\u0432, \\u0440\\u0430\\u0437\\u0434\\u0435\\u043b\\u044f\\u044e\\u0449\\u0438\\u0445 \\u0441\\u0435\\u0442\\u044c \\u0438 \\u0445\\u0440\\u0430\\u043d\\u0438\\u043b\\u0438\\u0449\\u0435", "\\u0411\\u0430\\u0437\\u0430 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445"]	2	null	Чаще всего под содержит один контейнер, но может содержать и несколько тесно связанных контейнеров (например, основной + вспомогательный для отправки логов).
87	Для чего нужен Kubernetes Deployment?	mcq	4	junior	["\\u0414\\u043b\\u044f \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u044f \\u0441\\u0435\\u043a\\u0440\\u0435\\u0442\\u043e\\u0432", "\\u0414\\u043b\\u044f \\u043f\\u043e\\u0434\\u043a\\u043b\\u044e\\u0447\\u0435\\u043d\\u0438\\u044f \\u043a \\u0431\\u0430\\u0437\\u0435 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "\\u0414\\u043b\\u044f \\u0434\\u0435\\u043a\\u043b\\u0430\\u0440\\u0430\\u0442\\u0438\\u0432\\u043d\\u043e\\u0433\\u043e \\u043e\\u0431\\u043d\\u043e\\u0432\\u043b\\u0435\\u043d\\u0438\\u044f \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u0439 (\\u043e\\u0431\\u0435\\u0441\\u043f\\u0435\\u0447\\u0438\\u0432\\u0430\\u0435\\u0442 \\u0436\\u0435\\u043b\\u0430\\u0435\\u043c\\u043e\\u0435 \\u043a\\u043e\\u043b\\u0438\\u0447\\u0435\\u0441\\u0442\\u0432\\u043e \\u0440\\u0435\\u043f\\u043b\\u0438\\u043a Pod'\\u043e\\u0432, \\u0441\\u0442\\u0440\\u0430\\u0442\\u0435\\u0433\\u0438\\u0438 \\u043e\\u0431\\u043d\\u043e\\u0432\\u043b\\u0435\\u043d\\u0438\\u044f, \\u043e\\u0442\\u043a\\u0430\\u0442\\u044b)", "\\u0414\\u043b\\u044f \\u043d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0438 \\u0441\\u0435\\u0442\\u0438"]	2	null	Вы говорите Deployment'у: "хочу 3 копии моего приложения", и Kubernetes следит, чтобы это количество всегда было.
88	Что такое Kubernetes Service?	mcq	4	junior	["\\u0421\\u0435\\u0440\\u0432\\u0435\\u0440 \\u0434\\u043b\\u044f \\u0441\\u0431\\u043e\\u0440\\u043a\\u0438 \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u0439", "\\u0410\\u0431\\u0441\\u0442\\u0440\\u0430\\u043a\\u0446\\u0438\\u044f, \\u043a\\u043e\\u0442\\u043e\\u0440\\u0430\\u044f \\u043e\\u043f\\u0440\\u0435\\u0434\\u0435\\u043b\\u044f\\u0435\\u0442 \\u043f\\u043e\\u043b\\u0438\\u0442\\u0438\\u043a\\u0443 \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u0430 \\u043a \\u0433\\u0440\\u0443\\u043f\\u043f\\u0435 Pod'\\u043e\\u0432 (\\u043f\\u043e\\u0441\\u0442\\u043e\\u044f\\u043d\\u043d\\u0430\\u044f \\u0442\\u043e\\u0447\\u043a\\u0430 \\u0432\\u0445\\u043e\\u0434\\u0430, \\u0434\\u0430\\u0436\\u0435 \\u0435\\u0441\\u043b\\u0438 Pod'\\u044b \\u043f\\u0435\\u0440\\u0435\\u0441\\u043e\\u0437\\u0434\\u0430\\u044e\\u0442\\u0441\\u044f)", "\\u041b\\u043e\\u0433\\u0438\\u043d \\u0438 \\u043f\\u0430\\u0440\\u043e\\u043b\\u044c \\u0434\\u043b\\u044f \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u0430 \\u043a \\u043a\\u043b\\u0430\\u0441\\u0442\\u0435\\u0440\\u0443", "\\u0418\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442 \\u043c\\u043e\\u043d\\u0438\\u0442\\u043e\\u0440\\u0438\\u043d\\u0433\\u0430"]	1	null	Так как Pod'ы могут умирать и появляться с новыми IP, Service дает им стабильный IP и DNS-имя.
89	Что такое ConfigMap в Kubernetes?	mcq	4	junior	["\\u041a\\u0430\\u0440\\u0442\\u0430 \\u0441\\u0435\\u0442\\u0438 \\u043a\\u043b\\u0430\\u0441\\u0442\\u0435\\u0440\\u0430", "\\u041e\\u0431\\u044a\\u0435\\u043a\\u0442 \\u0434\\u043b\\u044f \\u0445\\u0440\\u0430\\u043d\\u0435\\u043d\\u0438\\u044f \\u043a\\u043e\\u043d\\u0444\\u0438\\u0433\\u0443\\u0440\\u0430\\u0446\\u0438\\u043e\\u043d\\u043d\\u044b\\u0445 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445 \\u0432 \\u0432\\u0438\\u0434\\u0435 \\u043f\\u0430\\u0440 \\u043a\\u043b\\u044e\\u0447-\\u0437\\u043d\\u0430\\u0447\\u0435\\u043d\\u0438\\u0435, \\u043d\\u0435\\u0441\\u0435\\u043a\\u0440\\u0435\\u0442\\u043d\\u044b\\u0445", "\\u0421\\u0435\\u043a\\u0440\\u0435\\u0442\\u043d\\u044b\\u0439 \\u043a\\u043b\\u044e\\u0447 \\u0434\\u043b\\u044f \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u0430 \\u043a API", "\\u0418\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442 \\u0434\\u043b\\u044f \\u043c\\u043e\\u043d\\u0438\\u0442\\u043e\\u0440\\u0438\\u043d\\u0433\\u0430"]	1	null	ConfigMap позволяет отделить конфигурацию от образа приложения.
91	Что такое Continuous Delivery (CD)?	mcq	4	junior	["\\u0410\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0430\\u044f \\u043f\\u043e\\u0434\\u0433\\u043e\\u0442\\u043e\\u0432\\u043a\\u0430 \\u043a\\u043e\\u0434\\u0430 \\u043a \\u0440\\u0435\\u043b\\u0438\\u0437\\u0443 (\\u043f\\u043e\\u0441\\u043b\\u0435 CI \\u043a\\u043e\\u0434 \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438 \\u0440\\u0430\\u0437\\u0432\\u043e\\u0440\\u0430\\u0447\\u0438\\u0432\\u0430\\u0435\\u0442\\u0441\\u044f \\u043d\\u0430 staging-\\u043e\\u043a\\u0440\\u0443\\u0436\\u0435\\u043d\\u0438\\u0438, \\u043d\\u043e \\u0432\\u044b\\u043a\\u0430\\u0442\\u043a\\u0430 \\u0432 \\u043f\\u0440\\u043e\\u0434 \\u2014 \\u0440\\u0443\\u0447\\u043d\\u0430\\u044f)", "\\u0410\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438\\u0439 \\u0434\\u0435\\u043f\\u043b\\u043e\\u0439 \\u0432\\u0441\\u0435\\u0433\\u043e \\u043f\\u043e\\u0434\\u0440\\u044f\\u0434 \\u0431\\u0435\\u0437 \\u0442\\u0435\\u0441\\u0442\\u043e\\u0432", "\\u0420\\u0443\\u0447\\u043d\\u043e\\u0439 \\u043f\\u0435\\u0440\\u0435\\u043d\\u043e\\u0441 \\u0444\\u0430\\u0439\\u043b\\u043e\\u0432 \\u043f\\u043e FTP", "\\u0414\\u043e\\u0441\\u0442\\u0430\\u0432\\u043a\\u0430 \\u043a\\u043e\\u0444\\u0435 \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u0447\\u0438\\u043a\\u0430\\u043c"]	0	null	Continuous Delivery — код всегда в состоянии, готовом к выкатке в прод.
92	Чем Continuous Delivery отличается от Continuous Deployment?	mcq	4	junior	["Continuous Deployment \\u2014 \\u044d\\u0442\\u043e \\u0441\\u043b\\u0435\\u0434\\u0443\\u044e\\u0449\\u0438\\u0439 \\u0448\\u0430\\u0433, \\u0433\\u0434\\u0435 \\u0432\\u044b\\u043a\\u0430\\u0442\\u043a\\u0430 \\u0432 \\u043f\\u0440\\u043e\\u0434 \\u043f\\u0440\\u043e\\u0438\\u0441\\u0445\\u043e\\u0434\\u0438\\u0442 \\u0442\\u043e\\u0436\\u0435 \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438, \\u0431\\u0435\\u0437 \\u0443\\u0447\\u0430\\u0441\\u0442\\u0438\\u044f \\u0447\\u0435\\u043b\\u043e\\u0432\\u0435\\u043a\\u0430", "\\u042d\\u0442\\u043e \\u043e\\u0434\\u043d\\u043e \\u0438 \\u0442\\u043e \\u0436\\u0435", "Continuous Delivery \\u0431\\u044b\\u0441\\u0442\\u0440\\u0435\\u0435", "Continuous Deployment \\u043e\\u043f\\u0430\\u0441\\u043d\\u0435\\u0435 \\u0434\\u043b\\u044f Windows"]	0	null	Continuous Deployment — полностью автоматический пайплайн: коммит -> тесты -> сборка -> деплой на прод.
93	Какие инструменты чаще всего используются для построения CI/CD пайплайнов?	mcq	4	junior	["Microsoft Word, Excel", "Photoshop, Figma", "Jenkins, GitLab CI, GitHub Actions, CircleCI", "VS Code, Sublime Text"]	2	null	Это специализированные серверы автоматизации.
94	Что такое артефакт в CI/CD?	mcq	4	junior	["\\u041e\\u0448\\u0438\\u0431\\u043a\\u0430 \\u0432 \\u043a\\u043e\\u0434\\u0435", "\\u0420\\u0435\\u0437\\u0443\\u043b\\u044c\\u0442\\u0430\\u0442 \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u043f\\u0430\\u0439\\u043f\\u043b\\u0430\\u0439\\u043d\\u0430 (\\u0444\\u0430\\u0439\\u043b, Docker-\\u043e\\u0431\\u0440\\u0430\\u0437), \\u0433\\u043e\\u0442\\u043e\\u0432\\u044b\\u0439 \\u043a \\u0440\\u0430\\u0437\\u0432\\u0435\\u0440\\u0442\\u044b\\u0432\\u0430\\u043d\\u0438\\u044e", "\\u041d\\u0430\\u0437\\u0432\\u0430\\u043d\\u0438\\u0435 \\u0432\\u0435\\u0442\\u043a\\u0438 \\u0432 Git", "\\u041a\\u043e\\u043d\\u0444\\u0438\\u0433\\u0443\\u0440\\u0430\\u0446\\u0438\\u043e\\u043d\\u043d\\u044b\\u0439 \\u0444\\u0430\\u0439\\u043b Jenkins"]	1	null	Артефакты сохраняются и могут быть использованы позже (например, для отката).
95	В каком файле обычно описывается CI/CD пайплайн в GitLab CI?	mcq	4	junior	["Dockerfile", "Jenkinsfile", ".gitlab-ci.yml", "package.json"]	2	null	GitLab CI использует YAML-файл в корне репозитория.
96	Что такое GitHub Actions?	mcq	4	junior	["\\u041f\\u043b\\u0430\\u0433\\u0438\\u043d \\u0434\\u043b\\u044f VS Code", "\\u041f\\u043b\\u0430\\u0442\\u0444\\u043e\\u0440\\u043c\\u0430 \\u0434\\u043b\\u044f \\u0430\\u0432\\u0442\\u043e\\u043c\\u0430\\u0442\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438 \\u0437\\u0430\\u0434\\u0430\\u0447 \\u043f\\u0440\\u044f\\u043c\\u043e \\u0432 GitHub (CI/CD, \\u0438 \\u043d\\u0435 \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e)", "\\u0421\\u043e\\u0446\\u0438\\u0430\\u043b\\u044c\\u043d\\u0430\\u044f \\u0441\\u0435\\u0442\\u044c \\u0434\\u043b\\u044f \\u0440\\u0430\\u0437\\u0440\\u0430\\u0431\\u043e\\u0442\\u0447\\u0438\\u043a\\u043e\\u0432", "\\u0410\\u043d\\u0430\\u043b\\u043e\\u0433 Docker Compose"]	1	null	Позволяет создавать workflows, которые реагируют на события в репозитории (push, pull request).
97	Что такое Infrastructure as Code (IaC)? Мы уже спрашивали, но закрепим примером: какой инструмент лучше подойдет для создания виртуальной машины в AWS?	mcq	4	junior	["Ansible", "Terraform", "Docker", "Bash-\\u0441\\u043a\\u0440\\u0438\\u043f\\u0442 \\u0441 \\u0432\\u044b\\u0437\\u043e\\u0432\\u043e\\u043c AWS CLI"]	1	null	Terraform специализируется на создании ресурсов (provisioning). Ansible хорош для их настройки (configuration management). Хотя Ansible тоже может создать машину, но это не его основная роль.
98	Чем отличается Terraform от Ansible?	mcq	4	junior	["Terraform \\u0432 \\u043f\\u0435\\u0440\\u0432\\u0443\\u044e \\u043e\\u0447\\u0435\\u0440\\u0435\\u0434\\u044c \\u0434\\u043b\\u044f \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u044f \\u0438\\u043d\\u0444\\u0440\\u0430\\u0441\\u0442\\u0440\\u0443\\u043a\\u0442\\u0443\\u0440\\u044b (\\u0438\\u043c\\u043f\\u0435\\u0440\\u0430\\u0442\\u0438\\u0432\\u043d\\u043e), Ansible \\u2014 \\u0434\\u043b\\u044f \\u043d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0438 \\u041f\\u041e \\u043d\\u0430 \\u0443\\u0436\\u0435 \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u043d\\u044b\\u0445 \\u0441\\u0435\\u0440\\u0432\\u0435\\u0440\\u0430\\u0445 (\\u0445\\u043e\\u0442\\u044f \\u0444\\u0443\\u043d\\u043a\\u0446\\u0438\\u0438 \\u043f\\u0435\\u0440\\u0435\\u0441\\u0435\\u043a\\u0430\\u044e\\u0442\\u0441\\u044f)", "\\u042d\\u0442\\u043e \\u043e\\u0434\\u043d\\u043e \\u0438 \\u0442\\u043e \\u0436\\u0435", "Ansible \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0434\\u043b\\u044f Windows, Terraform \\u0442\\u043e\\u043b\\u044c\\u043a\\u043e \\u0434\\u043b\\u044f Linux", "Terraform \\u0440\\u0430\\u0431\\u043e\\u0442\\u0430\\u0435\\u0442 \\u0431\\u044b\\u0441\\u0442\\u0440\\u0435\\u0435"]	0	null	Terraform управляет состоянием инфраструктуры, Ansible — конфигурацией серверов. Часто их используют вместе.
99	Что такое декларативный подход в IaC (как в Terraform)?	mcq	4	junior	["\\u0412\\u044b \\u043f\\u0438\\u0448\\u0435\\u0442\\u0435 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442, \\u0433\\u0434\\u0435 \\u043f\\u043e \\u0448\\u0430\\u0433\\u0430\\u043c \\u0441\\u043e\\u0437\\u0434\\u0430\\u0435\\u0442\\u0435 \\u0440\\u0435\\u0441\\u0443\\u0440\\u0441", "\\u0412\\u044b \\u043e\\u043f\\u0438\\u0441\\u044b\\u0432\\u0430\\u0435\\u0442\\u0435 \\u043a\\u043e\\u043d\\u0435\\u0447\\u043d\\u044b\\u0439 \\u0440\\u0435\\u0437\\u0443\\u043b\\u044c\\u0442\\u0430\\u0442 (\\u0445\\u043e\\u0447\\u0443 \\u043c\\u0430\\u0448\\u0438\\u043d\\u0443 \\u0441 2 CPU \\u0438 4GB RAM), \\u0430 \\u0438\\u043d\\u0441\\u0442\\u0440\\u0443\\u043c\\u0435\\u043d\\u0442 \\u0441\\u0430\\u043c \\u0432\\u044b\\u043f\\u043e\\u043b\\u043d\\u044f\\u0435\\u0442 \\u043d\\u0443\\u0436\\u043d\\u044b\\u0435 \\u0434\\u0435\\u0439\\u0441\\u0442\\u0432\\u0438\\u044f", "\\u0412\\u044b \\u043e\\u043f\\u0438\\u0441\\u044b\\u0432\\u0430\\u0435\\u0442\\u0435, \\u043a\\u0430\\u043a \\u0443\\u0434\\u0430\\u043b\\u0438\\u0442\\u044c \\u0440\\u0435\\u0441\\u0443\\u0440\\u0441", "\\u042d\\u0442\\u043e \\u043f\\u043e\\u0434\\u0445\\u043e\\u0434, \\u043f\\u0440\\u0438 \\u043a\\u043e\\u0442\\u043e\\u0440\\u043e\\u043c \\u043a\\u043e\\u0434 \\u043d\\u0435 \\u043f\\u0438\\u0448\\u0435\\u0442\\u0441\\u044f, \\u0432\\u0441\\u0435 \\u0434\\u0435\\u043b\\u0430\\u0435\\u0442\\u0441\\u044f \\u0440\\u0443\\u043a\\u0430\\u043c\\u0438"]	1	null	Terraform сравнивает ваше описание (желаемое состояние) с реальным состоянием облака и создает план действий.
100	Для чего в облаках нужны Security Groups?	mcq	4	junior	["\\u0414\\u043b\\u044f \\u0443\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u044f \\u043f\\u043e\\u043b\\u044c\\u0437\\u043e\\u0432\\u0430\\u0442\\u0435\\u043b\\u044f\\u043c\\u0438 \\u0432 \\u043a\\u043e\\u043d\\u0441\\u043e\\u043b\\u0438", "\\u0412\\u0438\\u0440\\u0442\\u0443\\u0430\\u043b\\u044c\\u043d\\u044b\\u0439 firewall \\u043d\\u0430 \\u0443\\u0440\\u043e\\u0432\\u043d\\u0435 \\u0438\\u043d\\u0441\\u0442\\u0430\\u043d\\u0441\\u0430 (EC2), \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0439 \\u0440\\u0430\\u0437\\u0440\\u0435\\u0448\\u0430\\u0435\\u0442 \\u0438\\u043b\\u0438 \\u0437\\u0430\\u043f\\u0440\\u0435\\u0449\\u0430\\u0435\\u0442 \\u0442\\u0440\\u0430\\u0444\\u0438\\u043a \\u043f\\u043e \\u043f\\u043e\\u0440\\u0442\\u0430\\u043c \\u0438 IP", "\\u0414\\u043b\\u044f \\u0448\\u0438\\u0444\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u0434\\u0438\\u0441\\u043a\\u0430", "\\u0414\\u043b\\u044f \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u044f VPN"]	1	null	Правила Security Groups: разрешаем входящий трафик на порт 80 и 22, а остальное блокируем.
101	Что такое Virtual DOM в React?	mcq	1	junior	["\\u041f\\u0440\\u044f\\u043c\\u0430\\u044f \\u043a\\u043e\\u043f\\u0438\\u044f \\u0440\\u0435\\u0430\\u043b\\u044c\\u043d\\u043e\\u0433\\u043e DOM", "\\u041b\\u0435\\u0433\\u043a\\u043e\\u0432\\u0435\\u0441\\u043d\\u0430\\u044f \\u043a\\u043e\\u043f\\u0438\\u044f DOM \\u0432 \\u043f\\u0430\\u043c\\u044f\\u0442\\u0438, \\u0438\\u0441\\u043f\\u043e\\u043b\\u044c\\u0437\\u0443\\u0435\\u043c\\u0430\\u044f \\u0434\\u043b\\u044f \\u043e\\u043f\\u0442\\u0438\\u043c\\u0438\\u0437\\u0430\\u0446\\u0438\\u0438", "\\u0421\\u043f\\u043e\\u0441\\u043e\\u0431 \\u0441\\u043e\\u0437\\u0434\\u0430\\u043d\\u0438\\u044f DOM \\u044d\\u043b\\u0435\\u043c\\u0435\\u043d\\u0442\\u043e\\u0432", "\\u0411\\u0438\\u0431\\u043b\\u0438\\u043e\\u0442\\u0435\\u043a\\u0430 \\u0434\\u043b\\u044f \\u0440\\u0430\\u0431\\u043e\\u0442\\u044b \\u0441 DOM"]	1	\N	Virtual DOM - это легковесная копия реального DOM, которая хранится в памяти и используется React для оптимизации обновлений.
102	Какой хук React используется для управления состоянием в функциональном компоненте?	mcq	1	junior	["useEffect", "useState", "useContext", "useReducer"]	1	\N	useState - это хук для управления локальным состоянием в функциональных компонентах React.
103	Что такое REST API?	mcq	2	junior	["\\u041f\\u0440\\u043e\\u0442\\u043e\\u043a\\u043e\\u043b \\u043f\\u0435\\u0440\\u0435\\u0434\\u0430\\u0447\\u0438 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445", "\\u0410\\u0440\\u0445\\u0438\\u0442\\u0435\\u043a\\u0442\\u0443\\u0440\\u043d\\u044b\\u0439 \\u0441\\u0442\\u0438\\u043b\\u044c \\u043f\\u0440\\u043e\\u0435\\u043a\\u0442\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u0432\\u0435\\u0431-\\u0441\\u0435\\u0440\\u0432\\u0438\\u0441\\u043e\\u0432", "\\u042f\\u0437\\u044b\\u043a \\u043f\\u0440\\u043e\\u0433\\u0440\\u0430\\u043c\\u043c\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f", "\\u0411\\u0430\\u0437\\u0430 \\u0434\\u0430\\u043d\\u043d\\u044b\\u0445"]	1	\N	REST (Representational State Transfer) - это архитектурный стиль для проектирования распределенных систем.
104	Какой метод HTTP используется для обновления ресурса?	mcq	2	junior	["GET \\u0438 POST", "PUT \\u0438 PATCH", "DELETE", "OPTIONS"]	1	\N	PUT используется для полной замены ресурса, PATCH - для частичного обновления.
105	Что такое CORS?	mcq	3	junior	["\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0430 \\u0443\\u043f\\u0440\\u0430\\u0432\\u043b\\u0435\\u043d\\u0438\\u044f \\u0432\\u0435\\u0440\\u0441\\u0438\\u044f\\u043c\\u0438", "\\u041c\\u0435\\u0445\\u0430\\u043d\\u0438\\u0437\\u043c \\u0431\\u0435\\u0437\\u043e\\u043f\\u0430\\u0441\\u043d\\u043e\\u0441\\u0442\\u0438 \\u0431\\u0440\\u0430\\u0443\\u0437\\u0435\\u0440\\u043e\\u0432 \\u0434\\u043b\\u044f \\u043a\\u043e\\u043d\\u0442\\u0440\\u043e\\u043b\\u044f \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u0430 \\u043c\\u0435\\u0436\\u0434\\u0443 \\u0438\\u0441\\u0442\\u043e\\u0447\\u043d\\u0438\\u043a\\u0430\\u043c\\u0438", "\\u041f\\u0440\\u043e\\u0442\\u043e\\u043a\\u043e\\u043b \\u043f\\u0435\\u0440\\u0435\\u0434\\u0430\\u0447\\u0438 \\u0444\\u0430\\u0439\\u043b\\u043e\\u0432", "\\u042f\\u0437\\u044b\\u043a \\u0440\\u0430\\u0437\\u043c\\u0435\\u0442\\u043a\\u0438"]	1	\N	CORS (Cross-Origin Resource Sharing) - механизм безопасности браузеров для контроля доступа между разными источниками.
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (id, profession_id, user_id, question_ids, status, score, mode, time_limit, created_at, completed_at) FROM stdin;
1	4	\N	[98, 92, 95, 96, 81, 76, 80, 74, 97, 85, 68, 63, 88, 64, 94, 67, 75, 86, 72, 77]	active	0	practice	\N	2026-03-18 20:16:03.158472	\N
2	4	\N	[63, 84, 95, 83, 85, 71, 100, 66, 82, 70]	active	0	practice	\N	2026-03-18 20:18:47.763747	\N
3	4	1	[68]	completed	1	practice	\N	2026-03-18 20:20:05.237715	2026-03-18 20:20:19.219094
4	4	1	[15, 41, 50, 1, 51, 32, 27, 42, 9, 6, 4, 2, 36, 35, 10]	completed	13	practice	\N	2026-03-18 20:26:16.407602	2026-03-18 20:30:49.20861
\.


--
-- Data for Name: user_achievements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_achievements (id, user_id, achievement_id, unlocked_at) FROM stdin;
\.


--
-- Data for Name: user_progress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_progress (id, user_id, xp, level, total_sessions, completed_sessions, total_correct_answers, total_questions_answered, best_streak, current_streak, created_at, last_session_at, title, badges) FROM stdin;
1	1	140	1	2	2	14	16	1	0	2026-03-18 20:09:27.814342	2026-03-18 20:30:49.218483	Новичок	[]
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, hashed_password, is_admin, created_at) FROM stdin;
1	admin@example.com	$2b$12$fQnJJFN44qrbbL4vwog7Me94uClpeSITbJFIbCe6GUY4y1QyBJNQ.	t	2026-03-18 20:08:50.001966
\.


--
-- Name: achievements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.achievements_id_seq', 1, false);


--
-- Name: answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.answers_id_seq', 16, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 34, true);


--
-- Name: interview_configs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.interview_configs_id_seq', 1, false);


--
-- Name: ordering_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ordering_items_id_seq', 1, false);


--
-- Name: professions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.professions_id_seq', 4, true);


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_id_seq', 105, true);


--
-- Name: sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessions_id_seq', 4, true);


--
-- Name: user_achievements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_achievements_id_seq', 1, false);


--
-- Name: user_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_progress_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: achievements achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.achievements
    ADD CONSTRAINT achievements_pkey PRIMARY KEY (id);


--
-- Name: answers answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: interview_configs interview_configs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interview_configs
    ADD CONSTRAINT interview_configs_pkey PRIMARY KEY (id);


--
-- Name: ordering_items ordering_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ordering_items
    ADD CONSTRAINT ordering_items_pkey PRIMARY KEY (id);


--
-- Name: professions professions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.professions
    ADD CONSTRAINT professions_pkey PRIMARY KEY (id);


--
-- Name: question_categories question_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_categories
    ADD CONSTRAINT question_categories_pkey PRIMARY KEY (question_id, category_id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: user_achievements user_achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_achievements
    ADD CONSTRAINT user_achievements_pkey PRIMARY KEY (id);


--
-- Name: user_progress user_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_progress
    ADD CONSTRAINT user_progress_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_achievements_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_achievements_id ON public.achievements USING btree (id);


--
-- Name: ix_answers_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_answers_created_at ON public.answers USING btree (created_at);


--
-- Name: ix_answers_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_answers_id ON public.answers USING btree (id);


--
-- Name: ix_answers_is_correct; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_answers_is_correct ON public.answers USING btree (is_correct);


--
-- Name: ix_answers_question_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_answers_question_id ON public.answers USING btree (question_id);


--
-- Name: ix_answers_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_answers_user_id ON public.answers USING btree (user_id);


--
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- Name: ix_categories_profession_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_profession_id ON public.categories USING btree (profession_id);


--
-- Name: ix_interview_configs_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_interview_configs_created_at ON public.interview_configs USING btree (created_at);


--
-- Name: ix_interview_configs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_interview_configs_id ON public.interview_configs USING btree (id);


--
-- Name: ix_interview_configs_profession_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_interview_configs_profession_id ON public.interview_configs USING btree (profession_id);


--
-- Name: ix_interview_configs_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_interview_configs_user_id ON public.interview_configs USING btree (user_id);


--
-- Name: ix_ordering_items_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ordering_items_id ON public.ordering_items USING btree (id);


--
-- Name: ix_professions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_professions_id ON public.professions USING btree (id);


--
-- Name: ix_questions_difficulty; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_questions_difficulty ON public.questions USING btree (difficulty);


--
-- Name: ix_questions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_questions_id ON public.questions USING btree (id);


--
-- Name: ix_questions_profession_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_questions_profession_id ON public.questions USING btree (profession_id);


--
-- Name: ix_questions_question_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_questions_question_type ON public.questions USING btree (question_type);


--
-- Name: ix_sessions_completed_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sessions_completed_at ON public.sessions USING btree (completed_at);


--
-- Name: ix_sessions_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sessions_created_at ON public.sessions USING btree (created_at);


--
-- Name: ix_sessions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sessions_id ON public.sessions USING btree (id);


--
-- Name: ix_sessions_profession_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sessions_profession_id ON public.sessions USING btree (profession_id);


--
-- Name: ix_sessions_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sessions_status ON public.sessions USING btree (status);


--
-- Name: ix_sessions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sessions_user_id ON public.sessions USING btree (user_id);


--
-- Name: ix_user_achievements_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_achievements_id ON public.user_achievements USING btree (id);


--
-- Name: ix_user_progress_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_progress_id ON public.user_progress USING btree (id);


--
-- Name: ix_user_progress_level; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_progress_level ON public.user_progress USING btree (level);


--
-- Name: ix_user_progress_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_progress_user_id ON public.user_progress USING btree (user_id);


--
-- Name: ix_user_progress_xp; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_progress_xp ON public.user_progress USING btree (xp);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: answers answers_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: answers answers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: categories categories_profession_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_profession_id_fkey FOREIGN KEY (profession_id) REFERENCES public.professions(id);


--
-- Name: interview_configs interview_configs_profession_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interview_configs
    ADD CONSTRAINT interview_configs_profession_id_fkey FOREIGN KEY (profession_id) REFERENCES public.professions(id);


--
-- Name: interview_configs interview_configs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interview_configs
    ADD CONSTRAINT interview_configs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: question_categories question_categories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_categories
    ADD CONSTRAINT question_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: question_categories question_categories_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_categories
    ADD CONSTRAINT question_categories_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: questions questions_profession_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_profession_id_fkey FOREIGN KEY (profession_id) REFERENCES public.professions(id);


--
-- Name: sessions sessions_profession_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_profession_id_fkey FOREIGN KEY (profession_id) REFERENCES public.professions(id);


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_achievements user_achievements_achievement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_achievements
    ADD CONSTRAINT user_achievements_achievement_id_fkey FOREIGN KEY (achievement_id) REFERENCES public.achievements(id);


--
-- Name: user_achievements user_achievements_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_achievements
    ADD CONSTRAINT user_achievements_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_progress user_progress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_progress
    ADD CONSTRAINT user_progress_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict OWmUZvUx9fAnbsvZEuVhXVFdwZK6KEJf0tJYFwZ1SO42RimiG0EYKdff35SKbJb

