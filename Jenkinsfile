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
touch ~/.pylintrc
find . -iname "*.py" | xargs pylint -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > report.bat || || exit 0'''
          }
        }
      }
    }
  }
}