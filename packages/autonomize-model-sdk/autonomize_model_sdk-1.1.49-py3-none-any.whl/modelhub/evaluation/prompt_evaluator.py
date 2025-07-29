"""Simplified prompt evaluation using Evidently for offline evaluation."""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Literal, Optional

import pandas as pd

try:
    from evidently import DataDefinition, Dataset, Report
    from evidently.descriptors import SentenceCount, Sentiment, TextLength, WordCount
    from evidently.metrics import ColumnCount, MeanValue, RowCount, UniqueValueCount

    EVIDENTLY_AVAILABLE = True

    # Check for LLM descriptors (may not be available in all versions)
    LLM_DESCRIPTORS_AVAILABLE = False
    try:
        pass

        LLM_DESCRIPTORS_AVAILABLE = True
    except ImportError:
        pass

except ImportError:
    # Mock imports for graceful degradation
    Report = None
    Dataset = None
    DataDefinition = None
    TextLength = None
    WordCount = None
    SentenceCount = None
    Sentiment = None
    ColumnCount = None
    RowCount = None
    MeanValue = None
    UniqueValueCount = None
    EVIDENTLY_AVAILABLE = False
    LLM_DESCRIPTORS_AVAILABLE = False

from ..models.prompts import Message
from ..utils import setup_logger

logger = setup_logger(__name__)


@dataclass
class EvaluationConfig:
    """Configuration for prompt evaluation."""

    evaluations: List[Literal["quality", "safety", "correctness", "metrics"]] = field(
        default_factory=lambda: ["quality", "safety", "metrics"]
    )
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    save_html: bool = True
    save_json: bool = True
    output_dir: str = "./evaluation_reports"
    include_reasoning: bool = True
    batch_size: int = 10
    custom_descriptors: Optional[List[Any]] = None


@dataclass
class EvaluationReport:
    """Report containing evaluation results."""

    config: EvaluationConfig
    timestamp: datetime
    metrics: Dict[str, Any]
    summary: Dict[str, Any]
    html_path: Optional[str] = None
    json_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "config": {
                "evaluations": self.config.evaluations,
                "llm_provider": self.config.llm_provider,
                "llm_model": self.config.llm_model,
                "output_dir": self.config.output_dir,
            },
            "metrics": self.metrics,
            "summary": self.summary,
            "html_path": self.html_path,
            "json_path": self.json_path,
        }


class PromptEvaluator:
    """
    Simplified prompt evaluator using Evidently for offline evaluation.

    This class provides offline evaluation capabilities for prompt engineering,
    focusing on basic metrics that don't require LLM calls for quick development feedback.
    """

    def __init__(self, config: Optional[EvaluationConfig] = None):
        """
        Initialize the prompt evaluator.

        Args:
            config: Evaluation configuration. If None, uses default config.
        """
        if not EVIDENTLY_AVAILABLE:
            raise ImportError(
                "Evidently library is not available. "
                "Please install evidently with: pip install evidently"
            )

        self.config = config or EvaluationConfig()

        # Create output directory if it doesn't exist
        if not os.path.exists(self.config.output_dir):
            os.makedirs(self.config.output_dir)

    def _validate_data(
        self,
        data: pd.DataFrame,
        prompt_col: str,
        response_col: str,
        reference_col: Optional[str],
        context_col: Optional[str],
    ) -> None:
        """Validate input data."""
        if data.empty:
            raise ValueError("Data cannot be empty")

        required_columns = [prompt_col, response_col]
        optional_columns = [
            col for col in [reference_col, context_col] if col is not None
        ]
        all_columns = required_columns + optional_columns

        missing_columns = [col for col in all_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    def evaluate_offline(
        self,
        data: pd.DataFrame,
        prompt_col: str = "prompt",
        response_col: str = "response",
        reference_col: Optional[str] = None,
        context_col: Optional[str] = None,
    ) -> EvaluationReport:
        """
        Evaluate prompts offline using basic Evidently metrics.

        Args:
            data: DataFrame with prompt data
            prompt_col: Column name containing prompts
            response_col: Column name containing responses
            reference_col: Optional column with reference responses
            context_col: Optional column with context

        Returns:
            EvaluationReport with basic metrics
        """
        logger.info(f"Starting offline evaluation with {len(data)} samples")

        # Validate input data
        self._validate_data(data, prompt_col, response_col, reference_col, context_col)

        # Prepare data with basic text metrics
        eval_data = data.copy()

        # Add text length metrics
        text_columns = [prompt_col, response_col]
        if reference_col:
            text_columns.append(reference_col)
        if context_col:
            text_columns.append(context_col)

        for col in text_columns:
            eval_data[f"{col}_length"] = eval_data[col].str.len()
            eval_data[f"{col}_word_count"] = eval_data[col].str.split().str.len()

        # Use only very basic metrics that are guaranteed to work
        metrics = [
            RowCount(),
            ColumnCount(),
        ]

        # Add safe numeric metrics only for length columns
        length_columns = []
        for col in text_columns:
            length_col = f"{col}_length"
            word_col = f"{col}_word_count"
            length_columns.extend([length_col, word_col])

            # Add metrics for these numeric columns
            metrics.extend(
                [
                    MeanValue(column=length_col),
                    MeanValue(column=word_col),
                ]
            )

        # Create dataset with only length columns (numeric) to avoid text column issues
        numeric_data = eval_data[length_columns].copy()

        # Create simple dataset without complex data definition
        dataset = Dataset.from_pandas(numeric_data)

        # Create and run report
        report = Report(metrics=metrics)
        report.run(dataset)

        # Extract basic results - simplified since evidently API changed
        metrics_dict = self._extract_basic_metrics_simple(eval_data, text_columns)

        # Generate summary
        summary = {
            "total_samples": len(data),
            "evaluations_run": ["metrics"],  # Only basic metrics for now
            "timestamp": datetime.now().isoformat(),
            "text_columns_analyzed": text_columns,
            "basic_stats": {
                "avg_prompt_length": eval_data[f"{prompt_col}_length"].mean(),
                "avg_response_length": eval_data[f"{response_col}_length"].mean(),
                "avg_prompt_words": eval_data[f"{prompt_col}_word_count"].mean(),
                "avg_response_words": eval_data[f"{response_col}_word_count"].mean(),
            },
        }

        # Save reports
        html_path, json_path = self._save_reports(report, summary, metrics_dict)

        return EvaluationReport(
            config=self.config,
            timestamp=datetime.now(),
            metrics=metrics_dict,
            summary=summary,
            html_path=html_path,
            json_path=json_path,
        )

    def _extract_basic_metrics_simple(
        self, eval_data: pd.DataFrame, text_columns: List[str]
    ) -> Dict[str, Any]:
        """Extract basic metrics directly from data since evidently API is complex."""
        metrics = {}

        try:
            # Basic dataset metrics
            metrics["total_rows"] = len(eval_data)
            metrics["total_columns"] = len(eval_data.columns)

            # Calculate text metrics directly
            for col in text_columns:
                length_col = f"{col}_length"
                word_col = f"{col}_word_count"

                if length_col in eval_data.columns:
                    metrics[f"mean_{length_col}"] = float(eval_data[length_col].mean())
                    metrics[f"min_{length_col}"] = float(eval_data[length_col].min())
                    metrics[f"max_{length_col}"] = float(eval_data[length_col].max())

                if word_col in eval_data.columns:
                    metrics[f"mean_{word_col}"] = float(eval_data[word_col].mean())
                    metrics[f"min_{word_col}"] = float(eval_data[word_col].min())
                    metrics[f"max_{word_col}"] = float(eval_data[word_col].max())

                # Text uniqueness
                if col in eval_data.columns:
                    metrics[f"unique_{col}"] = int(eval_data[col].nunique())

        except Exception as e:
            logger.warning(f"Error calculating metrics: {e}")

        return metrics

    def _extract_basic_metrics(
        self, report_dict: Dict, text_columns: List[str]
    ) -> Dict[str, Any]:
        """Legacy method - kept for backward compatibility."""
        return self._extract_basic_metrics_simple(pd.DataFrame(), text_columns)

    def _save_reports(
        self, report: Report, summary: Dict[str, Any], metrics: Dict[str, Any]
    ) -> tuple[Optional[str], Optional[str]]:
        """Save HTML and JSON reports."""
        html_path = None
        json_path = None
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        try:
            if self.config.save_html:
                html_path = os.path.join(
                    self.config.output_dir, f"evaluation_report_{timestamp_str}.html"
                )

                # Create simple HTML report since evidently save_html is not available
                html_content = self._create_simple_html_report(summary, metrics)
                with open(html_path, "w") as f:
                    f.write(html_content)
                logger.info(f"HTML report saved to: {html_path}")

            if self.config.save_json:
                json_path = os.path.join(
                    self.config.output_dir, f"evaluation_report_{timestamp_str}.json"
                )

                report_data = {
                    "timestamp": summary["timestamp"],
                    "summary": summary,
                    "metrics": metrics,
                    "config": {
                        "evaluations": self.config.evaluations,
                        "output_dir": self.config.output_dir,
                    },
                }

                with open(json_path, "w") as f:
                    json.dump(report_data, f, indent=2)
                logger.info(f"JSON report saved to: {json_path}")

        except Exception as e:
            logger.error(f"Error saving reports: {e}")

        return html_path, json_path

    def _create_simple_html_report(
        self, summary: Dict[str, Any], metrics: Dict[str, Any]
    ) -> str:
        """Create a simple HTML report."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Prompt Evaluation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; }}
                .metric {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-radius: 3px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Prompt Evaluation Report</h1>
                <p>Generated: {summary.get('timestamp', 'Unknown')}</p>
                <p>Total Samples: {summary.get('total_samples', 0)}</p>
            </div>

            <div class="section">
                <h2>Basic Statistics</h2>
                <table>
                    <tr><th>Metric</th><th>Value</th></tr>
        """

        # Add basic stats
        basic_stats = summary.get("basic_stats", {})
        for key, value in basic_stats.items():
            html += f"<tr><td>{key}</td><td>{value:.2f}</td></tr>"

        html += "</table></div><div class='section'><h2>Detailed Metrics</h2><table><tr><th>Metric</th><th>Value</th></tr>"

        # Add detailed metrics
        for key, value in metrics.items():
            if isinstance(value, float):
                html += f"<tr><td>{key}</td><td>{value:.2f}</td></tr>"
            elif isinstance(value, int):
                html += f"<tr><td>{key}</td><td>{value}</td></tr>"
            else:
                html += f"<tr><td>{key}</td><td>{str(value)}</td></tr>"

        html += """
                </table>
            </div>
        </body>
        </html>
        """

        return html

    def _create_data_definition(
        self,
        prompt_col: str,
        response_col: str,
        reference_col: Optional[str],
        context_col: Optional[str],
    ) -> DataDefinition:
        """Create data definition for Evidently."""
        text_columns = [prompt_col, response_col]
        if reference_col:
            text_columns.append(reference_col)
        if context_col:
            text_columns.append(context_col)

        return DataDefinition(text_columns=text_columns)

    def evaluate_prompt_template(
        self,
        prompt_template: List[Message],
        test_data: pd.DataFrame,
        variables_col: str = "variables",
        expected_col: Optional[str] = None,
        llm_generate_func: Optional[Callable[[str], str]] = None,
    ) -> EvaluationReport:
        """
        Evaluate a prompt template with test data.

        Args:
            prompt_template: List of Message objects forming the template
            test_data: DataFrame with test cases
            variables_col: Column containing variable dictionaries
            expected_col: Optional column with expected responses
            llm_generate_func: Function to generate responses from prompts

        Returns:
            EvaluationReport with evaluation results
        """
        logger.info(f"Evaluating prompt template with {len(test_data)} test cases")

        # Generate prompts from template
        prompts = []
        responses = []

        for _, row in test_data.iterrows():
            variables = row[variables_col]
            formatted_prompt = self._format_template(prompt_template, variables)
            prompts.append(formatted_prompt)

            if llm_generate_func:
                response = llm_generate_func(formatted_prompt)
                responses.append(response)
            else:
                responses.append("No LLM function provided")

        # Create evaluation data
        eval_data = pd.DataFrame(
            {
                "prompt": prompts,
                "response": responses,
            }
        )

        if expected_col and expected_col in test_data.columns:
            eval_data["expected"] = test_data[expected_col].values
            return self.evaluate_offline(eval_data, reference_col="expected")
        else:
            return self.evaluate_offline(eval_data)

    def _format_template(
        self, template: List[Message], variables: Dict[str, str]
    ) -> str:
        """Format a prompt template with variables."""
        formatted_parts = []

        for message in template:
            text = message.content.text

            # Replace variables in the text
            for var_name in message.input_variables:
                if var_name in variables:
                    placeholder = f"{{{{{var_name}}}}}"
                    text = text.replace(placeholder, variables[var_name])

            formatted_parts.append(f"{message.role}: {text}")

        return "\n".join(formatted_parts)
