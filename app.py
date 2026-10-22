import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title='PATHFINDER | Engineering Career OS',page_icon='🧭',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');html,body,[class*="css"],.stApp{font-family:Inter,sans-serif} .stApp{background:#0a1020;color:#edf2ff}section[data-testid="stSidebar"]{background:#101a30;border-right:1px solid #283552}h1,h2,h3{letter-spacing:-.035em}h1{font-weight:800!important}div[data-testid="stMetric"]{background:#16223b;border:1px solid #2b3b5b;border-radius:16px;padding:18px}div.stButton>button[kind="primary"]{background:linear-gradient(90deg,#7c5cff,#4979f5);border:0;color:white}div[data-testid="stExpander"]{border:1px solid #2d3b58;border-radius:12px;background:#121d33}.stProgress>div>div>div{background:#8c7bff}.eyebrow{color:#9daeff;font-size:12px;letter-spacing:.14em;font-weight:800}.muted{color:#aebcda}.hero{background:linear-gradient(120deg,#1b2350,#142c47);padding:27px;border:1px solid #3b4a78;border-radius:20px;margin-bottom:22px}.chip{display:inline-block;border-radius:99px;background:#263659;color:#c5d3ff;padding:5px 11px;margin:3px;font-size:12px}</style>''',unsafe_allow_html=True)

# Each micro-lesson contains an explanation, a real example, a task and an assessment.
LESSONS={
'Programming Foundations':[
('Variables and types','A variable binds a name to a value. In Python, types are determined at runtime. Integers store whole numbers; floats store decimals; strings store text; booleans store True/False.','age = 18\nscore = 82.5\nname = "Asha"\nprint(type(score).__name__)','Write a program that reads a student name and three marks, then prints their average.','What is the type of 82.5 in Python?',['int','float','str'],'float','A decimal numeric literal is represented as a float.'),
('Conditions and comparisons','Use if, elif and else to branch based on boolean expressions. Comparison operators include ==, !=, <, >, <= and >=. Indentation defines each block.','marks = 74\nif marks >= 50:\n    print("Pass")\nelse:\n    print("Retry")','Build a grade classifier with explicit boundaries for A, B, C and fail.','Which operator compares two values for equality?',['=','==','!='],'==','A single = assigns; == compares.'),
('Loops and iteration','A for loop iterates over a sequence; while repeats until its condition becomes false. Use break to stop early and continue to skip an iteration.','total = 0\nfor n in range(1, 6):\n    total += n\nprint(total)','Compute the sum of even numbers from 1 to 100.','How many iterations does range(1, 4) produce?',['2','3','4'],'3','It produces 1, 2 and 3; the stop value is excluded.'),
('Functions and parameters','Functions package reusable logic. Parameters receive inputs; return sends results to the caller. Keep each function focused on one responsibility.','def square(n):\n    return n * n\nprint(square(5))','Write a function that checks whether a number is prime.','Which keyword sends a value back to the caller?',['print','return','yield'],'return','return ends a function and provides its result.'),
('Collections','Lists are ordered and mutable; tuples are ordered and immutable; sets store unique items; dictionaries map keys to values. Choose a structure based on access patterns.','marks = {"Asha": 92, "Ravi": 81}\nprint(marks.get("Asha"))','Count word frequencies in a sentence using a dictionary.','Which collection stores key-value pairs?',['list','dict','set'],'dict','Dictionaries map unique keys to values.'),
('Debugging and testing','Reproduce a bug, inspect inputs, isolate the cause, fix it, then retest. Unit tests compare actual output against expected behavior, including edge cases.','def add(a,b): return a+b\nassert add(2,3)==5\nassert add(0,0)==0','Create three tests for a function that finds the maximum in a list, including an empty list.','What is an edge case?',['Only the typical input','An unusual boundary input','A syntax error'],'An unusual boundary input','Boundary cases often reveal missing logic.')],
'Data Structures & Algorithms':[
('Time complexity','Big-O describes how running time grows with input size. O(1) is constant, O(n) is linear, O(n log n) often appears in efficient sorting, and O(n²) can result from nested scans.','for item in items:\n    print(item)  # O(n)','Compare linear search and binary search on a sorted list of 1000 values.','A single loop over n items is typically…',['O(1)','O(n)','O(n²)'],'O(n)','One pass scales linearly with input length.'),
('Arrays and strings','Array-like sequences support indexed access. Common tasks include traversal, counting, two pointers, sliding windows and substring operations.','values = [3, 8, 2]\nprint(values[1])','Find the second-largest distinct value in a list without sorting.','What is the first index of a Python list?',['0','1','-1'],'0','Python sequences use zero-based indexing.'),
('Stacks and queues','A stack follows last-in-first-out; a queue follows first-in-first-out. Stacks help with undo and bracket matching; queues help with task scheduling and breadth-first search.','stack = []\nstack.append("A")\nstack.append("B")\nprint(stack.pop())','Implement a balanced-parentheses checker with a stack.','Which principle describes a queue?',['LIFO','FIFO','Random'],'FIFO','The earliest enqueued item leaves first.'),
('Searching and sorting','Binary search halves a sorted search space. Merge sort uses divide-and-conquer and runs in O(n log n); selection sort is generally O(n²).','nums = sorted([5,1,3])\nprint(nums)','Implement binary search and test a missing target.','Binary search requires data to be…',['sorted','unique','reversed'],'sorted','Ordering lets the algorithm discard half of the search space.'),
('Recursion','A recursive function solves a smaller instance of the same problem. Every recursion needs a base case to terminate. Consider call-stack depth and repeated work.','def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)','Write recursive and iterative Fibonacci solutions and compare their work.','What stops infinite recursion?',['A loop','A base case','A list'],'A base case','The base case ends the recursive calls.')],
'Databases & SQL':[
('Relational modeling','Tables hold rows and columns. Primary keys uniquely identify records; foreign keys connect related tables. Normalization reduces unnecessary duplication.','CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL);','Design student, course and enrollment tables with correct relationships.','What uniquely identifies a table row?',['Foreign key','Primary key','Index name'],'Primary key','A primary key is unique and non-null.'),
('SELECT and filtering','SELECT chooses columns; WHERE filters rows; ORDER BY sorts results; LIMIT restricts output. Use parameterized queries rather than concatenating user input.','SELECT name FROM students WHERE year = 1 ORDER BY name;','Write a query to show second-year students sorted by name.','Which SQL clause filters rows?',['WHERE','ORDER BY','GROUP BY'],'WHERE','WHERE applies row-level conditions.'),
('Joins and aggregation','JOIN combines related rows; GROUP BY creates groups; aggregate functions such as COUNT, AVG and SUM summarize each group.','SELECT dept, COUNT(*) FROM students GROUP BY dept;','List each department and its average student score.','Which function counts rows?',['SUM','COUNT','AVG'],'COUNT','COUNT returns the number of qualifying rows.')],
'Git & Professional Workflow':[
('Git fundamentals','Git records versions of files. A commit captures a snapshot; branches isolate work; merging combines changes. Write meaningful commit messages.','git status\ngit add app.py\ngit commit -m "Add student profile"','Create a branch for a feature and make a focused commit.','What does git commit create?',['A snapshot','A website','A database'],'A snapshot','A commit records tracked changes in repository history.'),
('Pull requests and reviews','A pull request proposes merging a branch. Reviewers check behavior, readability, tests, security and documentation before merging.','git checkout -b feature/quiz\ngit push -u origin feature/quiz','Draft a pull-request description listing purpose, tests and screenshots.','Why use a pull request?',['To review changes','To delete history','To install Python'],'To review changes','Pull requests enable collaboration and quality checks.')],
'Web Engineering':[
('HTML semantics','HTML provides document structure. Semantic tags like header, main, nav, article and button improve accessibility and maintainability.','<main><h1>Career Dashboard</h1><button>Explore</button></main>','Build an accessible profile form with labeled inputs.','Which HTML element is intended for a clickable action?',['div','button','span'],'button','button supports keyboard and assistive technology semantics.'),
('CSS responsive design','Responsive layouts adapt to screen widths. Flexbox handles one-dimensional layout; CSS Grid handles two-dimensional layouts; media queries refine smaller screens.','.cards {display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;}','Design a two-column dashboard that becomes one column on mobile.','Which CSS property creates a grid container?',['display:grid','position:grid','layout:grid'],'display:grid','CSS Grid is enabled with display:grid.'),
('HTTP and APIs','Clients send HTTP requests; servers return status codes and data. GET retrieves, POST creates or submits, PUT replaces and DELETE removes resources.','GET /api/careers\n200 OK\n[{"name":"Developer"}]','Sketch API endpoints for student profiles, progress and assessments.','Which HTTP method commonly retrieves data?',['GET','DELETE','PATCH'],'GET','GET is used for retrieving resources.')],
'AI & Data Foundations':[
('Python data analysis','Pandas DataFrames organize tabular data. Check missing values, types, distributions and duplicates before drawing conclusions.','import pandas as pd\ndf = pd.DataFrame({"score":[72,85,90]})\nprint(df["score"].mean())','Load a small CSV and report missing values and mean score.','What is a DataFrame?',['A table-like structure','A neural network','A Python loop'],'A table-like structure','DataFrames represent labeled rows and columns.'),
('Statistics essentials','Mean describes average, median describes the middle observation, and standard deviation measures spread. Outliers can distort the mean.','scores = [50, 60, 70]\nmean = sum(scores)/len(scores)','Compare mean and median for salaries with one very large outlier.','Which measure is less affected by extreme outliers?',['Mean','Median','Sum'],'Median','The median depends on the ordered middle position.'),
('Machine learning workflow','Define a target, split train and test sets, preprocess using training data only, fit a baseline, and evaluate on held-out examples to reduce leakage.','# Workflow: split -> preprocess -> train -> evaluate','Plan a classifier for spam messages and identify possible data leakage.','Why reserve test data?',['To evaluate generalization','To increase training size','To skip preprocessing'],'To evaluate generalization','Held-out data approximates unseen examples.'),
('Model evaluation','Accuracy can be misleading for imbalanced classes. Precision describes positive-prediction quality; recall describes coverage of actual positives. Use a confusion matrix.','precision = tp/(tp+fp) if tp+fp else 0','For a medical screening toy example, explain why recall might matter.','Which metric measures captured actual positives?',['Recall','Precision','MAE'],'Recall','Recall = TP/(TP+FN).')],
'Networks & Security':[
('Network basics','IP addresses identify interfaces; DNS resolves names; TCP provides reliable ordered transport; HTTPS protects web traffic using TLS.','https://example.org  # DNS -> TCP/TLS -> HTTP','Draw the stages of opening a secure website in a browser.','What translates a domain name into an IP address?',['DNS','HTML','SQL'],'DNS','DNS resolves domain names.'),
('Security hygiene','Validate inputs, hash passwords using established password-hashing libraries, protect secrets, use least privilege and avoid storing credentials in source code.','# Keep secrets in environment variables, not Git.','List security checks for a student login form.','Where should API secrets NOT be stored?',['Environment variables','Public source code','Secret manager'],'Public source code','Public code can expose credentials.')]
}
TRACKS={
'CSE':['Programming Foundations','Data Structures & Algorithms','Databases & SQL','Git & Professional Workflow','Web Engineering','Networks & Security'],
'IT':['Programming Foundations','Networks & Security','Databases & SQL','Web Engineering','Git & Professional Workflow','Data Structures & Algorithms'],
'AI&DS':['Programming Foundations','AI & Data Foundations','Databases & SQL','Data Structures & Algorithms','Git & Professional Workflow','Networks & Security']}
CAREERS={'Software Engineer':['Programming Foundations','Data Structures & Algorithms','Databases & SQL','Git & Professional Workflow'], 'Full-Stack Developer':['Programming Foundations','Web Engineering','Databases & SQL','Git & Professional Workflow'], 'Data Analyst':['Programming Foundations','AI & Data Foundations','Databases & SQL'], 'ML Engineer':['Programming Foundations','AI & Data Foundations','Data Structures & Algorithms','Git & Professional Workflow'], 'Cloud / IT Engineer':['Networks & Security','Git & Professional Workflow','Databases & SQL']}

if 'passed' not in st.session_state: st.session_state.passed={}
if 'attempts' not in st.session_state: st.session_state.attempts={}
if 'profile' not in st.session_state: st.session_state.profile={'name':'Student','department':'CSE','year':'1st Year','career':'Software Engineer'}
if 'page' not in st.session_state: st.session_state.page='Overview'
profile=st.session_state.profile
with st.sidebar:
    st.markdown('## 🧭 PATHFINDER')
    st.caption('ENGINEERING CAREER OS  ·  BETA')
    st.divider()
    st.session_state.page=st.radio('WORKSPACE',['Overview','Skill Academy','Career Roadmap','Assessments','Progress & Backup'],index=['Overview','Skill Academy','Career Roadmap','Assessments','Progress & Backup'].index(st.session_state.page))
    st.divider()
    st.caption('YOUR PROFILE')
    profile['name']=st.text_input('Name',profile['name'],max_chars=60)
    profile['department']=st.selectbox('Department',list(TRACKS),index=list(TRACKS).index(profile['department']))
    profile['year']=st.selectbox('Study year',['1st Year','2nd Year','3rd Year','4th Year'],index=['1st Year','2nd Year','3rd Year','4th Year'].index(profile['year']))
    profile['career']=st.selectbox('Career goal',list(CAREERS),index=list(CAREERS).index(profile['career']))
    st.caption('Progress is stored in this browser session. Export a backup to keep it.')

relevant=CAREERS[profile['career']]
all_keys=[f'{module}::{lesson[0]}' for module in relevant for lesson in LESSONS[module]]
completed=sum(st.session_state.passed.get(k,False) for k in all_keys)
score=round(completed/len(all_keys)*100) if all_keys else 0

if st.session_state.page=='Overview':
    st.markdown(f'''<div class="hero"><div class="eyebrow">YOUR ENGINEERING JOURNEY</div><h1>Welcome back, {profile['name'].replace('<','&lt;').replace('>','&gt;')} 👋</h1><p class="muted">A clear route from foundational knowledge to practical engineering confidence.</p><span class="chip">{profile['department']}</span><span class="chip">{profile['year']}</span><span class="chip">{profile['career']}</span></div>''',unsafe_allow_html=True)
    a,b,c=st.columns(3);a.metric('Knowledge checks passed',completed);b.metric('Required micro-lessons',len(all_keys));c.metric('Assessment coverage',f'{score}%')
    st.progress(score/100)
    st.caption('Coverage measures passed knowledge checks only; it is not a hiring prediction or certification.')
    st.subheader('Your next learning action')
    pending=[k for k in all_keys if not st.session_state.passed.get(k)]
    if pending: st.info(f'📌 Study **{pending[0].split("::")[1]}** in **{pending[0].split("::")[0]}**, then take its knowledge check.')
    else: st.success('All current checks passed! Extend your learning with projects and external practice.')
    st.subheader('Career-aligned skill areas')
    for module in relevant:
        keys=[f'{module}::{l[0]}' for l in LESSONS[module]]
        count=sum(st.session_state.passed.get(k,False) for k in keys)
        st.write(f'**{module}** · {count}/{len(keys)} checks passed');st.progress(count/len(keys))
    st.caption('This starter curriculum is a foundation, not an exhaustive university syllabus.')
elif st.session_state.page=='Skill Academy':
    st.title('Skill Academy');st.caption('Learn → apply → check understanding. Open any lesson for its detailed content.')
    module=st.selectbox('Choose a skill area',TRACKS[profile['department']])
    for i,(name,explanation,example,task,question,choices,answer,feedback) in enumerate(LESSONS[module],1):
        key=f'{module}::{name}'
        with st.expander(f'{"✅" if st.session_state.passed.get(key) else "📖"} {i:02d} · {name}',expanded=i==1):
            st.markdown('**Concept explained**');st.write(explanation)
            st.markdown('**Worked example**');st.code(example,language='python' if not example.startswith('<') and not example.startswith('GET ') and not example.startswith('CREATE ') and not example.startswith('SELECT ') and not example.startswith('.') else 'text')
            st.markdown('**Practical challenge**');st.info(task)
            st.markdown('**Knowledge check**');st.write(question)
            choice=st.radio('Choose your answer',choices,key=f'answer_{key}',index=None)
            if st.button('Check answer',key=f'check_{key}',type='primary'):
                if choice is None: st.warning('Choose an answer first.')
                else:
                    st.session_state.attempts[key]=st.session_state.attempts.get(key,0)+1
                    if choice==answer: st.session_state.passed[key]=True;st.success('Correct! '+feedback)
                    else: st.error('Not quite. Review the explanation and try again.')
            if st.session_state.passed.get(key): st.success('Knowledge check passed. Practical challenge is self-guided, not automatically verified.')
elif st.session_state.page=='Career Roadmap':
    st.title('Your Career Roadmap');st.caption(f'Goal: {profile["career"]} · tailored by your chosen goal and department')
    stages=['Foundation','Build core knowledge','Apply through projects','Prepare for opportunities']
    for i,stage in enumerate(stages):
        with st.container(border=True):
            st.subheader(f'0{i+1}  {stage}')
            if i==0: st.write('Master basic programming, debugging and problem-solving habits.')
            elif i==1: st.write('Work through your career-aligned modules below, passing checks and practicing each challenge.')
            elif i==2: st.write('Build a small original project, document its design decisions, test it and publish a GitHub README.')
            else: st.write('Prepare a truthful resume, practice explaining your project, review technical fundamentals and apply through verified sources.')
            if i==1:
                for module in relevant: st.markdown(f'- {module}')
    st.info('Roadmap stages are recommendations. Internship and placement opportunities are not guaranteed.')
elif st.session_state.page=='Assessments':
    st.title('Knowledge Check Center');st.caption('Assessments are short recall questions, not comprehensive competency exams.')
    module=st.selectbox('Assess module',relevant)
    for lesson in LESSONS[module]:
        name,explanation,example,task,question,choices,answer,feedback=lesson
        key=f'{module}::{name}'
        with st.expander(f'{"✅" if st.session_state.passed.get(key) else "◯"} {name}'):
            st.write(question)
            chosen=st.radio('Answer',choices,index=None,key=f'exam_{key}')
            if st.button('Submit answer',key=f'submit_{key}'):
                if chosen is None: st.warning('Select an answer.')
                elif chosen==answer: st.session_state.passed[key]=True;st.success('Correct. '+feedback)
                else: st.error('Incorrect. Read the corresponding Skill Academy lesson and retry.')
    st.caption('Correct answers count once per micro-lesson, even if the check is repeated.')
else:
    st.title('Progress & Backup');st.metric('Passed checks for career goal',f'{completed} / {len(all_keys)}')
    st.progress(score/100)
    st.subheader('Download progress')
    payload={'format':'pathfinder-progress-v1','exported_at':datetime.now().isoformat(timespec='seconds'),'profile':profile,'passed':st.session_state.passed,'attempts':st.session_state.attempts}
    st.download_button('⬇️ Download JSON backup',json.dumps(payload,indent=2),file_name='pathfinder_progress.json',mime='application/json')
    st.subheader('Restore progress')
    uploaded=st.file_uploader('Upload a previously downloaded PATHFINDER JSON backup',type='json')
    if uploaded and st.button('Restore this backup'):
        try:
            data=json.load(uploaded)
            if data.get('format')!='pathfinder-progress-v1' or not isinstance(data.get('passed'),dict): raise ValueError('Not a supported PATHFINDER backup')
            p=data.get('profile',{})
            if p.get('department') not in TRACKS or p.get('career') not in CAREERS or p.get('year') not in ['1st Year','2nd Year','3rd Year','4th Year']: raise ValueError('Invalid profile')
            st.session_state.profile={'name':str(p.get('name','Student'))[:60], 'department':p['department'],'career':p['career'],'year':p['year']}
            valid={f'{m}::{l[0]}' for m in LESSONS for l in LESSONS[m]}
            st.session_state.passed={k:bool(v) for k,v in data['passed'].items() if k in valid}
            st.session_state.attempts={k:int(v) for k,v in data.get('attempts',{}).items() if k in valid and isinstance(v,int) and 0<=v<=100000}
            st.success('Backup restored.');st.rerun()
        except (ValueError,TypeError,KeyError,AttributeError,json.JSONDecodeError) as e: st.error(f'Could not restore backup: {e}')
    st.warning('Streamlit Community Cloud may restart or clear sessions. Save your backup regularly; this version does not have user accounts or permanent cloud storage.')
