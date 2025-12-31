#!/usr/bin/env python3
"""API Speculation Engine - Because reading docs is for quitters."""

import requests
import json
import sys
from urllib.parse import urljoin
from collections import defaultdict

class APISpeculator:
    """Guesses API endpoints so you don't have to think."""
    
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.found_endpoints = defaultdict(list)
        
    def speculate(self, endpoint):
        """Make educated guesses (mostly uneducated)."""
        url = urljoin(self.base_url + '/', endpoint)
        
        # Try common HTTP methods - because REST is just a suggestion
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        results = {}
        
        for method in methods:
            try:
                # Add some common headers to look legit
                headers = {
                    'User-Agent': 'API-Speculator/1.0 (Powered by Guesses)',
                    'Accept': 'application/json'
                }
                
                # Send minimal data for methods that need it
                data = {} if method == 'GET' else {'data': 'speculated'}
                
                response = self.session.request(
                    method, url, 
                    headers=headers, 
                    json=data if method != 'GET' else None,
                    timeout=5
                )
                
                if response.status_code < 500:  # Anything not server error is a win!
                    results[method] = {
                        'status': response.status_code,
                        'headers': dict(response.headers),
                        'body_preview': response.text[:200] if response.text else None
                    }
                    
            except Exception as e:
                results[method] = {'error': str(e)}
                
        return results
    
    def common_endpoints_scan(self):
        """Check for endpoints that probably exist (maybe)."""
        common = ['api', 'v1', 'users', 'products', 'auth', 'login', 'docs', 'health']
        print("\n🔮 Speculating common endpoints... (cross your fingers)")
        
        for endpoint in common:
            print(f"\nTrying '/{endpoint}':")
            results = self.speculate(endpoint)
            for method, result in results.items():
                if 'status' in result and result['status'] < 400:
                    print(f"  {method}: {result['status']} - Found something! (probably)")
                    self.found_endpoints[endpoint].append(method)
                
        if self.found_endpoints:
            print("\n🎉 Found endpoints (or at least got responses):")
            for endpoint, methods in self.found_endpoints.items():
                print(f"  /{endpoint}: {', '.join(methods)}")
        else:
            print("\n🤷 No luck. Maybe try sacrificing a goat to the API gods?")

def main():
    """Main function - because every script needs one."""
    if len(sys.argv) < 2:
        print("Usage: python api_speculator.py <base_url>")
        print("Example: python api_speculator.py https://api.example.com")
        sys.exit(1)
        
    base_url = sys.argv[1]
    speculator = APISpeculator(base_url)
    
    print(f"🔍 Speculating API at {base_url}")
    print("Disclaimer: This is basically API astrology. Results may vary.\n")
    
    # Scan common endpoints
    speculator.common_endpoints_scan()
    
    # Interactive mode
    print("\n💡 Try speculating your own endpoint (or type 'quit'):")
    while True:
        endpoint = input("Endpoint to speculate: ").strip()
        if endpoint.lower() in ['quit', 'exit', 'q']:
            break
            
        results = speculator.speculate(endpoint)
        print(f"\nResults for '{endpoint}':")
        for method, result in results.items():
            if 'status' in result:
                print(f"  {method}: Status {result['status']}")
                if result.get('body_preview'):
                    print(f"     Preview: {result['body_preview']}")
            else:
                print(f"  {method}: {result.get('error', 'Unknown error')}")
        print()

if __name__ == "__main__":
    main()
