--CREATE TABLE IF NOT EXISTS test (
--		id	serial		primary key,
--		t	text		NULL,
--		n	integer		null
--);
--select * from test;


/*
 * Concat rows of column into str
 */
--select
----	con_tags.id_tag
----	string_agg(con_tags.id_tag::text, '; ') as id_tags_concat
--	string_agg(tags.txt, '; ') as tags_concat
--from
--	consultation_tags con_tags
--	,tags
--where 1=1
----	and con_tags.id_consultation	= consults.id
--	and tags.id	= con_tags.id_tag 
--	and con_tags.id_consultation	= 91
--;


select * from raw_consultations;
select * from consultations;

select * from tags
order by txt;
select * from consultation_tags;

--select * from answers;
--select * from consultants;
--select * from consultant_answers;

--select * from questions;
--select * from asking_persons;

-- select * from categories;
-- select * from consultation_categories;


/*
 *	Get missing numbers in sequence 
 */
select
--	num as missing
	string_agg(numbers.num::varchar, ', ') as tags_concat
from generate_series(4001, 5000) as numbers(num)
left join consultations on
	(numbers.num = consultations.c_number)
where 1=1
	and consultations.c_number is null;


/*
 *	Find doubles 
 */
select * from consultations ou
where (
	select count(*) from consultations inr
	where inr.c_number = ou.c_number
) > 1;


/*
 * Count of all consultations
 */
select count(*) from consultations;


/*
 * Show not parsed consults
 */
select
	consults.id 
	,consults.c_number			c_number
	,consults.c_date			c_date
	,ask_persons.name			who_asks
	,questions.txt				question
	,consultants.name			consultant
	,answers.txt				answer
	,con_tags_l.tags_concat		tags
	,raw_cons.is_done			raw_con_is_done
	,raw_cons.problem_place		problem_place
	,raw_cons.txt				raw_con_txt
	,raw_cons.txt_rest			raw_con_txt_rest
	,raw_cons.processed_date	raw_con_proc_date
from
	consultations		consults
	,raw_consultations	raw_cons
	,answers			answers
	,consultants		consultants
	,consultant_answers	cons_answers
	,questions			questions
	,asking_persons		ask_persons
	,lateral (
		select
			string_agg(tags.txt, ';' || chr(10)) as tags_concat
		from
			consultation_tags con_tags
			,tags
		where 1=1
			and con_tags.id_consultation	= consults.id
			and tags.id						= con_tags.id_tag
	) con_tags_l	-- concat tags into str w/ new line as delimeter
where	1 = 1
	and consults.id_raw		= raw_cons.id
	and answers.id			= cons_answers.id_answer
	and consultants.id		= cons_answers.id_consultant
	and consults.id			= cons_answers.id_consultation
	and consults.id			= questions.id_consultation
	and consults.id			= ask_persons.id_consultation
--	and raw_cons.is_done 	= 0
order by
	c_number
--	problem_place
;