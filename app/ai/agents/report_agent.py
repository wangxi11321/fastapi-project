import os
from datetime import date
from typing import List, Dict, Any
from app.models.daily_reports import DailyReport
from app.models.feedback_tickets import FeedbackTicket
from app.ai.tools.report_generator import ReportGeneratorTool
from app.core.logger import logger

class ReportAgent:
    def __init__(self):
        self.generator_tool = ReportGeneratorTool()
        self.daily_prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/report_summary.txt")
        self.weekly_prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/weekly_summary.txt")

    def load_daily_prompt(self) -> str:
        if os.path.exists(self.daily_prompt_path):
            with open(self.daily_prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return self._get_default_daily_prompt()

    def load_weekly_prompt(self) -> str:
        if os.path.exists(self.weekly_prompt_path):
            with open(self.weekly_prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return self._get_default_weekly_prompt()

    def _get_default_daily_prompt(self) -> str:
        return """
你是一个专业的日报汇总分析师。请根据以下日报内容，生成一份简洁、专业的汇总报告。

日报汇总格式要求：
1. 标题：明确标注日期范围
2. 概览：报告总数、参与人员
3. 今日完成：汇总所有完成的工作
4. 明日计划：汇总所有计划任务
5. 需要关注的问题：汇总所有待解决问题

请使用markdown格式输出，语言简洁明了。

日报内容：
{daily_reports}
        """.strip()

    def _get_default_weekly_prompt(self) -> str:
        return """
你是一个专业的周报汇总分析师。请根据以下一周的日报内容，生成一份详细的周报汇总报告。

周报汇总格式要求：
1. 标题：明确标注周范围（如：2024-01-01 ~ 2024-01-07）
2. 概览：报告总数、参与人员、整体工作概况
3. 工作完成情况：按人员分组汇总完成的工作
4. 工作计划执行率：评估计划完成情况
5. 问题与风险：汇总所有待解决问题和潜在风险
6. 下周重点工作：总结需要重点关注的工作

请使用markdown格式输出，语言简洁专业。

日报内容：
{daily_reports}
        """.strip()

    def generate_daily_summary(self, reports: List[DailyReport]) -> str:
        logger.info(f"Generating daily summary for {len(reports)} reports")
        return self.generator_tool.generate_daily_summary(reports)

    def generate_weekly_summary(self, reports: List[DailyReport]) -> str:
        logger.info(f"Generating weekly summary for {len(reports)} reports")
        return self.generator_tool.generate_weekly_summary(reports)

    def generate_complaint_report(self, tickets: List[FeedbackTicket]) -> str:
        logger.info(f"Generating complaint report for {len(tickets)} tickets")
        return self.generator_tool.generate_complaint_report(tickets)