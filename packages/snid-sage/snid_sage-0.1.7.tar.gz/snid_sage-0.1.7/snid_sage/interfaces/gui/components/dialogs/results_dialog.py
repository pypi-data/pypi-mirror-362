"""
SNID SAGE - Results Dialog Component
===================================

Detailed results dialog for viewing, analyzing, and exporting SNID analysis results
with comprehensive statistics and export options.

Part of the SNID SAGE GUI restructuring - Components Module
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tb
from typing import Optional, Dict, Any, List
import os
import json
import csv
from pathlib import Path


class ResultsDialog:
    """
    Detailed results dialog that provides comprehensive viewing and analysis
    of SNID results with export and comparison capabilities.
    """
    
    def __init__(self, parent, results_data=None):
        """
        Initialize the results dialog.
        
        Args:
            parent: Parent window/widget
            results_data: SNID analysis results data
        """
        self.parent = parent
        self.results_data = results_data or {}
        self.dialog = None
        
        # Extract key results information
        self.templates = results_data.get('templates', [])
        self.correlations = results_data.get('correlations', [])
        self.best_match = results_data.get('best_match', {})
        self.statistics = results_data.get('statistics', {})
    
    def show(self):
        """Show the results dialog"""
        self._create_dialog()
        self._setup_interface()
        
        # Run the dialog
        self.dialog.wait_window()
    
    def _create_dialog(self):
        """Create the dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("SNID Analysis Results - Detailed View")
        self.dialog.geometry("1000x800")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (800 // 2)
        self.dialog.geometry(f"1000x800+{x}+{y}")
    
    def _setup_interface(self):
        """Setup the dialog interface"""
        # Main container
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Create notebook for different result views
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 15))
        
        # Create result tabs
        self._create_summary_tab(notebook)
        self._create_templates_tab(notebook)
        self._create_statistics_tab(notebook)
        self._create_export_tab(notebook)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(15, 0))
        
        # Buttons
        ttk.Button(button_frame, text="Export Summary", 
                  command=self._export_summary).pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="Export All Data", 
                  command=self._export_all_data).pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="Generate Report", 
                  command=self._generate_report).pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="Close", 
                  command=self._close).pack(side='right')
    
    def _create_summary_tab(self, notebook):
        """Create results summary tab"""
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="Summary")
        
        # Best match section
        best_frame = ttk.LabelFrame(summary_frame, text="Best Match", padding=15)
        best_frame.pack(fill='x', pady=(0, 15))
        
        if self.best_match:
            self._create_info_grid(best_frame, [
                ("Template:", self.best_match.get('template', 'N/A')),
                ("Type:", self.best_match.get('type', 'N/A')),
                ("Subtype:", self.best_match.get('subtype', 'N/A')),
                ("Age:", f"{self.best_match.get('age', 'N/A')} days"),
                ("Redshift:", f"{self.best_match.get('redshift', 'N/A'):.4f}"),
                ("Correlation:", f"{self.best_match.get('correlation', 'N/A'):.2f}"),
                ("Grade:", self.best_match.get('grade', 'N/A')),
                ("Velocity:", f"{self.best_match.get('velocity', 'N/A')} km/s")
            ])
        else:
            ttk.Label(best_frame, text="No match data available").pack()
        
        # Analysis overview
        overview_frame = ttk.LabelFrame(summary_frame, text="Analysis Overview", padding=15)
        overview_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Create text widget for overview
        overview_text = tk.Text(overview_frame, height=12, wrap='word', state='disabled')
        overview_scrollbar = ttk.Scrollbar(overview_frame, orient='vertical', command=overview_text.yview)
        overview_text.configure(yscrollcommand=overview_scrollbar.set)
        
        overview_text.pack(side='left', fill='both', expand=True)
        overview_scrollbar.pack(side='right', fill='y')
        
        # Add overview content
        overview_content = self._generate_overview_text()
        overview_text.config(state='normal')
        overview_text.insert('1.0', overview_content)
        overview_text.config(state='disabled')
    
    def _create_templates_tab(self, notebook):
        """Create clean templates results tab"""
        templates_frame = ttk.Frame(notebook)
        notebook.add(templates_frame, text="Top Templates")
        
        # Create simplified treeview - only essential columns
        columns = ('rank', 'template', 'type', 'rlap', 'redshift', 'age')
        tree = ttk.Treeview(templates_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        tree.heading('rank', text='#')
        tree.heading('template', text='Template')
        tree.heading('type', text='Type/Subtype')
        tree.heading('rlap', text='RLAP')
        tree.heading('redshift', text='Redshift')
        tree.heading('age', text='Age (days)')
        
        # Set column widths
        tree.column('rank', width=50, anchor='center')
        tree.column('template', width=150)
        tree.column('type', width=100, anchor='center')
        tree.column('rlap', width=80, anchor='center')
        tree.column('redshift', width=100, anchor='center')
        tree.column('age', width=90, anchor='center')
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(templates_frame, orient='vertical', command=tree.yview)
        h_scrollbar = ttk.Scrollbar(templates_frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack components
        tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Populate with template data
        self._populate_templates_tree(tree)
        
        # Add context menu
        self._create_templates_context_menu(tree)
    
    def _create_statistics_tab(self, notebook):
        """Create statistics tab"""
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")
        
        # Analysis statistics
        analysis_frame = ttk.LabelFrame(stats_frame, text="Analysis Statistics", padding=15)
        analysis_frame.pack(fill='x', pady=(0, 15))
        
        if self.statistics:
            self._create_info_grid(analysis_frame, [
                ("Total Templates Processed:", self.statistics.get('total_templates', 'N/A')),
                ("Valid Matches Found:", self.statistics.get('valid_matches', 'N/A')),
                ("Average Correlation:", f"{self.statistics.get('avg_correlation', 0):.2f}"),
                ("Best Correlation:", f"{self.statistics.get('best_correlation', 0):.2f}"),
                ("Processing Time:", f"{self.statistics.get('processing_time', 'N/A')} seconds"),
                ("Redshift Range:", f"{self.statistics.get('redshift_range', 'N/A')}"),
                ("Age Range:", f"{self.statistics.get('age_range', 'N/A')} days"),
                ("Template Types Found:", self.statistics.get('types_found', 'N/A'))
            ])
        else:
            ttk.Label(analysis_frame, text="No statistics available").pack()
        
        # Type distribution
        dist_frame = ttk.LabelFrame(stats_frame, text="Type Distribution", padding=15)
        dist_frame.pack(fill='both', expand=True)
        
        # Create distribution display
        self._create_type_distribution(dist_frame)
    
    def _create_export_tab(self, notebook):
        """Create export options tab"""
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="Export Options")
        
        # Export format selection
        format_frame = ttk.LabelFrame(export_frame, text="Export Format", padding=15)
        format_frame.pack(fill='x', pady=(0, 15))
        
        self.export_format = tk.StringVar(value='csv')
        ttk.Radiobutton(format_frame, text="CSV (Excel compatible)", 
                       variable=self.export_format, value='csv').pack(anchor='w')
        ttk.Radiobutton(format_frame, text="JSON (structured data)", 
                       variable=self.export_format, value='json').pack(anchor='w')
        ttk.Radiobutton(format_frame, text="Text Report", 
                       variable=self.export_format, value='txt').pack(anchor='w')
        ttk.Radiobutton(format_frame, text="HTML Report", 
                       variable=self.export_format, value='html').pack(anchor='w')
        
        # Export content selection
        content_frame = ttk.LabelFrame(export_frame, text="Export Content", padding=15)
        content_frame.pack(fill='x', pady=(0, 15))
        
        self.export_summary = tk.BooleanVar(value=True)
        self.export_templates = tk.BooleanVar(value=True)
        self.export_statistics = tk.BooleanVar(value=True)
        self.export_plots = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(content_frame, text="Summary Information", 
                       variable=self.export_summary).pack(anchor='w')
        ttk.Checkbutton(content_frame, text="Template Match Details", 
                       variable=self.export_templates).pack(anchor='w')
        ttk.Checkbutton(content_frame, text="Analysis Statistics", 
                       variable=self.export_statistics).pack(anchor='w')
        ttk.Checkbutton(content_frame, text="Plot Images (if available)", 
                       variable=self.export_plots).pack(anchor='w')
        
        # Export buttons
        export_buttons_frame = ttk.Frame(export_frame)
        export_buttons_frame.pack(fill='x', pady=(15, 0))
        
        ttk.Button(export_buttons_frame, text="Export Selected Data", 
                  command=self._export_selected).pack(side='left', padx=(0, 10))
        
        ttk.Button(export_buttons_frame, text="Export All Formats", 
                  command=self._export_all_formats).pack(side='left', padx=(0, 10))
        
        ttk.Button(export_buttons_frame, text="Custom Export", 
                  command=self._custom_export).pack(side='left')
    
    def _create_info_grid(self, parent, info_pairs):
        """Create a grid of information labels"""
        for i, (label, value) in enumerate(info_pairs):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(parent, text=label, font=('TkDefaultFont', 9, 'bold')).grid(
                row=row, column=col, sticky='w', padx=(0, 10), pady=2)
            ttk.Label(parent, text=str(value)).grid(
                row=row, column=col+1, sticky='w', padx=(0, 20), pady=2)
    
    def _generate_overview_text(self):
        """Generate clean, simplified overview text"""
        overview = "🔬 SNID CLASSIFICATION RESULTS\n"
        overview += "=" * 35 + "\n\n"
        
        if self.best_match:
            # Combine type and subtype for cleaner display
            type_name = self.best_match.get('type', 'N/A')
            subtype = self.best_match.get('subtype', '')
            if subtype and subtype != 'Unknown' and subtype != '':
                classification = f"{type_name}-{subtype}"
            else:
                classification = type_name
            
            overview += f"🎯 CLASSIFICATION: {classification}\n\n"
            overview += f"📏 MEASUREMENTS:\n"
            overview += f"   Redshift: {self.best_match.get('redshift', 'N/A')}\n"
            if self.best_match.get('age'):
                overview += f"   Age: {self.best_match.get('age', 'N/A')} days\n"
            overview += f"   Quality: {self.best_match.get('correlation', 'N/A')} RLAP\n\n"
        
        if self.templates:
            overview += f"📊 ANALYSIS:\n"
            overview += f"   Templates analyzed: {len(self.templates)}\n"
            
            if self.statistics and self.statistics.get('processing_time'):
                overview += f"   Runtime: {self.statistics.get('processing_time')} seconds\n"
        
        overview += "\n💡 This analysis provides automated classification.\n"
        overview += "See the 'Top Templates' tab for detailed matches."
        
        return overview
    
    def _populate_templates_tree(self, tree):
        """Populate the simplified templates treeview with essential data only"""
        for i, template in enumerate(self.templates[:10], 1):  # Show only top 10
            # Combine type and subtype for cleaner display
            type_name = template.get('type', 'Unknown')
            subtype = template.get('subtype', '')
            if subtype and subtype != 'Unknown' and subtype != '':
                display_type = f"{type_name}-{subtype}"
            else:
                display_type = type_name
            
            # Format age
            age = template.get('age', 0)
            age_str = f"{age:.0f}" if age and age > 0 else "N/A"
            
            values = (
                i,
                template.get('template', '')[:20],  # Truncate long names
                display_type,
                f"{template.get('rlap', 0):.1f}" if template.get('rlap') else 'N/A',
                f"{template.get('redshift', 0):.4f}" if template.get('redshift') else 'N/A',
                age_str
            )
            
            tree.insert('', 'end', values=values)
    
    def _create_templates_context_menu(self, tree):
        """Create context menu for templates tree"""
        def on_right_click(event):
            # Select item under cursor
            item = tree.identify_row(event.y)
            if item:
                tree.selection_set(item)
                context_menu.post(event.x_root, event.y_root)
        
        def copy_template_info():
            selection = tree.selection()
            if selection:
                item = selection[0]
                values = tree.item(item, 'values')
                template_info = f"Template: {values[1]}\nSubtype: {values[3]}\nType: {values[2]}\n"
                template_info += f"Age: {values[4]} days\nRedshift: {values[5]}\nCorrelation: {values[6]}"
                
                self.dialog.clipboard_clear()
                self.dialog.clipboard_append(template_info)
                messagebox.showinfo("Copied", "Template information copied to clipboard")
        
        context_menu = tk.Menu(tree, tearoff=0)
        context_menu.add_command(label="Copy Template Info", command=copy_template_info)
        context_menu.add_separator()
        context_menu.add_command(label="Export Selected", command=lambda: self._export_selected_template(tree))
        
        # Use the new cross-platform event binding system
        from snid_sage.interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
        
        # Set up cross-platform right-click handling
        CrossPlatformWindowManager.setup_mac_event_bindings(
            tree, 
            right_click_callback=on_right_click
        )
        
        # Fallback bindings for non-Mac platforms
        tree.bind("<Button-3>", on_right_click)  # Windows/Linux
        tree.bind("<Button-2>", on_right_click)  # macOS fallback
    
    def _create_type_distribution(self, parent):
        """Create type distribution display"""
        if not self.templates:
            ttk.Label(parent, text="No template data available for distribution").pack()
            return
        
        # Count types
        types = {}
        for template in self.templates:
            type_name = template.get('type', 'Unknown')
            types[type_name] = types.get(type_name, 0) + 1
        
        # Create distribution list
        dist_frame = ttk.Frame(parent)
        dist_frame.pack(fill='both', expand=True)
        
        # Headers
        ttk.Label(dist_frame, text="Type", font=('TkDefaultFont', 9, 'bold')).grid(
            row=0, column=0, sticky='w', padx=(0, 20), pady=5)
        ttk.Label(dist_frame, text="Count", font=('TkDefaultFont', 9, 'bold')).grid(
            row=0, column=1, sticky='w', padx=(0, 20), pady=5)
        ttk.Label(dist_frame, text="Percentage", font=('TkDefaultFont', 9, 'bold')).grid(
            row=0, column=2, sticky='w', pady=5)
        
        # Distribution data
        total = len(self.templates)
        for i, (type_name, count) in enumerate(sorted(types.items()), 1):
            percentage = (count / total) * 100
            
            ttk.Label(dist_frame, text=type_name).grid(
                row=i, column=0, sticky='w', padx=(0, 20), pady=2)
            ttk.Label(dist_frame, text=str(count)).grid(
                row=i, column=1, sticky='w', padx=(0, 20), pady=2)
            ttk.Label(dist_frame, text=f"{percentage:.1f}%").grid(
                row=i, column=2, sticky='w', pady=2)
    
    def _export_summary(self):
        """Export summary information"""
        file_path = filedialog.asksaveasfilename(
            title="Export Summary",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self._generate_overview_text())
                
                messagebox.showinfo("Success", f"Summary exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export summary: {e}")
    
    def _export_all_data(self):
        """Export all results data"""
        file_path = filedialog.asksaveasfilename(
            title="Export All Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.results_data, f, indent=2)
                
                messagebox.showinfo("Success", f"All data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")
    
    def _export_selected(self):
        """Export selected content in chosen format"""
        format_type = self.export_format.get()
        
        file_ext = {'csv': '.csv', 'json': '.json', 'txt': '.txt', 'html': '.html'}
        file_types = {
            'csv': [("CSV files", "*.csv")],
            'json': [("JSON files", "*.json")],
            'txt': [("Text files", "*.txt")],
            'html': [("HTML files", "*.html")]
        }
        
        file_path = filedialog.asksaveasfilename(
            title=f"Export as {format_type.upper()}",
            defaultextension=file_ext[format_type],
            filetypes=file_types[format_type] + [("All files", "*.*")]
        )
        
        if file_path:
            try:
                if format_type == 'csv':
                    self._export_csv(file_path)
                elif format_type == 'json':
                    self._export_json(file_path)
                elif format_type == 'txt':
                    self._export_txt(file_path)
                elif format_type == 'html':
                    self._export_html(file_path)
                
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def _export_csv(self, file_path):
        """Export data as CSV"""
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            if self.export_templates.get() and self.templates:
                writer.writerow(['Template Results'])
                writer.writerow(['Rank', 'Template', 'Type', 'Subtype', 'Age', 'Redshift', 'Correlation', 'Grade'])
                
                for i, template in enumerate(self.templates, 1):
                    writer.writerow([
                        i,
                        template.get('template', ''),
                        template.get('type', ''),
                        template.get('subtype', ''),
                        template.get('age', ''),
                        template.get('redshift', ''),
                        template.get('correlation', ''),
                        template.get('grade', '')
                    ])
                writer.writerow([])  # Empty row
    
    def _export_json(self, file_path):
        """Export data as JSON"""
        export_data = {}
        
        if self.export_summary.get():
            export_data['summary'] = self.best_match
        
        if self.export_templates.get():
            export_data['templates'] = self.templates
        
        if self.export_statistics.get():
            export_data['statistics'] = self.statistics
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def _export_txt(self, file_path):
        """Export data as text"""
        with open(file_path, 'w') as f:
            f.write(self._generate_overview_text())
    
    def _export_html(self, file_path):
        """Export data as HTML report"""
        html_content = self._generate_html_report()
        with open(file_path, 'w') as f:
            f.write(html_content)
    
    def _generate_html_report(self):
        """Generate HTML report content"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>SNID Analysis Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .summary { background-color: #f9f9f9; padding: 15px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>SNID Analysis Results</h1>
"""
        
        if self.best_match:
            html += f"""
    <div class="summary">
        <h2>Best Match Summary</h2>
        <p><strong>Template:</strong> {self.best_match.get('template', 'N/A')}</p>
        <p><strong>Type:</strong> {self.best_match.get('type', 'N/A')} {self.best_match.get('subtype', '')}</p>
        <p><strong>Correlation:</strong> {self.best_match.get('correlation', 'N/A')}</p>
        <p><strong>Redshift:</strong> {self.best_match.get('redshift', 'N/A')}</p>
        <p><strong>Age:</strong> {self.best_match.get('age', 'N/A')} days</p>
    </div>
"""
        
        if self.templates:
            html += """
    <h2>Template Matches</h2>
    <table>
        <tr>
            <th>Rank</th>
            <th>Template</th>
            <th>Type</th>
            <th>Subtype</th>
            <th>Age (days)</th>
            <th>Redshift</th>
            <th>Correlation</th>
            <th>Grade</th>
        </tr>
"""
            
            for i, template in enumerate(self.templates[:10], 1):  # Top 10
                html += f"""
        <tr>
            <td>{i}</td>
            <td>{template.get('template', '')}</td>
            <td>{template.get('type', '')}</td>
            <td>{template.get('subtype', '')}</td>
            <td>{template.get('age', '')}</td>
            <td>{template.get('redshift', '')}</td>
            <td>{template.get('correlation', '')}</td>
            <td>{template.get('grade', '')}</td>
        </tr>
"""
            
            html += """
    </table>
"""
        
        html += """
</body>
</html>
"""
        
        return html
    
    def _export_all_formats(self):
        """Export data in all available formats"""
        directory = filedialog.askdirectory(title="Select Export Directory")
        
        if directory:
            try:
                base_name = "snid_results"
                
                # Export each format
                self._export_csv(os.path.join(directory, f"{base_name}.csv"))
                self._export_json(os.path.join(directory, f"{base_name}.json"))
                self._export_txt(os.path.join(directory, f"{base_name}.txt"))
                self._export_html(os.path.join(directory, f"{base_name}.html"))
                
                messagebox.showinfo("Success", f"All formats exported to {directory}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export all formats: {e}")
    
    def _custom_export(self):
        """Open custom export dialog"""
        messagebox.showinfo("Custom Export", "Custom export functionality will be implemented in future versions")
    
    def _export_selected_template(self, tree):
        """Export selected template information"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a template to export")
            return
        
        item = selection[0]
        values = tree.item(item, 'values')
        
        file_path = filedialog.asksaveasfilename(
            title="Export Selected Template",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                template_info = f"SNID-SAGE Template Match Information\n"
                template_info += "=" * 35 + "\n\n"
                template_info += f"Rank: {values[0]}\n"
                template_info += f"Template: {values[1]}\n"
                template_info += f"Type: {values[2]}\n"
                template_info += f"Subtype: {values[3]}\n"
                template_info += f"Age: {values[4]} days\n"
                template_info += f"Redshift: {values[5]}\n"
                template_info += f"Correlation: {values[6]}\n"
                template_info += f"Grade: {values[7]}\n"
                
                with open(file_path, 'w') as f:
                    f.write(template_info)
                
                messagebox.showinfo("Success", f"Template information exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export template: {e}")
    
    def _generate_report(self):
        """Generate comprehensive analysis report"""
        file_path = filedialog.asksaveasfilename(
            title="Generate Analysis Report",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                report_content = self._generate_comprehensive_report()
                with open(file_path, 'w') as f:
                    f.write(report_content)
                
                messagebox.showinfo("Success", f"Comprehensive report generated: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def _generate_comprehensive_report(self):
        """Generate comprehensive HTML report with all available information"""
        # This would generate a more detailed report than the basic HTML export
        # Including plots, detailed statistics, and analysis interpretation
        return self._generate_html_report()  # Placeholder - can be enhanced
    
    def _close(self):
        """Close the dialog"""
        self.dialog.destroy()


def show_results_dialog(parent, results_data=None):
    """
    Convenience function to show the results dialog.
    
    Args:
        parent: Parent window
        results_data: SNID analysis results data
    """
    dialog = ResultsDialog(parent, results_data)
    dialog.show() 
