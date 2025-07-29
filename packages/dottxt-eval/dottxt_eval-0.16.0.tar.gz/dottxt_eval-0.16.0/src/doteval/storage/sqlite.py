import json
import sqlite3
import time
from typing import Optional

from doteval.metrics import registry
from doteval.models import Evaluation, EvaluationStatus, Record, Result, Score
from doteval.storage.base import Storage, _registry
from doteval.utils import deserialize_value, serialize_value

__all__ = ["SQLiteStorage"]


# Serialization functions moved to doteval.utils for reuse across storage backends


class SQLiteStorage(Storage):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Enable foreign keys (must be done for every connection)
            cursor.execute("PRAGMA foreign_keys = ON")

            # Experiments table (one row per experiment)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS experiments (
                    name TEXT PRIMARY KEY,
                    created_at REAL DEFAULT (unixepoch('now'))
                )
                """
            )

            # Evaluations table (one row per evaluation within an experiment)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluations (
                    id INTEGER PRIMARY KEY,
                    experiment_name TEXT,
                    evaluation_name TEXT,
                    status TEXT,
                    started_at REAL,
                    completed_at REAL,
                    metadata TEXT,
                    FOREIGN KEY(experiment_name) REFERENCES experiments(name) ON DELETE CASCADE,
                    UNIQUE(experiment_name, evaluation_name)
                )
                """
            )

            # Results table (one row per record)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    evaluation_id INTEGER,
                    item_id INTEGER,
                    dataset_row TEXT,
                    error TEXT,
                    timestamp REAL,
                    prompt TEXT,
                    model_response TEXT,
                    FOREIGN KEY(evaluation_id) REFERENCES evaluations(id) ON DELETE CASCADE
                )
                """
            )

            # Scores table (one row per score within a result)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY,
                    result_id INTEGER,
                    evaluator_name TEXT,
                    value TEXT,
                    metrics TEXT,
                    metadata TEXT,
                    FOREIGN KEY(result_id) REFERENCES results(id) ON DELETE CASCADE
                )
                """
            )

            # Create indexes for common queries
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_evaluations_experiment ON evaluations(experiment_name)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_results_evaluation_id ON results(evaluation_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_results_item_id ON results(item_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_scores_result_id ON scores(result_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_scores_evaluator ON scores(evaluator_name)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_scores_value ON scores(value)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_results_error ON results(error)"
            )

    def create_experiment(self, experiment_name: str):
        """Create an experiment. Idempotent - if experiment exists, do nothing."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(
                "INSERT OR IGNORE INTO experiments (name) VALUES (?)",
                (experiment_name,),
            )

    def delete_experiment(self, experiment_name: str):
        """Delete an experiment and all its evaluations."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("DELETE FROM experiments WHERE name = ?", (experiment_name,))
            if cursor.rowcount == 0:
                raise ValueError(f"Experiment '{experiment_name}' not found.")

    def rename_experiment(self, old_name: str, new_name: str):
        """Rename an experiment."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Temporarily disable foreign keys to allow renaming
            cursor.execute("PRAGMA foreign_keys = OFF")

            # Check if old experiment exists
            cursor.execute(
                "SELECT COUNT(*) FROM experiments WHERE name = ?", (old_name,)
            )
            if cursor.fetchone()[0] == 0:
                raise ValueError(f"Experiment '{old_name}' not found.")

            # Check if new name already exists
            cursor.execute(
                "SELECT COUNT(*) FROM experiments WHERE name = ?", (new_name,)
            )
            if cursor.fetchone()[0] > 0:
                raise ValueError(f"Experiment '{new_name}' already exists.")

            # Update evaluations first
            cursor.execute(
                "UPDATE evaluations SET experiment_name = ? WHERE experiment_name = ?",
                (new_name, old_name),
            )

            # Then rename experiment
            cursor.execute(
                "UPDATE experiments SET name = ? WHERE name = ?", (new_name, old_name)
            )

            # Re-enable foreign keys
            cursor.execute("PRAGMA foreign_keys = ON")

    def list_experiments(self) -> list[str]:
        """List all experiment names."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute("SELECT name FROM experiments ORDER BY created_at DESC")
            return [row[0] for row in cursor.fetchall()]

    def create_evaluation(self, experiment_name: str, evaluation: Evaluation):
        """Create an evaluation within an experiment."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            # Ensure experiment exists
            self.create_experiment(experiment_name)

            cursor.execute(
                """
                INSERT OR REPLACE INTO evaluations
                (experiment_name, evaluation_name, status, started_at, completed_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    experiment_name,
                    evaluation.evaluation_name,
                    evaluation.status.value,
                    evaluation.started_at,
                    evaluation.completed_at,
                    json.dumps(evaluation.metadata),
                ),
            )

    def load_evaluation(
        self, experiment_name: str, evaluation_name: str
    ) -> Optional[Evaluation]:
        """Load an evaluation by name."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(
                """
                SELECT status, started_at, completed_at, metadata
                FROM evaluations
                WHERE experiment_name = ? AND evaluation_name = ?
                """,
                (experiment_name, evaluation_name),
            )
            row = cursor.fetchone()
            if not row:
                return None

            status, started_at, completed_at, metadata_json = row
            return Evaluation(
                evaluation_name=evaluation_name,
                status=EvaluationStatus(status),
                started_at=started_at,
                completed_at=completed_at,
                metadata=json.loads(metadata_json),
            )

    def update_evaluation_status(
        self, experiment_name: str, evaluation_name: str, status: EvaluationStatus
    ):
        """Update the status of an evaluation."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            completed_at = (
                time.time()
                if status in (EvaluationStatus.COMPLETED, EvaluationStatus.FAILED)
                else None
            )

            cursor.execute(
                """
                UPDATE evaluations
                SET status = ?, completed_at = ?
                WHERE experiment_name = ? AND evaluation_name = ?
                """,
                (status.value, completed_at, experiment_name, evaluation_name),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Evaluation '{evaluation_name}' not found in experiment '{experiment_name}'."
                )

    def remove_error_result(
        self, experiment_name: str, evaluation_name: str, item_id: int
    ):
        """Remove an errored result for a specific item that will be retried."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            # Delete the error result for this item
            cursor.execute(
                """
                DELETE FROM results
                WHERE evaluation_id = (
                    SELECT id FROM evaluations
                    WHERE experiment_name = ? AND evaluation_name = ?
                )
                AND item_id = ?
                AND error IS NOT NULL
                """,
                (experiment_name, evaluation_name, item_id),
            )

    def remove_error_results_batch(
        self, experiment_name: str, evaluation_name: str, item_ids: list[int]
    ):
        """Remove multiple errored results efficiently in a single query."""
        if not item_ids:
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            # Create placeholders for the IN clause
            placeholders = ",".join("?" for _ in item_ids)

            # Delete all error results for the specified items in one query
            cursor.execute(
                f"""
                DELETE FROM results
                WHERE evaluation_id = (
                    SELECT id FROM evaluations
                    WHERE experiment_name = ? AND evaluation_name = ?
                )
                AND item_id IN ({placeholders})
                AND error IS NOT NULL
                """,
                (experiment_name, evaluation_name, *item_ids),
            )

    def completed_items(self, experiment_name: str, evaluation_name: str) -> list[int]:
        """Get list of completed item IDs for an evaluation."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(
                """
                SELECT r.item_id
                FROM results r
                JOIN evaluations e ON r.evaluation_id = e.id
                WHERE e.experiment_name = ? AND e.evaluation_name = ?
                AND r.error IS NULL
                ORDER BY r.item_id
                """,
                (experiment_name, evaluation_name),
            )
            return [row[0] for row in cursor.fetchall()]

    def list_evaluations(self, experiment_name: str) -> list[str]:
        """List all evaluation names within an experiment."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(
                """
                SELECT evaluation_name
                FROM evaluations
                WHERE experiment_name = ?
                ORDER BY started_at DESC
                """,
                (experiment_name,),
            )
            return [row[0] for row in cursor.fetchall()]

    def add_results(
        self,
        experiment_name: str,
        evaluation_name: str,
        results: list[Record],
    ):
        """Add results to an evaluation."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            # Get evaluation ID
            cursor.execute(
                """
                SELECT id FROM evaluations
                WHERE experiment_name = ? AND evaluation_name = ?
                """,
                (experiment_name, evaluation_name),
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(
                    f"Evaluation '{evaluation_name}' not found in experiment '{experiment_name}'."
                )
            evaluation_id = row[0]

            # Insert results and scores
            for result in results:
                cursor.execute(
                    """
                    INSERT INTO results (evaluation_id, item_id, dataset_row, error, timestamp, prompt, model_response)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        evaluation_id,
                        result.item_id,
                        json.dumps(serialize_value(result.dataset_row)),
                        result.error,
                        result.timestamp,
                        result.result.prompt,
                        result.result.model_response,
                    ),
                )
                result_id = cursor.lastrowid

                # Insert scores
                for score in result.result.scores:
                    cursor.execute(
                        """
                        INSERT INTO scores (result_id, evaluator_name, value, metrics, metadata)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            result_id,
                            score.name,
                            json.dumps(score.value),
                            json.dumps([m.__name__ for m in score.metrics]),
                            json.dumps(score.metadata),
                        ),
                    )

    def get_results(self, experiment_name: str, evaluation_name: str) -> list[Record]:
        """Get all results for an evaluation."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            # Get evaluation ID
            cursor.execute(
                """
                SELECT id FROM evaluations
                WHERE experiment_name = ? AND evaluation_name = ?
                """,
                (experiment_name, evaluation_name),
            )
            row = cursor.fetchone()
            if not row:
                return []
            evaluation_id = row[0]

            # Load results
            cursor.execute(
                """
                SELECT id, item_id, dataset_row, error, timestamp, prompt, model_response
                FROM results
                WHERE evaluation_id = ?
                ORDER BY item_id
                """,
                (evaluation_id,),
            )

            results = []
            for result_row in cursor.fetchall():
                (
                    result_id,
                    item_id,
                    dataset_row_json,
                    error,
                    timestamp,
                    prompt,
                    model_response,
                ) = result_row

                # Load scores for this result
                cursor.execute(
                    """
                    SELECT evaluator_name, value, metrics, metadata
                    FROM scores
                    WHERE result_id = ?
                    """,
                    (result_id,),
                )
                scores = []

                for score_row in cursor.fetchall():
                    (
                        evaluator_name,
                        value_json,
                        metrics_json,
                        metadata_json,
                    ) = score_row
                    metrics = [registry[name] for name in json.loads(metrics_json)]
                    score = Score(
                        name=evaluator_name,
                        value=json.loads(value_json),
                        metrics=metrics,
                        metadata=json.loads(metadata_json),
                    )
                    scores.append(score)

                result_obj = Result(
                    *scores, prompt=prompt, model_response=model_response
                )
                result = Record(
                    result=result_obj,
                    item_id=item_id,
                    dataset_row=deserialize_value(json.loads(dataset_row_json)),
                    error=error,
                    timestamp=timestamp,
                )
                results.append(result)

            return results

    # Query helper methods for error analysis

    def get_failed_results(
        self,
        experiment_name: str,
        evaluation_name: Optional[str] = None,
        evaluator_name: Optional[str] = None,
    ) -> list[dict]:
        """Get all failed results (score = False or 0) for an experiment."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            query = """
                SELECT
                    e.evaluation_name,
                    r.item_id,
                    r.dataset_row,
                    r.error,
                    r.timestamp,
                    s.evaluator_name,
                    s.value,
                    s.metadata
                FROM results r
                JOIN evaluations e ON r.evaluation_id = e.id
                JOIN scores s ON s.result_id = r.id
                WHERE e.experiment_name = ?
                AND (s.value = 'false' OR s.value = '0' OR s.value = '0.0')
            """
            params = [experiment_name]

            if evaluation_name:
                query += " AND e.evaluation_name = ?"
                params.append(evaluation_name)

            if evaluator_name:
                query += " AND s.evaluator_name = ?"
                params.append(evaluator_name)

            query += " ORDER BY e.evaluation_name, r.item_id"

            cursor.execute(query, params)

            results = []
            for row in cursor.fetchall():
                results.append(
                    {
                        "evaluation_name": row[0],
                        "item_id": row[1],
                        "dataset_row": deserialize_value(json.loads(row[2])),
                        "error": row[3],
                        "timestamp": row[4],
                        "evaluator_name": row[5],
                        "value": json.loads(row[6]),
                        "metadata": json.loads(row[7]),
                    }
                )

            return results

    def get_error_results(
        self, experiment_name: str, evaluation_name: Optional[str] = None
    ) -> list[dict]:
        """Get all results that had errors during evaluation."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            query = """
                SELECT
                    e.evaluation_name,
                    r.item_id,
                    r.dataset_row,
                    r.error,
                    r.timestamp
                FROM results r
                JOIN evaluations e ON r.evaluation_id = e.id
                WHERE e.experiment_name = ?
                AND r.error IS NOT NULL
            """
            params = [experiment_name]

            if evaluation_name:
                query += " AND e.evaluation_name = ?"
                params.append(evaluation_name)

            query += " ORDER BY e.evaluation_name, r.item_id"

            cursor.execute(query, params)

            results = []
            for row in cursor.fetchall():
                results.append(
                    {
                        "evaluation_name": row[0],
                        "item_id": row[1],
                        "dataset_row": deserialize_value(json.loads(row[2])),
                        "error": row[3],
                        "timestamp": row[4],
                    }
                )

            return results


# Register the SQLite backend
_registry.register("sqlite", SQLiteStorage)
