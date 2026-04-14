import sys
import os
import subprocess

# Ensure we are running from the venv
VENV_PYTHON = './venv/bin/python3'

def run_step(step_name, command):
    print(f"\n🚀 Running Pipeline Step: {step_name}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {step_name} completed.")
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {step_name}:")
        print(e.stderr)
        sys.exit(1)

def main():
    print("🔥 Starting NoLimits Data Pipeline...")

    # Step 1: Update simulated data (optional but good for the demo)
    # run_step("Sync Data", f"{VENV_PYTHON} scratch/mock_data.py")

    # Step 2: Re-train the ML Churn Model
    run_step("ML Model Training", f"{VENV_PYTHON} ml/churn_model.py")

    # Step 3: Recalculate Business Metrics
    run_step("Metric Verification", f"{VENV_PYTHON} -c 'import sys; sys.path.append(\".\"); from dashboard.queries.business import get_churn_rate; print(f\"Current Churn Rate: {{get_churn_rate():.2f}}%\")'")

    print("\n🏁 Pipeline finished successfully. Dashboard is ready.")

if __name__ == "__main__":
    main()
