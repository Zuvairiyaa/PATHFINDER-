import streamlit as st

st.set_page_config(page_title='PATHFINDER', page_icon='🧭', layout='wide')

CAREERS = {
    'Software Developer': {'interests': {'Coding', 'Problem Solving'}, 'skills': ['Python', 'Data Structures', 'SQL', 'Git']},
    'Data Analyst': {'interests': {'Data', 'Problem Solving'}, 'skills': ['Excel', 'SQL', 'Python', 'Data Visualization']},
    'Web Developer': {'interests': {'Design', 'Coding'}, 'skills': ['HTML', 'CSS', 'JavaScript', 'Git']},
    'AI/ML Engineer': {'interests': {'AI', 'Data', 'Coding'}, 'skills': ['Python', 'Math Basics', 'Pandas', 'Machine Learning Basics']},
}

st.title('🧭 PATHFINDER')
st.caption('From Confused to Career-Ready · Don’t know where to start? Start here.')

if 'career' not in st.session_state:
    st.session_state.career = None

with st.sidebar:
    st.header('Your Profile')
    name = st.text_input('Name', placeholder='Your name')
    department = st.selectbox('Department', ['CSE', 'IT', 'ECE', 'EEE', 'Mechanical', 'Civil', 'Other'])
    year = st.selectbox('Year', ['1', '2', '3', '4'])
    interests = set(st.multiselect('Your interests', ['Coding', 'Problem Solving', 'Data', 'Design', 'AI']))

st.subheader(f'Welcome{", " + name if name else ""}! 👋')
tab1, tab2, tab3 = st.tabs(['Discover Careers', 'My Roadmap', 'My Progress'])

with tab1:
    st.write('Select your interests in the sidebar to discover possible careers.')
    ranked = sorted(CAREERS.items(), key=lambda item: len(interests & item[1]['interests']), reverse=True)
    for career, details in ranked:
        matches = interests & details['interests']
        with st.container(border=True):
            st.markdown(f'**{career}**')
            st.write('Matched interests: ' + (', '.join(sorted(matches)) if matches else 'Explore to learn more'))
            if st.button('Choose this career', key=career):
                st.session_state.career = career
                st.success(f'{career} selected! Open My Roadmap.')

with tab2:
    career = st.session_state.career
    if not career:
        st.info('Choose a career in Discover Careers first.')
    else:
        st.subheader(f'Your {career} Roadmap')
        st.write('Build your foundations by learning these skills:')
        for skill in CAREERS[career]['skills']:
            st.checkbox(skill, key=f'{career}_{skill}')
        st.write('Next: build a mini project → create a portfolio → practice interviews.')

with tab3:
    career = st.session_state.career
    if not career:
        st.info('Choose a career to start tracking progress.')
    else:
        skills = CAREERS[career]['skills']
        completed = sum(bool(st.session_state.get(f'{career}_{skill}', False)) for skill in skills)
        percent = round(100 * completed / len(skills))
        st.metric('Foundation skills completed', f'{completed}/{len(skills)}')
        st.progress(percent / 100)
        st.write(f'Foundation progress: {percent}%')
        remaining = [skill for skill in skills if not st.session_state.get(f'{career}_{skill}', False)]
        st.info(f'Next focus: {remaining[0]}' if remaining else 'Great! Move on to your first project.')
        st.caption('This is a foundation-skills progress score, not a prediction of employment.')

st.divider()
st.caption('PATHFINDER prototype · Progress resets when the browser session ends. Persistent saving comes next.')
