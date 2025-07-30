import logging
import json
import re
import os
import sys
import importlib.util
from typing import List, Dict, Any, Optional
from collections import defaultdict

from .llm_providers import get_llm_provider
# # --- Import the new prompt template ---
# from chatbot_test_framework.default_configs.prompts import (
#     STEP_EVALUATION_PROMPT, 
#     FINAL_ANSWER_EVALUATION_PROMPT, 
#     CUSTOM_POLICIES,
#     DEEP_DIVE_SUMMARY_PROMPT
# )

logger = logging.getLogger(__name__)

class PerformanceEvaluator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm_provider = get_llm_provider(config['llm_provider'])
        self.workflow_description = config['workflow_description']

        self._load_prompts_from_config()

    def _load_prompts_from_config(self):
        """Dynamically loads prompts and policies from the user-specified file."""
        prompts_path = self.config.get('prompts_path')
        if not prompts_path:
            raise ValueError("Configuration error: 'prompts_path' is missing from the [evaluation] section.")

        # Resolve the path relative to the current working directory
        absolute_path = os.path.abspath(prompts_path)
        logger.info(f"Loading custom prompts from: {absolute_path}")

        if not os.path.exists(absolute_path):
            raise FileNotFoundError(f"Prompts file not found at the specified path: {absolute_path}")

        try:
            # Use importlib to load the file as a module
            spec = importlib.util.spec_from_file_location("user_prompts", absolute_path)
            user_prompts_module = importlib.util.module_from_spec(spec)
            sys.modules["user_prompts"] = user_prompts_module
            spec.loader.exec_module(user_prompts_module)

            # Store the loaded variables as instance attributes
            self.CUSTOM_POLICIES = getattr(user_prompts_module, 'CUSTOM_POLICIES')
            self.STEP_EVALUATION_PROMPT = getattr(user_prompts_module, 'STEP_EVALUATION_PROMPT')
            self.FINAL_ANSWER_EVALUATION_PROMPT = getattr(user_prompts_module, 'FINAL_ANSWER_EVALUATION_PROMPT')
            self.DEEP_DIVE_SUMMARY_PROMPT = getattr(user_prompts_module, 'DEEP_DIVE_SUMMARY_PROMPT')
        except (AttributeError, FileNotFoundError) as e:
            logger.error(f"Failed to load prompts from '{absolute_path}'. Make sure the file exists and contains all required prompt variables.")
            raise e

    def _extract_json_from_response(self, text: str) -> str:
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def evaluate_trace(self, trace_data: List[Dict[str, Any]], original_question: str, model_answer: Optional[str]) -> Dict[str, Any]:
        # This method remains the same as the previous version.
        # It performs the individual evaluations that will be used as input for the deep dive.
        report = {"step_evaluations": []}
        if not trace_data:
            logger.warning("Cannot evaluate trace: trace data is empty.")
            return report

        sorted_trace = sorted(trace_data, key=lambda x: x.get('start_time', 0))

        for step in sorted_trace:
            step_name = step.get('name', 'Unknown Step')
            logger.info(f"  - Evaluating step: {step_name}")
            prompt = self.STEP_EVALUATION_PROMPT.format(
                workflow_description=self.workflow_description, original_question=original_question, step_name=step_name,
                step_inputs=json.dumps(step.get('inputs', 'N/A'), indent=2, default=str),
                step_outputs=json.dumps(step.get('outputs', 'N/A'), indent=2, default=str)
            )
            try:
                raw_response = self.llm_provider.invoke(prompt)
                json_str = self._extract_json_from_response(raw_response)
                llm_eval = json.loads(json_str)
                report["step_evaluations"].append({
                    "session_id": step.get('run_id'), "step_name": step_name, "evaluation": llm_eval
                })
            except Exception as e:
                logger.error(f"Failed to evaluate step '{step_name}'. Error: {e}")
                report["step_evaluations"].append({
                    "session_id": step.get('run_id'), "step_name": step_name,
                    "evaluation": {"error": f"LLM evaluation failed. Details: {str(e)}"}
                })
        
        if model_answer:
            final_step = sorted_trace[-1]
            chatbot_final_output = final_step.get('outputs', {})
            if isinstance(chatbot_final_output, str) and chatbot_final_output:
                chatbot_answer_str = chatbot_final_output
            elif isinstance(chatbot_final_output, dict) and 'final_answer' in chatbot_final_output:
                chatbot_answer_str = chatbot_final_output.get('final_answer', str(chatbot_final_output))
            else:
                chatbot_answer_str = str(chatbot_final_output)
                
            policies_str = "\n     ".join(f"{i+1}. {policy}" for i, policy in enumerate(self.CUSTOM_POLICIES))
            logger.info(f"  - Performing sophisticated evaluation of final answer.")
            prompt = self.FINAL_ANSWER_EVALUATION_PROMPT.format(
                original_question=original_question, model_answer=model_answer,
                chatbot_answer=chatbot_answer_str, policies=policies_str
            )
            try:
                raw_response = self.llm_provider.invoke(prompt)
                json_str = self._extract_json_from_response(raw_response)
                llm_eval = json.loads(json_str)
                report["final_answer_evaluation"] = {
                    "session_id": final_step.get('run_id'), "original_question": original_question,
                    "model_answer": model_answer, "chatbot_answer": chatbot_answer_str, "evaluation": llm_eval
                }
            except Exception as e:
                logger.error(f"Failed to evaluate final answer. Error: {e}")
                report["final_answer_evaluation"] = {
                    "session_id": final_step.get('run_id'), "original_question": original_question,
                    "evaluation": {"error": f"LLM evaluation failed. Details: {str(e)}"}
                }
        return report

    def _generate_deep_dive_summary(self, all_step_evaluations: List[Dict]) -> str:
        """
        Uses an LLM to generate a qualitative deep-dive summary from all step evaluations.
        """
        logger.info("Generating deep-dive performance summary...")
        
        # 1. Pre-process the raw step evaluation data into a concise summary
        step_analysis = defaultdict(lambda: {
            'correctness_scores': [], 
            'relevance_scores': [],
            'failure_reasons': []
        })

        for eval_item in all_step_evaluations:
            step_name = eval_item['step_name']
            eval_data = eval_item.get('evaluation', {})
            if 'error' in eval_data:
                continue

            correctness = eval_data.get('correctness', {})
            relevance = eval_data.get('relevance', {})

            if (score := correctness.get('score')) is not None:
                step_analysis[step_name]['correctness_scores'].append(score)
                if score < 4: # Consider a score below 4 a notable failure
                    step_analysis[step_name]['failure_reasons'].append(correctness.get('reasoning', 'No reasoning provided.'))

            if (score := relevance.get('score')) is not None:
                step_analysis[step_name]['relevance_scores'].append(score)
                if score < 4 and (reasoning := relevance.get('reasoning')):
                     # Avoid duplicate reasons if both scores are low
                    if reasoning not in step_analysis[step_name]['failure_reasons']:
                        step_analysis[step_name]['failure_reasons'].append(reasoning)

        # 2. Format the processed data into a string for the prompt
        summary_for_prompt = []
        for step_name, data in sorted(step_analysis.items()):
            c_scores = data['correctness_scores']
            r_scores = data['relevance_scores']
            avg_c = f"{sum(c_scores) / len(c_scores):.2f}" if c_scores else "N/A"
            avg_r = f"{sum(r_scores) / len(r_scores):.2f}" if r_scores else "N/A"

            summary_for_prompt.append(f"### Step: {step_name}")
            summary_for_prompt.append(f"- Average Correctness Score: {avg_c} / 5.0")
            summary_for_prompt.append(f"- Average Relevance Score: {avg_r} / 5.0")
            
            if data['failure_reasons']:
                summary_for_prompt.append("- Examples of Failure Reasons:")
                # Limit to 5 unique reasons to keep the prompt concise
                unique_reasons = list(set(data['failure_reasons']))
                for reason in unique_reasons[:5]:
                    summary_for_prompt.append(f"  - \"{reason}\"")
            summary_for_prompt.append("\n")

        # 3. Create the final prompt and invoke the LLM
        prompt = self.DEEP_DIVE_SUMMARY_PROMPT.format(step_data_summary="\n".join(summary_for_prompt))
        
        try:
            deep_dive_text = self.llm_provider.invoke(prompt)
            return deep_dive_text
        except Exception as e:
            logger.error(f"Failed to generate deep-dive summary from LLM: {e}")
            return "Error: The deep-dive summary could not be generated due to an LLM provider error."

    def generate_overall_summary(self, all_step_evaluations: List[Dict], all_final_evaluations: List[Dict]) -> str:
        """Generates the complete summary, including metrics, violations, and the deep-dive analysis."""
        report_lines = ["# Performance Evaluation Summary\n"]
        
        # --- Section 1: Final Answer Violations (from previous step) ---
        if all_final_evaluations:
            # (Safety and Policy violation reporting logic remains here)
            report_lines.append("\n## 🚨 Safety Violations (Score < 5)\n")
            safety_violations = [f for f in all_final_evaluations if f.get('evaluation', {}).get('safety', {}).get('score', 5) < 5]
            if not safety_violations:
                report_lines.append("- ✅ No safety violations detected.")
            else:
                # ... (error reporting logic) ...
                pass 
            
            report_lines.append("\n## 📜 Policy Adherence Issues (Score < 5)\n")
            policy_violations = [f for f in all_final_evaluations if f.get('evaluation', {}).get('policy_adherence', {}).get('score', 5) < 5]
            if not policy_violations:
                report_lines.append("- ✅ No policy violations detected.")
            else:
                # ... (error reporting logic) ...
                pass

        # --- Section 2: LLM-Generated Deep Dive Analysis ---
        if all_step_evaluations:
            report_lines.append("\n# Deep Dive Workflow Analysis\n")
            deep_dive_report = self._generate_deep_dive_summary(all_step_evaluations)
            report_lines.append(deep_dive_report)
        
        return "\n".join(report_lines)