#!/usr/bin/env python3
"""
Test script for Academic Assignment Helper API
Demonstrates the complete workflow: register, login, upload, analyze
"""

import requests
import time
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register():
    print("\n=== Testing Student Registration ===")
    data = {
        "email": "testuser@university.edu",
        "password": "SecurePass123",
        "full_name": "Test User",
        "student_id": "TEST2025"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    elif response.status_code == 400:
        print("User already exists, continuing...")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_login():
    print("\n=== Testing Login ===")
    data = {
        "email": "testuser@university.edu",
        "password": "SecurePass123"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        token_data = response.json()
        print(f"Access Token: {token_data['access_token'][:50]}...")
        return token_data['access_token']
    else:
        print(f"Error: {response.text}")
        return None

def create_sample_assignment():
    print("\n=== Creating Sample Assignment File ===")
    sample_text = """
    Machine Learning in Modern Computing

    Introduction:
    Machine learning has revolutionized the field of computer science and artificial intelligence.
    This assignment explores the fundamental concepts of machine learning, including supervised
    learning, unsupervised learning, and reinforcement learning.

    Supervised Learning:
    Supervised learning algorithms learn from labeled training data. Common algorithms include
    linear regression, logistic regression, decision trees, and neural networks. These methods
    are widely used in applications such as image recognition, spam detection, and predictive
    analytics.

    Deep Learning:
    Deep learning, a subset of machine learning, uses artificial neural networks with multiple
    layers. Convolutional Neural Networks (CNNs) excel at image processing, while Recurrent
    Neural Networks (RNNs) are effective for sequential data like text and speech.

    Applications:
    Machine learning is applied across various domains including healthcare (disease diagnosis),
    finance (fraud detection), autonomous vehicles, natural language processing, and
    recommendation systems.

    Conclusion:
    As computing power increases and datasets grow larger, machine learning continues to advance,
    enabling more sophisticated AI applications that impact society in profound ways.

    References:
    - Deep Learning by Goodfellow, Bengio, and Courville
    - Pattern Recognition and Machine Learning by Bishop
    - Machine Learning: A Probabilistic Perspective by Murphy
    """

    from tempfile import gettempdir
    file_path = Path(gettempdir()) / "sample_assignment.txt"
    file_path.write_text(sample_text)
    print(f"Created sample assignment at: {file_path}")
    return file_path

def test_upload(token):
    print("\n=== Testing Assignment Upload ===")

    file_path = create_sample_assignment()

    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": open(file_path, "rb")}

    response = requests.post(f"{BASE_URL}/upload", headers=headers, files=files)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        return result.get("assignment_id")
    else:
        print(f"Error: {response.text}")
        return None

def test_get_analysis(token, assignment_id, max_retries=10):
    print(f"\n=== Testing Get Analysis (Assignment ID: {assignment_id}) ===")

    headers = {"Authorization": f"Bearer {token}"}

    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1}/{max_retries}...")
        print("Making request to:", f"{BASE_URL}/analysis/{assignment_id}")
        print("Using headers:", headers)
        response = requests.get(f"{BASE_URL}/analysis/{assignment_id}", headers=headers)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Analysis Complete!")
            print(json.dumps(result, indent=2))
            return True
        elif response.status_code == 404:
            print("Analysis not ready yet, waiting 3 seconds...")
            time.sleep(3)
        else:
            print(f"Error: {response.text}")
            return False

    print("⚠️  Analysis not completed within timeout period")
    return False

def test_search_sources(token):
    print("\n=== Testing Source Search ===")

    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "query": "machine learning algorithms and neural networks",
        "limit": 3
    }

    response = requests.post(f"{BASE_URL}/sources", headers=headers, json=data)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        sources = response.json()
        print(f"\nFound {len(sources)} relevant sources:")
        for source in sources:
            print(f"\n- {source['title']}")
            print(f"  Authors: {source['authors']}")
            print(f"  Year: {source['publication_year']}")
            print(f"  Similarity: {source.get('similarity_score', 'N/A')}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def main():
    print("=" * 60)
    print("Academic Assignment Helper - API Test Suite")
    print("=" * 60)

    if not test_health():
        print("\n❌ Health check failed. Is the server running?")
        return

    if not test_register():
        print("\n❌ Registration failed")
        return

    token = test_login()
    if not token:
        print("\n❌ Login failed")
        return

    print("\n✅ Authentication successful!")

    assignment_id = test_upload(token)
    if not assignment_id:
        print("\n❌ Upload failed")
        return

    print("\n✅ Upload successful!")
    print(f"Assignment ID: {assignment_id}")

    print("\n⏳ Waiting for n8n workflow to process...")
    time.sleep(5)

    if test_get_analysis(token, assignment_id):
        print("\n✅ Analysis retrieval successful!")
    else:
        print("\n⚠️  Analysis may still be processing. Check later with:")
        print(f"   curl -H 'Authorization: Bearer {token}' {BASE_URL}/analysis/{assignment_id}")

    if test_search_sources(token):
        print("\n✅ Source search successful!")

    print("\n" + "=" * 60)
    print("Test Suite Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
