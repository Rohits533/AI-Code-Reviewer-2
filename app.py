
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rohit Savan | AI Developer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #0f1117; color: #ffffff; overflow-x: hidden; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0f1117; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(#00d4ff, #7b2ff7); border-radius: 3px; }
        nav { position: fixed; top: 0; width: 100%; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; background: rgba(15, 17, 23, 0.85); backdrop-filter: blur(20px); z-index: 1000; border-bottom: 1px solid rgba(0, 212, 255, 0.1); }
        .logo { font-size: 22px; font-weight: 700; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .nav-links a { color: #888; text-decoration: none; margin-left: 30px; font-size: 14px; transition: color 0.3s; position: relative; }
        .nav-links a::after { content: ''; position: absolute; bottom: -4px; left: 0; width: 0; height: 2px; background: linear-gradient(90deg, #00d4ff, #7b2ff7); transition: width 0.3s; }
        .nav-links a:hover { color: #00d4ff; }
        .nav-links a:hover::after { width: 100%; }
        #particles-canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; }
        .hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 100px 20px 60px; position: relative; z-index: 1; }
        .hero-badge { background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 50px; padding: 8px 20px; font-size: 13px; color: #00d4ff; margin-bottom: 24px; animation: fadeInDown 0.8s ease; }
        .hero h1 { font-size: clamp(40px, 8vw, 80px); font-weight: 800; line-height: 1.1; margin-bottom: 20px; animation: fadeInDown 1s ease; }
        .gradient-text { background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .typing-text::after { content: '|'; animation: blink 0.7s infinite; color: #00d4ff; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
        .hero p { font-size: 18px; color: #888; max-width: 600px; line-height: 1.7; margin-bottom: 40px; animation: fadeInUp 1s ease; }
        .hero-buttons { display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; animation: fadeInUp 1.2s ease; }
        .btn-primary { background: linear-gradient(90deg, #00d4ff, #7b2ff7); color: white; padding: 14px 32px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 15px; transition: transform 0.3s, box-shadow 0.3s; position: relative; overflow: hidden; z-index: 2; }
        .btn-primary::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); transition: left 0.5s; }
        .btn-primary:hover::before { left: 100%; }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4); }
        .btn-secondary { background: transparent; color: #00d4ff; padding: 14px 32px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 15px; border: 1px solid rgba(0, 212, 255, 0.4); transition: all 0.3s; z-index: 2; }
        .btn-secondary:hover { background: rgba(0, 212, 255, 0.1); transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2); }
        .stats { display: flex; gap: 40px; justify-content: center; flex-wrap: wrap; margin-top: 60px; animation: fadeInUp 1.4s ease; }
        .stat { text-align: center; }
        .stat-number { font-size: 36px; font-weight: 800; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stat-label { font-size: 13px; color: #888; margin-top: 4px; }
        .reveal { opacity: 0; transform: translateY(40px); transition: all 0.8s ease; }
        .reveal.active { opacity: 1; transform: translateY(0); }
        section { padding: 80px 20px; max-width: 1100px; margin: 0 auto; position: relative; z-index: 1; }
        .section-title { font-size: 36px; font-weight: 700; text-align: center; margin-bottom: 12px; }
        .section-subtitle { color: #888; text-align: center; font-size: 16px; margin-bottom: 50px; }
        .skills-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; }
        .skill-card { background: linear-gradient(135deg, #1e1e2e, #2a2a3e); border-radius: 16px; padding: 20px; text-align: center; border: 1px solid rgba(0, 212, 255, 0.1); transition: all 0.3s; cursor: default; }
        .skill-card:hover { border-color: rgba(0, 212, 255, 0.6); transform: translateY(-8px) scale(1.05); box-shadow: 0 15px 40px rgba(0, 212, 255, 0.15); background: linear-gradient(135deg, #2a2a3e, #3a2a4e); }
        .skill-icon { font-size: 32px; margin-bottom: 10px; transition: transform 0.3s; }
        .skill-card:hover .skill-icon { transform: scale(1.2); }
        .skill-name { font-size: 13px; font-weight: 500; color: #cdd6f4; }
        .projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; }
        .project-card { background: linear-gradient(135deg, #1e1e2e, #2a2a3e); border-radius: 20px; padding: 28px; border: 1px solid rgba(0, 212, 255, 0.1); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; z-index: 2; overflow: hidden; }
        .project-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #00d4ff, #7b2ff7); transform: scaleX(0); transition: transform 0.4s ease; }
        .project-card::after { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at 50% 0%, rgba(0, 212, 255, 0.05) 0%, transparent 60%); opacity: 0; transition: opacity 0.4s; pointer-events: none; }
        .project-card:hover::before { transform: scaleX(1); }
        .project-card:hover::after { opacity: 1; }
        .project-card:hover { border-color: rgba(0, 212, 255, 0.4); transform: translateY(-10px); box-shadow: 0 25px 50px rgba(0, 212, 255, 0.15); }
        .project-icon { font-size: 40px; margin-bottom: 16px; display: inline-block; transition: transform 0.3s; }
        .project-card:hover .project-icon { transform: scale(1.2) rotate(5deg); }
        .project-title { font-size: 20px; font-weight: 700; margin-bottom: 10px; color: #ffffff; }
        .project-desc { font-size: 14px; color: #888; line-height: 1.7; margin-bottom: 20px; }
        .project-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
        .tag { background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 20px; padding: 4px 12px; font-size: 12px; color: #00d4ff; transition: all 0.3s; }
        .tag:hover { background: rgba(0, 212, 255, 0.2); border-color: #00d4ff; }
        .project-link { display: inline-flex; align-items: center; gap: 8px; color: #00d4ff; text-decoration: none; font-size: 14px; font-weight: 600; transition: gap 0.3s; position: relative; z-index: 10; }
        .project-link:hover { gap: 14px; }
        .about-content { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
        .about-text h2 { font-size: 32px; font-weight: 700; margin-bottom: 20px; }
        .about-text p { color: #888; line-height: 1.8; margin-bottom: 16px; font-size: 15px; }
        .about-highlights { display: flex; flex-direction: column; gap: 16px; }
        .highlight { background: linear-gradient(135deg, #1e1e2e, #2a2a3e); border-radius: 12px; padding: 16px 20px; border-left: 3px solid #00d4ff; font-size: 14px; color: #cdd6f4; transition: all 0.3s; }
        .highlight:hover { transform: translateX(8px); border-left-color: #7b2ff7; box-shadow: -4px 0 20px rgba(123, 47, 247, 0.2); }
        .contact-section { text-align: center; padding: 80px 20px; background: linear-gradient(135deg, #1a1a2e, #16213e); position: relative; z-index: 1; }
        .contact-links { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 40px; }
        .contact-link { background: linear-gradient(135deg, #1e1e2e, #2a2a3e); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 16px; padding: 20px 30px; text-decoration: none; color: #ffffff; font-size: 15px; font-weight: 500; transition: all 0.3s; display: flex; align-items: center; gap: 10px; position: relative; z-index: 2; }
        .contact-link:hover { border-color: #00d4ff; transform: translateY(-8px); box-shadow: 0 15px 40px rgba(0, 212, 255, 0.25); background: linear-gradient(135deg, #2a2a3e, #3a2a4e); }
        footer { text-align: center; padding: 30px; color: #444; font-size: 13px; border-top: 1px solid rgba(255,255,255,0.05); position: relative; z-index: 1; }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @media (max-width: 768px) { nav { padding: 16px 20px; } .nav-links { display: none; } .about-content { grid-template-columns: 1fr; gap: 30px; } .projects-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>

<canvas id="particles-canvas"></canvas>

<nav>
    <div class="logo">Rohit Savan</div>
    <div class="nav-links">
        <a href="#projects">Projects</a>
        <a href="#skills">Skills</a>
        <a href="#about">About</a>
        <a href="#contact">Contact</a>
    </div>
</nav>

<div class="hero">
    <div class="hero-badge">🚀 AI Developer & BTech AIML Student</div>
    <h1>Building the Future<br>with <span class="gradient-text typing-text" id="typing"></span></h1>
    <p>17 year old AI developer from Mumbai. I build and deploy real AI applications using Python, LangChain, and Groq. <strong>15 live projects and counting.</strong></p>
    <div class="hero-buttons">
        <a href="#projects" class="btn-primary">View My Projects →</a>
        <a href="#contact" class="btn-secondary">Get In Touch</a>
    </div>
    <div class="stats">
        <div class="stat"><div class="stat-number" data-target="15">0</div><div class="stat-label">Live Projects</div></div>
        <div class="stat"><div class="stat-number" data-target="8">0</div><div class="stat-label">Libraries Mastered</div></div>
        <div class="stat"><div class="stat-number" data-target="17">0</div><div class="stat-label">Years Old</div></div>
        <div class="stat"><div class="stat-number" data-target="100">0</div><div class="stat-label">% Self Taught</div></div>
    </div>
</div>

<section id="projects">
    <h2 class="section-title reveal">🚀 My <span class="gradient-text">Projects</span></h2>
    <p class="section-subtitle reveal">15 deployed AI applications built from scratch</p>
    <div class="projects-grid">

        <div class="project-card reveal">
            <div class="project-icon">🤖</div>
            <div class="project-title">AI Assistant Platform</div>
            <div class="project-desc">Multi-feature AI platform with chatbot, web search agent, code explainer, quiz generator and PDF reader.</div>
            <div class="project-tags"><span class="tag">LangChain</span><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">RAG</span></div>
            <a href="https://rohit-ai-chatbot-2026.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">📄</div>
            <div class="project-title">AI Resume Builder</div>
            <div class="project-desc">Fill in your details and AI generates a professional ATS-friendly resume with PDF download.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">ReportLab</span><span class="tag">PDF</span></div>
            <a href="https://rohit-resume-builder.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">📰</div>
            <div class="project-title">AI News Summarizer</div>
            <div class="project-desc">Enter any topic and AI searches the web for latest news and summarizes top stories in real time.</div>
            <div class="project-tags"><span class="tag">LangChain</span><span class="tag">DuckDuckGo</span><span class="tag">Streamlit</span><span class="tag">Web Search</span></div>
            <a href="https://rohit-news-summarizer.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">🃏</div>
            <div class="project-title">AI Flashcard Generator</div>
            <div class="project-desc">Enter any topic and AI generates interactive flashcards with reveal animations for exam preparation.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">JSON</span><span class="tag">Animations</span></div>
            <a href="https://rohit-flashcards.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">🎯</div>
            <div class="project-title">AI Interview Coach</div>
            <div class="project-desc">Practice interviews with AI. Get asked questions, submit answers and receive instant feedback with scores.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">Session State</span><span class="tag">PDF</span></div>
            <a href="https://rohit-interview-coach.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">⭐</div>
            <div class="project-title">AI Code Reviewer</div>
            <div class="project-desc">Paste any code and get a professional senior developer review with bugs, security issues and improvements.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">ReportLab</span><span class="tag">Multi-language</span></div>
            <a href="https://rohit-code-reviewer.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">🌍</div>
            <div class="project-title">AI Translator</div>
            <div class="project-desc">Translate any text into 20+ languages including Indian languages with pronunciation guides and cultural notes.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">20+ Languages</span><span class="tag">PDF</span></div>
            <a href="https://rohit-translator.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">📖</div>
            <div class="project-title">AI Story Generator</div>
            <div class="project-desc">Enter a genre, character and plot idea — AI writes a creative story with real-time streaming output word by word.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">Streaming</span><span class="tag">ReportLab</span></div>
            <a href="https://rohit-story-generator.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">📧</div>
            <div class="project-title">AI Email Generator</div>
            <div class="project-desc">Generate professional emails instantly. Select email type, tone and context — AI writes a perfect email with streaming output.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">Streaming</span><span class="tag">9 Email Types</span></div>
            <a href="https://rohit-email-generator.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">📅</div>
            <div class="project-title">AI Study Planner</div>
            <div class="project-desc">Enter your exam date and subjects — AI creates a personalized day by day study schedule with streaming output.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">Streaming</span><span class="tag">PDF</span></div>
            <a href="https://rohit-study-planner.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">🔍</div>
            <div class="project-title">AI Image Analyzer</div>
            <div class="project-desc">Upload any image and AI analyzes it in detail — objects, colors, emotions, text extraction and more using multimodal AI.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">Llama 4 Vision</span><span class="tag">Multimodal</span><span class="tag">Streamlit</span></div>
            <a href="https://rohit-image-analyzer.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">📊</div>
            <div class="project-title">AI Data Analyzer</div>
            <div class="project-desc">Upload any CSV dataset — AI analyzes, visualizes with charts, builds ML models automatically and answers questions about your data.</div>
            <div class="project-tags"><span class="tag">Scikit-learn</span><span class="tag">Pandas</span><span class="tag">NumPy</span><span class="tag">Matplotlib</span></div>
            <a href="https://rohit-data-analyzer.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">🎓</div>
            <div class="project-title">AI Student Performance Predictor</div>
            <div class="project-desc">Enter study hours, attendance and marks — real ML model predicts your final grade with personalized AI study advice.</div>
            <div class="project-tags"><span class="tag">Scikit-learn</span><span class="tag">RandomForest</span><span class="tag">Groq</span><span class="tag">Matplotlib</span></div>
            <a href="https://rohit-student-predictor.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <div class="project-card reveal">
            <div class="project-icon">💼</div>
            <div class="project-title">AI Career Coach</div>
            <div class="project-desc">Upload resume and paste job description — AI analyzes match score, identifies skill gaps, generates cover letters and tracks applications.</div>
            <div class="project-tags"><span class="tag">Groq</span><span class="tag">SQLite</span><span class="tag">PyPDF2</span><span class="tag">Free Jobscan</span></div>
            <a href="https://rohit-career-coach.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

        <!-- ============================================================ -->
        <!-- 15. AI Code Reviewer & Debugger (NEW)                         -->
        <!-- ============================================================ -->
        <div class="project-card reveal">
            <div class="project-icon">🧠</div>
            <div class="project-title">AI Code Reviewer & Debugger</div>
            <div class="project-desc">Paste any Python code and get a professional senior developer review with static analysis (AST) + AI-powered bug detection, severity ratings, and suggested fixes.</div>
            <div class="project-tags"><span class="tag">AST</span><span class="tag">Groq</span><span class="tag">Streamlit</span><span class="tag">Static Analysis</span><span class="tag">Python</span></div>
            <a href="https://ai-code-reviewer-2.streamlit.app" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo →</a>
        </div>

    </div>
</section>

<section id="skills" style="background: linear-gradient(135deg, #1a1a2e, #0f1117); padding: 80px 20px; max-width: 100%;">
    <div style="max-width: 1100px; margin: 0 auto;">
        <h2 class="section-title reveal">🛠️ My <span class="gradient-text">Skills</span></h2>
        <p class="section-subtitle reveal">Technologies I use to build AI applications</p>
        <div class="skills-grid">
            <div class="skill-card reveal"><div class="skill-icon">🐍</div><div class="skill-name">Python</div></div>
            <div class="skill-card reveal"><div class="skill-icon">🤖</div><div class="skill-name">LangChain</div></div>
            <div class="skill-card reveal"><div class="skill-icon">⚡</div><div class="skill-name">Groq API</div></div>
            <div class="skill-card reveal"><div class="skill-icon">🎨</div><div class="skill-name">Streamlit</div></div>
            <div class="skill-card reveal"><div class="skill-icon">🔢</div><div class="skill-name">NumPy</div></div>
            <div class="skill-card reveal"><div class="skill-icon">🐼</div><div class="skill-name">Pandas</div></div>
            <div class="skill-card reveal"><div class="skill-icon">📊</div><div class="skill-name">Matplotlib</div></div>
            <div class="skill-card reveal"><div class="skill-icon">🧪</div><div class="skill-name">Scikit-learn</div></div>
            <div class="skill-card reveal"><div class="skill-icon">🐙</div><div class="skill-name">GitHub</div></div>
            <div class="skill-card reveal"><div class="skill-icon">☁️</div><div class="skill-name">Deployment</div></div>
            <div class="skill-card reveal"><div class="skill-icon">🧠</div><div class="skill-name">Prompt Engineering</div></div>
            <div class="skill-card reveal"><div class="skill-icon">🗄️</div><div class="skill-name">SQL & SQLite</div></div>
        </div>
    </div>
</section>

<section id="about">
    <div class="about-content">
        <div class="about-text reveal">
            <h2>About <span class="gradient-text">Me</span></h2>
            <p>I'm Rohit Savan, a 17 year old AI developer from Mumbai, India. I'm passionate about building practical AI applications that solve real problems.</p>
            <p>I started learning AI development from scratch and built 15 deployed applications in a short time. I'm about to start my BTech in AI & ML and I'm already ahead of the curve.</p>
            <p>I believe in learning by building — every project teaches me something new and adds real value to my portfolio.</p>
        </div>
        <div class="about-highlights reveal">
            <div class="highlight">🎓 Incoming BTech AIML Student</div>
            <div class="highlight">🚀 15 Live Deployed AI Applications</div>
            <div class="highlight">🌍 Based in Mumbai, India</div>
            <div class="highlight">💡 Self Taught AI Developer</div>
            <div class="highlight">🔥 Building with Python, LangChain & Groq</div>
            <div class="highlight">📈 Always learning, always building</div>
        </div>
    </div>
</section>

<div class="contact-section" id="contact">
    <h2 class="section-title reveal">📬 Get In <span class="gradient-text">Touch</span></h2>
    <p class="section-subtitle reveal">Feel free to reach out for collaborations or just a chat!</p>
    <div class="contact-links reveal">
        <a href="https://github.com/Rohits533" target="_blank" rel="noopener noreferrer" class="contact-link">🐙 GitHub</a>
        <a href="mailto:rohitsavan360@gmail.com" class="contact-link">📧 Email</a>
        <a href="https://rohit-ai-chatbot-2026.streamlit.app" target="_blank" rel="noopener noreferrer" class="contact-link">🤖 Try My AI</a>
    </div>
</div>

<footer>
    <p>Built with ❤️ by Rohit Savan • 2026 • Mumbai, India</p>
</footer>

<script>
    const canvas = document.getElementById('particles-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });
    const particles = [];
    for (let i = 0; i < 80; i++) {
        particles.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, vx: (Math.random() - 0.5) * 0.5, vy: (Math.random() - 0.5) * 0.5, size: Math.random() * 2 + 1, opacity: Math.random() * 0.5 + 0.1 });
    }
    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach((p, i) => {
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(0, 212, 255, ${p.opacity})`; ctx.fill();
            particles.forEach((p2, j) => {
                if (i === j) return;
                const dx = p.x - p2.x, dy = p.y - p2.y, dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 120) { ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p2.x, p2.y); ctx.strokeStyle = `rgba(0, 212, 255, ${0.1 * (1 - dist/120)})`; ctx.lineWidth = 0.5; ctx.stroke(); }
            });
        });
        requestAnimationFrame(drawParticles);
    }
    drawParticles();

    const texts = ['Artificial Intelligence', 'Machine Learning', 'LangChain', 'The Future'];
    let textIndex = 0, charIndex = 0, isDeleting = false;
    const typingEl = document.getElementById('typing');
    function type() {
        const current = texts[textIndex];
        if (isDeleting) { typingEl.textContent = current.substring(0, charIndex - 1); charIndex--; }
        else { typingEl.textContent = current.substring(0, charIndex + 1); charIndex++; }
        if (!isDeleting && charIndex === current.length) setTimeout(() => isDeleting = true, 2000);
        else if (isDeleting && charIndex === 0) { isDeleting = false; textIndex = (textIndex + 1) % texts.length; }
        setTimeout(type, isDeleting ? 50 : 100);
    }
    type();

    function animateCounter(el, target) {
        let count = 0;
        const increment = target / 60;
        const timer = setInterval(() =>
