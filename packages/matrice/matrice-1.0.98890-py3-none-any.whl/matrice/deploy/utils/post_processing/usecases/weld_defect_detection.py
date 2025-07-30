"""
Weld Defect Detection use case implementation.

This module provides a structured implementation of weld defect detection
with counting, insights generation, alerting, and tracking.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time

from ..core.base import (
    BaseProcessor,
    ProcessingContext,
    ProcessingResult,
    ConfigProtocol,
)
from ..core.config import BaseConfig, AlertConfig
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)

@dataclass
class WeldDefectConfig(BaseConfig):
    confidence_threshold: float = 0.5

    violation_categories: List[str] = field(
        default_factory=lambda: ["Bad Welding", "Crack", "Porosity", "Spatters"]
    )

    alert_config: Optional[AlertConfig] = None

    time_window_minutes: int = 60
    enable_unique_counting: bool = True

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            1: "Bad Welding",
            2: "Crack",
            3: "Good Welding",
            4: "Porosity",
            5: "Reinforcement",
            6: "Spatters"
        }
    )

    enable_smoothing: bool = False
    smoothing_algorithm: str = "linear"
    smoothing_window_size: int = 5
    smoothing_cooldown_frames: int = 10
    smoothing_confidence_range_factor: float = 0.2

    def __post_init__(self):
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        self.violation_categories = [cat.lower() for cat in self.violation_categories]
        if self.index_to_category:
            self.index_to_category = {k: v.lower() for k, v in self.index_to_category.items()}

class WeldDefectUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("weld_defect_detection")
        self.category = "weld"
        self.smoothing_tracker = None
        self._weld_defect_recent_history = []

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5,
                    "description": "Minimum confidence threshold for detections",
                },
                "violation_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["Bad Welding", "Crack", "Porosity", "Spatters"],
                    "description": "Category names that represent weld defects",
                },
                "index_to_category": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Mapping from category indices to names",
                },
                "alert_config": {
                    "type": "object",
                    "properties": {
                        "count_thresholds": {
                            "type": "object",
                            "additionalProperties": {"type": "integer", "minimum": 1},
                            "description": "Count thresholds for alerts",
                        }
                    },
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides) -> WeldDefectConfig:
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.5,
            "violation_categories": ["Bad Welding", "Crack", "Porosity", "Spatters"],
        }
        defaults.update(overrides)
        return WeldDefectConfig(**defaults)

    def process(
            self,
            data: Any,
            config: ConfigProtocol,
            context: Optional[ProcessingContext] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        start_time = time.time()

        try:
            if not isinstance(config, WeldDefectConfig):
                return self.create_error_result(
                    "Invalid configuration type for weld defect detection",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if context is None:
                context = ProcessingContext()
            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            self.logger.info(f"Processing weld defect detection with format: {input_format.value}")

            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")

            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")

            if config.enable_smoothing:
                if self.smoothing_tracker is None:
                    smoothing_config = BBoxSmoothingConfig(
                        smoothing_algorithm=config.smoothing_algorithm,
                        window_size=config.smoothing_window_size,
                        cooldown_frames=config.smoothing_cooldown_frames,
                        confidence_threshold=config.confidence_threshold,
                        confidence_range_factor=config.smoothing_confidence_range_factor,
                        enable_smoothing=True
                    )
                    self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)

                smooth_categories = {cat.lower() for cat in config.violation_categories}
                weld_defect_detections = [d for d in processed_data if d.get("category", "").lower() in smooth_categories]

                smoothed_detections = bbox_smoothing(
                    weld_defect_detections,
                    self.smoothing_tracker.config,
                    self.smoothing_tracker
                )
                non_smoothed_detections = [d for d in processed_data if d.get("category", "").lower() not in smooth_categories]

                processed_data = non_smoothed_detections + smoothed_detections
                self.logger.debug("Applied bbox smoothing for weld defect categories")

            weld_defect_summary = self._calculate_weld_defect_summary(processed_data, config)
            general_summary = calculate_counting_summary(processed_data)

            insights = self._generate_insights(weld_defect_summary, config)
            alerts = self._check_alerts(weld_defect_summary, config)

            metrics = self._calculate_metrics(weld_defect_summary, config, context)

            predictions = self._extract_predictions(processed_data, config)

            summary_text = self._generate_summary(weld_defect_summary, general_summary, alerts)

            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame
                elif start_frame is not None:
                    frame_number = start_frame

            events_dict = self._generate_events(weld_defect_summary, alerts, config, frame_number=frame_number)
            tracking_stats_dict = self._generate_tracking_stats(
                weld_defect_summary, insights, summary_text, config,
                frame_number=frame_number,
                stream_info=stream_info
            )

            context.processing_time = time.time() - start_time
            context.mark_completed()

            result = self.create_result(
                data={
                    "weld_defect_summary": weld_defect_summary,
                    "general_counting_summary": general_summary,
                    "alerts": alerts,
                    "total_weld_defect_detections": weld_defect_summary.get("total_objects", 0),
                    "total_bad_welding_detections": weld_defect_summary.get("by_category", {}).get("bad welding", 0),
                    "total_crack_detections": weld_defect_summary.get("by_category", {}).get("crack", 0),
                    "total_porosity_detections": weld_defect_summary.get("by_category", {}).get("porosity", 0),
                    "total_spatters_detections": weld_defect_summary.get("by_category", {}).get("spatters", 0),
                    "events": events_dict,
                    "tracking_stats": tracking_stats_dict,
                },
                usecase=self.name,
                category=self.category,
                context=context,
            )

            result.summary = summary_text
            result.insights = insights
            result.metrics = metrics
            result.predictions = predictions
            return result

        except Exception as e:
            self.logger.error(f"Error in weld defect processing: {str(e)}")
            return self.create_error_result(
                f"Weld defect processing failed: {str(e)}",
                error_type="WeldDefectProcessingError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    def _calculate_weld_defect_summary(
            self, data: Any, config: WeldDefectConfig
    ) -> Dict[str, Any]:
        if isinstance(data, list):
            valid_categories = [cat.lower() for cat in config.violation_categories]

            detections = [
                det for det in data
                if det.get("category", "").lower() in valid_categories
            ]

            summary = {
                "total_objects": len(detections),
                "by_category": {},
                "detections": detections,
            }

            for category in config.violation_categories:
                count = len([
                    det for det in detections
                    if det.get("category", "").lower() == category.lower()
                ])
                summary["by_category"][category.lower()] = count

            return summary

        return {"total_objects": 0, "by_category": {}, "detections": []}

    def _generate_insights(
            self, summary: Dict, config: WeldDefectConfig
    ) -> List[str]:
        insights = []

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_bad_welding = by_category.get("bad welding", 0)
        total_crack = by_category.get("crack", 0)
        total_porosity = by_category.get("porosity", 0)
        total_spatters = by_category.get("spatters", 0)

        if total == 0:
            insights.append("EVENT: No weld defects detected in the scene")
        else:
            if total_bad_welding > 0:
                insights.append(f"EVENT: {total_bad_welding} bad welding defect{'s' if total_bad_welding != 1 else ''} detected")
            if total_crack > 0:
                insights.append(f"EVENT: {total_crack} crack defect{'s' if total_crack != 1 else ''} detected")
            if total_porosity > 0:
                insights.append(f"EVENT: {total_porosity} porosity defect{'s' if total_porosity != 1 else ''} detected")
            if total_spatters > 0:
                insights.append(f"EVENT: {total_spatters} spatter{'s' if total_spatters != 1 else ''} detected")

            total_defects = total_bad_welding + total_crack + total_porosity + total_spatters
            if total_defects > 0:
                bad_welding_percent = (total_bad_welding / total_defects) * 100 if total_defects else 0
                crack_percent = (total_crack / total_defects) * 100 if total_defects else 0
                porosity_percent = (total_porosity / total_defects) * 100 if total_defects else 0
                spatters_percent = (total_spatters / total_defects) * 100 if total_defects else 0
                insights.append(f"ANALYSIS: {bad_welding_percent:.1f}% bad welding, {crack_percent:.1f}% crack, {porosity_percent:.1f}% porosity, {spatters_percent:.1f}% spatters in detected defects")

            total_area = 0.0
            for det in detections:
                bbox = det.get("bounding_box") or det.get("bbox")
                if bbox:
                    xmin = bbox.get("xmin")
                    ymin = bbox.get("ymin")
                    xmax = bbox.get("xmax")
                    ymax = bbox.get("ymax")
                    if None not in (xmin, ymin, xmax, ymax):
                        width = xmax - xmin
                        height = ymax - ymin
                        if width > 0 and height > 0:
                            total_area += width * height

            threshold_area = 10000.0
            intensity_pct = min(100.0, (total_area / threshold_area) * 100)

            if intensity_pct < 20:
                insights.append(f"INTENSITY: Low weld defect activity ({intensity_pct:.1f}% area coverage)")
            elif intensity_pct <= 50:
                insights.append(f"INTENSITY: Moderate weld defect activity ({intensity_pct:.1f}%)")
            elif intensity_pct <= 80:
                insights.append(f"INTENSITY: High weld defect activity ({intensity_pct:.1f}%)")
            else:
                insights.append(f"INTENSITY: Very high weld defect activity — critical hazard ({intensity_pct:.1f}%)")

        return insights

    def _check_alerts(
            self, summary: Dict, config: WeldDefectConfig
    ) -> List[Dict]:
        alerts = []
        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        if total == 0:
            return []

        total_area = 0.0
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            if bbox:
                xmin = bbox.get("xmin")
                ymin = bbox.get("ymin")
                xmax = bbox.get("xmax")
                ymax = bbox.get("ymax")
                if None not in (xmin, ymin, xmax, ymax):
                    width = xmax - xmin
                    height = ymax - ymin
                    if width > 0 and height > 0:
                        total_area += width * height

        threshold_area = 10000.0
        intensity_pct = min(100.0, (total_area / threshold_area) * 100)

        if intensity_pct > 80:
            severity = "critical"
        elif intensity_pct > 50:
            severity = "warning"
        else:
            severity = "info"

        alert = {
            "type": "weld_defect_alert",
            "message": f"{total} weld defect{'s' if total != 1 else ''} with intensity {intensity_pct:.1f}%",
            "severity": severity,
            "detected_bad_welding": by_category.get("bad welding", 0),
            "detected_crack": by_category.get("crack", 0),
            "detected_porosity": by_category.get("porosity", 0),
            "detected_spatters": by_category.get("spatters", 0),
        }

        alerts.append(alert)
        return alerts

    def _calculate_metrics(
            self,
            summary: Dict,
            config: WeldDefectConfig,
            context: ProcessingContext,
    ) -> Dict[str, Any]:
        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_bad_welding = by_category.get("bad welding", 0)
        total_crack = by_category.get("crack", 0)
        total_porosity = by_category.get("porosity", 0)
        total_spatters = by_category.get("spatters", 0)

        metrics = {
            "total_detections": total,
            "total_bad_welding": total_bad_welding,
            "total_crack": total_crack,
            "total_porosity": total_porosity,
            "total_spatters": total_spatters,
            "processing_time": context.processing_time or 0.0,
            "confidence_threshold": config.confidence_threshold,
            "intensity_percentage": 0.0,
            "hazard_level": "unknown",
        }

        total_area = 0.0
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            if bbox:
                xmin = bbox.get("xmin")
                ymin = bbox.get("ymin")
                xmax = bbox.get("xmax")
                ymax = bbox.get("ymax")
                if None not in (xmin, ymin, xmax, ymax):
                    width = xmax - xmin
                    height = ymax - ymin
                    if width > 0 and height > 0:
                        total_area += width * height

        threshold_area = 10000.0
        intensity_pct = min(100.0, (total_area / threshold_area) * 100)
        metrics["intensity_percentage"] = intensity_pct

        if intensity_pct < 20:
            metrics["hazard_level"] = "low"
        elif intensity_pct < 50:
            metrics["hazard_level"] = "moderate"
        elif intensity_pct < 80:
            metrics["hazard_level"] = "high"
        else:
            metrics["hazard_level"] = "critical"

        return metrics

    def _extract_predictions(
            self, data: Any, config: WeldDefectConfig
    ) -> List[Dict[str, Any]]:
        predictions = []

        try:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        prediction = {
                            "category": item.get("category", item.get("class", "unknown")),
                            "confidence": item.get("confidence", item.get("score", 0.0)),
                            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                        }
                        predictions.append(prediction)

        except Exception as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")

        return predictions

    def _generate_summary(
            self, summary: Dict, general_summary: Dict, alerts: List
    ) -> str:
        total = summary.get("total_objects", 0)
        total_bad_welding = summary.get("by_category", {}).get("bad welding", 0)
        total_crack = summary.get("by_category", {}).get("crack", 0)
        total_porosity = summary.get("by_category", {}).get("porosity", 0)
        total_spatters = summary.get("by_category", {}).get("spatters", 0)

        if total == 0:
            return "No weld defects detected"

        summary_parts = []

        if total_bad_welding > 0:
            summary_parts.append(
                f"{total_bad_welding} bad welding defect{'s' if total_bad_welding != 1 else ''} detected"
            )
        if total_crack > 0:
            summary_parts.append(
                f"{total_crack} crack defect{'s' if total_crack != 1 else ''} detected"
            )
        if total_porosity > 0:
            summary_parts.append(
                f"{total_porosity} porosity defect{'s' if total_porosity != 1 else ''} detected"
            )
        if total_spatters > 0:
            summary_parts.append(
                f"{total_spatters} spatter{'s' if total_spatters != 1 else ''} detected"
            )

        if alerts:
            alert_count = len(alerts)
            summary_parts.append(
                f"{alert_count} alert{'s' if alert_count != 1 else ''}"
            )

        return ", ".join(summary_parts)

    def _generate_events(
            self,
            summary: Dict,
            alerts: List[Dict],
            config: WeldDefectConfig,
            frame_number: Optional[int] = None
    ) -> Dict:
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        events = {frame_key: []}
        frame_events = events[frame_key]

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_bad_welding = by_category.get("bad welding", 0)
        total_crack = by_category.get("crack", 0)
        total_porosity = by_category.get("porosity", 0)
        total_spatters = by_category.get("spatters", 0)

        if total > 0:
            total_area = 0.0
            for det in detections:
                bbox = det.get("bounding_box") or det.get("bbox")
                if bbox:
                    xmin = bbox.get("xmin")
                    ymin = bbox.get("ymin")
                    xmax = bbox.get("xmax")
                    ymax = bbox.get("ymax")
                    if None not in (xmin, ymin, xmax, ymax):
                        width = xmax - xmin
                        height = ymax - ymin
                        if width > 0 and height > 0:
                            total_area += width * height

            threshold_area = 10000.0
            intensity = min(10.0, (total_area / threshold_area) * 10)

            if intensity >= 7:
                level = "critical"
            elif intensity >= 5:
                level = "warning"
            else:
                level = "info"

            human_lines = []
            if total_bad_welding > 0:
                human_lines.append(f"    - {total_bad_welding} bad welding detected")
            if total_crack > 0:
                human_lines.append(f"    - {total_crack} crack detected")
            if total_porosity > 0:
                human_lines.append(f"    - {total_porosity} porosity detected")
            if total_spatters > 0:
                human_lines.append(f"    - {total_spatters} spatters detected")
            if total == 0:
                human_lines.append("    - no weld defects detected")

            weld_defect_event = {
                "type": "weld_defect_detection",
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": level,
                "intensity": round(intensity, 1),
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7},
                },
                "application_name": "Weld Defect Detection System",
                "application_version": "1.0",
                "location_info": None,
                "human_text": "\n".join(human_lines),
            }
            frame_events.append(weld_defect_event)

        for alert in alerts:
            alert_lines = []
            if total_bad_welding > 0:
                alert_lines.append(f"    - {total_bad_welding} bad welding[s] detected")
            if total_crack > 0:
                alert_lines.append(f"    - {total_crack} crack[s] detected")
            if total_porosity > 0:
                alert_lines.append(f"    - {total_porosity} porosity detected")
            if total_spatters > 0:
                alert_lines.append(f"    - {total_spatters} spatters[s] detected")
            if total == 0:
                alert_lines.append("    - no weld defects detected")

            alert_text = "\n".join(alert_lines)

            alert_event = {
                "type": alert.get("type", "weld_defect_alert"),
                "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
                "level": alert.get("severity", "warning"),
                "intensity": 8.0,
                "config": {
                    "min_value": 0,
                    "max_value": 10,
                    "level_settings": {"info": 2, "warning": 5, "critical": 7},
                },
                "application_name": "Weld Defect Alert System",
                "application_version": "1.0",
                "location_info": None,
                "human_text": alert_text,
            }
            frame_events.append(alert_event)

        return events

    def _generate_tracking_stats(
            self,
            summary: Dict,
            insights: List[str],
            summary_text: str,
            config: WeldDefectConfig,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> Dict:
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = {frame_key: []}
        frame_tracking_stats = tracking_stats[frame_key]

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_bad_welding = by_category.get("bad welding", 0)
        total_crack = by_category.get("crack", 0)
        total_porosity = by_category.get("porosity", 0)
        total_spatters = by_category.get("spatters", 0)

        if frame_number is not None:
            self._weld_defect_recent_history.append({
                "frame": frame_number,
                "bad_welding": total_bad_welding,
                "crack": total_crack,
                "porosity": total_porosity,
                "spatters": total_spatters,
            })
            if len(self._weld_defect_recent_history) > 150:
                self._weld_defect_recent_history.pop(0)

        total_area = 0.0
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            if bbox:
                xmin = bbox.get("xmin")
                ymin = bbox.get("ymin")
                xmax = bbox.get("xmax")
                ymax = bbox.get("ymax")
                if None not in (xmin, ymin, xmax, ymax):
                    width = xmax - xmin
                    height = ymax - ymin
                    if width > 0 and height > 0:
                        total_area += width * height

        threshold_area = 10000.0
        intensity_pct = min(100.0, (total_area / threshold_area) * 100)

        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)

        human_lines = [f"CURRENT FRAME @ {current_timestamp}:"]
        if total > 0:
            if total_bad_welding > 0:
                human_lines.append(f"\t- Bad Welding: {total_bad_welding}")
            if total_crack > 0:
                human_lines.append(f"\t- Crack: {total_crack}")
            if total_porosity > 0:
                human_lines.append(f"\t- Porosity: {total_porosity}")
            if total_spatters > 0:
                human_lines.append(f"\t- Spatters: {total_spatters}")
        if total == 0:
            human_lines.append(f"\t- No weld defects detected")

        human_lines.append("")
        human_lines.append(f"ALERTS SINCE @ {start_timestamp}:")

        recent_bad_welding_detected = any(entry.get("bad_welding", 0) > 0 for entry in self._weld_defect_recent_history)
        recent_crack_detected = any(entry.get("crack", 0) > 0 for entry in self._weld_defect_recent_history)
        recent_porosity_detected = any(entry.get("porosity", 0) > 0 for entry in self._weld_defect_recent_history)
        recent_spatters_detected = any(entry.get("spatters", 0) > 0 for entry in self._weld_defect_recent_history)

        total_counts = {
            "Bad Welding": sum(entry.get("bad_welding", 0) for entry in self._weld_defect_recent_history),
            "Crack": sum(entry.get("crack", 0) for entry in self._weld_defect_recent_history),
            "Porosity": sum(entry.get("porosity", 0) for entry in self._weld_defect_recent_history),
            "Spatters": sum(entry.get("spatters", 0) for entry in self._weld_defect_recent_history)
        }

        if any([recent_bad_welding_detected, recent_crack_detected, recent_porosity_detected, recent_spatters_detected]):
            if recent_bad_welding_detected:
                human_lines.append(f"\t- Bad Welding: {total_counts['Bad Welding']}")
            if recent_crack_detected:
                human_lines.append(f"\t- Crack: {total_counts['Crack']}")
            if recent_porosity_detected:
                human_lines.append(f"\t- Porosity: {total_counts['Porosity']}")
            if recent_spatters_detected:
                human_lines.append(f"\t- Spatters: {total_counts['Spatters']}")
        else:
            human_lines.append(f"\t- No weld defects detected in recent frames")

        human_text = "\n".join(human_lines)

        tracking_stat = {
            "all_results_for_tracking": {
                "total_detections": total,
                "total_bad_welding": total_bad_welding,
                "total_crack": total_crack,
                "total_porosity": total_porosity,
                "total_spatters": total_spatters,
                "intensity_percentage": intensity_pct,
                "weld_defect_summary": summary,
                "unique_count": self._count_unique_tracks(summary)
            },
            "human_text": human_text
        }

        frame_tracking_stats.append(tracking_stat)
        return tracking_stats

    def _count_unique_tracks(self, summary: Dict) -> Optional[int]:
        detections = summary.get("detections", [])
        if not detections:
            return None

        unique_tracks = set()
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is not None:
                unique_tracks.add(track_id)

        return len(unique_tracks) if unique_tracks else None

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        if not stream_info:
            return "00:00:00.00"
        if stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
            return stream_info.get("video_timestamp", "")[:8]
        else:
            stream_time_str = stream_info.get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except:
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        if not stream_info:
            return "00:00:00"
        is_video_chunk = stream_info.get("input_settings", {}).get("is_video_chunk", False)
        if is_video_chunk or stream_info.get("input_settings", {}).get("stream_type", "video_file") == "video_file":
            return "00:00:00"
        else:
            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()
            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = timestamp % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.2f}"

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')