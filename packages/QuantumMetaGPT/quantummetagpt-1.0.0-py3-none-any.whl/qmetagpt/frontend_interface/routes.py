from fastapi import APIRouter, HTTPException, BackgroundTasks
from qmetagpt.llm_paper_parser import parse_arxiv_paper
from qmetagpt.task_synthesizer import TaskSynthesizer
from qmetagpt import quantum_algorithm_generator, optimizer_engine, evaluation_engine
from qmetagpt.security_licensing.license_manager import LicenseManager
import os
import uuid
import json

router = APIRouter()
TASKS = {}

@router.post("/run_pipeline")
async def run_pipeline(arxiv_id: str, background_tasks: BackgroundTasks):
    if not LicenseManager().validate_license():
        raise HTTPException(status_code=403, detail="Invalid license")
    
    task_id = str(uuid.uuid4())
    TASKS[task_id] = {"status": "queued", "arxiv_id": arxiv_id}
    
    # Run pipeline in background
    background_tasks.add_task(execute_pipeline, task_id, arxiv_id)
    
    return {"task_id": task_id, "status": "processing"}

@router.get("/task_status/{task_id}")
def get_task_status(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/task_result/{task_id}")
def get_task_result(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task not completed")
    return task["result"]

def execute_pipeline(task_id: str, arxiv_id: str):
    try:
        TASKS[task_id]["status"] = "processing"
        
        # Paper parsing
        paper = parse_arxiv_paper(arxiv_id)
        
        # Task synthesis
        synthesizer = TaskSynthesizer()
        task = synthesizer.synthesize(paper)
        
        # Algorithm generation
        agent = quantum_algorithm_generator.get_agent(
            agent_name="PPO",
            state_dim=10,
            action_dim=5
        )
        agent.build_model()
        circuit = agent.generate_circuit(task)
        
        # Optimization
        optimizer = optimizer_engine.HybridOptimizer(optimizer_type="COBYLA")
        optimized_params = optimizer.optimize(circuit, lambda params: 0.5)  # Placeholder
        
        # Evaluation
        evaluator = evaluation_engine.QuantumEvaluator(use_hardware=False)
        results = evaluator.evaluate(circuit)
        
        # Store results
        TASKS[task_id]["status"] = "completed"
        TASKS[task_id]["result"] = {
            "paper": paper,
            "task": task,
            "circuit": str(circuit),
            "results": results
        }
        
    except Exception as e:
        TASKS[task_id]["status"] = "failed"
        TASKS[task_id]["error"] = str(e)