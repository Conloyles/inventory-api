import requests
from kubernetes import client, config

def get_cluster_state():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    
    pods = v1.list_namespaced_pod(namespace="default")
    
    pod_info = []
    for pod in pods.items:
        container_statuses = pod.status.container_statuses or []
        restarts = sum(cs.restart_count for cs in container_statuses)
        ready = all(cs.ready for cs in container_statuses)
        
        pod_info.append({
            "name": pod.metadata.name,
            "status": pod.status.phase,
            "ready": ready,
            "restarts": restarts,
            "node": pod.spec.node_name
        })
    
    return pod_info

def ask_ollama(question, cluster_data):
    prompt = f"""You are a Kubernetes cluster assistant helping a platform engineer.

Here is the current state of the cluster pods:
{cluster_data}

Answer this question clearly and concisely:
{question}

If you see any issues, explain what they might mean and suggest what to check next.
"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )
    
    return response.json()["response"]

def ask_cluster(question):
    cluster_data = get_cluster_state()
    answer = ask_ollama(question, cluster_data)
    return {
        "question": question,
        "cluster_data": cluster_data,
        "answer": answer
    }