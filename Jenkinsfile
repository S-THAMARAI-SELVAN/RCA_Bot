pipeline {

```
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
            bat '"C:\\Users\\thama\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" RCA_Bot\\validator.py'
        }
    }

    stage('Merge To Production') {
        steps {

            bat '''
            git config --global user.name "Jenkins"
            git config --global user.email "jenkins@example.com"

            git fetch origin

            git checkout production
            git pull origin production

            git checkout main
            git pull origin main

            git checkout production

            git merge main

            git status

            git push origin production --verbose
            '''
        }
    }

    stage('Deploy') {
        steps {

            bat '''
            if not exist C:\\website mkdir C:\\website

            xcopy /E /I /Y * C:\\website\\
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

        bat '"C:\\Users\\thama\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" RCA_Bot\\rca_agent.py'

        bat '"C:\\Users\\thama\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" RCA_Bot\\send_discord_alert.py'
    }

    always {
        echo 'Pipeline Execution Completed'
    }
}
```

}
