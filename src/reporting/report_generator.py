"""
Report generator for network simulation results
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class NetworkReportGenerator:
    """Generate comprehensive reports from simulation results"""
    
    def __init__(self):
        self.report_dir = "reports"
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
    def generate_full_report(self, scenario_name: str, simulation_data: Dict) -> Dict:
        """Generate complete report with graphics and narrative"""
        report = {
            'scenario': scenario_name,
            'timestamp': datetime.now().isoformat(),
            'graphical_report': self.generate_graphical_report(scenario_name, simulation_data),
            'narrative_report': self.generate_narrative_report(scenario_name, simulation_data),
            'statistics': self.calculate_statistics(simulation_data)
        }
        
        # Generate PDF reports
        report['graphical_pdf'] = self.generate_graphical_pdf(scenario_name, simulation_data, report['graphical_report'])
        report['narrative_pdf'] = self.generate_narrative_pdf(scenario_name, simulation_data)
        
        # Save report
        report_path = os.path.join(self.report_dir, f"{scenario_name}_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_graphical_report(self, scenario_name: str, data: Dict) -> str:
        """Generate graphical visualizations"""
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle(f'AI Network Security Analysis: {scenario_name}', fontsize=16, fontweight='bold')
        
        gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Threat Timeline
        ax1 = fig.add_subplot(gs[0, :])
        self._plot_threat_timeline(ax1, data['events'])
        
        # 2. Anomaly Score Heatmap
        ax2 = fig.add_subplot(gs[1, 0])
        self._plot_anomaly_heatmap(ax2, data['anomaly_scores'])
        
        # 3. Attack Phase Progression
        ax3 = fig.add_subplot(gs[1, 1])
        self._plot_attack_phases(ax3, data['attack_phases'])
        
        # 4. Network Topology Impact
        ax4 = fig.add_subplot(gs[1, 2])
        self._plot_network_impact(ax4, data['network_impact'])
        
        # 5. ML Model Performance
        ax5 = fig.add_subplot(gs[2, 0])
        self._plot_ml_performance(ax5, data['ml_metrics'])
        
        # 6. Threat Distribution
        ax6 = fig.add_subplot(gs[2, 1])
        self._plot_threat_distribution(ax6, data['threat_types'])
        
        # 7. Real-time Detection Rate
        ax7 = fig.add_subplot(gs[2, 2])
        self._plot_detection_rate(ax7, data['detection_timeline'])
        
        # Save figure
        output_path = os.path.join(self.report_dir, f"{scenario_name}_analysis.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _plot_threat_timeline(self, ax, events):
        """Plot threat events over time"""
        times = []
        threat_levels = []
        colors = []
        
        threat_colors = {
            'low': '#2ecc71',
            'medium': '#f39c12',
            'high': '#e74c3c',
            'critical': '#c0392b'
        }
        
        for event in events:
            times.append(event['timestamp'])
            threat_levels.append(event['threat_score'])
            colors.append(threat_colors.get(event['threat_level'], '#95a5a6'))
        
        # Convert to relative time (minutes from start)
        if times:
            start_time = min(times)
            times_relative = [(t - start_time).total_seconds() / 60 for t in times]
            
            ax.scatter(times_relative, threat_levels, c=colors, s=100, alpha=0.6, edgecolors='black')
            ax.plot(times_relative, threat_levels, 'k--', alpha=0.3)
            
            # Add threat zones
            ax.axhspan(0, 25, alpha=0.1, color='green', label='Low Risk')
            ax.axhspan(25, 50, alpha=0.1, color='yellow', label='Medium Risk')
            ax.axhspan(50, 75, alpha=0.1, color='orange', label='High Risk')
            ax.axhspan(75, 100, alpha=0.1, color='red', label='Critical Risk')
        
        ax.set_xlabel('Time (minutes from start)')
        ax.set_ylabel('Threat Score')
        ax.set_title('Threat Level Timeline')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
    
    def _plot_anomaly_heatmap(self, ax, anomaly_scores):
        """Plot anomaly score heatmap by device and time"""
        if not anomaly_scores:
            return
        
        # Create matrix of anomaly scores
        devices = sorted(set(score['device'] for score in anomaly_scores))
        time_slots = 20  # Divide timeline into slots
        
        matrix = np.zeros((len(devices), time_slots))
        
        for score in anomaly_scores:
            device_idx = devices.index(score['device'])
            time_idx = min(int(score['time_slot']), time_slots - 1)
            matrix[device_idx, time_idx] = max(matrix[device_idx, time_idx], score['anomaly_score'])
        
        im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
        ax.set_yticks(range(len(devices)))
        ax.set_yticklabels(devices, fontsize=8)
        ax.set_xlabel('Time Progression')
        ax.set_title('Anomaly Score Heatmap by Device')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Anomaly Score')
    
    def _plot_attack_phases(self, ax, phases):
        """Plot attack phase progression"""
        if not phases:
            return
        
        phase_names = [p['name'] for p in phases]
        durations = [p['duration'] for p in phases]
        
        # Map threat levels to severity for coloring
        threat_level_map = {'low': 0, 'medium': 1, 'high': 2, 'critical': 3}
        severities = [threat_level_map.get(p.get('threat_level', 'low'), 0) for p in phases]
        
        # Create stacked bar chart
        colors = ['#3498db', '#f39c12', '#e74c3c', '#c0392b']
        bars = ax.bar(phase_names, durations, color=[colors[s] for s in severities])
        
        # Add annotations
        for i, (bar, phase) in enumerate(zip(bars, phases)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f"{phase['packets']} packets",
                   ha='center', va='bottom', fontsize=8)
        
        ax.set_ylabel('Duration (minutes)')
        ax.set_title('Attack Phase Progression')
        ax.set_xticks(range(len(phase_names)))
        ax.set_xticklabels(phase_names, rotation=45, ha='right')
    
    def _plot_network_impact(self, ax, impact_data):
        """Plot network impact visualization"""
        if not impact_data:
            return
        
        categories = ['Availability', 'Integrity', 'Confidentiality', 'Performance']
        before = [impact_data.get(f'{cat.lower()}_before', 100) for cat in categories]
        after = [impact_data.get(f'{cat.lower()}_after', 50) for cat in categories]
        
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, before, width, label='Before Attack', color='#2ecc71')
        bars2 = ax.bar(x + width/2, after, width, label='After Attack', color='#e74c3c')
        
        ax.set_ylabel('Score (%)')
        ax.set_title('Network Security Impact Analysis')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.set_ylim(0, 110)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{height:.0f}%', ha='center', va='bottom', fontsize=8)
    
    def _plot_ml_performance(self, ax, metrics):
        """Plot ML model performance metrics"""
        if not metrics:
            return
        
        models = list(metrics.keys())
        precision = [metrics[m].get('precision', 0) for m in models]
        recall = [metrics[m].get('recall', 0) for m in models]
        f1_score = [metrics[m].get('f1_score', 0) for m in models]
        
        x = np.arange(len(models))
        width = 0.25
        
        ax.bar(x - width, precision, width, label='Precision', color='#3498db')
        ax.bar(x, recall, width, label='Recall', color='#2ecc71')
        ax.bar(x + width, f1_score, width, label='F1-Score', color='#f39c12')
        
        ax.set_ylabel('Score')
        ax.set_title('ML Model Performance Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=45, ha='right')
        ax.legend()
        ax.set_ylim(0, 1.1)
        ax.grid(True, alpha=0.3)
    
    def _plot_threat_distribution(self, ax, threat_types):
        """Plot threat type distribution"""
        if not threat_types:
            return
        
        labels = list(threat_types.keys())
        sizes = list(threat_types.values())
        colors = ['#e74c3c', '#f39c12', '#3498db', '#9b59b6', '#2ecc71']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors[:len(labels)],
                                          autopct='%1.1f%%', startangle=90)
        
        ax.set_title('Threat Type Distribution')
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_weight('bold')
            autotext.set_color('white')
    
    def _plot_detection_rate(self, ax, detection_timeline):
        """Plot real-time detection rate"""
        if not detection_timeline:
            return
        
        times = [d['time'] for d in detection_timeline]
        true_positives = [d['true_positives'] for d in detection_timeline]
        false_positives = [d['false_positives'] for d in detection_timeline]
        false_negatives = [d['false_negatives'] for d in detection_timeline]
        
        ax.plot(times, true_positives, 'g-', linewidth=2, label='True Positives')
        ax.plot(times, false_positives, 'r--', linewidth=2, label='False Positives')
        ax.plot(times, false_negatives, 'b:', linewidth=2, label='False Negatives')
        
        ax.fill_between(times, 0, true_positives, alpha=0.3, color='green')
        
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('Detection Count')
        ax.set_title('Real-time Detection Performance')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def generate_narrative_report(self, scenario_name: str, data: Dict) -> str:
        """Generate narrative text report"""
        narrative = f"""
# AI Network Security Analysis Report
## Scenario: {scenario_name}
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Executive Summary
The AI-powered network security monitoring system analyzed a {scenario_name} scenario 
involving {data.get('total_packets', 0)} network packets over a {data.get('duration', 0):.1f} minute period. 
The system detected {data.get('total_threats', 0)} security threats with an overall accuracy of 
{data.get('accuracy', 0):.1%}.

### Attack Narrative
"""
        
        # Add phase-by-phase narrative
        for phase in data.get('attack_phases', []):
            narrative += f"""
#### Phase {phase['id']}: {phase['name']}
- **Duration**: {phase['duration']:.1f} minutes
- **Packets Analyzed**: {phase['packets']}
- **Threat Level**: {phase['threat_level']}

{phase['description']}

**AI Detection**: {phase['ai_response']}
**Recommended Actions**: {', '.join(phase['recommendations'])}
"""
        
        # Add ML insights
        narrative += """
### Machine Learning Insights
"""
        for insight in data.get('ml_insights', []):
            narrative += f"- {insight}\n"
        
        # Add critical findings
        narrative += f"""
### Critical Findings
1. **Most Affected Devices**: {', '.join(data.get('affected_devices', [])[:5])}
2. **Primary Attack Vectors**: {', '.join(data.get('attack_vectors', []))}
3. **Data Exfiltration Risk**: {data.get('exfiltration_risk', 'Unknown')}
4. **Network Integrity Status**: {data.get('integrity_status', 'Unknown')}

### Response Effectiveness
- **Mean Time to Detect (MTTD)**: {data.get('mttd', 0):.2f} seconds
- **Detection Rate**: {data.get('detection_rate', 0):.1%}
- **False Positive Rate**: {data.get('false_positive_rate', 0):.1%}

### Recommendations
"""
        for i, rec in enumerate(data.get('final_recommendations', []), 1):
            narrative += f"{i}. {rec}\n"
        
        # Save narrative
        narrative_path = os.path.join(self.report_dir, f"{scenario_name}_narrative.md")
        with open(narrative_path, 'w', encoding='utf-8') as f:
            f.write(narrative)
        
        return narrative
    
    def calculate_statistics(self, data: Dict) -> Dict:
        """Calculate comprehensive statistics"""
        stats = {
            'total_packets': data.get('total_packets', 0),
            'threats_detected': data.get('total_threats', 0),
            'avg_anomaly_score': np.mean([s['anomaly_score'] for s in data.get('anomaly_scores', [])]) if data.get('anomaly_scores') else 0,
            'max_threat_level': max([e['threat_score'] for e in data.get('events', [])]) if data.get('events') else 0,
            'detection_accuracy': data.get('accuracy', 0),
            'response_time': data.get('mttd', 0),
            'affected_devices': len(set(s['device'] for s in data.get('anomaly_scores', []))) if data.get('anomaly_scores') else 0
        }
        
        return stats
    
    def generate_graphical_pdf(self, scenario_name: str, data: Dict, image_path: str) -> str:
        """Generate graphical PDF report"""
        pdf_path = os.path.join(self.report_dir, f"{scenario_name}_graphical_report.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        )
        
        # Title
        elements.append(Paragraph(f"AI Network Security Analysis<br/>{scenario_name}", title_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Packets Analyzed', f"{data.get('total_packets', 0):,}"],
            ['Threats Detected', f"{data.get('total_threats', 0)}"],
            ['Detection Accuracy', f"{data.get('accuracy', 0):.1%}"],
            ['Mean Time to Detect', f"{data.get('mttd', 0):.2f} seconds"],
            ['Affected Devices', f"{len(data.get('affected_devices', []))}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Add main visualization
        elements.append(Paragraph("Attack Analysis Visualization", heading_style))
        if os.path.exists(image_path):
            img = Image(image_path, width=7*inch, height=5.25*inch)
            elements.append(img)
        
        elements.append(PageBreak())
        
        # ML Model Performance
        elements.append(Paragraph("Machine Learning Model Performance", heading_style))
        ml_data = [['Model', 'Precision', 'Recall', 'F1-Score']]
        for model, metrics in data.get('ml_metrics', {}).items():
            ml_data.append([
                model,
                f"{metrics.get('precision', 0):.3f}",
                f"{metrics.get('recall', 0):.3f}",
                f"{metrics.get('f1_score', 0):.3f}"
            ])
        
        ml_table = Table(ml_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        ml_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(ml_table)
        
        # Build PDF
        doc.build(elements)
        return pdf_path
    
    def generate_narrative_pdf(self, scenario_name: str, data: Dict) -> str:
        """Generate narrative PDF report"""
        pdf_path = os.path.join(self.report_dir, f"{scenario_name}_narrative_report.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=10
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        
        # Title
        elements.append(Paragraph(f"AI Network Security Analysis Report<br/>{scenario_name}", title_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", heading_style))
        summary_text = f"""The AI-powered network security monitoring system analyzed a {scenario_name} scenario 
        involving {data.get('total_packets', 0):,} network packets over a {data.get('duration', 0):.1f} minute period. 
        The system detected {data.get('total_threats', 0)} security threats with an overall accuracy of 
        {data.get('accuracy', 0):.1%}."""
        elements.append(Paragraph(summary_text, body_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Attack Narrative
        elements.append(Paragraph("Attack Narrative", heading_style))
        
        for phase in data.get('attack_phases', []):
            elements.append(Paragraph(f"Phase {phase['id']}: {phase['name']}", subheading_style))
            
            phase_info = f"""
            <b>Duration:</b> {phase['duration']:.1f} minutes<br/>
            <b>Packets Analyzed:</b> {phase['packets']}<br/>
            <b>Threat Level:</b> {phase['threat_level']}<br/><br/>
            {phase['description']}<br/><br/>
            <b>AI Detection:</b> {phase['ai_response']}<br/>
            <b>Recommended Actions:</b> {', '.join(phase['recommendations'])}
            """
            elements.append(Paragraph(phase_info, body_style))
            elements.append(Spacer(1, 0.2*inch))
        
        elements.append(PageBreak())
        
        # Machine Learning Insights
        elements.append(Paragraph("Machine Learning Insights", heading_style))
        for insight in data.get('ml_insights', [])[:10]:
            elements.append(Paragraph(f"• {insight}", body_style))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Critical Findings
        elements.append(Paragraph("Critical Findings", heading_style))
        findings = f"""
        1. <b>Most Affected Devices:</b> {', '.join(data.get('affected_devices', [])[:5])}<br/>
        2. <b>Primary Attack Vectors:</b> {', '.join(data.get('attack_vectors', []))}<br/>
        3. <b>Data Exfiltration Risk:</b> {data.get('exfiltration_risk', 'Unknown')}<br/>
        4. <b>Network Integrity Status:</b> {data.get('integrity_status', 'Unknown')}
        """
        elements.append(Paragraph(findings, body_style))
        
        # Response Effectiveness
        elements.append(Paragraph("Response Effectiveness", heading_style))
        response_data = [
            ['Metric', 'Value'],
            ['Mean Time to Detect (MTTD)', f"{data.get('mttd', 0):.2f} seconds"],
            ['Detection Rate', f"{data.get('detection_rate', 0):.1%}"],
            ['False Positive Rate', f"{data.get('false_positive_rate', 0):.1%}"],
            ['Overall Accuracy', f"{data.get('accuracy', 0):.1%}"]
        ]
        
        response_table = Table(response_data, colWidths=[3*inch, 2*inch])
        response_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(response_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        elements.append(Paragraph("Security Recommendations", heading_style))
        for i, rec in enumerate(data.get('final_recommendations', []), 1):
            elements.append(Paragraph(f"{i}. {rec}", body_style))
        
        # Build PDF
        doc.build(elements)
        return pdf_path