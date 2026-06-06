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
                bat '''
                C:\\Users\\thama\\AppData\\Local\\Programs\\Python\\Python314\\python.exe RCA_Bot\\validator.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                if not exist C:\\website mkdir C:\\website
                xcopy /E /Y /I * C:\\website\\

                cd /d %WORKSPACE%

                git config user.name "jenkins"
                git config user.email "jenkins@local"

                REM Ensure we are on main branch
                git checkout main

                REM Pull latest changes to avoid conflicts
                git pull origin main

                REM Commit only if changes exist
                git add .
                git diff --cached --quiet || git commit -m "Auto deploy commit from Jenkins"

                REM Push main first
                git push origin main

                REM Switch to production
                git checkout production

                REM Merge safely
                git merge main

                REM Push production
                git push origin production
                '''
            }
        }
    }

    post {

        success {
            echo 'Website deployed successfully to production'
        }

        failure {
            echo 'Pipeline Failed - Running RCA Bot'

            bat '''
            C:\\Users\\thama\\AppData\\Local\\Programs\\Python\\Python314\\python.exe RCA_Bot\\rca_agent.py
            '''

            bat '''
            C:\\Users\\thama\\AppData\\Local\\Programs\\Python\\Python314\\python.exe RCA_Bot\\send_discord_alert.py
            '''
        }
    }
}