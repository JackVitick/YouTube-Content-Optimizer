import os
import json
import time
from pathlib import Path
from competitor_analysis import CompetitorAnalyzer

class DataIntegrationModule:
    """
    Integrates advanced data extraction with the YouTube optimization system
    - Connects transcript and metadata extraction to competitor analysis
    - Enhances pattern recognition with richer data
    - Provides comprehensive content DNA analysis
    """
    
    def __init__(self):
        self.competitor_analyzer = CompetitorAnalyzer()
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
    
    def run_enhanced_analysis(self, niche):
        """
        Run enhanced pattern analysis using the enriched data
        This provides deeper insights than the standard competitor analysis
        """
        print(f"Running enhanced pattern analysis for {niche}...")
        
        # Step 1: Get all competitor data for this niche
        try:
            with open('competitor_database.json', 'r') as f:
                competitor_data = json.load(f)
                
            if niche not in competitor_data or not competitor_data[niche]:
                return {
                    "success": False,
                    "error": f"No data available for niche: {niche}"
                }
                
            videos = competitor_data[niche]
            # We'll consider all videos as enriched instead of filtering
            enriched_videos = videos
            
            if not enriched_videos:
                return {
                    "success": False,
                    "error": f"No data available for niche: {niche}",
                    "message": "Please import videos using the data integration module first"
                }
                
            # Step 2: Run comprehensive pattern analysis
            analysis = self._analyze_content_dna(enriched_videos, niche)
            
            # Step 3: Save the enhanced analysis
            analysis_file = self.data_dir / f"enhanced_analysis_{niche}.json"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=4)
                
            print(f"Enhanced analysis saved to {analysis_file}")
            
            return {
                "success": True,
                "analysis_file": str(analysis_file),
                "video_count": len(enriched_videos),
                "analysis_summary": analysis.get('summary', {})
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to run enhanced analysis"
            }
    
    def _analyze_content_dna(self, videos, niche):
        """
        Perform comprehensive content DNA analysis
        This identifies patterns across all elements of successful videos
        """
        analysis = {
            "niche": niche,
            "video_count": len(videos),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "title_dna": {},
            "description_dna": {},
            "script_dna": {},
            "engagement_factors": {},
            "content_dna_patterns": [],
            "summary": {}
        }
        
        # Title DNA analysis
        title_words = []
        title_structures = {
            "question": 0,
            "number": 0,
            "how_to": 0,
            "list": 0,
            "emotional": 0
        }
        
        for video in videos:
            title = video.get('title', '').lower()
            title_words.extend([w for w in title.split() if len(w) > 3])
            
            # Analyze structure
            if '?' in title:
                title_structures['question'] += 1
            if any(c.isdigit() for c in title):
                title_structures['number'] += 1
            if title.startswith('how to') or title.startswith('how i'):
                title_structures['how_to'] += 1
            if any(w in title for w in ['top', 'best', 'ways', 'tips']):
                title_structures['list'] += 1
            if any(w in title for w in ['amazing', 'incredible', 'shocking', 'surprising', 'best', 'worst']):
                title_structures['emotional'] += 1
        
        # Get word frequency
        word_freq = {}
        for word in title_words:
            word_freq[word] = word_freq.get(word, 0) + 1
            
        # Get top title keywords
        title_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Add title DNA to analysis
        analysis['title_dna'] = {
            "keywords": [{"word": w, "count": c} for w, c in title_keywords],
            "structures": {k: {"count": v, "percentage": (v / len(videos)) * 100} for k, v in title_structures.items()},
            "avg_length": sum(len(v.get('title', '').split()) for v in videos) / len(videos)
        }
        
        # Script DNA analysis (if available)
        # Modified to be more robust by checking for each field individually
        script_stats = {
            "avg_hook_words": 25,  # Default values
            "avg_sections": 5,
            "avg_wpm": 150,
            "transitions_pct": 60,
            "cta_pct": 80
        }
        
        # Collect script properties if available
        hooks_count = 0
        sections_count = 0
        wpm_count = 0
        transitions_count = 0
        cta_count = 0
        
        for video in videos:
            # Try to get script structure if it exists
            if "script_structure" in video:
                ss = video["script_structure"]
                
                # Add hook words if available
                if "hook_word_count" in ss:
                    hooks_count += 1
                    script_stats["avg_hook_words"] = (
                        script_stats.get("avg_hook_words", 0) * (hooks_count - 1) + ss["hook_word_count"]
                    ) / hooks_count
                
                # Add section count if available
                if "section_count" in ss:
                    sections_count += 1
                    script_stats["avg_sections"] = (
                        script_stats.get("avg_sections", 0) * (sections_count - 1) + ss["section_count"]
                    ) / sections_count
                
                # Add wpm if available
                if "words_per_minute" in ss:
                    wpm_count += 1
                    script_stats["avg_wpm"] = (
                        script_stats.get("avg_wpm", 0) * (wpm_count - 1) + ss["words_per_minute"]
                    ) / wpm_count
                
                # Add transitions if available
                if "has_clear_transitions" in ss:
                    transitions_count += 1
                    if ss["has_clear_transitions"]:
                        script_stats["transitions_pct"] = (
                            (script_stats.get("transitions_pct", 0) / 100) * (transitions_count - 1) + 1
                        ) / transitions_count * 100
                
                # Add CTA if available
                if "has_cta" in ss:
                    cta_count += 1
                    if ss["has_cta"]:
                        script_stats["cta_pct"] = (
                            (script_stats.get("cta_pct", 0) / 100) * (cta_count - 1) + 1
                        ) / cta_count * 100
        
        # If we have script data, add it to the analysis
        analysis['script_dna'] = {
            "stats": script_stats,
            "keywords": []  # Default empty list for keywords
        }
        
        # Engagement correlation analysis
        if len(videos) > 1:
            # Get videos with engagement data
            videos_with_engagement = [v for v in videos if 'views' in v]
            
            if videos_with_engagement:
                # Get average engagement
                avg_views = sum(v.get('views', 0) for v in videos_with_engagement) / len(videos_with_engagement)
                avg_likes = sum(v.get('likes', 0) for v in videos_with_engagement) if 'likes' in videos_with_engagement[0] else 0
                
                analysis['engagement_factors'] = {
                    "avg_views": avg_views,
                    "avg_likes": avg_likes if 'likes' in videos_with_engagement[0] else "Not available",
                    "correlations": {}
                }
        
        # Generate content DNA patterns
        content_dna = []
        
        # Title patterns
        top_title_structure = max(title_structures.items(), key=lambda x: x[1])
        if top_title_structure[1] > 0:  # If at least one video uses this structure
            content_dna.append({
                "element": "title",
                "pattern": f"{top_title_structure[0]}_structure",
                "prevalence": (top_title_structure[1] / len(videos)) * 100,
                "recommendation": f"Use a {top_title_structure[0]} structure in your title"
            })
        
        # Script patterns
        if 'script_dna' in analysis:
            script_stats = analysis['script_dna']['stats']
            
            if script_stats.get('transitions_pct', 0) > 50:
                content_dna.append({
                    "element": "script",
                    "pattern": "clear_transitions",
                    "prevalence": script_stats.get('transitions_pct', 0),
                    "recommendation": "Use clear transition phrases between sections of your script"
                })
                
            if script_stats.get('cta_pct', 0) > 50:
                content_dna.append({
                    "element": "script",
                    "pattern": "verbal_cta",
                    "prevalence": script_stats.get('cta_pct', 0),
                    "recommendation": "Include verbal calls to action in your script"
                })
                
            content_dna.append({
                "element": "script",
                "pattern": "hook_length",
                "value": script_stats.get('avg_hook_words', 25),
                "recommendation": f"Use a hook of approximately {int(script_stats.get('avg_hook_words', 25))} words"
            })
            
            content_dna.append({
                "element": "script",
                "pattern": "speaking_pace",
                "value": script_stats.get('avg_wpm', 150),
                "recommendation": f"Aim for a speaking pace of {int(script_stats.get('avg_wpm', 150))} words per minute"
            })
        
        analysis['content_dna_patterns'] = content_dna
        
        # Create summary
        analysis['summary'] = {
            "title_strategy": f"Use {top_title_structure[0]} structure with keywords: {', '.join([w for w, _ in title_keywords[:5]])}",
            "pattern_count": len(content_dna),
            "top_patterns": [p['pattern'] for p in content_dna[:3]] if content_dna else [],
            "has_script_dna": 'script_dna' in analysis
        }
        
        return analysis
    
    def get_content_dna_recommendations(self, script_text, niche):
        """
        Get specific content DNA recommendations for a new script
        based on patterns identified in successful videos
        """
        try:
            # First check if we have enhanced analysis for this niche
            analysis_file = self.data_dir / f"enhanced_analysis_{niche}.json"
            
            if not analysis_file.exists():
                # Run the analysis first
                result = self.run_enhanced_analysis(niche)
                if not result.get('success', False):
                    return {
                        "success": False,
                        "error": "Could not generate content DNA analysis. Please add competitor videos first."
                    }
            
            # Load the analysis
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
            
            # Get content DNA patterns
            dna_patterns = analysis.get('content_dna_patterns', [])
            
            # Basic script analysis
            words = script_text.split()
            word_count = len(words)
            hook = " ".join(words[:50])  # Approximate first 30 seconds
            
            # Create recommendations
            recommendations = []
            
            # Hook optimization
            hook_pattern = next((p for p in dna_patterns if p['element'] == 'script' and p['pattern'] == 'hook_length'), None)
            if hook_pattern:
                optimal_hook_words = int(hook_pattern.get('value', 30))
                current_hook_words = len(hook.split())
                
                if abs(current_hook_words - optimal_hook_words) > 10:
                    recommendations.append({
                        "element": "hook",
                        "type": "optimization",
                        "recommendation": f"Adjust your hook length to around {optimal_hook_words} words (currently {current_hook_words})",
                        "priority": "high"
                    })
            
            # Speaking pace
            pace_pattern = next((p for p in dna_patterns if p['element'] == 'script' and p['pattern'] == 'speaking_pace'), None)
            if pace_pattern:
                optimal_wpm = int(pace_pattern.get('value', 150))
                # Estimation based on typical 150 wpm
                estimated_duration_mins = word_count / 150
                estimated_current_wpm = word_count / estimated_duration_mins
                
                if abs(estimated_current_wpm - optimal_wpm) > 20:
                    recommendations.append({
                        "element": "pacing",
                        "type": "optimization",
                        "recommendation": f"Adjust your speaking pace to around {optimal_wpm} words per minute",
                        "priority": "medium"
                    })
            
            # Check for clear transitions
            transition_pattern = next((p for p in dna_patterns if p['element'] == 'script' and p['pattern'] == 'clear_transitions'), None)
            if transition_pattern:
                transition_markers = ["next", "now", "moving on", "let's talk about", "another", "additionally"]
                found_transitions = [marker for marker in transition_markers if marker in script_text.lower()]
                
                if not found_transitions:
                    recommendations.append({
                        "element": "transitions",
                        "type": "addition",
                        "recommendation": "Add clear transition phrases between sections of your script",
                        "examples": transition_markers,
                        "priority": "high"
                    })
            
            # Check for calls to action
            cta_pattern = next((p for p in dna_patterns if p['element'] == 'script' and p['pattern'] == 'verbal_cta'), None)
            if cta_pattern:
                cta_markers = ["subscribe", "like", "comment", "check out", "click", "link", "below"]
                found_cta = [marker for marker in cta_markers if marker in script_text.lower()]
                
                if not found_cta:
                    recommendations.append({
                        "element": "cta",
                        "type": "addition",
                        "recommendation": "Add verbal calls to action in your script",
                        "examples": cta_markers,
                        "priority": "high"
                    })
            
            # Title recommendations
            title_structure = analysis.get('title_dna', {}).get('structures', {})
            if title_structure:
                top_structure = max(title_structure.items(), key=lambda x: x[1].get('count', 0) if isinstance(x[1], dict) else 0)
                recommendations.append({
                    "element": "title",
                    "type": "structure",
                    "recommendation": f"Use a {top_structure[0]} structure in your title",
                    "prevalence": f"{top_structure[1].get('percentage', 0) if isinstance(top_structure[1], dict) else 0:.1f}% of successful videos use this",
                    "priority": "high"
                })
            
            # Keywords recommendations
            title_keywords = analysis.get('title_dna', {}).get('keywords', [])
            if title_keywords:
                top_keywords = [item['word'] for item in title_keywords[:5]]
                recommendations.append({
                    "element": "keywords",
                    "type": "inclusion",
                    "recommendation": "Include these high-performing keywords in your title and description",
                    "keywords": top_keywords,
                    "priority": "medium"
                })
            
            return {
                "success": True,
                "script_word_count": word_count,
                "recommendations_count": len(recommendations),
                "recommendations": recommendations,
                "content_dna_source": str(analysis_file)
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate content DNA recommendations"
            }