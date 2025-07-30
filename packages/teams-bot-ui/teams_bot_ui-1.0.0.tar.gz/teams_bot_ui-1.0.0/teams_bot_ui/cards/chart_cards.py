from botbuilder.schema import Attachment
from typing import Dict, Any, List, Optional


def create_chart_card(
    title: str,
    chart_data: Dict[str, Any],
    chart_type: str = "bar",
    copilot_info: Optional[Dict[str, Any]] = None,
) -> Attachment:
    """
    Create a card with a data visualization chart

    Args:
        title: Chart title
        chart_data: Dictionary with labels and datasets
        chart_type: Type of chart (bar, line, pie)
        copilot_info: Optional bot/assistant information (kept for backward compatibility)

    Returns:
        Attachment: An adaptive card with an embedded HTML chart
    """
    # Handle both copilot_info (backward compatibility) and bot_info
    bot_info = copilot_info

    # Create the labels and datasets JS code
    labels_str = ", ".join([f"'{label}'" for label in chart_data["labels"]])

    datasets_str = "["
    for dataset in chart_data["datasets"]:
        dataset_str = "{\n"
        dataset_str += f"  label: '{dataset['label']}',\n"
        dataset_str += f"  data: [{', '.join([str(v) for v in dataset['data']])}],\n"

        # Add colors if provided
        if "backgroundColor" in dataset:
            bg_colors = dataset["backgroundColor"]
            if isinstance(bg_colors, list):
                bg_colors_str = ", ".join([f"'{c}'" for c in bg_colors])
                dataset_str += f"  backgroundColor: [{bg_colors_str}],\n"
            else:
                dataset_str += f"  backgroundColor: '{bg_colors}',\n"

        if "borderColor" in dataset:
            border_color = dataset["borderColor"]
            if isinstance(border_color, list):
                border_colors_str = ", ".join([f"'{c}'" for c in border_color])
                dataset_str += f"  borderColor: [{border_colors_str}],\n"
            else:
                dataset_str += f"  borderColor: '{border_color}',\n"

        dataset_str += "}"
        datasets_str += dataset_str + ","
    datasets_str += "]"

    # Create the HTML content with the chart
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.1/chart.min.js"></script>
        <style>
        .chart-container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 10px;
        }}
        .chart-title {{
            text-align: center;
            font-weight: bold;
            margin-bottom: 10px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        </style>
    </head>
    <body>
        <div class="chart-container">
            <div class="chart-title">{title}</div>
            <canvas id="myChart"></canvas>
        </div>
        
        <script>
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {{
            type: '{chart_type}',
            data: {{
                labels: [{labels_str}],
                datasets: {datasets_str}
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'top',
                    }},
                }},
                animation: {{
                    duration: 1000,
                    easing: 'easeOutQuart'
                }}
            }}
        }});
        </script>
    </body>
    </html>
    """

    # Create the adaptive card with the HTML content
    card_json = {
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "Container",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": title,
                        "weight": "Bolder",
                        "size": "Medium",
                        "horizontalAlignment": "Center",
                    }
                ],
            },
            {"type": "HtmlBlock", "html": html_content},
        ],
    }

    # Add bot info if provided
    if bot_info:
        header = {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": bot_info.get(
                                "logo", "https://via.placeholder.com/16?text=🤖"
                            ),
                            "size": "Small",
                        }
                    ],
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": bot_info.get("name", "AI Assistant"),
                            "size": "Small",
                            "weight": "Bolder",
                        }
                    ],
                },
            ],
        }
        # Insert header at the beginning
        card_json["body"].insert(0, header)

    return Attachment(
        content_type="application/vnd.microsoft.card.adaptive",
        content=card_json,
    )
