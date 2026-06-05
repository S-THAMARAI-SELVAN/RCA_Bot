pipeline {

    agent any

    stages {

        stage('Build') {
            steps {
                bat 'echo Building Website...'
            }
        }

        stage('Test') {
            steps {
                bat 'python RCA_Bot\\validator.py'
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                if not exist C:\\website mkdir C:\\website
                xcopy /E /Y * C:\\website\\
                '''
            }
        }
    }

    post {

        success {
            echo 'Website deployed successfully'
        }

        failure {

            echo 'Pipeline Failed - Running RCA Bot'

            bat 'python RCA_Bot\\rca_agent.py'

            bat 'python RCA_Bot\\send_mail.py'
        }
    }
}