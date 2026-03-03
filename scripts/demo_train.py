import random
import time

from mltrack import Run

def main() -> None:
    run = Run.create(
        project="demo",
        experiment="mnist",
        name="demo-train",
        params={
            "lr": 0.001,
            "batch_size": 64,
            "model": "mlp",
            "seed": 42,
        },
    )

    print(f"Created run_id={run.id}")

    loss = 1.2
    acc = 0.30

    for step in range(20):
        # Fake training dynamics
        loss = max(0.05, loss * (0.90 + random.random() * 0.03))
        acc = min(0.99, acc + (0.02 + random.random() * 0.01))

        run.log_metrics({"loss": loss, "acc": acc}, step=step)
        print(f"step={step:02d} loss={loss:.4f} acc={acc:.4f}")

        time.sleep(0.2)

    print("Done.")
    print("Dashboard:")
    print("  http://127.0.0.1:8000/ui")
    print("API docs:")
    print("  http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    main()