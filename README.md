add readme to check conntection with jira


        <!-- git_readme = git_soup.select_one("article.markdown-body.entry-content.container-lg").text.strip()
        project_crawling_info = git_readme.split('Project Crawling')[1].strip()
        project_name = project_crawling_info.split('PROJECT_NAME : ')[1].split('\n')[0]
        project_description = project_crawling_info.split('PROJECT_DESCRIPTION : ')[1].split('\n')[0]
        project_url = project_crawling_info.split('PROJECT_URL : ')[1].split('\n')[0]
        project_complete_status = project_crawling_info.split('PROJECT_COMPLETION_STATUS : ')[1].split('\n')[0]
        multi_projects = project_crawling_info.split('PROJECT_MULTI : ')[1].split('\n')[0]
        project_category = project_crawling_info.split('PROJECT_SUBPROJECT : ')[1].split('\n')[0]
        sub_project = project_category.split(', ') -->

## Project Crawling

PROJECT_NAME: portfolio-project
PROJECT_DESCRIPTION: This repository showcases Jeong Eun Seong's portfolio. It contains various projects that I have worked on. The website presents these projects in a 3D space. The project leverages several advanced technologies, including fine-tuned AI models using OpenAI's GPT-3.5, Three.js for 3D rendering, and an optimal algorithm to categorize and display the projects. It utilizes full-stack development for both backend and frontend functionalities. Additionally, the server crawls my GitHub repository daily to update the portfolio website automatically. 
PROJECT_URL: 'https://github.com/Tyranno-Rex/portfolio-project'
PROJECT_COMPLETION_STATUS: FALSE
PROJECT_MULTI: FALSE
PROJECT_SUBPROJECT: 'NONE'
PROJECT_CATEGORY: 'graphic', 'ai', 'web/mobile', 'algorithm', 'fullstack'
