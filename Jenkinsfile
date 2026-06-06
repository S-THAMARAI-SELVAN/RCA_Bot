pipeline {
    agent any

    options {
        timestamps()
    }

    stages {

        stage('Build') {
            steps {
                echo 'Building Website...'
            }
        }

        stage('Test') {
            steps {
                bat 'python RCA_Bot\\validator.py'
            }
        }

        stage('Merge To Production') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-creds',
                                                  usernameVariable: 'S-THAMARAI-SELVAN',
                                                  passwordVariable: 'mUDAIYAR00@')]) {

                    bat '''
                        git config --global user.name "Jenkins"
                        git config --global user.email "jenkins@example.com"
                        git config --global --add safe.directory "%WORKSPACE%"

                        git remote set-url origin https://%GIT_USER%:%GIT_PASS%@github.com/S-THAMARAI-SELVAN/RCA_Bot.git
                        git push origin HEAD:production --verbose
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                    if not exist C:\\website mkdir C:\\website
                    robocopy . C:\\website /E /XD .git
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
            bat 'python RCA_Bot\\send_discord_alert.py'
        }

        always {
            echo 'Pipeline Execution Completed'
        }
    }
}