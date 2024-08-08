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
        stage('Git Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Tyranno-Rex/portfolio-project.git'
            }
        }
        stage('Build Spare Docker Image') {
            steps {
                dir("./back-end/main") {
                    sh "docker build -t backend-image-docker-spare ."
                } 
                dir("./front-end") {
                    sh "docker build -t frontend-image-docker-spare ."
                }
            }
        }
        stage('Check Docker Network') {
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

        stage('aws configure') {
            steps {
                sh "aws configure set aws_access_key_id {AWS_ACCESS_KEY_ID}"
                sh "aws configure set aws_secret_access_key {AWS_SECRET_ACCESS_KEY}"
                sh "aws configure set region ap-northeast-2"
            }
        }

        // load-balancer-group 타겟 그룹에 Port를 추가하는 명령어
        stage('Add load-balancer-group Target Group to 8001 Port and 19998 Port by aws cli') {
            steps {
                sh "aws elbv2 register-targets --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/backend/e63aa5e555913ff4 --region ap-northeast-2 --targets Id=i-0b712766be7d02193,Port=8001"
                sh "aws elbv2 register-targets --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/loadbalancer-group/c1d8f0cda7db431b --region ap-northeast-2 --targets Id=i-0b712766be7d02193,Port=19998"
            }
        }
        stage('Spare Docker Run') {
            steps {
                sh "docker run -d --network docker-network -p 19998:80 --name front-container-spare frontend-image-docker-spare"
                sh "docker run -d --network docker-network -p 8001:8000 -v /home/git-token.txt:/app/git-token.txt -v /home/mongo-token.txt:/app/mongo-token.txt -v /home/access-token.txt:/app/access-token.txt --name back-container-spare backend-image-docker-spare"
            }
        }


        // load-balancer-group 타겟 그룹에서 해당 port가 열렸을 때까지 대기
        stage('Check load-balancer-group Target Group Health Check') {
            steps {
                script {
                    def targetGroupArn = 'arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/loadbalancer-group/c1d8f0cda7db431b'
                    def region = 'ap-northeast-2'
                    def isHealthy = false

                    while (!isHealthy) {
                        def result = sh(
                            script: "aws elbv2 describe-target-health --target-group-arn ${targetGroupArn} --region ${region}",
                            returnStdout: true
                        ).trim()
                        
                        echo "Checking target group health status..."
                        def json = readJSON text: result
                        isHealthy = json.TargetHealthDescriptions.every { it.TargetHealth.State == 'healthy' }

                        if (!isHealthy) {
                            echo "Not all targets are healthy yet. Waiting for 10 seconds..."
                            sleep 10
                        } else {
                            echo "All targets are healthy!"
                        }
                    }
                }
            }
        }
        stage('Check backend Target Group Health Check') {
            steps {
                script {
                    def targetGroupArn = 'arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/backend/e63aa5e555913ff4'
                    def region = 'ap-northeast-2'
                    def isHealthy = false

                    while (!isHealthy) {
                        def result = sh(
                            script: "aws elbv2 describe-target-health --target-group-arn ${targetGroupArn} --region ${region}",
                            returnStdout: true
                        ).trim()
                        
                        echo "Checking target group health status..."
                        def json = readJSON text: result
                        isHealthy = json.TargetHealthDescriptions.every { it.TargetHealth.State == 'healthy' }

                        if (!isHealthy) {
                            echo "Not all targets are healthy yet. Waiting for 10 seconds..."
                            sleep 10
                        } else {
                            echo "All targets are healthy!"
                        }
                    }
                }
            }
        }
        // load-balancer-group에 8000번과 19999 포트를 닫는 명령어
        stage('Remove load-balancer-group Target Group to 8000 Port and 19999 Port by aws cli') {
            steps {
                sh "aws elbv2 deregister-targets --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/backend/e63aa5e555913ff4 --region ap-northeast-2 --targets Id=i-0b712766be7d02193,Port=8000"
                sh "aws elbv2 deregister-targets --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/loadbalancer-group/c1d8f0cda7db431b --region ap-northeast-2 --targets Id=i-0b712766be7d02193,Port=19999"
            }
        }
        stage('Docker Container Stop and Delete') {
            steps {
                script {
                    def containers = ["front-container", "back-container"]
                    def containerList = sh(script: "docker ps --format '{{.Names}}'", returnStdout: true).trim().split("\n")
                    containers.each { containerName ->
                        if (containerList.contains(containerName)) {
                            sh "docker stop ${containerName}"
                            sh "docker rm ${containerName}"
                        } else {
                            echo "Docker container ${containerName} does not exist, skipping deletion."
                        }
                    }
                }
            }
        }
        stage('Docker Image Delete') {
            steps {
                script {
                    def images = ["backend-image-docker", "frontend-image-docker"]
                    def imageList = sh(script: "docker images --format '{{.Repository}}:{{.Tag}}'", returnStdout: true).trim().split("\n")
                    images.each { imageName ->
                        if (imageList.contains(imageName)) {
                            sh "docker rmi ${imageName}"
                        } else {
                            echo "Docker image ${imageName} does not exist, skipping deletion."
                        }
                    }
                }
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
        stage('Docker Run') {
            steps {
                sh "docker run -d --network docker-network -p 19999:80 --name front-container frontend-image-docker"
                sh "docker run -d --network docker-network -p 8000:8000 -v /home/git-token.txt:/app/git-token.txt -v /home/mongo-token.txt:/app/mongo-token.txt -v /home/access-token.txt:/app/access-token.txt --name back-container backend-image-docker"
            }
        }
        // load-balancer-group 타겟 그룹에 8000번과 19999 포트를 추가하는 명령어
        stage('Add load-balancer-group Target Group to 8000 Port and 19999 Port by aws cli') {
            steps {
                sh "aws elbv2 register-targets --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/backend/e63aa5e555913ff4 --region ap-northeast-2 --targets Id=i-0b712766be7d02193,Port=8000"
                sh "aws elbv2 register-targets --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/loadbalancer-group/c1d8f0cda7db431b --region ap-northeast-2 --targets Id=i-0b712766be7d02193,Port=19999"
            }
        }
        // load-balancer-group 타겟 그룹에서 해당 port가 열렸을 때까지 대기
        stage('Check load-balancer-group Target Group Health Check2') {
            steps {
                script {
                    def targetGroupArn = 'arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/loadbalancer-group/c1d8f0cda7db431b'
                    def region = 'ap-northeast-2'
                    def isHealthy = false

                    while (!isHealthy) {
                        def result = sh(
                            script: "aws elbv2 describe-target-health --target-group-arn ${targetGroupArn} --region ${region}",
                            returnStdout: true
                        ).trim()
                        
                        echo "Checking target group health status..."
                        def json = readJSON text: result
                        isHealthy = json.TargetHealthDescriptions.every { it.TargetHealth.State == 'healthy' }

                        if (!isHealthy) {
                            echo "Not all targets are healthy yet. Waiting for 10 seconds..."
                            sleep 10
                        } else {
                            echo "All targets are healthy!"
                        }
                    }
                }
            }
        }
        // backend 타겟 그룹에서 해당 port가 열렸을 때까지 대기
        stage('Check backend Target Group Health Check2') {
            steps {
                script {
                    def targetGroupArn = 'arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/backend/e63aa5e555913ff4'
                    def region = 'ap-northeast-2'
                    def isHealthy = false

                    while (!isHealthy) {
                        def result = sh(
                            script: "aws elbv2 describe-target-health --target-group-arn ${targetGroupArn} --region ${region}",
                            returnStdout: true
                        ).trim()
                        
                        echo "Checking target group health status..."
                        def json = readJSON text: result
                        isHealthy = json.TargetHealthDescriptions.every { it.TargetHealth.State == 'healthy' }

                        if (!isHealthy) {
                            echo "Not all targets are healthy yet. Waiting for 10 seconds..."
                            sleep 10
                        } else {
                            echo "All targets are healthy!"
                        }
                    }
                }
            }
        }
        // load-balancer-group에 8001번과 19998 포트를 닫는 명령어
        stage('Remove load-balancer-group Target Group to 8001 Port and 19998 Port by aws cli') {
            steps {
                sh "aws elbv2 deregister-targets --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/backend/e63aa5e555913ff4 --region ap-northeast-2 --targets Id=i-0b712766be7d02193,Port=8001"
                sh "aws elbv2 deregister-targets --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:533267203583:targetgroup/loadbalancer-group/c1d8f0cda7db431b --region ap-northeast-2 --targets Id=i-0b712766be7d02193,Port=19998"
            }
        }
        stage('Spare Docker Container Stop and Delete') {
            steps {
                script {
                    sh "docker stop front-container-spare"
                    sh "docker rm front-container-spare"
                    sh "docker stop back-container-spare"
                    sh "docker rm back-container-spare"
                }
            }
        }
        stage('Spare Docker Image Delete') {
            steps {
                script {
                    sh "docker rmi backend-image-docker-spare"
                    sh "docker rmi frontend-image-docker-spare"
                }
            }
        }
    }
}