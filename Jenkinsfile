pipeline {
  agent any
  stages {
    stage('Coverage') {
      parallel {
        stage('Coverage') {
          steps {
            sh '''export PATH="/usr/local/bin:$PATH"
$WORKSPACE/make_coverage.sh'''
          }
        }
        stage('Static analysis') {
          steps {
            sh '''export PATH="/usr/local/bin:$PATH"
/Users/chrisarchibald/test.sh
'''
          }
        }
      }
    }
    stage('SonarQube analysis') {
      steps {
        sh '/Users/chrisarchibald/Desktop/SonarTestInstances/sonar-scanner-3.0.3.778-macosx 2/bin/sonar-scanner'
      }
    }
  }
}