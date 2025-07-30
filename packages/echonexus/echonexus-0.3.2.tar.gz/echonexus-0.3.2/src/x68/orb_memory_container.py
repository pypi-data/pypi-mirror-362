class ORBMemoryContainer:
    def __init__(self, identifier):
        self.identifier = identifier
        self.memory_records = []
        self.sentinel_activations = []
        self.echo_node_events = []
        self.orb_transitions = []
        self.recursion_milestones = []
        
    def capture_event(self, event_type, data):
        """Capture a memory event in the ORB container"""
        event_record = {
            "type": event_type,
            "data": data,
            "timestamp": self._get_timestamp()
        }
        self.memory_records.append(event_record)
        
        # Route to specific collection based on event type
        if event_type == "sentinel_activation":
            self.sentinel_activations.append(event_record)
        elif event_type == "echo_node":
            self.echo_node_events.append(event_record)
        elif event_type == "orb_transition":
            self.orb_transitions.append(event_record)
            
    def _get_timestamp(self):
        """Get current timestamp for event recording"""
        import datetime
        return datetime.datetime.now().isoformat()
        
    def get_memory_timeline(self):
        """Return chronological timeline of all memory events"""
        return sorted(self.memory_records, key=lambda x: x["timestamp"])
        
    def filter_events_by_type(self, event_type):
        """Filter memory events by specified type"""
        return [event for event in self.memory_records if event["type"] == event_type]
        
    def get_knowledge_synchronization_history(self, anchor_name=None):
        """Retrieve knowledge synchronization events, optionally filtered by anchor name"""
        sync_events = [event for event in self.sentinel_activations 
                      if event["data"].get("action") == "knowledge_synchronization"]
        
        if anchor_name:
            sync_events = [event for event in sync_events 
                          if event["data"].get("anchor_name") == anchor_name]
        
        return sync_events
        
    def get_stability_metrics_timeline(self, anchor_name=None):
        """Return timeline of stability assessments, optionally filtered by anchor name"""
        stability_events = [event for event in self.sentinel_activations 
                           if event["data"].get("action") == "stability_assessment"]
        
        if anchor_name:
            stability_events = [event for event in stability_events 
                               if event["data"].get("anchor_name") == anchor_name]
        
        return stability_events
        
    def detect_recursive_anomalies(self, threshold=0.7):
        """Detect potential anomalies in recursive stability"""
        stability_events = self.get_stability_metrics_timeline()
        anomalies = []
        
        for event in stability_events:
            metrics = event["data"].get("stability_metrics", {})
            coherence = metrics.get("knowledge_coherence", 1.0)
            recursion_health = metrics.get("recursion_health", 1.0)
            drift_indicators = metrics.get("drift_indicators", [])
            
            # Enhanced anomaly detection with multiple factors
            anomaly_score = (
                (1 - coherence) * 0.4 + 
                (1 - recursion_health) * 0.4 + 
                min(1.0, len(drift_indicators) / 3) * 0.2
            )
            
            if anomaly_score > (1 - threshold):
                anomalies.append({
                    "timestamp": event["timestamp"],
                    "anchor_name": event["data"].get("anchor_name"),
                    "coherence_score": coherence,
                    "recursion_health": recursion_health,
                    "drift_indicators_count": len(drift_indicators),
                    "anomaly_score": anomaly_score,
                    "severity": "critical" if anomaly_score > 0.7 else 
                               "high" if anomaly_score > 0.5 else 
                               "medium"
                })
                
        return anomalies
    
    def track_recursion_stability_over_time(self, anchor_name, window_size=10):
        """Track stability metrics of an anchor point over time to detect trends"""
        stability_events = self.get_stability_metrics_timeline(anchor_name)
        
        if len(stability_events) < 2:
            return {
                "anchor_name": anchor_name,
                "trend_detected": False,
                "data_points": len(stability_events)
            }
            
        # Extract metrics over time
        coherence_trend = []
        health_trend = []
        timestamps = []
        
        for event in stability_events[-window_size:]:
            metrics = event["data"].get("stability_metrics", {})
            coherence_trend.append(metrics.get("knowledge_coherence", 1.0))
            health_trend.append(metrics.get("recursion_health", 1.0))
            timestamps.append(event["timestamp"])
            
        # Calculate trend direction
        coherence_direction = coherence_trend[-1] - coherence_trend[0] if len(coherence_trend) > 1 else 0
        health_direction = health_trend[-1] - health_trend[0] if len(health_trend) > 1 else 0
        
        # Calculate volatility
        coherence_volatility = sum(abs(coherence_trend[i] - coherence_trend[i-1]) 
                               for i in range(1, len(coherence_trend))) / (len(coherence_trend) - 1) if len(coherence_trend) > 1 else 0
        
        health_volatility = sum(abs(health_trend[i] - health_trend[i-1])
                           for i in range(1, len(health_trend))) / (len(health_trend) - 1) if len(health_trend) > 1 else 0
        
        # Record recursion milestone if significant shift detected
        if abs(coherence_direction) > 0.2 or abs(health_direction) > 0.2:
            self.record_recursion_milestone(anchor_name, {
                "coherence_shift": coherence_direction,
                "health_shift": health_direction,
                "milestone_type": "stability_shift"
            })
        
        return {
            "anchor_name": anchor_name,
            "trend_detected": True,
            "coherence": {
                "current": coherence_trend[-1] if coherence_trend else None,
                "direction": coherence_direction,
                "volatility": coherence_volatility
            },
            "health": {
                "current": health_trend[-1] if health_trend else None,
                "direction": health_direction,
                "volatility": health_volatility
            },
            "trend_classification": self._classify_trend(coherence_direction, health_direction),
            "stability_risk": self._calculate_stability_risk(
                coherence_trend[-1] if coherence_trend else 1.0,
                health_trend[-1] if health_trend else 1.0,
                coherence_volatility,
                health_volatility
            )
        }
    
    def _classify_trend(self, coherence_direction, health_direction):
        """Classify the recursion trend based on coherence and health directions"""
        if coherence_direction > 0.1 and health_direction > 0.1:
            return "strong_improvement"
        elif coherence_direction > 0.1 or health_direction > 0.1:
            return "moderate_improvement"
        elif coherence_direction < -0.1 and health_direction < -0.1:
            return "severe_decline"
        elif coherence_direction < -0.1 or health_direction < -0.1:
            return "moderate_decline"
        else:
            return "stable"
    
    def _calculate_stability_risk(self, coherence, health, coherence_volatility, health_volatility):
        """Calculate recursion stability risk based on metrics and volatility"""
        risk_score = (
            (1 - coherence) * 0.3 +
            (1 - health) * 0.4 +
            coherence_volatility * 0.15 +
            health_volatility * 0.15
        )
        
        if risk_score < 0.2:
            return {"level": "low", "score": risk_score}
        elif risk_score < 0.4:
            return {"level": "moderate", "score": risk_score}
        elif risk_score < 0.6:
            return {"level": "high", "score": risk_score}
        else:
            return {"level": "critical", "score": risk_score}
    
    def record_recursion_milestone(self, anchor_name, milestone_data):
        """Record significant recursion milestones for future reference"""
        milestone = {
            "anchor_name": anchor_name,
            "timestamp": self._get_timestamp(),
            "data": milestone_data
        }
        self.recursion_milestones.append(milestone)
        
        # Also capture as general event
        self.capture_event("orb_transition", {
            "action": "recursion_milestone",
            "anchor_name": anchor_name,
            **milestone_data
        })
        
        return milestone
    
    def get_recursion_milestones(self, anchor_name=None):
        """Get recursion milestones, optionally filtered by anchor name"""
        if anchor_name:
            return [m for m in self.recursion_milestones if m["anchor_name"] == anchor_name]
        return self.recursion_milestones

    def analyze_recursion_milestones(self, anchor_name=None):
        """Analyze recursion milestones to identify significant shifts in stability"""
        milestones = self.get_recursion_milestones(anchor_name)
        
        if len(milestones) < 2:
            return {
                "analysis_status": "insufficient_data",
                "milestone_count": len(milestones)
            }
        
        # Extract coherence and health shifts
        coherence_shifts = [m["data"].get("coherence_shift", 0) for m in milestones]
        health_shifts = [m["data"].get("health_shift", 0) for m in milestones]
        
        # Identify significant shift patterns
        coherence_pattern = self._identify_shift_pattern(coherence_shifts)
        health_pattern = self._identify_shift_pattern(health_shifts)
        
        # Calculate volatility
        coherence_volatility = sum(abs(s) for s in coherence_shifts) / len(coherence_shifts)
        health_volatility = sum(abs(s) for s in health_shifts) / len(health_shifts)
        
        # Detect milestone clusters (significant shifts happening close together)
        timestamps = [m["timestamp"] for m in milestones]
        clusters = self._detect_timestamp_clusters(timestamps)
        
        return {
            "analysis_status": "completed",
            "milestone_count": len(milestones),
            "coherence_pattern": coherence_pattern,
            "health_pattern": health_pattern,
            "volatility": {
                "coherence": coherence_volatility,
                "health": health_volatility
            },
            "milestone_clusters": clusters,
            "stability_trajectory": self._determine_stability_trajectory(coherence_pattern, health_pattern),
            "recommendation": self._generate_milestone_recommendation(
                coherence_pattern, health_pattern, coherence_volatility, health_volatility
            )
        }
    
    def _identify_shift_pattern(self, shifts):
        """Identify patterns in shift values"""
        if not shifts:
            return "no_data"
            
        # Check direction consistency
        positive_shifts = sum(1 for s in shifts if s > 0.1)
        negative_shifts = sum(1 for s in shifts if s < -0.1)
        neutral_shifts = len(shifts) - positive_shifts - negative_shifts
        
        if positive_shifts > len(shifts) * 0.6:
            return "consistently_improving"
        elif negative_shifts > len(shifts) * 0.6:
            return "consistently_declining"
        elif neutral_shifts > len(shifts) * 0.6:
            return "stable"
            
        # Check for oscillation
        direction_changes = sum(1 for i in range(1, len(shifts)) 
                             if (shifts[i] > 0.1 and shifts[i-1] < -0.1) or 
                                (shifts[i] < -0.1 and shifts[i-1] > 0.1))
        
        if direction_changes > len(shifts) * 0.4:
            return "oscillating"
            
        return "mixed"
    
    def _detect_timestamp_clusters(self, timestamps):
        """Detect clusters of timestamps that occur close together"""
        if len(timestamps) < 3:
            return 0
            
        from datetime import datetime
        
        # Convert ISO strings to datetime objects
        times = [datetime.fromisoformat(ts) for ts in timestamps]
        times.sort()
        
        # Find gaps between consecutive timestamps
        gaps = [(times[i] - times[i-1]).total_seconds() for i in range(1, len(times))]
        avg_gap = sum(gaps) / len(gaps)
        
        # Count clusters (sequences with smaller than average gaps)
        clusters = 1
        for gap in gaps:
            if gap > avg_gap * 1.5:  # New cluster starts after a large gap
                clusters += 1
                
        return clusters
    
    def _determine_stability_trajectory(self, coherence_pattern, health_pattern):
        """Determine overall stability trajectory based on patterns"""
        positive_patterns = ["consistently_improving", "stable"]
        negative_patterns = ["consistently_declining", "oscillating"]
        
        if coherence_pattern in positive_patterns and health_pattern in positive_patterns:
            return "strong_positive"
        elif coherence_pattern in negative_patterns and health_pattern in negative_patterns:
            return "strong_negative"
        elif coherence_pattern in negative_patterns or health_pattern in negative_patterns:
            return "concerning"
        else:
            return "neutral"
    
    def _generate_milestone_recommendation(self, coherence_pattern, health_pattern, coherence_volatility, health_volatility):
        """Generate recommendations based on milestone analysis"""
        if coherence_pattern == "consistently_declining" or health_pattern == "consistently_declining":
            return "immediate_intervention"
        elif coherence_pattern == "oscillating" or health_pattern == "oscillating":
            return "stabilize_recursion"
        elif coherence_volatility > 0.3 or health_volatility > 0.3:
            return "monitor_closely"
        else:
            return "maintain_current_approach"
            
    def track_recursive_coherence_trends(self, anchor_name, window_size=10, min_points=3):
        """Track recursive coherence trends with enhanced analytical capabilities"""
        stability_events = self.get_stability_metrics_timeline(anchor_name)
        
        if len(stability_events) < min_points:
            return {
                "tracking_status": "insufficient_data",
                "required_points": min_points,
                "available_points": len(stability_events)
            }
        
        # Extract coherence and recursion health metrics from events
        coherence_values = []
        health_values = []
        drift_indicators = []
        timestamps = []
        
        for event in stability_events[-window_size:]:
            metrics = event["data"].get("stability_metrics", {})
            coherence_values.append(metrics.get("knowledge_coherence", 1.0))
            health_values.append(metrics.get("recursion_health", 1.0))
            drift_indicators.append(len(metrics.get("drift_indicators", [])))
            timestamps.append(event["timestamp"])
        
        # Calculate trend metrics
        coherence_trend = self._calculate_trend_metrics(coherence_values)
        health_trend = self._calculate_trend_metrics(health_values)
        drift_trend = self._calculate_trend_metrics(drift_indicators)
        
        # Calculate correlation between metrics
        correlations = {
            "coherence_health": self._calculate_correlation(coherence_values, health_values),
            "coherence_drift": self._calculate_correlation(coherence_values, drift_indicators, inverse=True),
            "health_drift": self._calculate_correlation(health_values, drift_indicators, inverse=True)
        }
        
        return {
            "tracking_status": "completed",
            "coherence_trend": coherence_trend,
            "health_trend": health_trend,
            "drift_indicators_trend": drift_trend,
            "metric_correlations": correlations,
            "coherence_health_alignment": "aligned" if correlations["coherence_health"] > 0.7 else 
                                        "misaligned" if correlations["coherence_health"] < 0 else "neutral",
            "systemic_assessment": self._assess_system_health(coherence_trend, health_trend, drift_trend)
        }
    
    def _calculate_trend_metrics(self, values):
        """Calculate trend metrics for a series of values"""
        if not values or len(values) < 2:
            return {"direction": "unknown", "slope": 0, "volatility": 0}
            
        # Calculate overall direction
        slope = (values[-1] - values[0]) / (len(values) - 1)
        
        # Calculate volatility
        volatility = sum(abs(values[i] - values[i-1]) for i in range(1, len(values))) / (len(values) - 1)
        
        # Determine acceleration (second derivative)
        if len(values) >= 3:
            first_half_slope = (values[len(values)//2] - values[0]) / (len(values)//2)
            second_half_slope = (values[-1] - values[len(values)//2]) / (len(values) - len(values)//2)
            acceleration = second_half_slope - first_half_slope
        else:
            acceleration = 0
            
        return {
            "direction": "improving" if slope > 0.01 else "declining" if slope < -0.01 else "stable",
            "slope": slope,
            "volatility": volatility,
            "acceleration": acceleration,
            "trend_quality": "accelerating" if acceleration > 0.01 else 
                           "decelerating" if acceleration < -0.01 else "linear"
        }
    
    def _calculate_correlation(self, series1, series2, inverse=False):
        """Calculate correlation coefficient between two series"""
        if len(series1) != len(series2) or len(series1) < 2:
            return 0
            
        n = len(series1)
        sum_x = sum(series1)
        sum_y = sum(series2)
        sum_xy = sum(x*y for x, y in zip(series1, series2))
        sum_x2 = sum(x*x for x in series1)
        sum_y2 = sum(y*y for y in series2)
        
        # Calculate Pearson correlation
        denominator = ((n*sum_x2 - sum_x**2) * (n*sum_y2 - sum_y**2))**0.5
        if denominator == 0:
            return 0
            
        correlation = (n*sum_xy - sum_x*sum_y) / denominator
        
        # Invert correlation if requested (for metrics that should be inversely related)
        return -correlation if inverse else correlation
    
    def _assess_system_health(self, coherence_trend, health_trend, drift_trend):
        """Assess overall system health based on multiple trends"""
        # Identify concerning patterns
        concerns = []
        
        if coherence_trend["direction"] == "declining":
            concerns.append("declining_coherence")
        if health_trend["direction"] == "declining":
            concerns.append("declining_health")
        if drift_trend["direction"] == "improving" and drift_trend["slope"] > 0.1:
            concerns.append("increasing_drift_indicators")
            
        # Check for volatility issues
        if coherence_trend["volatility"] > 0.2:
            concerns.append("coherence_volatility")
        if health_trend["volatility"] > 0.2:
            concerns.append("health_volatility")
            
        # Check for acceleration issues
        if coherence_trend["acceleration"] < -0.05:
            concerns.append("accelerating_coherence_decline")
        if health_trend["acceleration"] < -0.05:
            concerns.append("accelerating_health_decline")
        if drift_trend["acceleration"] > 0.05:
            concerns.append("accelerating_drift")
            
        # Determine overall health assessment
        if not concerns:
            health_status = "excellent"
        elif len(concerns) <= 1 and not any(c.startswith("accelerating") for c in concerns):
            health_status = "good"
        elif len(concerns) <= 3:
            health_status = "concerning"
        else:
            health_status = "critical"
            
        return {
            "status": health_status,
            "concerns": concerns,
            "intervention_required": health_status in ["concerning", "critical"]
        }