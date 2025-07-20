# Jenkins + Wiz CLI Integration

## Overview
This project demonstrates the integration of Wiz CLI security scanning into Jenkins CI/CD pipelines for automated security validation.

## Architecture
The integration follows a hybrid security approach with:
- **Jenkins Pipeline**: Orchestrates the CI/CD workflow
- **Wiz CLI Integration**: Security scanning execution
- **Security Analysis**: Result processing and threshold checking
- **Enhanced Reporting**: HTML reports and Jenkins integration

## Directory Structure
`
jenkins-pipeline/
 config/
    Jenkinsfile          # Main Jenkins pipeline configuration
 scripts/
    analyze_security.py  # Python script for security analysis
    wiz_cli_integration.sh # Enhanced Wiz CLI integration script
 reports/                 # Security scan reports and outputs
 docs/                    # Documentation and usage examples
`

## Setup Instructions

### 1. Jenkins Configuration
1. Create a Jenkins credential named 'wiz-token' with your Wiz CLI token
2. Install required Jenkins plugins:
   - HTML Publisher Plugin
   - Credentials Plugin

### 2. Pipeline Configuration
1. Copy jenkins-pipeline/config/Jenkinsfile to your Jenkins job
2. Configure the job to use the Jenkinsfile from SCM
3. Set up the WIZ_TOKEN credential in Jenkins

### 3. Environment Setup
The pipeline will automatically:
- Download and install Wiz CLI
- Set up the scanning environment
- Run security scans
- Generate reports

## Pipeline Stages

### 1. Checkout
- Checks out the source code from SCM

### 2. Setup Environment
- Downloads and installs Wiz CLI
- Verifies installation

### 3. Run Tests
- Installs Python dependencies
- Runs pytest validation

### 4. Security Scan
- Executes Wiz CLI security scanning
- Generates JSON and HTML reports
- Archives scan results

### 5. Security Analysis
- Analyzes scan results using Python script
- Checks against configurable thresholds
- Determines pipeline success/failure

### 6. Deploy (Conditional)
- Only executes if security scan passes
- Can be customized for your deployment needs

## Security Thresholds
- **Critical Issues**: 0 (Pipeline fails)
- **High Issues**: 5 (Pipeline fails if exceeded)
- **Medium/Low Issues**: Monitored but don't fail pipeline

## Reports
- **JSON Report**: jenkins-pipeline/reports/security-scan.json
- **HTML Report**: jenkins-pipeline/reports/security-report.html
- **Summary Report**: jenkins-pipeline/reports/security-summary.txt

## Customization
- Modify thresholds in nalyze_security.py
- Adjust scan parameters in wiz_cli_integration.sh
- Customize pipeline stages in Jenkinsfile

## Troubleshooting
- Ensure WIZ_TOKEN credential is properly configured
- Check network connectivity for Wiz CLI download
- Verify Python dependencies are installed
- Review Jenkins console output for detailed logs
