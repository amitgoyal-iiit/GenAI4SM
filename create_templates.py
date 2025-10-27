import os
import re

def extract_routes_from_main():
    """Extract routes from main.py"""
    routes = []
    with open('main.py', 'r') as f:
        content = f.read()
        # Find all route decorators
        matches = re.findall(r'@app\.route\("/(.*?)"', content)
        routes = [route for route in matches if route.endswith('.html')]
    return routes

def create_template(template_name):
    """Create a template file if it doesn't exist"""
    template_path = os.path.join('templates', template_name)
    if not os.path.exists(template_path):
        template_content = '''
{{% extends "base.html" %}}

{{% block content %}}
<div class="container">
    <h1>{}</h1>
    {{% if content %}}
        {{{{ content | markdown }}}}
    {{% endif %}}
</div>
{{% endblock %}}
'''.format(template_name.replace(".html", "").title())
        
        with open(template_path, 'w') as f:
            f.write(template_content)
        print(f"Created template: {template_name}")
    else:
        print(f"Template already exists: {template_name}")

def create_specific_template(route_name):
    """Get specific template content based on route name"""
    templates = {
        'schedule.html': '''
{%% extends "base.html" %%}

{%% block content %%}
<div class="container">
    <h1>Workshop Schedule</h1>
    {{ schedule | markdown }}
    {%% include 'schedule_head.html' %%}
</div>
{%% endblock %%}
''',
        'submissions.html': '''
{%% extends "base.html" %%}

{%% block content %%}
<div class="container">
    <h1>Paper Submissions</h1>
    {{ cfp | markdown }}
    {%% if papers %%}
    <div class="papers-list">
        {%% for paper in papers %%}
            <div class="paper-item">
                <h3>{{ paper.title }}</h3>
                <p>{{ paper.authors | join(", ") }}</p>
            </div>
        {%% endfor %%}
    </div>
    {%% endif %%}
</div>
{%% endblock %%}
'''
    }
    return templates.get(route_name)

def main():
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("Created templates directory")

    # Extract routes from main.py
    routes = extract_routes_from_main()
    
    # Create templates for each route
    for route in routes:
        template_path = os.path.join('templates', route)
        if not os.path.exists(template_path):
            # Check if we have a specific template for this route
            specific_content = create_specific_template(route)
            if specific_content:
                with open(template_path, 'w') as f:
                    f.write(specific_content)
                print(f"Created specific template: {route}")
            else:
                create_template(route)

if __name__ == "__main__":
    main()

