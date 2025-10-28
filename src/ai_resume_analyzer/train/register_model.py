# src/ai_resume_analyzer/train/register_model.py
import argparse
import mlflow
import os
import json
from mlflow.tracking import MlflowClient

def register(model_path: str, model_name: str, run_name: str = None, artifact_path: str = "model"):
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", f"file://{os.path.abspath('mlruns')}")
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient(tracking_uri)
    # create a run to log artifact
    with mlflow.start_run(run_name=run_name):
        mlflow.log_artifact(model_path, artifact_path=artifact_path)
        # register model from the run artifact
        artifact_uri = mlflow.get_artifact_uri(artifact_path)
        result = client.create_registered_model(model_name) if model_name not in [m.name for m in client.list_registered_models()] else None
        mv = client.create_model_version(name=model_name, source=artifact_uri, run_id=mlflow.active_run().info.run_id)
        print("Registered model version:", mv.version)
        return mv

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model-path", required=True)
    p.add_argument("--model-name", required=True)
    p.add_argument("--run-name", default=None)
    args = p.parse_args()
    register(args.model_path, args.model_name, args.run_name)
