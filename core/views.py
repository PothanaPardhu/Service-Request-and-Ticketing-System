from django.shortcuts import render
from django.http import HttpResponse

def landing_page(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enterprise Ticketing System | Portal</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #6366f1;
                --secondary: #4f46e5;
                --bg: #0f172a;
                --card-bg: rgba(30, 41, 59, 0.7);
                --text: #f8fafc;
            }
            body {
                margin: 0;
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                color: var(--text);
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }
            .glass {
                background: var(--card-bg);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 3rem;
                text-align: center;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                max-width: 600px;
                animation: fadeIn 0.8s ease-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                background: linear-gradient(to right, #818cf8, #c084fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p {
                color: #94a3b8;
                font-size: 1.1rem;
                margin-bottom: 2.5rem;
            }
            .buttons {
                display: flex;
                gap: 1rem;
                justify-content: center;
            }
            .btn {
                padding: 0.8rem 2rem;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .btn-primary {
                background: var(--primary);
                color: white;
            }
            .btn-primary:hover {
                background: var(--secondary);
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
            }
            .btn-secondary {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .btn-secondary:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            .badge {
                display: inline-block;
                padding: 0.4rem 1rem;
                background: rgba(129, 140, 248, 0.1);
                color: #818cf8;
                border-radius: 100px;
                font-size: 0.8rem;
                font-weight: 700;
                text-transform: uppercase;
                margin-bottom: 1rem;
            }
        </style>
    </head>
    <body>
        <div class="glass">
            <span class="badge">Production Ready</span>
            <h1>Enterprise Ticketing</h1>
            <p>A high-performance Service Request System built with Django REST Framework, featuring RBAC, SLA tracking, and real-time audit logs.</p>
            <div class="buttons">
                <a href="http://localhost:5173" class="btn btn-primary">Launch Dashboard</a>
                <a href="/api/docs/" class="btn btn-secondary">API Docs</a>
                <a href="/admin/" class="btn btn-secondary">Admin Portal</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)
