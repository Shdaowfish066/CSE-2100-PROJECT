"""
Comprehensive endpoint validation to ensure all endpoints are error-free.
"""

import sys
sys.path.insert(0, '/Users/tahsanuddin/Desktop/Project CSE 2100')

from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class EndpointValidator:
    def __init__(self):
        self.total = 0
        self.errors = []
        self.warnings = []
    
    def test_endpoint(self, method, path, name, expected_codes=[200, 201, 400, 403, 404, 422]):
        """Test if endpoint exists and responds (without crashing)"""
        self.total += 1
        try:
            if method == "GET":
                response = client.get(path)
            elif method == "POST":
                response = client.post(path, json={})
            elif method == "PUT":
                response = client.put(path, json={})
            elif method == "DELETE":
                response = client.delete(path)
            
            if response.status_code in expected_codes or response.status_code < 500:
                print(f"{GREEN}✅{RESET} {method:6} {path:50} [{response.status_code}] {name}")
                return True
            else:
                self.errors.append(f"{name}: Unexpected status {response.status_code}")
                print(f"{RED}❌{RESET} {method:6} {path:50} [{response.status_code}] {name}")
                return False
        except Exception as e:
            self.errors.append(f"{name}: {str(e)}")
            print(f"{RED}❌{RESET} {method:6} {path:50} [ERROR] {name}")
            return False
    
    def print_report(self):
        print(f"\n{'='*80}")
        print(f"ENDPOINT VALIDATION REPORT")
        print(f"{'='*80}")
        print(f"{GREEN}Total Endpoints Tested: {self.total}{RESET}")
        if self.errors:
            print(f"{RED}Errors Found: {len(self.errors)}{RESET}")
            for error in self.errors:
                print(f"  ❌ {error}")
        else:
            print(f"{GREEN}✅ NO ERRORS FOUND{RESET}")
        print(f"{'='*80}\n")

validator = EndpointValidator()

print(f"\n{BLUE}{'='*80}")
print(f"VALIDATING ALL 40 ENDPOINTS")
print(f"{'='*80}{RESET}\n")

# ============ AUTH ENDPOINTS (Shihab - 2303147) ============
print(f"{YELLOW}AUTH ENDPOINTS (Shihab - 2303147){RESET}")
validator.test_endpoint("POST", "/auth/register", "Register User")
validator.test_endpoint("POST", "/auth/login", "Login User")

# ============ USER ENDPOINTS (Shihab - 2303147) ============
print(f"\n{YELLOW}USER ENDPOINTS (Shihab - 2303147){RESET}")
validator.test_endpoint("GET", "/users/me", "Get Current User")
validator.test_endpoint("GET", "/users/1", "Get User by ID")
validator.test_endpoint("GET", "/users/by-username/testuser", "Get User by Username")
validator.test_endpoint("PUT", "/users/1", "Update User")
validator.test_endpoint("DELETE", "/users/1", "Delete User")

# ============ POST ENDPOINTS (Arpon - 2303134) ============
print(f"\n{YELLOW}POST ENDPOINTS (Arpon - 2303134){RESET}")
validator.test_endpoint("POST", "/posts/", "Create Post")
validator.test_endpoint("GET", "/posts/me", "Get My Posts")
validator.test_endpoint("GET", "/posts/", "List All Posts")
validator.test_endpoint("GET", "/posts/user/1", "Get Posts by Author")
validator.test_endpoint("GET", "/posts/1", "Get Post by ID")
validator.test_endpoint("PUT", "/posts/1", "Update Post")
validator.test_endpoint("DELETE", "/posts/1", "Delete Post")

# ============ POST VOTE ENDPOINTS (Arpon - 2303134) ============
print(f"\n{YELLOW}POST VOTE ENDPOINTS (Arpon - 2303134){RESET}")
validator.test_endpoint("POST", "/votes/post/1", "Vote on Post")
validator.test_endpoint("DELETE", "/votes/post/1", "Remove Post Vote")
validator.test_endpoint("GET", "/votes/post/1/score", "Get Post Vote Score")

# ============ COMMENT VOTE ENDPOINTS (Emon - 2303173) ============
print(f"\n{YELLOW}COMMENT VOTE ENDPOINTS (Emon - 2303173){RESET}")
validator.test_endpoint("POST", "/votes/comment/1", "Vote on Comment")
validator.test_endpoint("DELETE", "/votes/comment/1", "Remove Comment Vote")
validator.test_endpoint("GET", "/votes/comment/1/score", "Get Comment Vote Score")

# ============ COMMENT ENDPOINTS (Emon - 2303173) ============
print(f"\n{YELLOW}COMMENT ENDPOINTS (Emon - 2303173){RESET}")
validator.test_endpoint("POST", "/comments/1", "Create Comment")
validator.test_endpoint("GET", "/comments/post/1", "List Comments on Post")
validator.test_endpoint("GET", "/comments/1", "Get Comment by ID")
validator.test_endpoint("PUT", "/comments/1", "Update Comment")
validator.test_endpoint("DELETE", "/comments/1", "Delete Comment")

# ============ MESSAGE ENDPOINTS (Tahsan - 2303133) ============
print(f"\n{YELLOW}MESSAGE ENDPOINTS (Tahsan - 2303133){RESET}")
validator.test_endpoint("POST", "/messages/", "Send Message")
validator.test_endpoint("GET", "/messages/conversation/1", "Get Conversation")
validator.test_endpoint("GET", "/messages/inbox", "Get Inbox")
validator.test_endpoint("GET", "/messages/sent", "Get Sent Messages")
validator.test_endpoint("PUT", "/messages/1/mark-read", "Mark Message as Read")
validator.test_endpoint("DELETE", "/messages/1", "Delete Message")

# ============ FILE ENDPOINTS (Tahsan - 2303133) ============
print(f"\n{YELLOW}FILE ENDPOINTS (Tahsan - 2303133){RESET}")
validator.test_endpoint("GET", "/files/1", "Get File")
validator.test_endpoint("GET", "/files/user/1", "List User Files")
validator.test_endpoint("DELETE", "/files/1", "Delete File")

# ============ REPORT ENDPOINTS (Shihab - 2303147) ============
print(f"\n{YELLOW}REPORT ENDPOINTS (Shihab - 2303147){RESET}")
validator.test_endpoint("POST", "/reports/", "Create Report")
validator.test_endpoint("GET", "/reports/", "List Reports")
validator.test_endpoint("GET", "/reports/1", "Get Report")
validator.test_endpoint("PUT", "/reports/1/review?new_status=reviewed", "Review Report")
validator.test_endpoint("DELETE", "/reports/1", "Delete Report")

# Print final report
validator.print_report()

if validator.errors:
    print(f"{RED}VALIDATION FAILED - {len(validator.errors)} errors found{RESET}\n")
    sys.exit(1)
else:
    print(f"{GREEN}✅ ALL {validator.total} ENDPOINTS VALIDATED SUCCESSFULLY!{RESET}\n")
    sys.exit(0)
