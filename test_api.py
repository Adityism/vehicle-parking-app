#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5009/api"

def test_login():
    """Test login endpoint"""
    print("Testing login...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@parking.com",
        "password": "admin123"
    })
    print(f"Login status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Login successful: {data.get('user', {}).get('name')}")
        return data.get('access_token')
    else:
        print(f"Login failed: {response.text}")
        return None

def test_me_endpoint(token):
    """Test /auth/me endpoint"""
    print("\nTesting /auth/me endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"/auth/me status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"User info: {data}")
    else:
        print(f"/auth/me failed: {response.text}")

def test_reservations_active(token):
    """Test /reservations/active endpoint"""
    print("\nTesting /reservations/active endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/reservations/active", headers=headers)
    print(f"/reservations/active status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Active reservation: {data}")
    else:
        print(f"/reservations/active failed: {response.text}")

def test_admin_lots(token):
    """Test /admin/lots endpoint"""
    print("\nTesting /admin/lots endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/lots", headers=headers)
    print(f"/admin/lots status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Lots: {len(data)} found")
    else:
        print(f"/admin/lots failed: {response.text}")

def test_available_lots():
    """Test /admin/lots/available endpoint (public)"""
    print("\nTesting /admin/lots/available endpoint...")
    response = requests.get(f"{BASE_URL}/admin/lots/available")
    print(f"/admin/lots/available status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Available lots: {len(data)} found")
    else:
        print(f"/admin/lots/available failed: {response.text}")

if __name__ == "__main__":
    print("Testing Vehicle Parking App API...")
    
    # Test login
    token = test_login()
    
    if token:
        # Test authenticated endpoints
        test_me_endpoint(token)
        test_reservations_active(token)
        test_admin_lots(token)
    
    # Test public endpoints
    test_available_lots()
    
    print("\nAPI testing completed!") 