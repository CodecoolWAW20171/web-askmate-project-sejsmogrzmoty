--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS fk_mate_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_mate_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_mate_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.mate DROP CONSTRAINT IF EXISTS pk_mate_id CASCADE;





DROP TABLE IF EXISTS public.question;
DROP SEQUENCE IF EXISTS public.question_id_seq;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer DEFAULT 0,
    vote_number integer DEFAULT 0,
    title text,
    message text,
    image text,
    mate_id integer
);

DROP TABLE IF EXISTS public.answer;
DROP SEQUENCE IF EXISTS public.answer_id_seq;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer DEFAULT 0,
    question_id integer,
    message text,
    image text,
    mate_id integer

);

DROP TABLE IF EXISTS public.comment;
DROP SEQUENCE IF EXISTS public.comment_id_seq;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer DEFAULT 0,
    mate_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
DROP SEQUENCE IF EXISTS public.tag_id_seq;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.mate;
DROP SEQUENCE IF EXISTS public.mate_id_seq;
CREATE TABLE mate (
    id serial NOT NULL,
    username text,
    registration_time timestamp without time zone,
    profile_pic text,
    reputation integer
);




ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY mate
    ADD CONSTRAINT pk_mate_id PRIMARY KEY (id);

ALTER TABLE public.comment
  ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id)
      REFERENCES public.answer (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;

ALTER TABLE public.answer
  ADD CONSTRAINT pk_question_id FOREIGN KEY (question_id)
      REFERENCES public.question (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;


ALTER TABLE public.question_tag
  ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id)
      REFERENCES public.question (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;
      
ALTER TABLE public.comment
  ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id)
      REFERENCES public.question (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;

ALTER TABLE public.question_tag
  ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id)
      REFERENCES public.tag (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;


ALTER TABLE public.answer
  ADD CONSTRAINT pk_mate_id FOREIGN KEY (mate_id)
      REFERENCES public.mate (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;

ALTER TABLE public.question
  ADD CONSTRAINT pk_mate_id FOREIGN KEY (mate_id)
      REFERENCES public.mate (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;

ALTER TABLE public.comment
  ADD CONSTRAINT pk_mate_id FOREIGN KEY (mate_id)
      REFERENCES public.mate (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;


GRANT INSERT, SELECT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO askmate_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO askmate_user;


INSERT INTO mate VALUES (0, 'piczka','2017-03-27 07:00:13', NULL, 0);
INSERT INTO mate VALUES (1, 'pipka','2016-03-27 07:00:13', NULL, 0);


INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL, 0);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png', 0);
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL, 0);

INSERT INTO question VALUES (30, '2017-06-02 12:41:00', 201, -52, 'Is n-word offensive to all people with name begining with letter "n"?', '', NULL, 0);
INSERT INTO question VALUES (31, '2017-06-04 05:41:00', 621, -200, 'if con is the opposite of pro, what is the opposite of progress', 'Regress', 'http://i0.kym-cdn.com/entries/icons/original/000/017/618/pepefroggie.jpg', 0);
INSERT INTO question VALUES (32, '2016-12-01 16:58:00', 1221, 80, 'Saying that the Easter Bunny does not orgasm with every egg laid is considered blasphemy and grounds for excommunication from the Church.', 'Weird fact: the Easter Bunny was the source of a significant amount of theological debate during the 1200''s, as Catholic philosophers debated why God would create a creature in a constant state of labor (and thus suffering). The Catholic Church ultimately resolved this question by declaring that the Easter Bunny orgasmed every time it laid it an egg (which it was doing constantly). This is now codified in Canon Law (the legal code of the Catholic Church and much of Europe in the pre-modern era) and saying that the Easter Bunny does not orgasm with every egg laid is considered blasphemy and grounds for excommunication from the Church.', NULL, 0);
INSERT INTO question VALUES (33, '2016-02-01 06:14:00', 2201, 9, 'Daily Life', '-    wake up ☑
-    check if rice dropped a new diss track ;) ☑
-    he didnt ☑
-    damn :/ ☑
-    when my boy ricegum gon drop some h e a t ??? ☑
-    play fortnite ☑
-    get #1 victory and share it on sc story ☑
-    wait patiently for all the girls to reply to the story', NULL, 0);
INSERT INTO question VALUES (34, '2014-10-21 12:54:00', 1846, 49, 'I commented on a logan paul video "So does Logan Paul have some kind of fetish for dead things﻿" And someone said shut up, and I replied with this', 'Wow, I mean wow, your comment has really enlightened me.
The beautiful effort put into writing this comment is really expressed through the extremely subtle message that is hidden deep within it.
After reading your comment, I immediately resigned from being a hater, and can proudly say I joined the logang. I can''t imagine the effort and countless hours you poured into that comment, and I must thank you for it, it has completely changed who I am as a person.
I think you need to show your exquisite writing to Harvard because you could get a fully paid English scholarship with the Divine skill that you posses. I wish you luck with your wondrous career in English writing, and I hope to read multiple novels in the future written by none other than the person who turned my life around, karina ivonne riojas infante.
Such a stupendous name as well m''lady. Well tips fedora thanks, and thanks again for helping me join the logang. #logangforlife﻿', NULL, 0);
INSERT INTO question VALUES (35, '2018-03-20 13:19:21', 63, 4, 'PyCharm doing a refactor on an ID not replacing it in associated CSS and JS files', 'I tried to perform a refactor on an element''s ID by highlighting it and right clicking to perform a refactor to rename it.
However, all that PyCharm did was rename the element''s ID without searching for it in the other files associated in the project.
Is there an option / plugin that I can use to be able to rename all times an ID is used in my JavaScript and CSS when I rename it in the HTML file with a refactor?', NULL, 0);
INSERT INTO question VALUES (36, '2012-06-21 18:30:19', 25796, 69, 'Numpy: cartesian product of x and y array points into single array of 2D points', 'I have two numpy arrays that define the x and y axes of a grid. For example:
x = numpy.array([1,2,3])
y = numpy.array([4,5])
I''d like to generate the Cartesian product of these arrays to generate:
array([[1,4],[2,4],[3,4],[1,5],[2,5],[3,5]])
In a way that''s not terribly inefficient since I need to do this many times in a loop. I''m assuming that converting them to a Python list and using itertools.product and back to a numpy array is not the most efficient form.', NULL, 0);
INSERT INTO question VALUES (37, '2018-03-27 10:05:45', 11085, 98, 'Remove ✅, 🔥, ✈ , ♛ and other such emojis/images/signs from Java string', 'I have some strings with all kinds of different emojis/images/signs in them. Not all the strings are in English. Some of them are in other non-Latin languages, for example:
▓ railway??
→ Cats and dogs
I''m on 🔥
Apples ⚛ 
✅ Vi sign
♛ I''m the king ♛ 
Corée ♦ du Nord ☁  (French)
 gjør at både ◄╗ (Norwegian)
Star me ★
Star ⭐ once more
早上好 ♛ (Chinese)
Καλημέρα ✂ (Greek)
another ✓ sign ✓
добрай раніцы ✪ (Belarus)
◄ शुभ प्रभात ◄ (Hindi)
✪ ✰ ❈ ❧ Let''s get together ★. We shall meet at 12/10/2018 10:00 AM at Tony''s.❉
and many more of these.

I like to get rid of all these signs/images and to keep only the letters in the different languages & the punctuation.

I tried to clean the signs using the EmojiParser library:

String withoutEmojis = EmojiParser.removeAllEmojis(input);
The problem is that EmojiParser is not able to removed the majority of the signs. The ♦ sign is the only one I found till now that it removed. Other signs such as ✪ ❉ ★ ✰ ❈ ❧ ✂ ❋ ⓡ ✿ ♛ 🔥 are not removed.

Is there a way to remove all these signs from the input strings and keeping only the letters & punctuation in the different languages?', NULL, 0);
INSERT INTO question VALUES (38, '2018-03-27 07:00:13', 1046, 16, 'Three lists zipped into list of dicts', 'Consider the following:
>>> # list of length n
>>> idx = [''a'', ''b'', ''c'', ''d'']
>>> # list of length n
>>> l_1 = [1, 2, 3, 4]
>>> # list of length n
>>> l_2 = [5, 6, 7, 8]
>>> # first key
>>> key_1 = ''mkt_o''
>>> # second key
>>> key_2 = ''mkt_c''
How do I zip this mess to look like this?
{
    ''a'': {''mkt_o'': 1, ''mkt_c'': 5},
    ''b'': {''mkt_o'': 2, ''mkt_c'': 6},
    ''c'': {''mkt_o'': 3, ''mkt_c'': 6},
    ''d'': {''mkt_o'': 4, ''mkt_c'': 7},
    ...
}
The closest I''ve got is something like this:
>>> dict(zip(idx, zip(l_1, l_2)))
{''a'': (1, 5), ''b'': (2, 6), ''c'': (3, 7), ''d'': (4, 8)}
Which if course has tuples as the values instead of dictionaries, and
>>> dict(zip((''mkt_o'', ''mkt_c''), (1,2)))
{''mkt_o'': 1, ''mkt_c'': 2}
Which seems like it might be promising but again, fails to meet requirements.', NULL, 0);
INSERT INTO question VALUES (39, '2018-03-24 21:37:00', 180, 12, 'Why is Haskell monadic bind left-associative?', 'The >>= and >> operators are both infixl 1. Why the left-associativity?
In particular, I observe the equivalences:
(do a; b; c ) == (a >> (b >> c))   -- Do desugaring
(a >> b >> c) == ((a >> b) >> c)   -- Fixity definition
So do is desugared differently to how the fixity definition naturally works, which is surprising.', NULL, 0);
INSERT INTO question VALUES (40, '2011-04-01 00:50:02', 297676, 472, 'Why is this program erroneously rejected by three C++ compilers?','I am having some difficulty compiling a C++ program that I''ve written.
This program is very simple and, to the best of my knowledge, conforms to all the rules set forth in the C++ Standard. I''ve read over the entirety of ISO/IEC 14882:2003 twice to be sure.
The program is as follows:
Here is the output I received when trying to compile this program with Visual C++ 2010:
c:\dev>cl /nologo helloworld.png
cl : Command line warning D9024 : unrecognized source file type ''helloworld.png'', object file assumed
helloworld.png : fatal error LNK1107: invalid or corrupt file: cannot read at 0x5172
Dismayed, I tried g++ 4.5.2, but it was equally unhelpful:
c:\dev>g++ helloworld.png
helloworld.png: file not recognized: File format not recognized
collect2: ld returned 1 exit status
I figured that Clang (version 3.0 trunk 127530) must work, since it is so highly praised for its standards conformance. Unfortunately, it didn''t even give me one of its pretty, highlighted error messages:
c:\dev>clang++ helloworld.png
helloworld.png: file not recognized: File format not recognized
collect2: ld returned 1 exit status
clang++: error: linker (via gcc) command failed with exit code 1 (use -v to see invocation)
To be honest, I don''t really know what any of these error message mean.
Many other C++ programs have source files with a .cpp extension, so I thought perhaps I needed to rename my file. I changed its name to helloworld.cpp, but that didn''t help. I think there is a very serious bug in Clang because when I tried using it to compile the renamed program, it flipped out, printed "84 warnings and 20 errors generated." and made my computer beep a lot!
What have I done wrong here? Have I missed some critical part of the C++ Standard? Or are all three compilers really just so broken that they can''t compile this simple program?', 'https://i.stack.imgur.com/JQXWL.png', 0);

SELECT pg_catalog.setval('question_id_seq', 40, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', NULL, 0);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Look it up in the Python docs', 'images/image2.jpg', 0);
INSERT INTO answer VALUES (3, '2018-03-22 21:39:44', 4, 35, 'In order for PyCharm to refactor your ID correctly, there needs to be an association between the file you''re updating the ID in and the CSS that''s related to that ID.
Even though you might have defined that ID in a CSS file, it might be possible that the ID is defined in multiple CSS files. If you were to refactor an ID and it changed it for all CSS files, it wouldn''t really be doing the what is intended by "refactor".
If you want to have it change everywhere, you might just want to do a global find & replace, instead of using the "refactor" option.', NULL, 0);
INSERT INTO answer VALUES (4, '2017-06-04 22:18:12', 50, 30, 'Directly from Wikipedia:

The N-word euphemism
The euphemism the N-word became mainstream American English usage during the racially contentious O. J. Simpson murder case in 1995.
Key prosecution witness Detective Mark Fuhrman, of the Los Angeles Police Department – who denied using racist language on duty – impeached himself with his prolific use of nigger in tape recordings about his police work. The recordings, by screenplay writer Laura McKinney, were from a 1985 research session wherein the detective assisted her with a screenplay about LAPD policewomen.
Fuhrman excused his use of the word saying he used nigger in the context of his "bad cop" persona. The popular press reporting and discussing Fuhrman''s testimony substituted the N-word for nigger.', NULL, 0);
INSERT INTO answer VALUES (5, '2016-12-05 14:19:34', 24, 32, 'You are one enormous weirdo. Stop talking shit about the easter bunny. He does not appreciate it.', NULL, 0);
INSERT INTO answer VALUES (6, '2012-06-21 18:43:01', 45, 36, '>>> numpy.transpose([numpy.tile(x, len(y)), numpy.repeat(y, len(x))])
array([[1, 4],
       [2, 4],
       [3, 4],
       [1, 5],
       [2, 5],
       [3, 5]])
See Using numpy to build an array of all combinations of two arrays for a general solution for computing the Cartesian product of N arrays.', NULL, 0);
INSERT INTO answer VALUES (7, '2012-06-21 20:58:40', 86, 36, 'A canonical cartesian_product (almost)
There are many approaches to this problem with different properties. Some are faster than others, and some are more general-purpose. After a lot of testing and tweaking, I''ve found that the following function, which calculates an n-dimensional cartesian_product, is faster than most others for many inputs. For a pair of approaches that are slightly more complex, but are even a bit faster in many cases, see the answer by Paul Panzer.

Given that answer, this is no longer the fastest implementation of the cartesian product in numpy that I''m aware of. However, I think its simplicity will continue to make it a useful benchmark for future improvement:

def cartesian_product(*arrays):
    la = len(arrays)
    dtype = numpy.result_type(*arrays)
    arr = numpy.empty([len(a) for a in arrays] + [la], dtype=dtype)
    for i, a in enumerate(numpy.ix_(*arrays)):
        arr[...,i] = a
    return arr.reshape(-1, la)
It''s worth mentioning that this function uses ix_ in an unusual way; whereas the documented use of ix_ is to generate indices into an array, it just so happens that arrays with the same shape can be used for broadcasted assignment. Many thanks to mgilson, who inspired me to try using ix_ this way, and to unutbu, who provided some extremely helpful feedback on this answer, including the suggestion to use numpy.result_type.

Notable alternatives
It''s sometimes faster to write contiguous blocks of memory in Fortran order. That''s the basis of this alternative, cartesian_product_transpose, which has proven faster on some hardware than cartesian_product (see below). However, Paul Panzer''s answer, which uses the same principle, is even faster. Still, I include this here for interested readers:

def cartesian_product_transpose(*arrays):
    broadcastable = numpy.ix_(*arrays)
    broadcasted = numpy.broadcast_arrays(*broadcastable)
    rows, cols = numpy.prod(broadcasted[0].shape), len(broadcasted)
    dtype = numpy.result_type(*arrays)

    out = numpy.empty(rows * cols, dtype=dtype)
    start, end = 0, rows
    for a in broadcasted:
        out[start:end] = a.reshape(-1)
        start, end = end, end + rows
    return out.reshape(cols, rows).T
After coming to understand Panzer''s approach, I wrote a new version that''s almost as fast as his, and is almost as simple as cartesian_product:

def cartesian_product_simple_transpose(arrays):
    la = len(arrays)
    dtype = numpy.result_type(*arrays)
    arr = numpy.empty([la] + [len(a) for a in arrays], dtype=dtype)
    for i, a in enumerate(numpy.ix_(*arrays)):
        arr[i, ...] = a
    return arr.reshape(la, -1).T
This appears to have some constant-time overhead that makes it run slower than Panzer''s for small inputs. But for larger inputs, in all the tests I ran, it performs just as well as his fastest implementation (cartesian_product_transpose_pp).', NULL, 0);
INSERT INTO answer VALUES (8, '2013-10-18 22:00:34', 22, 36, 'You can just do normal list comprehension in python
x = numpy.array([1,2,3])
y = numpy.array([4,5])
[[x0, y0] for x0 in x for y0 in y]
which should give you
[[1, 4], [1, 5], [2, 4], [2, 5], [3, 4], [3, 5]]', NULL, 0);
INSERT INTO answer VALUES (9, '2018-03-27 14:46:45', 160, 37, 'Instead of blacklisting some elements, how about creating a whitelist of the characters you do wish to keep? This way you don''t need to worry about every new emoji being added.
String characterFilter = "[^\\p{L}\\p{M}\\p{N}\\p{P}\\p{Z}\\p{Cf}\\p{Cs}\\s]";
String emotionless = aString.replaceAll(characterFilter,"");
So:
[\\p{L}\\p{M}\\p{N}\\p{P}\\p{Z}\\p{Cf}\\p{Cs}\\s] is a range representing all numeric (\\p{N}), letter (\\p{L}), mark (\\p{M}), punctuation (\\p{P}), whitespace/separator (\\p{Z}), other formatting (\\p{Cf}) and other characters above U+FFFF in Unicode (\\p{Cs}), and newline (\\s) characters, including those from other alphabets such as Cyrillic, Latin, Kanji, etc.
The ^ in the regex character set negates the match.
Example:
String str = "hello world _# 皆さん、こんにちは！　私はジョンと申します。🔥";
System.out.print(str.replaceAll("[^\\p{L}\\p{M}\\p{N}\\p{P}\\p{Z}\\p{Cf}\\p{Cs}\\s]",""));
// Output:
//   "hello world _# 皆さん、こんにちは！　私はジョンと申します。"
If you need more information, check out the Java documentation for regexes.', NULL, 0);
INSERT INTO answer VALUES (10, '2018-03-27 10:10:46', 42, 37, 'Based on Full Emoji List, v11.0 you have 1644 different Unicode code points to remove. For example ✅ is on this list as U+2705.
Having the full list of emojis you need to filter them out using code points. Iterating over single char or byte won''t work as single code point can span multiple bytes. Because Java uses UTF-16 emojis will usually take two chars.
String input = "ab✅cd";
for (int i = 0; i < input.length();) {
  int cp = input.codePointAt(i);
  // filter out if matches
  i += Character.charCount(cp); 
}
Mapping from Unicode code point U+2705 to Java int is straightforward:
int viSign = 0x2705;
or since Java supports Unicode Strings:
int viSign = "✅".codePointAt(0);', NULL, 0);
INSERT INTO answer VALUES (11, '2018-03-28 11:00:03', 12, 37, 'ICU4J is your friend.
UCharacter.hasBinaryProperty(UProperty.EMOJI);
Remember to keep your version of icu4j up to date and note this will only filter out official Unicode emoji, not symbol characters. Combine with filtering out other character types as desired.
More information: http://icu-project.org/apiref/icu4j/com/ibm/icu/lang/UProperty.html#EMOJI', NULL, 0);
INSERT INTO answer VALUES (12, '2018-03-27 07:03:14', 29, 38, '{k : {key_1 : v1, key_2 : v2} for k,v1,v2 in zip(idx, l_1, l_2)}', NULL, 0);
INSERT INTO answer VALUES (13, '2018-03-27 07:07:18', 12, 38, 'Solution 1: You may use zip twice (actually thrice) with dictionary comprehension to achieve this as:
idx = [''a'', ''b'', ''c'', ''d'']
l_1 = [1, 2, 3, 4]
l_2 = [5, 6, 7, 8]
keys = [''mkt_o'', ''mkt_c'']   # yours keys in another list
new_dict = {k: dict(zip(keys, v)) for k, v in zip(idx, zip(l_1, l_2))}
Solution 2: You may also use zip with nested list comprehension as:
new_dict = dict(zip(idx, [{key_1: i, key_2: j} for i, j in zip(l_1, l_2)]))
Solution 3: using dictionary comprehension on top of zip as shared in DYZ''s answer:
new_dict = {k : {key_1 : v1, key_2 : v2} for k,v1,v2 in zip(idx, l_1, l_2)}
All the above solutions will return new_dict as:
{
     ''a'': {''mkt_o'': 1, ''mkt_c'': 5}, 
     ''b'': {''mkt_o'': 2, ''mkt_c'': 6}, 
     ''c'': {''mkt_o'': 3, ''mkt_c'': 7},
     ''d'': {''mkt_o'': 4, ''mkt_c'': 8}
 }', NULL, 0);
INSERT INTO answer VALUES (14, '2018-03-24 23:47:32', 14, 39, '>>= must surely be left-associative.
Prelude> ["bla","bli di","blub"] >>= words >>= reverse
"albilbidbulb"
Prelude> ["bla","bli di","blub"] >>= (words >>= reverse)
<interactive>:3:30: error:
    • Couldn''t match expected type ‘[[b0]]’
                  with actual type ‘String -> [String]’
    • Probable cause: ‘words’ is applied to too few arguments
      In the first argument of ‘(>>=)’, namely ‘words’
      In the second argument of ‘(>>=)’, namely ‘(words >>= reverse)’
      In the expression:
        ["bla", "bli di", "blub"] >>= (words >>= reverse)
And >> pretty much follows >>=; if it had another fixity it would not only feel weird as Lennart said, it would also prevent you from using both operators in a chain:
Prelude> ["bla","bli di","blub"] >>= words >> "Ha"
"HaHaHaHa"
Prelude> infixr 1 ⬿≫; (⬿≫) = (>>)
Prelude> ["bla","bli di","blub"] >>= words ⬿≫ "Ha"
<interactive>:6:1: error:
    Precedence parsing error
        cannot mix ‘>>=’ [infixl 1] and ‘⬿≫’ [infixr 1] in the same infix expression', NULL, 0);
INSERT INTO answer VALUES (15, '2018-03-24 23:50:39', 6, 39, '>>= is left-associative because it''s convenient. We want m >>= f1 >>= f2 to be parsed as (m >>= f1) >>= f2, not as m >>= (f1 >>= f2), which would likely not type check, as pointed out in the comments.

The associativity of >> however, is simply a mirror of >>=. This is likely for the sake of consistency, since we can prove that >> is associative via the third monad law: (m >>= f) >>= g ≡ m >>= ( \x -> f x >>= g ). That is to say, its associativity doesn''t theoretically matter. Here is the proof:

-- Definition:
a >> b ≡ a >>= (\_ -> b)

-- Proof: (a >> b) >> c ≡ a >> (b >> c)
  (a >> b) >> c
≡ (a >>= (\_ -> b)) >> c                  -- [Definition]
≡ (a >>= (\_ -> b)) >>= (\_ -> c)         -- [Definition]
≡ a >>= (\x -> (\_ -> b) x >>= (\_ -> c)) -- [Monad law]
≡ a >>= (\_ -> b >>= (\_ -> c))           -- [Beta-reduction]
≡ a >>= (\_ -> b >> c)                    -- [Definition]
≡ a >> (b >> c)                           -- [Definition]
∎
do-notation de-sugars differently because it has a different goal. Essentially, since do-notation is essentially writing out a lambda, right-association is needed. This is because m >>= (\v -> (...)) is written as do {v <- m; (...)}. As earlier, the de-sugaring of >> here seems to follow >>= for the sake of consistency.', NULL, 0);
INSERT INTO answer VALUES (16, '2018-03-24 23:50:39', 174, 40, 'In the standard, §2.1/1 specifies:
Physical source file characters are mapped, in an implementation-defined manner, to the basic source character set (introducing new-line characters for end-of-line indicators) if necessary.
Your compiler doesn''t support that format (aka cannot map it to the basic source character set), so it cannot move into further processing stages, hence the error. It is entirely possible that your compiler support a mapping from image to basic source character set, but is not required to.
Since this mapping is implementation-defined, you''ll need to look at your implementations documentation to see the file formats it supports. Typically, every major compiler vendor supports (canonically defined) text files: any file produced by a text editor, typically a series of characters.
Note that the C++ standard is based off the C standard (§1.1/2), and the C(99) standard says, in §1.2:
This International Standard does not specify
— the mechanism by which C programs are transformed for use by a data-processing system;
— the mechanism by which C programs are invoked for use by a data-processing system;
— the mechanism by which input data are transformed for use by a C program;
So, again, the treatment of source files is something you need to find in your compilers documentation.', NULL, 0);
INSERT INTO answer VALUES (17, '2011-04-01 05:35:37', 576, 40, 'Originally from Overv @ reddit.', 'https://i.imgur.com/QlGpd.gif', 0);
INSERT INTO answer VALUES (18, '2011-04-01 13:55:50', 320, 40, 'Try this way:', 'https://i.stack.imgur.com/OjB9Z.png', 0);
INSERT INTO answer VALUES (19, '2011-04-01 01:03:33', 212, 40, 'Your < and  >, ( and  ), { and  } don''t seem to match very well; Try drawing them better.', NULL, 0);

SELECT pg_catalog.setval('answer_id_seq', 19, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00', 0);
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00', 0);
INSERT INTO comment VALUES (3, 35, NULL, 'The refactor will work if your HTML has a reference to the CSS file, otherwise the refactor won''t be able co-relate', '2018-03-22 17:14:06', 0);
INSERT INTO comment VALUES (4, 30, NULL, 'You are one stupid i-word as in idiot.', '2017-06-06 14:14:42', 0);
INSERT INTO comment VALUES (5, 31, NULL, 'You should kill yourself. Wait, no it is not punishing enough', '2017-06-04 18:33:00', 0);
INSERT INTO comment VALUES (6, 32, NULL, 'WTF did I just read!', '2016-12-04 09:23:04', 0);
INSERT INTO comment VALUES (7, 36, NULL, 'I noticed that the most expensive step in itertools approach is the final conversion from list to array. Without this last step it''s twice as fast as Ken''s example', '2012-06-21 19:09:29', 0);
INSERT INTO comment VALUES (8, NULL, 6, 'An advantage of this approach is that it produces consistent output for arrays of the same size. The meshgrid + dstack approach, while faster in some cases, can lead to bugs if you expect the cartesian product to be constructed in the same order for arrays of the same size.', '2015-07-27 18:35:12', 0);
INSERT INTO comment VALUES (9, NULL, 6, 'I haven''t noticed any case where this approach produces different results from those produced by meshgrid + dstack. Could you post an example?', '2017-07-16 22:26:26', 0);
INSERT INTO comment VALUES (10, 37, NULL, 'what you want to keep?', '2018-03-27 10:07:06', 0);
INSERT INTO comment VALUES (11, 37, NULL, 'Two problems: What is EmojiParser? Doesn''t seem to be part of a standard library, so this mention is not very helpful. And what characters exactly do you want to filter? You say "many more of this kind", but there are many character groups and families. We need to know more about your criteria', '2018-03-27 10:08:07', 0);
INSERT INTO comment VALUES (12, 37, NULL, 'Note that all of your symbols above are not emojis in the official list except ✂ black scissors 0x2702: ✪ circled white star 0x272A, ❉ balloon-spoked asterisk 0x2749, ★ black star 0x2605, ✰ shadowed white star 0x2730, ❈ heavy sparkle 0x2748, ❧ rotated floral heart bullet 0x2767, ❋ heavy eight teardrop-spoked propeller asterisk 0x274B, ⓡ circled latin small letter r 0x24E1, ✿ black florette 0x273F, ♛ black chess queen 0x265B', '2018-03-27 13:23:22', 0);
INSERT INTO comment VALUES (13, 37, NULL, 'IDK what your motivations behind this are, but if it''s too filter text input: don''t. I''m tired of being forced to use a-zA-Z. Let me write in my native language, or emojis, or whatever I want. Do I really want me calendar appointment to be called "🤦🏻‍♂️"? Yes, yes I do. Now get out of my way.', '2018-03-27 18:14:10', 0);
INSERT INTO comment VALUES (14, 37, NULL, 'Please clarify what exactly you want to keep and remove. On the surface the question appears to be clear but because of the complexity of Unicode it is not and because of that it''s impossible to provide a good answer.', '2018-03-27 18:16:47', 0);
INSERT INTO comment VALUES (15, NULL, 9, 'The obvious gap between ASCII alphanumeric characters and emoji is accentated and non-latin letters. Without the OP''s input on these we don''t know whether this is a good answer (not my DV though)', '2018-03-27 15:55:46', 0);
INSERT INTO comment VALUES (16, NULL, 9, 'Yeah I''m curious as to why this would possibly get downvoted. The second I saw this question, a regular expression was the absolute first thing that came to mind (P.S. since he''s looking for standard characters and punctuation, I''d use something like [^\w\^\-\[\]\.!@#$%&*\(\)/+''":;~?,] but that''s just me being robust and trying collect all typical characters that aren''t symbols). Upvoted because this is definitely a potential solution. If he wants to add some other language characters, he can add them to the expression as necessary.', '2018-03-27 16:05:20', 0);
INSERT INTO comment VALUES (17, NULL, 9, 'great punctuation regex example, looks extensive enough to me for some cases. Also maybe people aren''t reading the whole answer then - as stated at the bottom of the answer, p{L} handles non-English alphabetical characters. I hope it''s understood that I can''t list extensively through every non-English alphabet in my answer as that would be impractically verbose.', '2018-03-27 16:09:15', 0);
INSERT INTO comment VALUES (18, NULL, 10, 'Very useful list. Interesting that something called EmojiParser with a method called removeAllEmojis fails to handle these... :-)', '2018-03-27 10:20:05', 0);
INSERT INTO comment VALUES (19, NULL, 10, 'No, since input.codePointAt only looks at up to 2 characters at most which is a constant upper bound. Also (the newly added) i += Character.charCount(cp) skips over all characters that input.codePointAt inspected (minus 1 in some corner cases).', '2018-03-27 11:36:05', 0);
INSERT INTO comment VALUES (20, NULL, 10, 'String.chars() streams over characters not codepoints. There''s a separate method String.codePoints() for that.', '2018-03-27 11:37:21', 0);
INSERT INTO comment VALUES (21, NULL, 10, 'There are at least two problems here: you are using a "closed" list of emojis, so each year you have to extend it (but this probably isn''t easily solvabile), and this code won''t probably work correctly with codepoints sequences (see for example unicode.org/Public/emoji/11.0/emoji-zwj-sequences.txt)', '2018-03-27 11:43:36', 0);
INSERT INTO comment VALUES (22, NULL, 10, 'This is basically the same approach as used by EmojiParser and it will soon fail for the same reason. New emojis are relatively frequently added to the Unicode character database and if you are now implementing a solution using the currently defined 1644 emojis for a negative rule set, the implementation will fail as soon as new emojis become available.', '2018-03-27 12:04:50', 0);
INSERT INTO comment VALUES (23, NULL, 12, 'Please take a bow. The audience is cheering. Perfect, thanks.', '2018-03-27 07:07:08', 0);
INSERT INTO comment VALUES (24, NULL, 13, 'The first solution brings the advantage of working n keys. Nice!', '2018-03-27 09:54:58', 0);
INSERT INTO comment VALUES (25, 39, NULL, 'Why wouldn''t it be left-associative? You wouldn''t want monad >>= action1 >>= action2 being parsed as monad >>= (action1 >>= action2), would you?', '2018-03-24 21:44:46', 0);
INSERT INTO comment VALUES (26, 39, NULL, 'Also, the fixity of >> doesn''t theoretically matter, since it is associative by the monad laws.', '2018-03-24 21:45:46', 0);
INSERT INTO comment VALUES (27, 39, NULL, 'worth noting that the usual set of actions you''d want to bind is m a, a->m b, b->m c so the right-associated bind wouldn''t typecheck', '2018-03-24 21:50:05', 0);
INSERT INTO comment VALUES (28, 39, NULL, 'For >> it would often be better to associate the other way, but maybe this was chosen for consistency with >>=.', '2018-03-24 21:58:39', 0);
INSERT INTO comment VALUES (29, 39, NULL, 'It would feel weird if >>= and >> did not associate the same way.', '2018-03-24 22:03:47', 0);
INSERT INTO comment VALUES (30, NULL, 14, 'This is the key observation - you couldn''t chain both operators if it wasn''t infixl.', '2018-03-25 09:50:57', 0); 
INSERT INTO comment VALUES (31, NULL, 16, 'I think that sentence is ambiguous at best. The Merriam-Webster dictionary says that text is the original words and form of a written or printed work or a work containing such text. This source file clearly falls under that definition. Do you think I should file a defect report with the Core Language Working Group?', '2011-04-01 01:27:54', 0);
INSERT INTO comment VALUES (32, NULL, 19, 'While I don''t appreciate you making fun of my handwriting, this might be the real issue, and would explain the error I get when I try compiling the renamed helloworld.cpp with Visual C++: "fatal error C1004: unexpected end-of-file found" I''ll try again and report back soon. Thanks!', '2011-04-01 01:31:23', 0);

SELECT pg_catalog.setval('comment_id_seq', 32, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);

