--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1 (Ubuntu 15.1-1.pgdg20.04+1)
-- Dumped by pg_dump version 15.1 (Ubuntu 15.1-1.pgdg20.04+1)

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
-- Name: accounts; Type: TABLE; Schema: public; Owner: chatterbox
--

CREATE TABLE public.accounts (
    name character varying(50) NOT NULL,
    phone character varying(10) NOT NULL,
    age smallint,
    password character varying(50) NOT NULL
);


ALTER TABLE public.accounts OWNER TO chatterbox;

--
-- Name: userserver; Type: TABLE; Schema: public; Owner: chatterbox
--

CREATE TABLE public.userserver (
    phone character varying(10),
    serverid smallint
);


ALTER TABLE public.userserver OWNER TO chatterbox;

--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: chatterbox
--

COPY public.accounts (name, phone, age, password) FROM stdin;
Aman	7977265537	20	asdfghjkl
\.


--
-- Data for Name: userserver; Type: TABLE DATA; Schema: public; Owner: chatterbox
--

COPY public.userserver (phone, serverid) FROM stdin;
\.


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: chatterbox
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (phone);


--
-- Name: userserver userserver_phone_fkey; Type: FK CONSTRAINT; Schema: public; Owner: chatterbox
--

ALTER TABLE ONLY public.userserver
    ADD CONSTRAINT userserver_phone_fkey FOREIGN KEY (phone) REFERENCES public.accounts(phone);


--
-- PostgreSQL database dump complete
--

