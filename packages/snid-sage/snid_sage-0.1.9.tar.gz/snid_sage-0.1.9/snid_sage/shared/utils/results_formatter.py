"""
Unified Results Formatter
========================

Shared utility for formatting SNID analysis results consistently across CLI and GUI interfaces.
Ensures all output formats (display, export, save) use the same information and structure.
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import numpy as np
import re


class UnifiedResultsFormatter:
    """
    Unified formatter for SNID analysis results that ensures consistency
    between CLI and GUI output formats.
    """
    
    def __init__(self, result, spectrum_name: str = None, spectrum_path: str = None):
        """
        Initialize formatter with SNID result object.
        
        Args:
            result: SNIDResult object
            spectrum_name: Name of the spectrum (optional)
            spectrum_path: Path to spectrum file (optional)
        """
        self.result = result
        self.spectrum_name = spectrum_name or getattr(result, 'spectrum_name', 'Unknown')
        self.spectrum_path = spectrum_path or getattr(result, 'spectrum_path', '')
        
        # Determine which metric is being used
        self.use_rlap_cos = False
        self.metric_name = "RLAP"
        if hasattr(result, 'clustering_results') and result.clustering_results:
            self.use_rlap_cos = result.clustering_results.get('use_rlap_cos', False)
            self.metric_name = result.clustering_results.get('metric_used', 'RLAP-Cos' if self.use_rlap_cos else 'RLAP')
        
        # Create standardized summary data
        self.summary_data = self._create_standardized_summary()
    
    def _create_standardized_summary(self) -> Dict[str, Any]:
        """Create standardized summary data structure used by all output formats"""
        result = self.result
        
        # Get the winning cluster (user selected or automatic best)
        winning_cluster = None
        cluster_label = ""
        cluster_index = -1
        is_manual_selection = False
        
        if hasattr(result, 'clustering_results') and result.clustering_results:
            clustering_results = result.clustering_results
            if clustering_results.get('success'):
                if 'user_selected_cluster' in clustering_results:
                    winning_cluster = clustering_results['user_selected_cluster']
                    cluster_index = clustering_results.get('user_selected_index', -1)
                    cluster_label = f"User Selected Cluster #{cluster_index + 1}"
                    
                    # Check if this is actually a manual selection (different from automatic best)
                    if 'best_cluster' in clustering_results:
                        best_cluster = clustering_results['best_cluster']
                        
                        # Compare the clusters to see if they're different
                        # Compare multiple fields to ensure we catch all differences
                        is_same_cluster = (
                            winning_cluster.get('type') == best_cluster.get('type') and
                            winning_cluster.get('cluster_id') == best_cluster.get('cluster_id') and
                            winning_cluster.get('size') == best_cluster.get('size')
                        )
                        
                        # Additional fallback comparison - check if they're the same object
                        is_same_object = (winning_cluster is best_cluster)
                        
                        # Use the more reliable comparison
                        if is_same_object or is_same_cluster:
                            # User selected the same cluster that was automatically chosen as best
                            cluster_label = "Best Cluster (Auto-Selected)"
                            is_manual_selection = False
                        else:
                            # User selected a different cluster than the automatic best
                            is_manual_selection = True
                    else:
                        # No best_cluster to compare against, assume it's manual
                        is_manual_selection = True
                elif 'best_cluster' in clustering_results:
                    winning_cluster = clustering_results['best_cluster']
                    cluster_label = "Best Cluster (Auto-Selected)"
                    # Find index of best cluster
                    all_candidates = clustering_results.get('all_candidates', [])
                    for i, cluster in enumerate(all_candidates):
                        if cluster == winning_cluster:
                            cluster_index = i
                            break
        
        # Get cluster matches if available
        cluster_matches = []
        if winning_cluster:
            cluster_matches = winning_cluster.get('matches', [])
            # Sort by best available metric (RLAP-Cos if available, otherwise RLAP) descending
            from snid_sage.shared.utils.math_utils import get_best_metric_value
            cluster_matches = sorted(cluster_matches, key=get_best_metric_value, reverse=True)
        
        # Use cluster matches if available, otherwise fall back to regular matches
        active_matches = cluster_matches if cluster_matches else (
            getattr(result, 'filtered_matches', []) or getattr(result, 'best_matches', [])
        )
        
        # Calculate enhanced estimates from cluster if available
        enhanced_redshift = result.consensus_redshift
        enhanced_redshift_error = result.consensus_redshift_error
        enhanced_age = getattr(result, 'consensus_age', 0)
        enhanced_age_error = getattr(result, 'consensus_age_error', 0)
        
        if winning_cluster and cluster_matches:
            # Use cluster-weighted estimates
            enhanced_redshift = winning_cluster.get('enhanced_redshift', result.consensus_redshift)
            enhanced_redshift_error = winning_cluster.get('weighted_redshift_uncertainty', result.consensus_redshift_error)
            
            # Calculate enhanced age from cluster matches
            try:
                from snid_sage.shared.utils.math_utils.weighted_statistics import calculate_rlap_weighted_age
                ages = []
                age_rlaps = []
                for m in cluster_matches:
                    template = m.get('template', {})
                    age = template.get('age', 0.0) if template else 0.0
                    if age > 0:
                        ages.append(age)
                        # Use RLAP-cos if available, otherwise RLAP
                        from snid_sage.shared.utils.math_utils import get_best_metric_value
                        age_rlaps.append(get_best_metric_value(m))
                
                if ages:
                    ages = np.array(ages)
                    # Use RLAP-cos instead of RLAP for age weighting
                    from snid_sage.shared.utils.math_utils import get_best_metric_value
                    age_rlaps = np.array([get_best_metric_value(m) for m in cluster_matches if m.get('template', {}).get('age', 0.0) > 0])
                    age_mean, _, age_total_error, _ = calculate_rlap_weighted_age(
                        ages, age_rlaps, include_cluster_scatter=True
                    )
                    enhanced_age = age_mean
                    enhanced_age_error = age_total_error
            except ImportError:
                pass  # Fall back to consensus values
        
        # Calculate subtype information for the active cluster (not the original result)
        subtype_confidence = 0
        subtype_margin_over_second = 0
        second_best_subtype = None
        consensus_subtype = result.best_subtype  # Default to original
        
        if winning_cluster and cluster_matches:
            # First, try to use pre-calculated subtype information from the cluster
            if 'subtype_info' in winning_cluster:
                subtype_info = winning_cluster['subtype_info']
                consensus_subtype = subtype_info.get('best_subtype', result.best_subtype)
                subtype_confidence = subtype_info.get('subtype_confidence', 0)
                subtype_margin_over_second = subtype_info.get('subtype_margin_over_second', 0)
                second_best_subtype = subtype_info.get('second_best_subtype', None)
            else:
                # Fall back to recalculating subtype information for the active cluster
                try:
                    from snid_sage.snid.cosmological_clustering import choose_subtype_weighted_voting
                    
                    # Get the cluster type and matches
                    cluster_type = winning_cluster.get('type', 'Unknown')
                    type_matches = [m for m in cluster_matches if m['template'].get('type') == cluster_type]
                    
                    if type_matches and hasattr(result, 'clustering_results') and result.clustering_results:
                        clustering_results = result.clustering_results
                        # Find the cluster index within its type
                        type_data = clustering_results.get('type_data', {})
                        if cluster_type in type_data:
                            type_clusters = type_data[cluster_type].get('clusters', [])
                            # Find which cluster this is within the type
                            cluster_idx = None
                            for i, cluster in enumerate(type_clusters):
                                if cluster == winning_cluster:
                                    cluster_idx = i
                                    break
                            
                            if cluster_idx is not None:
                                gamma = type_data[cluster_type].get('gamma', np.array([]))
                                if gamma.size > 0:
                                    consensus_subtype, subtype_confidence, subtype_margin_over_second, second_best_subtype = choose_subtype_weighted_voting(
                                        cluster_type, cluster_idx, type_matches, gamma
                                    )
                except (ImportError, Exception) as e:
                    # Fall back to original values if calculation fails
                    subtype_confidence = getattr(result, 'subtype_confidence', 0)
                    subtype_margin_over_second = getattr(result, 'subtype_margin_over_second', 0)
                    second_best_subtype = getattr(result, 'second_best_subtype', None)
        else:
            # Use original values if no clustering
            subtype_confidence = getattr(result, 'subtype_confidence', 0)
            subtype_margin_over_second = getattr(result, 'subtype_margin_over_second', 0)
            second_best_subtype = getattr(result, 'second_best_subtype', None)
        
        # Create standardized summary
        summary = {
            # Basic identification
            'spectrum_name': self.spectrum_name,
            'spectrum_path': self.spectrum_path,
            'success': result.success,
            'timestamp': datetime.now().isoformat(),
            
            # Primary classification results
            'best_template': result.template_name,
            'best_template_type': result.template_type,
            'best_template_subtype': result.template_subtype,
            'consensus_type': result.consensus_type,
            'consensus_subtype': consensus_subtype,  # Use recalculated subtype
            
            # Primary measurements
            'redshift': result.redshift,
            'redshift_error': result.redshift_error,
            'rlap': result.rlap,
            'r_value': getattr(result, 'r', 0),
            'lap_value': getattr(result, 'lap', 0),
            
            # Enhanced estimates (cluster-weighted when available)
            'enhanced_redshift': enhanced_redshift,
            'enhanced_redshift_error': enhanced_redshift_error,
            'enhanced_age': enhanced_age,
            'enhanced_age_error': enhanced_age_error,
            
            # Security and confidence
            'subtype_confidence': subtype_confidence,  # Use recalculated confidence
            'subtype_margin_over_second': subtype_margin_over_second,  # Use recalculated margin
            'second_best_subtype': second_best_subtype,  # Use recalculated second best
            
            # Analysis metadata
            'runtime_seconds': result.runtime_sec,
            'total_matches': len(getattr(result, 'best_matches', [])),
            'analysis_method': 'GMM Clustering' if winning_cluster else 'Standard Analysis',
            
            # Clustering information
            'has_clustering': winning_cluster is not None,
            'cluster_label': cluster_label,
            'cluster_index': cluster_index,
            'is_manual_selection': is_manual_selection,  # Store manual selection flag
            'cluster_size': len(cluster_matches) if cluster_matches else 0,
            'cluster_type': winning_cluster.get('type', '') if winning_cluster else '',
            'cluster_quality': winning_cluster.get('redshift_quality', '') if winning_cluster else '',
            'cluster_mean_rlap': winning_cluster.get('mean_rlap', 0) if winning_cluster else 0,
            'cluster_mean_metric': winning_cluster.get('mean_metric', winning_cluster.get('mean_rlap', 0)) if winning_cluster else 0,
            'cluster_score': winning_cluster.get('composite_score', 0) if winning_cluster else 0,
            
            # New quality metrics
            'cluster_quality_level': winning_cluster.get('quality_assessment', {}).get('quality_category', '') if winning_cluster else '',
            'cluster_quality_description': winning_cluster.get('quality_assessment', {}).get('quality_description', '') if winning_cluster else '',
            'cluster_mean_top_5': winning_cluster.get('quality_assessment', {}).get('mean_top_5', 0) if winning_cluster else 0,
            'cluster_penalized_score': winning_cluster.get('quality_assessment', {}).get('penalized_score', 0) if winning_cluster else 0,
            'cluster_confidence_level': winning_cluster.get('confidence_assessment', {}).get('confidence_level', '') if winning_cluster else '',
            'cluster_confidence_description': winning_cluster.get('confidence_assessment', {}).get('confidence_description', '') if winning_cluster else '',
            'cluster_statistical_significance': winning_cluster.get('confidence_assessment', {}).get('statistical_significance', '') if winning_cluster else '',
            'cluster_second_best_type': winning_cluster.get('confidence_assessment', {}).get('second_best_type', '') if winning_cluster else '',
            
            # Template matches (ALL from active matches if clustering, otherwise top 10)
            'template_matches': self._format_template_matches(cluster_matches) if winning_cluster and cluster_matches else self._format_template_matches(active_matches[:10]),
            
            # Additional clustering statistics
            'clustering_overview': self._get_clustering_overview() if hasattr(result, 'clustering_results') else None,
        }
        
        return summary
    
    def _format_template_matches(self, matches: List[Dict]) -> List[Dict[str, Any]]:
        """Format template matches for consistent display - now includes ALL matches from cluster"""
        formatted_matches = []
        
        # If we have clustering, get ALL matches from the winning cluster, not just top 10
        # Check clustering state directly from result object to avoid circular dependency
        has_clustering = (hasattr(self.result, 'clustering_results') and 
                         self.result.clustering_results and 
                         self.result.clustering_results.get('success'))
        
        if has_clustering:
            winning_cluster = self._get_active_cluster()
            if winning_cluster:
                cluster_matches = winning_cluster.get('matches', [])
                # Sort by best available metric (RLAP-Cos if available, otherwise RLAP) descending
                from snid_sage.shared.utils.math_utils import get_best_metric_value
                matches = sorted(cluster_matches, key=get_best_metric_value, reverse=True)
        
        for i, match in enumerate(matches, 1):
            template = match.get('template', {})
            template_name = match.get('name', template.get('name', 'Unknown'))
            
            # Get type and subtype separately
            main_type = match.get('type', template.get('type', 'Unknown'))
            subtype = template.get('subtype', '')
            if not subtype or subtype == 'Unknown':
                subtype = ''
            
            # Get age from template
            age = template.get('age', 0.0) if template else 0.0
            
            # Get redshift error from correlation analysis
            redshift_error = match.get('redshift_error', 0)
            
            # Get all available metric values for display
            from snid_sage.shared.utils.math_utils import get_metric_display_values, get_best_metric_value
            metric_values = get_metric_display_values(match)
            
            formatted_match = {
                'rank': i,
                'template_name': template_name,
                'display_type': subtype if subtype else main_type,  # Prefer subtype for display
                'full_type': main_type,
                'subtype': subtype,
                'age_days': age,
                'redshift': match.get('redshift', 0),
                'redshift_error': redshift_error,
                'rlap': match.get('rlap', 0),
                'correlation': match.get('correlation', 0),
                'grade': match.get('grade', ''),
                
                # Enhanced metric information
                'primary_metric': metric_values['primary_metric'],
                'metric_name': metric_values['metric_name'],
                'best_metric_value': get_best_metric_value(match)
            }
            
            # Add RLAP-Cos specific fields if available
            if 'rlap_cos' in metric_values:
                formatted_match.update({
                    'rlap_cos': metric_values['rlap_cos'],
                    'cosine_similarity': metric_values['cosine_similarity'],
                    'cosine_similarity_capped': metric_values['cosine_similarity_capped']
                })
            
            formatted_matches.append(formatted_match)
        
        return formatted_matches
    
    def _get_clustering_overview(self) -> Optional[Dict[str, Any]]:
        """Get clustering overview information"""
        if not hasattr(self.result, 'clustering_results') or not self.result.clustering_results:
            return None
        
        clustering_results = self.result.clustering_results
        if not clustering_results.get('success'):
            return None
        
        all_candidates = clustering_results.get('all_candidates', [])
        if len(all_candidates) <= 1:
            return None
        
        # Get active cluster
        active_cluster = None
        if 'user_selected_cluster' in clustering_results:
            active_cluster = clustering_results['user_selected_cluster']
        elif 'best_cluster' in clustering_results:
            active_cluster = clustering_results['best_cluster']
        
        # Get other clusters (top 3)
        other_clusters = [c for c in all_candidates if c != active_cluster][:3]
        
        return {
            'total_clusters_found': len(all_candidates),
            'active_cluster_type': active_cluster.get('type', 'Unknown') if active_cluster else 'Unknown',
            'other_top_clusters': [
                {
                    'type': c.get('type', 'Unknown'),
                    'size': c.get('size', 0),
                    'mean_rlap': c.get('mean_rlap', 0),
                    'mean_metric': c.get('mean_metric', c.get('mean_rlap', 0))
                }
                for c in other_clusters
            ]
        }
    
    def get_display_summary(self) -> str:
        """Get formatted summary for display (CLI/GUI)"""
        s = self.summary_data
        
        # Use the manual selection flag from summary data
        is_manual_selection = s.get('is_manual_selection', False)
        
        # Build display summary
        lines = [
            "SNID CLASSIFICATION RESULTS",
            "=" * 50,
            "",
        ]
        
        # Different header based on selection method
        if is_manual_selection:
            lines.append("FINAL CLASSIFICATION (Manual Selection):")
        else:
            lines.append("FINAL CLASSIFICATION (Automatic Method):")
        
        # Type with quality metrics (always show quality as it's cluster-specific)
        if s['has_clustering'] and s['cluster_quality_level']:
            lines.append(f"   Type: {s['consensus_type']} (Quality: {s['cluster_quality_level'].title()})")
        else:
            lines.append(f"   Type: {s['consensus_type']}")
        
        # Add confidence level and type margin ONLY for automatic selection
        if not is_manual_selection and s['has_clustering'] and s['cluster_confidence_level']:
            lines.append(f"   Confidence Level: {s['cluster_confidence_level'].title()}")
            if s['cluster_confidence_description']:
                second_best_type = s.get('cluster_second_best_type', None)
                if second_best_type and second_best_type != 'N/A':
                    # Try to extract the margin percentage from the description
                    if '% better than second best' in s['cluster_confidence_description']:
                        # Extract just the percentage number, not the full text
                        margin_match = re.search(r'(\d+\.?\d*)% better than second best', s['cluster_confidence_description'])
                        if margin_match:
                            margin_text = margin_match.group(1)
                            lines.append(f"   └─ Winning type is {margin_text}% better than second best ({second_best_type})")
                        else:
                            # Fallback to original logic if regex doesn't work
                            margin_text = s['cluster_confidence_description'].split('% better than second best')[0]
                            margin_text = margin_text.strip()
                            lines.append(f"   └─ Winning type is {margin_text}% better than second best ({second_best_type})")
                    else:
                        lines.append(f"   └─ Winning type margin: {s['cluster_confidence_description']} ({second_best_type})")
                else:
                    lines.append(f"   └─ {s['cluster_confidence_description']}")
        
        # Subtype with its specific confidence if available (always show as it's within-cluster)
        if s['consensus_subtype'] and s['consensus_subtype'] != 'Unknown':
            subtype_conf_text = ""
            if s['subtype_confidence'] > 0:
                # Convert to descriptive level
                if s['subtype_confidence'] > 0.7:
                    subtype_level = "High"
                elif s['subtype_confidence'] > 0.4:
                    subtype_level = "Medium"
                else:
                    subtype_level = "Low"
                subtype_conf_text = f" (confidence: {subtype_level})"
            
            lines.append(f"   Subtype: {s['consensus_subtype']}{subtype_conf_text}")
            
            # Always show margin/second best subtype if second_best_subtype is present
            second_best = s.get('second_best_subtype')
            margin = s.get('subtype_margin_over_second', 0)
            if second_best and second_best != s['consensus_subtype']:
                if margin == 0:
                    lines.append(f"   └─ Winning subtype is tied with ({second_best})")
                else:
                    # The margin is now calculated as relative percentage in choose_subtype_weighted_voting
                    lines.append(f"   └─ Winning subtype is {margin:.1f}% better than second best ({second_best})")
        
        lines.extend([
            "",
            "📏 MEASUREMENTS:",
        ])
        
        # Use enhanced (weighted) redshift if clustering was used, otherwise regular
        if s['has_clustering'] and s['enhanced_redshift'] != s['redshift']:
            # Show the weighted redshift with combined uncertainty
            redshift_text = f"   Redshift: {s['enhanced_redshift']:.6f} ± {s['enhanced_redshift_error']:.6f}"
            
            # Optionally show components of uncertainty in parentheses
            try:
                # Try to get the separate uncertainty components if available
                winning_cluster = self._get_active_cluster()
                if winning_cluster:
                    stat_error = winning_cluster.get('statistical_redshift_uncertainty', 0)
                    sys_error = winning_cluster.get('systematic_redshift_uncertainty', 0)
                    if stat_error > 0 and sys_error > 0:
                        redshift_text += f" (stat: ±{stat_error:.6f}, sys: ±{sys_error:.6f})"
            except:
                pass  # If components not available, just show combined
            
            lines.append(redshift_text)
            lines.append(f"   └─ Weighted from {s['cluster_size']} cluster templates (includes individual errors + cluster scatter τ)")
        else:
            # Regular redshift from best template
            lines.append(f"   Redshift: {s['redshift']:.6f} ± {s['redshift_error']:.6f} (correlation fit uncertainty)")
        
        if s['enhanced_age'] > 0:
            lines.append(f"   Age: {s['enhanced_age']:.0f} ± {s['enhanced_age_error']:.0f} days")
        
        lines.append("")
        
        # Show clustering overview if multiple clusters found
        if s['has_clustering']:
            overview = s['clustering_overview']
            if overview and overview['total_clusters_found'] > 1:
                lines.extend([
                    "📈 CLUSTERING OVERVIEW:",
                    f"   Total Clusters Found: {overview['total_clusters_found']}",
                    f"   Active Cluster: {overview['active_cluster_type']}",
                ])
                
                if overview['other_top_clusters']:
                    other_types = [f"{c['type']} ({c['size']})" for c in overview['other_top_clusters']]
                    lines.append(f"   Other Clusters: {', '.join(other_types)}")
                lines.append("")
        

        
        # Template matches - show ALL from winning cluster with detailed info and improved formatting
        if s['template_matches']:
            cluster_note = f" (from {s['cluster_label']})" if s['has_clustering'] else ""
            lines.extend([
                f"🏆 TEMPLATE MATCHES{cluster_note}:",
                f"{'#':<3} {'Template':<18} {'Type':<8} {'Subtype':<10} {self.metric_name:<8}     {'Redshift':<12}     {'±Error':<10}     {'Age':<8}",
                "-" * 105,
            ])
            
            for match in s['template_matches']:
                age_str = f"{match['age_days']:.1f}" if match['age_days'] is not None else "N/A"
                redshift_error_str = f"{match.get('redshift_error', 0):.6f}" if match.get('redshift_error', 0) > 0 else "N/A"
                
                # Use best available metric value
                metric_value = match.get('best_metric_value', match['rlap'])
                
                lines.append(
                    f"{match['rank']:<3} {match['template_name'][:17]:<18} "
                    f"{match['full_type'][:7]:<8} {match['subtype'][:9]:<10} {metric_value:<8.1f}     "
                    f"{match['redshift']:<12.6f}     {redshift_error_str:<10}     {age_str:<8}"
                )
        
        # Filter out empty strings and join
        return "\n".join(line for line in lines if line is not None)
    
    def get_export_data(self) -> Dict[str, Any]:
        """Get data structure for export (JSON, CSV, etc.)"""
        return self.summary_data.copy()
    
    def get_cli_one_line_summary(self) -> str:
        """Get one-line summary for CLI batch processing"""
        s = self.summary_data
        
        # Format type display
        type_display = f"{s['consensus_type']} {s['consensus_subtype']}".strip()
        
        # Use enhanced redshift if clustering was used
        if s['has_clustering']:
            redshift = s['enhanced_redshift']
            z_marker = "🎯"  # Cluster analysis marker
        else:
            redshift = s['redshift']
            z_marker = ""
        
        # Get best metric value
        if s['template_matches']:
            best_metric = s['template_matches'][0].get('best_metric_value', s['rlap'])
        else:
            best_metric = s['rlap']
        
        return f"{self.spectrum_name}: {type_display} z={redshift:.4f} {self.metric_name}={best_metric:.1f} {z_marker}"
    
    def save_to_file(self, filename: str, format_type: str = 'txt'):
        """Save results to file in specified format"""
        if format_type.lower() == 'json':
            self._save_json(filename)
        elif format_type.lower() == 'csv':
            self._save_csv(filename)
        else:  # txt
            self._save_txt(filename)
    
    def _save_json(self, filename: str):
        """Save results as JSON"""
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.get_export_data(), f, indent=2, default=str)
    
    def _save_csv(self, filename: str):
        """Save results as CSV"""
        import csv
        data = self.get_export_data()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Basic information
            writer.writerow(['Property', 'Value'])
            for key, value in data.items():
                if not isinstance(value, (list, dict)) or value is None:
                    writer.writerow([key, value])
            
            # Template matches
            if data['template_matches']:
                writer.writerow([])
                writer.writerow(['Template Matches'])
                writer.writerow(['Rank', 'Template', 'Type', 'Subtype', 'Age', 'Redshift', self.metric_name])
                
                for match in data['template_matches']:
                    writer.writerow([
                        match['rank'], match['template_name'], match['full_type'],
                        match['subtype'], match['age_days'], match['redshift'], 
                        match.get('best_metric_value', match['rlap'])
                    ])
    
    def _save_txt(self, filename: str):
        """Save results as text"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"SNID-SAGE Analysis Results\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            f.write(self.get_display_summary())
    
    def _get_active_cluster(self):
        """Get the active cluster being used"""
        if not hasattr(self.result, 'clustering_results') or not self.result.clustering_results:
            return None
        
        clustering_results = self.result.clustering_results
        if not clustering_results.get('success'):
            return None
        
        if 'user_selected_cluster' in clustering_results:
            return clustering_results['user_selected_cluster']
        elif 'best_cluster' in clustering_results:
            return clustering_results['best_cluster']
        
        return None


def create_unified_formatter(result, spectrum_name: str = None, spectrum_path: str = None) -> UnifiedResultsFormatter:
    """
    Convenience function to create a unified results formatter.
    
    Args:
        result: SNIDResult object
        spectrum_name: Name of the spectrum (optional)
        spectrum_path: Path to spectrum file (optional)
    
    Returns:
        UnifiedResultsFormatter instance
    """
    return UnifiedResultsFormatter(result, spectrum_name, spectrum_path) 