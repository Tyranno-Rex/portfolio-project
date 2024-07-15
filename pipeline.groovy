pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'portfolio_github_access_token',
                    url: 'https://github.com/Tyranno-Rex/portfolio-project.git'
            }
        }
    }
}