// Simple API test script
const API_BASE_URL = 'http://localhost:8000';

async function testAPI() {
    console.log('🧪 Testing API connection...');
    
    try {
        // Test health endpoint
        console.log('1. Testing health endpoint...');
        const healthResponse = await fetch(`${API_BASE_URL}/health`);
        const healthData = await healthResponse.json();
        console.log('✅ Health check:', healthData);
        
        // Test login endpoint
        console.log('2. Testing login endpoint...');
        const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: 'admin',
                password: 'admin123'
            })
        });
        
        if (loginResponse.ok) {
            const loginData = await loginResponse.json();
            console.log('✅ Login successful:', {
                user: loginData.user.username,
                role: loginData.user.role,
                status: loginData.user.status,
                tokenLength: loginData.access_token.length
            });
        } else {
            const errorData = await loginResponse.json();
            console.log('❌ Login failed:', errorData);
        }
        
    } catch (error) {
        console.error('❌ API test failed:', error);
    }
}

// Run the test
testAPI();
