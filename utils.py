# utils.py - Utility functions for logging, analytics, and notifications

from datetime import datetime
from typing import List, Dict, Optional

# In-memory storage (use database in production)
audit_logs = []
analytics_data = {
    "total_queries": 0,
    "tool_calls": {},
    "model_usage": {},
    "errors": 0,
    "avg_response_time": 0,
    "response_times": []
}


def log_interaction(
    user_message: str,
    assistant_response: str,
    tools_used: List[str] = None,
    model: str = "gpt-4o-mini",
    response_time: float = 0,
    error: str = None
) -> Dict:
    """
    Log an interaction for audit and analytics.
    """
    timestamp = datetime.now().isoformat()
    
    log_entry = {
        "timestamp": timestamp,
        "user_message": user_message,
        "assistant_response": assistant_response[:500] + "..." if len(assistant_response) > 500 else assistant_response,
        "tools_used": tools_used or [],
        "model": model,
        "response_time_ms": round(response_time * 1000, 2),
        "error": error
    }
    
    audit_logs.append(log_entry)
    
    # Update analytics
    analytics_data["total_queries"] += 1
    analytics_data["response_times"].append(response_time)
    analytics_data["avg_response_time"] = sum(analytics_data["response_times"]) / len(analytics_data["response_times"])
    
    # Track model usage
    analytics_data["model_usage"][model] = analytics_data["model_usage"].get(model, 0) + 1
    
    # Track tool usage
    for tool in (tools_used or []):
        analytics_data["tool_calls"][tool] = analytics_data["tool_calls"].get(tool, 0) + 1
    
    if error:
        analytics_data["errors"] += 1
    
    return log_entry


def get_recent_logs(n: int = 10) -> List[Dict]:
    """
    Get the n most recent log entries.
    """
    return audit_logs[-n:]


def get_analytics_summary() -> Dict:
    """
    Get analytics summary.
    """
    return {
        "total_queries": analytics_data["total_queries"],
        "total_errors": analytics_data["errors"],
        "avg_response_time_ms": round(analytics_data["avg_response_time"] * 1000, 2),
        "tool_usage": analytics_data["tool_calls"],
        "model_usage": analytics_data["model_usage"]
    }


def get_analytics_display() -> str:
    """
    Get formatted analytics for Gradio display.
    """
    stats = get_analytics_summary()
    
    output = "## 📊 Analytics Dashboard\n\n"
    output += f"**Total Queries:** {stats['total_queries']}\n\n"
    output += f"**Total Errors:** {stats['total_errors']}\n\n"
    output += f"**Avg Response Time:** {stats['avg_response_time_ms']}ms\n\n"
    
    output += "### 🔧 Tool Usage\n"
    if stats['tool_usage']:
        for tool, count in sorted(stats['tool_usage'].items(), key=lambda x: -x[1]):
            output += f"- {tool}: {count} calls\n"
    else:
        output += "- No tools used yet\n"
    
    output += "\n### 🤖 Model Usage\n"
    if stats['model_usage']:
        for model, count in sorted(stats['model_usage'].items(), key=lambda x: -x[1]):
            output += f"- {model}: {count} queries\n"
    else:
        output += "- No queries yet\n"
    
    return output


def get_logs_display() -> str:
    """
    Get formatted recent logs for Gradio display.
    """
    logs = get_recent_logs(10)
    
    if not logs:
        return "## 📝 Recent Interactions\n\nNo logs yet. Start chatting to see interaction logs!"
    
    output = "## 📝 Recent Interactions\n\n"
    for log in reversed(logs):
        timestamp = log['timestamp'][:19].replace('T', ' ')
        output += f"**{timestamp}** ({log['model']})\n"
        
        user_msg = log['user_message']
        if len(user_msg) > 100:
            user_msg = user_msg[:100] + "..."
        output += f"- 👤 User: {user_msg}\n"
        
        tools = ', '.join(log['tools_used']) if log['tools_used'] else 'None'
        output += f"- 🔧 Tools: {tools}\n"
        output += f"- ⏱️ Time: {log['response_time_ms']}ms\n"
        
        if log['error']:
            output += f"- ⚠️ Error: {log['error']}\n"
        
        output += "\n---\n\n"
    
    return output


def export_logs(filepath: str = "audit_logs.json") -> str:
    """
    Export all audit logs to a JSON file.
    """
    import json
    
    with open(filepath, 'w') as f:
        json.dump(audit_logs, f, indent=2)
    
    print(f"✅ Logs exported to {filepath}")
    return filepath


def export_analytics(filepath: str = "analytics.json") -> str:
    """
    Export analytics data to a JSON file.
    """
    import json
    
    with open(filepath, 'w') as f:
        json.dump(get_analytics_summary(), f, indent=2)
    
    print(f"✅ Analytics exported to {filepath}")
    return filepath


def reset_analytics():
    """
    Reset all analytics data.
    """
    global analytics_data
    analytics_data = {
        "total_queries": 0,
        "tool_calls": {},
        "model_usage": {},
        "errors": 0,
        "avg_response_time": 0,
        "response_times": []
    }
    print("✅ Analytics reset!")


def clear_logs():
    """
    Clear all audit logs.
    """
    global audit_logs
    audit_logs = []
    print("✅ Logs cleared!")


# Notification system
notification_callbacks = []


def add_notification_callback(callback):
    """
    Register a notification callback function.
    """
    notification_callbacks.append(callback)


def send_notification(title: str, message: str, level: str = "info"):
    """
    Send a notification to all registered callbacks.
    
    Args:
        title: Notification title
        message: Notification message
        level: info, warning, error, critical
    """
    notification = {
        "timestamp": datetime.now().isoformat(),
        "title": title,
        "message": message,
        "level": level
    }
    
    level_emoji = {
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌",
        "critical": "🚨"
    }
    
    emoji = level_emoji.get(level, "📢")
    print(f"{emoji} [{level.upper()}] {title}: {message}")
    
    for callback in notification_callbacks:
        try:
            callback(notification)
        except Exception as e:
            print(f"Notification callback failed: {e}")


def check_error_rate():
    """
    Check if error rate is too high and send notification.
    """
    stats = get_analytics_summary()
    if stats['total_queries'] > 10:
        error_rate = stats['total_errors'] / stats['total_queries']
        if error_rate > 0.1:  # More than 10% errors
            send_notification(
                "High Error Rate",
                f"Error rate is {error_rate:.1%} ({stats['total_errors']}/{stats['total_queries']})",
                level="warning"
            )
            return True
    return False


def check_response_time():
    """
    Check if average response time is too high.
    """
    stats = get_analytics_summary()
    if stats['avg_response_time_ms'] > 5000:  # More than 5 seconds
        send_notification(
            "Slow Response Times",
            f"Average response time is {stats['avg_response_time_ms']}ms",
            level="warning"
        )
        return True
    return False