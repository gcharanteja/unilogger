# main.py

import pandas as pd
import numpy as np
from datasets import Dataset, DatasetDict
import json
import os
from pck67_pkg import TrackingClient
from logger import setup_tracking_logger

client = TrackingClient(
    api_key="51ef227e5469c6ca7446edfea41fefd0cab4ee4f20250706100d122b72a0cde5"
)

# ---------------------------
# Initialize Tracking Client
# ---------------------------

# Get or create project
teams = client.list_teams()
if not teams:
    team = client.create_team("My Team", "Default team")
    team_id = team['id']
else:
    team_id = teams[0]['id']

projects = client.list_projects(team_id)
if not projects:
    project = client.create_project(team_id, "Logistics Project", "Project for logistics experiments")
    project_id = project['id']
else:
    project_id = projects[0]['id']

print(f"Usando ID de proyecto: {project_id}")

# Start a run with the correct project_id
run = client.init_run(project_id=project_id, name="Generación de datos logísticos", config={"task": "synthetic_logistics"})

# Setup logger
logger = setup_tracking_logger(client, run.id, name="logistics_logger")

# ---------------------------
# Generate Synthetic Logistics Data
# ---------------------------

np.random.seed(42)

statuses = ["pending", "processing", "in_transit", "delayed", "delivered", "lost", "returned"]
regions = ["North", "South", "East", "West", "Central"]
carriers = ["FedEx", "UPS", "DHL", "Local", "Express"]
priority_levels = ["standard", "express", "overnight"]

def generate_sample(idx):
    """Generate a single logistics order record."""
    status = np.random.choice(statuses)
    region = np.random.choice(regions)
    carrier = np.random.choice(carriers)
    priority = np.random.choice(priority_levels)
    days_in_transit = np.random.randint(1, 14)

    order_text = f"Order #{idx:05d}: Shipped via {carrier} ({priority}) to {region} region. Status: {status}. Days in transit: {days_in_transit}."

    if status in ["delivered"]:
        label = 2
    elif status in ["delayed", "lost", "returned"]:
        label = 0
    else:
        label = 1

    return {
        "text": order_text,
        "status": status,
        "region": region,
        "carrier": carrier,
        "priority": priority,
        "days": days_in_transit,
        "label": label
    }

# Generate 10,000 samples
logger.info("Generando 10,000 muestras de pedidos logísticos...")

samples = [generate_sample(i) for i in range(10000)]
df = pd.DataFrame(samples)

# Save raw CSV
raw_path = "data/raw/logistics_orders.csv"
os.makedirs("data/raw", exist_ok=True)
df.to_csv(raw_path, index=False)

logger.info(f"✓ Datos brutos guardados: {raw_path}")
logger.info(f"  Forma de los datos: {df.shape}")
logger.info(f"\nDistribución de etiquetas:\n{df['label'].value_counts()}")

# Create HuggingFace Dataset
train_test_split = 0.8
split_idx = int(len(df) * train_test_split)

train_df = df[:split_idx]
test_df = df[split_idx:]

train_dataset = Dataset.from_pandas(train_df[["text", "label"]])
test_dataset = Dataset.from_pandas(test_df[["text", "label"]])

dataset_dict = DatasetDict({
    "train": train_dataset,
    "validation": test_dataset
})

# Save datasets locally
dataset_path = "data/processed/logistics_dataset"
os.makedirs("data/processed", exist_ok=True)
dataset_dict.save_to_disk(dataset_path)

logger.info(f"\n✓ Conjunto de datos de HuggingFace guardado: {dataset_path}")
logger.info(f"  Conjunto de entrenamiento: {len(train_dataset)} muestras")
logger.info(f"  Conjunto de validación: {len(test_dataset)} muestras")

# Finish run
run.finish()

# Optionally fetch aggregated metrics (numeric only)
aggregated = run.get_aggregated_metrics()
logger.info(f"Métricas agregadas: {aggregated}")