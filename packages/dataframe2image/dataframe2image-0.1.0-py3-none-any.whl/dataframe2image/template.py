"""
HTML template for rendering DataFrame tables
"""

from jinja2 import Template

TABLE_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataFrame Table</title>
    <style>
        {% if font_files %}
        {% for font_name, font_path in font_files.items() %}
        @font-face {
            font-family: '{{ font_name }}';
            src: url('file://{{ font_path }}') format('truetype');
        }
        {% endfor %}
        {% endif %}
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: {{ style.font_family }};
            background-color: transparent;
            padding: 20px;
        }
        
        .table-container {
            display: inline-block;
            background-color: white;
            border-radius: {{ style.table_border_radius }};
            box-shadow: {{ style.box_shadow }};
            overflow: hidden;
            border: {{ style.border_width }}px solid {{ style.border_color }};
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            font-size: {{ style.font_size }}px;
        }
        
        th {
            background-color: {{ style.header_bg_color }};
            color: {{ style.header_text_color }};
            font-weight: bold;
            text-align: left;
            padding: {{ style.cell_padding }};
            border-bottom: {{ style.border_width }}px solid {{ style.border_color }};
        }
        
        td {
            padding: {{ style.cell_padding }};
            color: {{ style.row_text_color }};
            border-bottom: {{ style.border_width }}px solid {{ style.border_color }};
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        /* Row background colors using nth-child for proper alternating pattern */
        tr:nth-child(odd) td {
            background-color: {{ style.row_bg_colors[0] }};
        }
        tr:nth-child(even) td {
            background-color: {{ style.row_bg_colors[1] if style.row_bg_colors|length > 1 else style.row_bg_colors[0] }};
        }
        
        /* Index column styling - should follow row background colors */
        .index-col {
            font-weight: bold;
            border-right: 2px solid {{ style.border_color }};
            /* Use row text color instead of header text color for better consistency */
            color: {{ style.row_text_color }};
        }
        
        /* Override index column background to follow row patterns */
        tr:nth-child(odd) .index-col {
            background-color: {{ style.row_bg_colors[0] }};
        }
        tr:nth-child(even) .index-col {
            background-color: {{ style.row_bg_colors[1] if style.row_bg_colors|length > 1 else style.row_bg_colors[0] }};
        }
        
        /* Numeric alignment */
        .numeric {
            text-align: right;
        }
        
        /* Handle long text */
        td, th {
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .table-container {
                font-size: {{ style.font_size - 2 }}px;
            }
            
            td, th {
                padding: 6px 8px;
            }
        }
    </style>
</head>
<body>
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    {% if show_index %}
                    <th class="index-header">{{ index_name or '' }}</th>
                    {% endif %}
                    {% for col in columns %}
                    <th>{{ col }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row_idx, row in data %}
                <tr>
                    {% if show_index %}
                    <td class="index-col">{{ row_idx }}</td>
                    {% endif %}
                    {% for value in row %}
                    <td class="{% if value is number %}numeric{% endif %}">{{ value }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
""")


def render_dataframe_html(df, style, show_index=True, font_files=None):
    """Render DataFrame as HTML using the template."""
    import pandas as pd
    import numpy as np
    
    # Prepare data
    data = []
    for idx, row in df.iterrows():
        row_data = []
        for value in row:
            if pd.isna(value):
                row_data.append("")
            elif isinstance(value, (int, float, np.number)):
                if isinstance(value, float):
                    row_data.append(f"{value:.2f}" if not np.isnan(value) else "")
                else:
                    row_data.append(str(value))
            else:
                row_data.append(str(value))
        data.append((str(idx), row_data))
    
    # Render template
    return TABLE_TEMPLATE.render(
        style=style,
        columns=df.columns.tolist(),
        data=data,
        show_index=show_index,
        index_name=df.index.name,
        font_files=font_files
    )
