#!/usr/bin/env python3
"""
Script de testing rápido para validar Día 2 - APIs CRUD
Valida que los endpoints principales respondan correctamente
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test básico de health check"""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ Health check OK")
                return True
            else:
                print("❌ Health check failed - unhealthy status")
                return False
        else:
            print(f"❌ Health check failed - status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed - {str(e)}")
        return False

def test_docs_endpoint():
    """Test que la documentación carga"""
    print("📚 Testing docs endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Docs endpoint OK")
            return True
        else:
            print(f"❌ Docs failed - status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Docs failed - {str(e)}")
        return False

def test_auth_endpoints_without_token():
    """Test que endpoints de auth requieren autenticación"""
    print("🔒 Testing auth endpoints (should fail without token)...")

    endpoints = [
        "/auth/verify",
        "/auth/me",
        "/businesses/",
        "/services/?business_id=test",
        "/employees/?business_id=test"
    ]

    all_passed = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 401:
                print(f"✅ {endpoint} correctly requires auth")
            else:
                print(f"⚠️  {endpoint} returned {response.status_code} (expected 401)")
                all_passed = False
        except Exception as e:
            print(f"❌ Error testing {endpoint}: {str(e)}")
            all_passed = False

    return all_passed

def test_openapi_schema():
    """Test que el schema OpenAPI se genera correctamente"""
    print("📋 Testing OpenAPI schema...")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            schema = response.json()

            # Verificar que incluye nuestros endpoints
            paths = schema.get("paths", {})
            expected_paths = [
                "/health",
                "/auth/verify",
                "/auth/me",
                "/businesses/",
                "/services/",
                "/employees/"
            ]

            missing_paths = []
            for path in expected_paths:
                if path not in paths:
                    missing_paths.append(path)

            if missing_paths:
                print(f"⚠️  Missing paths in OpenAPI: {missing_paths}")
                return False
            else:
                print("✅ OpenAPI schema includes all expected endpoints")
                return True
        else:
            print(f"❌ OpenAPI schema failed - status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OpenAPI schema failed - {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todos los tests"""
    print("🚀 Running IRIS Day 2 API Tests")
    print("=" * 50)

    tests = [
        ("Health Check", test_health_check),
        ("Docs Endpoint", test_docs_endpoint),
        ("Auth Protection", test_auth_endpoints_without_token),
        ("OpenAPI Schema", test_openapi_schema)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n📝 {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1

    print("-" * 50)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Ready for commit!")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed - Check FastAPI is running")
        return False

def main():
    """Main function"""
    print("IRIS Day 2 Testing Script")
    print("Make sure FastAPI is running on http://localhost:8000")
    print()

    success = run_all_tests()

    if success:
        print("\n✅ API testing completed successfully!")
        print("Ready to commit Day 2 changes.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed.")
        print("Make sure FastAPI is running: python main.py")
        sys.exit(1)

if __name__ == "__main__":
    main()