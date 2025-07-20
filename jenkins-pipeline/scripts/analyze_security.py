#!/usr/bin/env python3
"""
Security Analysis Script for Jenkins + Wiz CLI Integration
Parses Wiz CLI scan results and provides analysis for Jenkins pipeline
"""

import json
import sys
import os
from typing import Dict, List, Any

class SecurityAnalyzer:
    def __init__(self, scan_results_file: str):
        self.scan_results_file = scan_results_file
        self.scan_data = None
        self.load_scan_results()
    
    def load_scan_results(self):
        """Load and parse Wiz CLI scan results"""
        try:
            with open(self.scan_results_file, 'r') as f:
                self.scan_data = json.load(f)
            print(f" Loaded scan results from {self.scan_results_file}")
        except FileNotFoundError:
            print(f" Scan results file not found: {self.scan_results_file}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f" Invalid JSON in scan results file: {self.scan_results_file}")
            sys.exit(1)
    
    def analyze_severity_distribution(self) -> Dict[str, int]:
        """Analyze vulnerability severity distribution"""
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0,
            'INFORMATIONAL': 0
        }
        
        if self.scan_data and 'issues' in self.scan_data:
            for issue in self.scan_data['issues']:
                severity = issue.get('severity', 'UNKNOWN').upper()
                if severity in severity_counts:
                    severity_counts[severity] += 1
        
        return severity_counts
    
    def check_critical_thresholds(self, max_critical: int = 0, max_high: int = 5) -> bool:
        """Check if security scan passes threshold criteria"""
        severity_counts = self.analyze_severity_distribution()
        
        critical_count = severity_counts.get('CRITICAL', 0)
        high_count = severity_counts.get('HIGH', 0)
        
        print(f" Security Scan Analysis:")
        print(f"   Critical vulnerabilities: {critical_count}")
        print(f"   High vulnerabilities: {high_count}")
        print(f"   Medium vulnerabilities: {severity_counts.get('MEDIUM', 0)}")
        print(f"   Low vulnerabilities: {severity_counts.get('LOW', 0)}")
        
        # Check thresholds
        if critical_count > max_critical:
            print(f" FAIL: Critical vulnerabilities ({critical_count}) exceed threshold ({max_critical})")
            return False
        
        if high_count > max_high:
            print(f" FAIL: High vulnerabilities ({high_count}) exceed threshold ({max_high})")
            return False
        
        print(f" PASS: Security scan meets threshold criteria")
        return True
    
    def generate_summary_report(self) -> str:
        """Generate a summary report for Jenkins"""
        severity_counts = self.analyze_severity_distribution()
        total_issues = sum(severity_counts.values())
        
        report = f"""
=== SECURITY SCAN SUMMARY ===
Total Issues Found: {total_issues}
Severity Distribution:
  - Critical: {severity_counts['CRITICAL']}
  - High: {severity_counts['HIGH']}
  - Medium: {severity_counts['MEDIUM']}
  - Low: {severity_counts['LOW']}
  - Informational: {severity_counts['INFORMATIONAL']}

Pipeline Status: {'PASS' if self.check_critical_thresholds() else 'FAIL'}
"""
        return report

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_security.py <scan_results_file>")
        sys.exit(1)
    
    scan_file = sys.argv[1]
    analyzer = SecurityAnalyzer(scan_file)
    
    # Generate and print summary
    summary = analyzer.generate_summary_report()
    print(summary)
    
    # Check thresholds and exit with appropriate code
    if analyzer.check_critical_thresholds():
        print(" Security scan PASSED - Pipeline can proceed")
        sys.exit(0)
    else:
        print(" Security scan FAILED - Pipeline blocked")
        sys.exit(1)

if __name__ == "__main__":
    main()
