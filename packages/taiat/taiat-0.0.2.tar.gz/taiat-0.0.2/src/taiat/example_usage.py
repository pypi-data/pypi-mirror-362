#!/usr/bin/env python3
"""
Example usage of the Taiat job manager.

This script demonstrates how to:
1. Create jobs with dependencies
2. Monitor job status
3. Use the job manager programmatically

Usage:
    python example_usage.py [--database-url DATABASE_URL]
"""

import argparse
import logging
import os
import sys
import time
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .init_worker import get_database_url, setup_logging, test_connection
from .job_manager import JobManager, JobPriority, JobType


def setup_job_manager(database_url: str) -> JobManager:
    """Setup job manager with database connection."""
    engine = create_engine(database_url)
    if not test_connection(engine):
        raise RuntimeError("Cannot connect to database")

    session_maker = sessionmaker(bind=engine)
    return JobManager(session_maker)


def create_example_jobs(job_manager: JobManager):
    """Create example jobs with dependencies."""
    logger = logging.getLogger(__name__)

    # Job 1: Data preprocessing
    logger.info("Creating data preprocessing job...")
    job1 = job_manager.create_job(
        job_type=JobType.AGENT,
        name="data_preprocessing",
        description="Preprocess the input data",
        payload={
            "agent_name": "data_preprocessor",
            "parameters": {
                "input_file": "data.csv",
                "output_file": "processed_data.csv",
                "normalize": True,
            },
        },
        priority=JobPriority.HIGH,
    )
    logger.info(f"Created job: {job1.id}")

    # Job 2: Feature extraction (depends on preprocessing)
    logger.info("Creating feature extraction job...")
    job2 = job_manager.create_job(
        job_type=JobType.AGENT,
        name="feature_extraction",
        description="Extract features from preprocessed data",
        payload={
            "agent_name": "feature_extractor",
            "parameters": {
                "input_file": "processed_data.csv",
                "output_file": "features.csv",
                "feature_types": ["numerical", "categorical"],
            },
        },
        dependencies=[job1.id],
        priority=JobPriority.NORMAL,
    )
    logger.info(f"Created job: {job2.id}")

    # Job 3: Model training (depends on feature extraction)
    logger.info("Creating model training job...")
    job3 = job_manager.create_job(
        job_type=JobType.AGENT,
        name="model_training",
        description="Train machine learning model",
        payload={
            "agent_name": "model_trainer",
            "parameters": {
                "input_file": "features.csv",
                "model_type": "random_forest",
                "output_file": "model.pkl",
            },
        },
        dependencies=[job2.id],
        priority=JobPriority.NORMAL,
    )
    logger.info(f"Created job: {job3.id}")

    # Job 4: Query job (depends on model training)
    logger.info("Creating query job...")
    job4 = job_manager.create_job(
        job_type=JobType.QUERY,
        name="model_evaluation",
        description="Evaluate the trained model",
        payload={
            "query": "Evaluate the performance of the trained model on test data",
            "inferred_goal_output": "Model evaluation report with metrics",
        },
        dependencies=[job3.id],
        priority=JobPriority.LOW,
    )
    logger.info(f"Created job: {job4.id}")

    return [job1, job2, job3, job4]


def monitor_jobs(job_manager: JobManager, job_ids: list[str], duration: int = 60):
    """Monitor job status for a specified duration."""
    logger = logging.getLogger(__name__)

    start_time = time.time()
    while time.time() - start_time < duration:
        print("\n" + "=" * 50)
        print(f"Job Status at {time.strftime('%H:%M:%S')}")
        print("=" * 50)

        for job_id in job_ids:
            job = job_manager.get_job(job_id)
            if job:
                status_icon = {
                    "pending": "⏳",
                    "running": "🔄",
                    "completed": "✅",
                    "failed": "❌",
                    "cancelled": "🚫",
                }.get(job.status.value, "❓")

                print(f"{status_icon} {job.name}: {job.status.value}")
                if job.error_message:
                    print(f"    Error: {job.error_message}")
                if job.result:
                    print(f"    Result: {job.result}")
            else:
                print(f"❓ Job {job_id}: Not found (may be in history)")

        # Check if all jobs are completed
        all_completed = True
        for job_id in job_ids:
            job = job_manager.get_job(job_id)
            if job and job.status.value not in ["completed", "failed", "cancelled"]:
                all_completed = False
                break

        if all_completed:
            print("\n🎉 All jobs completed!")
            break

        time.sleep(5)  # Wait 5 seconds before next check


def show_job_history(job_manager: JobManager):
    """Show recent job history."""
    logger = logging.getLogger(__name__)

    history = job_manager.get_job_history(limit=10)

    print("\n" + "=" * 50)
    print("Recent Job History")
    print("=" * 50)

    if not history:
        print("No job history found.")
        return

    for entry in history:
        status_icon = "✅" if entry.status.value == "completed" else "❌"
        duration = f" ({entry.duration_seconds:.1f}s)" if entry.duration_seconds else ""

        print(
            f"{status_icon} {entry.job_id}: {entry.name} ({entry.status.value}){duration}"
        )
        if entry.error_message:
            print(f"    Error: {entry.error_message}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Example usage of Taiat job manager")
    parser.add_argument(
        "--database-url",
        help="Database connection URL (defaults to TAIAT_DATABASE_URL env var or localhost/taiat)",
    )
    parser.add_argument(
        "--monitor-duration",
        type=int,
        default=60,
        help="Duration to monitor jobs in seconds (default: 60)",
    )
    parser.add_argument(
        "--show-history", action="store_true", help="Show job history and exit"
    )

    args = parser.parse_args()

    # Get database URL
    database_url = args.database_url or get_database_url()

    try:
        # Setup job manager
        job_manager = setup_job_manager(database_url)

        if args.show_history:
            show_job_history(job_manager)
            return

        # Create example jobs
        print("Creating example jobs with dependencies...")
        jobs = create_example_jobs(job_manager)
        job_ids = [job.id for job in jobs]

        print(f"\nCreated {len(jobs)} jobs:")
        for job in jobs:
            deps = ", ".join(job.dependencies) if job.dependencies else "none"
            print(f"  - {job.name} (ID: {job.id}, Dependencies: {deps})")

        # Monitor jobs
        print(f"\nMonitoring jobs for {args.monitor_duration} seconds...")
        print(
            "(You can start the worker in another terminal with: python -m taiat.run_worker)"
        )
        monitor_jobs(job_manager, job_ids, args.monitor_duration)

        # Show final history
        show_job_history(job_manager)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
