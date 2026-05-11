from datetime import date, timedelta
from typing import List, Dict, Any
from app.models.daily_reports import DailyReport
from app.models.feedback_tickets import FeedbackTicket

class ReportGeneratorTool:
    @staticmethod
    def generate_daily_summary(reports: List[DailyReport]) -> str:
        if not reports:
            return "今日暂无日报数据"
        
        summary_lines = []
        summary_lines.append(f"📊 日报汇总 ({date.today().strftime('%Y-%m-%d')})")
        summary_lines.append(f"---")
        summary_lines.append(f"共收到 {len(reports)} 份日报")
        
        tasks_done = []
        tasks_tomorrow = []
        issues = []
        
        for report in reports:
            summary_lines.append(f"\n👤 {report.employee_name}")
            if report.summary:
                summary_lines.append(f"  工作总结: {report.summary}")
            if report.tasks_done:
                tasks_done.append(f"- {report.employee_name}: {report.tasks_done}")
            if report.tasks_tomorrow:
                tasks_tomorrow.append(f"- {report.employee_name}: {report.tasks_tomorrow}")
            if report.issues:
                issues.append(f"- {report.employee_name}: {report.issues}")
        
        if tasks_done:
            summary_lines.append("\n✅ 今日完成:")
            summary_lines.extend(tasks_done)
        
        if tasks_tomorrow:
            summary_lines.append("\n📋 明日计划:")
            summary_lines.extend(tasks_tomorrow)
        
        if issues:
            summary_lines.append("\n⚠️ 需要关注的问题:")
            summary_lines.extend(issues)
        
        return "\n".join(summary_lines)

    @staticmethod
    def generate_weekly_summary(reports: List[DailyReport]) -> str:
        if not reports:
            return "本周暂无日报数据"
        
        summary_lines = []
        start_date = min(r.date for r in reports)
        end_date = max(r.date for r in reports)
        
        summary_lines.append(f"📈 周报汇总 ({start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')})")
        summary_lines.append(f"---")
        summary_lines.append(f"共收到 {len(reports)} 份日报")
        
        employee_reports = {}
        for report in reports:
            if report.employee_name not in employee_reports:
                employee_reports[report.employee_name] = []
            employee_reports[report.employee_name].append(report)
        
        summary_lines.append(f"\n👥 参与人员: {', '.join(employee_reports.keys())}")
        
        for emp_name, emp_reports in employee_reports.items():
            summary_lines.append(f"\n👤 {emp_name} ({len(emp_reports)}份)")
            for r in emp_reports:
                summary_lines.append(f"  • {r.date.strftime('%m-%d')}: {r.summary[:50]}..." if r.summary else f"  • {r.date.strftime('%m-%d')}: 无总结")
        
        return "\n".join(summary_lines)

    @staticmethod
    def generate_complaint_report(tickets: List[FeedbackTicket]) -> str:
        if not tickets:
            return "暂无投诉数据"
        
        summary_lines = []
        summary_lines.append(f"🔴 投诉处理周报")
        summary_lines.append(f"---")
        summary_lines.append(f"共 {len(tickets)} 条投诉")
        
        status_counts = {}
        type_counts = {}
        
        for ticket in tickets:
            status_counts[ticket.status] = status_counts.get(ticket.status, 0) + 1
            type_counts[ticket.type] = type_counts.get(ticket.type, 0) + 1
        
        summary_lines.append("\n📊 状态分布:")
        for status, count in status_counts.items():
            summary_lines.append(f"  • {status}: {count}条")
        
        summary_lines.append("\n🏷️ 投诉类型:")
        for type_name, count in type_counts.items():
            summary_lines.append(f"  • {type_name}: {count}条")
        
        pending_tickets = [t for t in tickets if t.status == "pending"]
        if pending_tickets:
            summary_lines.append("\n⏳ 待处理投诉:")
            for t in pending_tickets[:5]:
                summary_lines.append(f"  • {t.student_name}: {t.content[:30]}...")
        
        return "\n".join(summary_lines)

    @staticmethod
    def export_to_markdown(content: str, filename: str) -> str:
        output_path = f"reports/{filename}.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path