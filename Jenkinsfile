pipeline {
    agent any

    environment {
        DB_CONTAINER_NAME = 'fastapi-db'
        MAX_RETRIES = 20
        RETRY_INTERVAL = 5
    }

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'github-ssh-key', url: 'git@github.com:james8hutch/fastapi-docker-app.git', branch: 'main'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose down'
                sh 'docker system prune -f'
                sh 'docker-compose build --no-cache'
            }
        }

        stage('Start Database') {
            steps {
                sh 'docker-compose up --build -d db'
                script {
                    def retries = 0
                    while (retries < MAX_RETRIES.toInteger()) {
                        def status = sh(script: "docker inspect --format='{{.State.Health.Status}}' $DB_CONTAINER_NAME", returnStdout: true).trim()
                        if (status == 'healthy') {
                            echo "✅ Database is healthy!"
                            break
                        } else if (status == 'unhealthy') {
                            error("❌ Database container is unhealthy. Check logs: docker logs $DB_CONTAINER_NAME")
                        }
                        echo "⏳ Waiting for database to be healthy... (Retry ${retries + 1}/${MAX_RETRIES})"
                        sleep(RETRY_INTERVAL.toInteger())
                        retries++
                    }
                    if (retries == MAX_RETRIES.toInteger()) {
                        error("❌ Database did not become healthy in time.")
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker-compose run --rm test'
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker-compose down'
            }
        }
    }

    post {
        success {
            echo "✅ Build and tests completed successfully!"
        }
        failure {
            echo "❌ Build or tests failed. Check logs for details."
            sh 'docker-compose logs test'
        }
    }
}

