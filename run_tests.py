import requests
import time

API = "http://localhost:8000"

# Test 1: Recommend - Security vulnerabilities (should find code now with max_distance=1.5)
resp = requests.post(f"{API}/recommend", 
    json={"question": "Quels sont les problèmes de sécurité?"})
status1 = resp.status_code
result1 = resp.json()["result"]
found1 = "pertinent" not in result1.lower() and len(result1) > 400
print(f"TEST 1 (Recommend Security):")
print(f"  Status: {status1}")
print(f"  Code found: {'✅ YES' if found1 else '❌ NO'}")
print(f"  Length: {len(result1)}")
if found1 and len(result1) < 500:
    print(f"  Preview: {result1[:200]}")

# Test 2: Recommend - Performance optimization
resp = requests.post(f"{API}/recommend", 
    json={"question": "Comment optimiser les performances?"})
status2 = resp.status_code
result2 = resp.json()["result"]
found2 = "pertinent" not in result2.lower() and len(result2) > 400
print(f"\nTEST 2 (Recommend Performance):")
print(f"  Status: {status2}")
print(f"  Code found: {'✅ YES' if found2 else '❌ NO'}")
print(f"  Length: {len(result2)}")

# Test 3: Explain - should also work
resp = requests.post(f"{API}/explain", 
    json={"question": "Explique la fonction authenticate"})
status3 = resp.status_code
result3 = resp.json()["result"]
found3 = "pertinent" not in result3.lower() and len(result3) > 300
print(f"\nTEST 3 (Explain):")
print(f"  Status: {status3}")
print(f"  Code found: {'✅ YES' if found3 else '❌ NO'}")
print(f"  Length: {len(result3)}")

# Test 4: Search
resp = requests.post(f"{API}/search", 
    json={"question": "password authentication security"})
status4 = resp.status_code
result4 = resp.json()["result"]
found4 = "pertinent" not in result4.lower() and len(result4) > 200
print(f"\nTEST 4 (Search):")
print(f"  Status: {status4}")
print(f"  Code found: {'✅ YES' if found4 else '❌ NO'}")
print(f"  Length: {len(result4)}")

print(f"\n✅ Summary: {sum([found1, found2, found3, found4])}/4 tests passed")