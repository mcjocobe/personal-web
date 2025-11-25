import pytest
import subprocess
import time
import urllib.request
import urllib.error

@pytest.fixture(scope="module")
def docker_container():
    # Build the image
    subprocess.run(["docker", "build", "-t", "test-web-image", "."], check=True, capture_output=True)
    
    # Run the container
    container_name = "test-web-container-pytest"
    subprocess.run([
        "docker", "run", "-d", 
        "-p", "8081:80", 
        "--name", container_name, 
        "test-web-image"
    ], check=True, capture_output=True)
    
    # Wait for container to be ready
    time.sleep(2)
    
    yield "http://localhost:8081"
    
    # Cleanup
    subprocess.run(["docker", "rm", "-f", container_name], check=False, capture_output=True)

def test_landing_page(docker_container):
    url = docker_container
    try:
        response = urllib.request.urlopen(url)
        assert response.status == 200
        content = response.read().decode('utf-8')
        assert "<title>" in content # Basic check that we got HTML
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to container: {e}")
