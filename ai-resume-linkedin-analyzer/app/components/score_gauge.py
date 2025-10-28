"""
Score Gauge Component
Displays scores with visual indicators
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Optional


def render_score_gauge(
    score: float,
    title: str = "Score",
    height: int = 300,
    show_delta: bool = True,
    reference: float = 70.0
):
    """
    Render a gauge chart for displaying scores
    
    Args:
        score: Score value (0-100)
        title: Chart title
        height: Chart height in pixels
        show_delta: Show delta indicator
        reference: Reference value for delta
    """
    # Determine color based on score
    if score >= 85:
        color = "#2ecc71"  # Green
    elif score >= 70:
        color = "#3498db"  # Blue
    elif score >= 60:
        color = "#f39c12"  # Orange
    else:
        color = "#e74c3c"  # Red
    
    # Create gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number" + ("+delta" if show_delta else ""),
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': '#2c3e50'}},
        number={'font': {'size': 40, 'color': color}},
        delta={
            'reference': reference,
            'increasing': {'color': "#2ecc71"},
            'decreasing': {'color': "#e74c3c"}
        } if show_delta else {},
        gauge={
            'axis': {
                'range': [None, 100],
                'tickwidth': 2,
                'tickcolor': "#34495e",
                'tickfont': {'size': 12}
            },
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#bdc3c7",
            'steps': [
                {'range': [0, 60], 'color': '#ffebee'},
                {'range': [60, 70], 'color': '#fff3e0'},
                {'range': [70, 85], 'color': '#e3f2fd'},
                {'range': [85, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        font={'color': "#2c3e50", 'family': "Arial"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_progress_gauge(
    value: float,
    max_value: float,
    label: str,
    color: str = "#3498db"
):
    """
    Render a simple progress gauge
    
    Args:
        value: Current value
        max_value: Maximum value
        label: Label text
        color: Progress bar color
    """
    percentage = (value / max_value * 100) if max_value > 0 else 0
    
    st.markdown(f"**{label}**")
    st.progress(min(percentage / 100, 1.0))
    st.caption(f"{value:.0f} / {max_value:.0f} ({percentage:.0f}%)")


def render_mini_gauge(score: float, size: str = "small"):
    """
    Render a compact gauge for inline display
    
    Args:
        score: Score value (0-100)
        size: Size variant ('small', 'medium', 'large')
    """
    if score >= 80:
        color = "#2ecc71"
        emoji = "🟢"
    elif score >= 60:
        color = "#f39c12"
        emoji = "🟡"
    else:
        color = "#e74c3c"
        emoji = "🔴"
    
    size_map = {
        'small': ('1.2em', '12px'),
        'medium': ('1.5em', '14px'),
        'large': ('2em', '16px')
    }
    
    font_size, badge_size = size_map.get(size, size_map['small'])
    
    st.markdown(f"""
    <div style='display: inline-flex; align-items: center; gap: 8px;'>
        <span style='font-size: {font_size};'>{emoji}</span>
        <span style='font-size: {font_size}; font-weight: bold; color: {color};'>
            {score:.1f}%
        </span>
    </div>
    """, unsafe_allow_html=True)