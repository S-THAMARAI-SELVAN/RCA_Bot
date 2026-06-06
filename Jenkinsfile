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

        echo ===== MAIN BRANCH =====
        git checkout main
        git pull origin main

        git add .

        git diff --cached --quiet
        if %errorlevel%==0 (
            echo No changes to commit
        ) else (
            git commit -m "Auto deploy commit from Jenkins"
        )

        git push origin main

        echo ===== PRODUCTION DEPLOY =====
        git checkout production || git checkout -b production

        git merge main

        if errorlevel 1 (
            echo MERGE FAILED - STOPPING PIPELINE
            exit /b 1
        )

        git push origin production
        '''
    }
}
    }

    post {

        success {
            echo 'Website deployed successfully to production...'
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