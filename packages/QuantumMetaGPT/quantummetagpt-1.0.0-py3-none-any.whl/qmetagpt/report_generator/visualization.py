import matplotlib.pyplot as plt
import numpy as np
from qiskit.visualization import plot_histogram, plot_state_city
from qmetagpt.utils.logger import get_logger

logger = get_logger(__name__)

def create_performance_plot(metrics):
    """Create a bar plot for performance metrics"""
    fig, ax = plt.subplots(figsize=(10, 6))
    metric_names = list(metrics.keys())
    values = list(metrics.values())
    
    bars = ax.bar(metric_names, values, color='skyblue')
    ax.set_title('Quantum Algorithm Performance Metrics')
    ax.set_ylabel('Value')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def create_training_curve(rewards, losses=None):
    """Create training curve plot for RL agent"""
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Plot rewards
    color = 'tab:blue'
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Reward', color=color)
    ax1.plot(rewards, color=color, label='Reward')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Plot losses if available
    if losses:
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Loss', color=color)
        ax2.plot(losses, color=color, linestyle='--', label='Loss')
        ax2.tick_params(axis='y', labelcolor=color)
    
    ax1.set_title('Reinforcement Learning Training Progress')
    fig.tight_layout()
    return fig

def plot_quantum_state(statevector):
    """Visualize quantum state using city plot"""
    return plot_state_city(statevector)