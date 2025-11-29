from joblegitchecker2 import JobLegitimacyChecker

# Test the improved detection logic
j = JobLegitimacyChecker()

# Test 1: Clear scam with multiple red flags
scam_text = "Guaranteed income! Easy money with no experience needed. Pay upfront via Western Union. $5k per week!"
result1 = j.analyze_job_description(scam_text)
print("Test 1 - Clear Scam:")
print(f"  Risk Score: {result1['risk_score']}")
print(f"  Red Flags Found: {result1['red_flag_count']} - {result1['red_flag_matches']}")
print(f"  Suspicious Patterns: {result1['suspicious_pattern_count']} (severity: {result1['suspicious_pattern_severity']})")
print()

# Test 2: Legitimate job posting
legit_text = "We are looking for a Software Engineer with 3-5 years of experience. Competitive salary and benefits package. Please submit your resume."
result2 = j.analyze_job_description(legit_text)
print("Test 2 - Legitimate Job:")
print(f"  Risk Score: {result2['risk_score']}")
print(f"  Red Flags Found: {result2['red_flag_count']} - {result2['red_flag_matches']}")
print(f"  Suspicious Patterns: {result2['suspicious_pattern_count']} (severity: {result2['suspicious_pattern_severity']})")
print()

# Test 3: URL validation improvements
print("Test 3 - URL Validation:")
print(f"  Valid URL (with TLD): {j.validate_url('https://example.com/job')}")
print(f"  Invalid URL (no TLD): {j.validate_url('https://localhost/job')}")
print(f"  Invalid URL (no scheme): {j.validate_url('example.com')}")
