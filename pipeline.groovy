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
        stage('Clean Up') {
            steps {
                sh "rm -rf ./back-end"
                sh "rm -rf ./front-end"
                sh "rm -rf ./README.md"
            }
        }
        stage ('Docker Container Stop and Delete') {
            steps {
                script {
                    def containerName = "front-container"
                    def containerList = sh(script: "docker ps --format '{{.Names}}'", returnStdout: true).trim()
                    if (containerList.contains(containerName)) {
                        sh "docker stop ${containerName}"
                        sh "docker rm ${containerName}"
                    } else {
                        echo "Docker container ${containerName} does not exist, skipping deletion."
                    }
                }
                script {
                    def containerName = "back-container"
                    def containerList = sh(script: "docker ps --format '{{.Names}}'", returnStdout: true).trim()
                    if (containerList.contains(containerName)) {
                        sh "docker stop ${containerName}"
                        sh "docker rm ${containerName}"
                    } else {
                        echo "Docker container ${containerName} does not exist, skipping deletion."
                    }
                }
            }
        }
        stage('Docker Image Delete') {
            steps {
                script {
                    def imageName = "backend-image-docker"
                    def imageList = sh(script: "docker images --format '{{.Repository}}:{{.Tag}}'", returnStdout: true).trim()
                    if (imageList.contains(imageName)) {
                        sh "docker rmi ${imageName}"
                    } else {
                        echo "Docker image ${imageName} does not exist, skipping deletion."
                    }
                }
                script {
                    def imageName = "frontend-image-docker"
                    def imageList = sh(script: "docker images --format '{{.Repository}}:{{.Tag}}'", returnStdout: true).trim()
                    if (imageList.contains(imageName)) {
                        sh "docker rmi ${imageName}"
                    } else {
                        echo "Docker image ${imageName} does not exist, skipping deletion."
                    }
                }
            }
        }
        stage('Git Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Tyranno-Rex/portfolio-project.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                dir("./back-end/main") {
                    sh "docker build -t backend-image-docker ."
                } 
                dir("./front-end") {
                    sh "docker build -t frontend-image-docker ."
                }
            }
        }
        stage ('Check Docker Network') {
            steps {
                script {
                    def networkName = "docker-network"
                    def networkList = sh(script: "docker network ls --format '{{.Name}}'", returnStdout: true).trim()
                    if (networkList.contains(networkName)) {
                        echo "Docker network ${networkName} already exists, skipping creation."
                    } else {
                        sh "docker network create ${networkName}"
                    }
                }
            }
        }
        stage('Docker Run') {
            steps {
                sh "docker run -d --network docker-network -p 8000:8000 --name front-container backend-image-docker"
                sh "docker run -d --network docker-network -v /home/ubuntu/git-token.txt:/app/git-token.txt -p 19999:80 --name back-container frontend-image-docker"
                // docker run -it --name my_container -v /home/ubuntu/git-token.txt:/app/git-token.txt my_python_image
                // sh "docker run -d --network docker-network -p 19999:80 --name back-container frontend-image-docker"
            }
        }
    }
}