"""
DataFlow Smart Operations

Smart nodes that provide intelligent database operations with auto-detection.
"""

import logging
from typing import Any, Dict, List, Optional

from kailash.nodes.base import Node, NodeParameter, NodeRegistry

from .workflow_connection_manager import SmartNodeConnectionMixin

logger = logging.getLogger(__name__)


class SmartMergeNode(SmartNodeConnectionMixin, Node):
    """Smart merge node with auto-relationship detection.

    This node can automatically detect foreign key relationships and perform
    intelligent merges without requiring explicit join conditions.

    Features:
    - Auto-detection of foreign key relationships
    - Support for "auto" merge type
    - "enrich" mode to add related data
    - Natural language merge specifications
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._relationships_cache = {}

    def get_parameters(self) -> Dict[str, NodeParameter]:
        """Define parameters for SmartMergeNode."""
        return {
            "left_data": NodeParameter(
                name="left_data",
                type=list,
                required=True,
                description="Left dataset for merge operation",
            ),
            "right_data": NodeParameter(
                name="right_data",
                type=list,
                required=True,
                description="Right dataset for merge operation",
            ),
            "merge_type": NodeParameter(
                name="merge_type",
                type=str,
                required=False,
                default="auto",
                description="Type of merge: 'auto', 'inner', 'left', 'right', 'outer', 'enrich'",
            ),
            "left_model": NodeParameter(
                name="left_model",
                type=str,
                required=False,
                description="Name of left model for auto-detection",
            ),
            "right_model": NodeParameter(
                name="right_model",
                type=str,
                required=False,
                description="Name of right model for auto-detection",
            ),
            "join_conditions": NodeParameter(
                name="join_conditions",
                type=dict,
                required=False,
                default={},
                description="Manual join conditions (overrides auto-detection)",
            ),
            "enrich_fields": NodeParameter(
                name="enrich_fields",
                type=list,
                required=False,
                default=[],
                description="Specific fields to enrich when using enrich mode",
            ),
            "natural_language_spec": NodeParameter(
                name="natural_language_spec",
                type=str,
                required=False,
                description="Natural language merge specification (e.g., 'merge users with their orders')",
            ),
            "connection_pool_id": NodeParameter(
                name="connection_pool_id",
                type=str,
                required=False,
                description="ID of DataFlowConnectionManager node for database operations",
            ),
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute smart merge operation with connection pool integration."""
        return self._execute_with_connection(self._perform_merge, **kwargs)

    def _perform_merge(self, **kwargs) -> Dict[str, Any]:
        """Perform the actual smart merge operation."""
        left_data = kwargs.get("left_data", [])
        right_data = kwargs.get("right_data", [])
        merge_type = kwargs.get("merge_type", "auto")
        left_model = kwargs.get("left_model")
        right_model = kwargs.get("right_model")
        join_conditions = kwargs.get("join_conditions", {})
        enrich_fields = kwargs.get("enrich_fields", [])
        natural_language_spec = kwargs.get("natural_language_spec")

        logger.info(f"Executing SmartMergeNode with merge_type: {merge_type}")

        # Normalize data to lists
        if isinstance(left_data, dict):
            left_data = [left_data]
        if isinstance(right_data, dict):
            right_data = [right_data]

        # Auto-detect relationships if merge_type is "auto"
        if merge_type == "auto":
            detected_conditions = self._auto_detect_join_conditions(
                left_data, right_data, left_model, right_model
            )
            if detected_conditions:
                join_conditions = detected_conditions
                logger.info(f"Auto-detected join conditions: {join_conditions}")
            else:
                logger.warning(
                    "Could not auto-detect join conditions, falling back to inner join on 'id'"
                )
                join_conditions = {"left_key": "id", "right_key": "id"}

        # Process natural language specification if provided
        if natural_language_spec:
            nl_conditions = self._parse_natural_language_spec(natural_language_spec)
            if nl_conditions:
                join_conditions.update(nl_conditions)
                logger.info(f"Applied natural language conditions: {nl_conditions}")

        # Perform the merge based on type
        if merge_type in ["auto", "inner"]:
            result = self._inner_join(left_data, right_data, join_conditions)
        elif merge_type == "left":
            result = self._left_join(left_data, right_data, join_conditions)
        elif merge_type == "right":
            result = self._right_join(left_data, right_data, join_conditions)
        elif merge_type == "outer":
            result = self._outer_join(left_data, right_data, join_conditions)
        elif merge_type == "enrich":
            result = self._enrich_merge(
                left_data, right_data, join_conditions, enrich_fields
            )
        else:
            raise ValueError(f"Unsupported merge_type: {merge_type}")

        return {
            "merged_data": result,
            "merge_type": merge_type,
            "join_conditions": join_conditions,
            "left_count": len(left_data),
            "right_count": len(right_data),
            "result_count": len(result),
            "auto_detected": merge_type == "auto" and not kwargs.get("join_conditions"),
        }

    def _auto_detect_join_conditions(
        self,
        left_data: List[Dict],
        right_data: List[Dict],
        left_model: Optional[str] = None,
        right_model: Optional[str] = None,
    ) -> Dict[str, str]:
        """Auto-detect join conditions based on data structure and model relationships."""

        if not left_data or not right_data:
            return {}

        # Get sample records
        left_sample = left_data[0]
        right_sample = right_data[0]

        # Strategy 1: Use model relationship information if available
        if left_model and right_model:
            model_conditions = self._detect_from_models(left_model, right_model)
            if model_conditions:
                return model_conditions

        # Strategy 2: Common foreign key patterns
        left_keys = set(left_sample.keys())
        right_keys = set(right_sample.keys())

        # Look for foreign key patterns
        # Check for foreign key in right table pointing to left table's id
        if (
            left_model
            and f"{left_model.lower()}_id" in right_keys
            and "id" in left_keys
        ):
            return {"left_key": "id", "right_key": f"{left_model.lower()}_id"}

        # Check for foreign key in left table pointing to right table's id
        if (
            right_model
            and f"{right_model.lower()}_id" in left_keys
            and "id" in right_keys
        ):
            return {"left_key": f"{right_model.lower()}_id", "right_key": "id"}

        # Common foreign key patterns (left_key, right_key)
        foreign_key_patterns = [
            ("id", "user_id"),  # users.id -> orders.user_id
            ("id", "customer_id"),  # customers.id -> orders.customer_id
            ("id", "product_id"),  # products.id -> order_items.product_id
            ("id", "order_id"),  # orders.id -> order_items.order_id
        ]

        for left_key, right_key in foreign_key_patterns:
            if left_key in left_keys and right_key in right_keys:
                return {"left_key": left_key, "right_key": right_key}

        # Strategy 3: Look for common field names
        common_fields = left_keys.intersection(right_keys)
        priority_fields = ["id", "user_id", "customer_id", "product_id", "order_id"]

        for field in priority_fields:
            if field in common_fields:
                return {"left_key": field, "right_key": field}

        # Strategy 4: First common field
        if common_fields:
            common_field = next(iter(common_fields))
            return {"left_key": common_field, "right_key": common_field}

        return {}

    def _detect_from_models(self, left_model: str, right_model: str) -> Dict[str, str]:
        """Detect join conditions from model relationship metadata."""
        # This would integrate with the DataFlow relationship detection
        # For now, return common patterns based on model names

        # Common relationship patterns
        relationships = {
            ("User", "Order"): {"left_key": "id", "right_key": "user_id"},
            ("Order", "User"): {"left_key": "user_id", "right_key": "id"},
            ("User", "Profile"): {"left_key": "id", "right_key": "user_id"},
            ("Profile", "User"): {"left_key": "user_id", "right_key": "id"},
            ("Order", "OrderItem"): {"left_key": "id", "right_key": "order_id"},
            ("OrderItem", "Order"): {"left_key": "order_id", "right_key": "id"},
            ("Product", "OrderItem"): {"left_key": "id", "right_key": "product_id"},
            ("OrderItem", "Product"): {"left_key": "product_id", "right_key": "id"},
        }

        return relationships.get((left_model, right_model), {})

    def _parse_natural_language_spec(self, spec: str) -> Dict[str, str]:
        """Parse natural language merge specifications."""
        spec_lower = spec.lower()

        # Simple pattern matching for common phrases
        patterns = {
            "users with their orders": {"left_key": "id", "right_key": "user_id"},
            "orders with users": {"left_key": "user_id", "right_key": "id"},
            "customers with orders": {"left_key": "id", "right_key": "customer_id"},
            "orders with customers": {"left_key": "customer_id", "right_key": "id"},
            "products with order items": {"left_key": "id", "right_key": "product_id"},
            "order items with products": {"left_key": "product_id", "right_key": "id"},
        }

        for pattern, conditions in patterns.items():
            if pattern in spec_lower:
                return conditions

        return {}

    def _inner_join(
        self,
        left_data: List[Dict],
        right_data: List[Dict],
        join_conditions: Dict[str, str],
    ) -> List[Dict]:
        """Perform inner join merge."""
        left_key = join_conditions.get("left_key")
        right_key = join_conditions.get("right_key")

        if not left_key or not right_key:
            return []

        # Create index for right data
        right_index = {}
        for right_record in right_data:
            key_value = right_record.get(right_key)
            if key_value is not None:
                if key_value not in right_index:
                    right_index[key_value] = []
                right_index[key_value].append(right_record)

        # Perform join
        result = []
        for left_record in left_data:
            left_value = left_record.get(left_key)
            if left_value is not None and left_value in right_index:
                for right_record in right_index[left_value]:
                    merged_record = self._merge_records(
                        left_record, right_record, left_key, right_key
                    )
                    result.append(merged_record)

        return result

    def _merge_records(
        self, left_record: Dict, right_record: Dict, left_key: str, right_key: str
    ) -> Dict:
        """Merge two records handling field name conflicts."""
        merged_record = left_record.copy()

        for key, value in right_record.items():
            if key in merged_record:
                if key == left_key and key == right_key:
                    # Same join key, no conflict - keep the same value
                    pass  # Already in merged_record
                elif key == right_key:
                    # This is the right join key, add it
                    merged_record[key] = value
                else:
                    # Field name conflict (not a join key), prefix right table field
                    merged_record[f"right_{key}"] = value
            else:
                # No conflict, add directly
                merged_record[key] = value

        return merged_record

    def _merge_records_right_primary(
        self, right_record: Dict, left_record: Dict, right_key: str, left_key: str
    ) -> Dict:
        """Merge two records with right table as primary (for right joins)."""
        merged_record = right_record.copy()

        for key, value in left_record.items():
            if key in merged_record:
                if key == left_key and key == right_key:
                    # Same join key, no conflict - keep the right value
                    pass  # Already in merged_record
                elif key == left_key and key != right_key:
                    # This is the left join key but conflicts with a right field
                    # In right join, prefix the left join key to avoid overwriting right field
                    merged_record[f"left_{key}"] = value
                else:
                    # Field name conflict (not a join key), prefix left table field
                    # In right join, right table fields have priority
                    merged_record[f"left_{key}"] = value
            else:
                # No conflict, add directly
                merged_record[key] = value

        return merged_record

    def _left_join(
        self,
        left_data: List[Dict],
        right_data: List[Dict],
        join_conditions: Dict[str, str],
    ) -> List[Dict]:
        """Perform left join merge."""
        left_key = join_conditions.get("left_key")
        right_key = join_conditions.get("right_key")

        if not left_key or not right_key:
            return left_data.copy()

        # Create index for right data
        right_index = {}
        for right_record in right_data:
            key_value = right_record.get(right_key)
            if key_value is not None:
                if key_value not in right_index:
                    right_index[key_value] = []
                right_index[key_value].append(right_record)

        # Perform left join
        result = []
        for left_record in left_data:
            left_value = left_record.get(left_key)
            if left_value is not None and left_value in right_index:
                for right_record in right_index[left_value]:
                    merged_record = self._merge_records(
                        left_record, right_record, left_key, right_key
                    )
                    result.append(merged_record)
            else:
                # Include left record even without match
                result.append(left_record.copy())

        return result

    def _right_join(
        self,
        left_data: List[Dict],
        right_data: List[Dict],
        join_conditions: Dict[str, str],
    ) -> List[Dict]:
        """Perform right join merge."""
        left_key = join_conditions.get("left_key")
        right_key = join_conditions.get("right_key")

        if not left_key or not right_key:
            return right_data.copy()

        # Create index for left data
        left_index = {}
        for left_record in left_data:
            key_value = left_record.get(left_key)
            if key_value is not None:
                if key_value not in left_index:
                    left_index[key_value] = []
                left_index[key_value].append(left_record)

        # Perform right join (preserve all right records)
        result = []
        for right_record in right_data:
            right_value = right_record.get(right_key)
            if right_value is not None and right_value in left_index:
                for left_record in left_index[right_value]:
                    # For right join, right table is "primary", so swap merge order
                    merged_record = self._merge_records_right_primary(
                        right_record, left_record, right_key, left_key
                    )
                    result.append(merged_record)
            else:
                # Include right record even without match
                result.append(right_record.copy())

        return result

    def _outer_join(
        self,
        left_data: List[Dict],
        right_data: List[Dict],
        join_conditions: Dict[str, str],
    ) -> List[Dict]:
        """Perform outer join merge."""
        left_key = join_conditions.get("left_key")
        right_key = join_conditions.get("right_key")

        if not left_key or not right_key:
            return left_data + right_data

        # Get left join results
        left_results = self._left_join(left_data, right_data, join_conditions)

        # Find unmatched right records
        left_values = {
            record.get(left_key)
            for record in left_data
            if record.get(left_key) is not None
        }
        unmatched_right = []
        for right_record in right_data:
            right_value = right_record.get(right_key)
            if right_value is not None and right_value not in left_values:
                unmatched_right.append(right_record.copy())

        return left_results + unmatched_right

    def _enrich_merge(
        self,
        left_data: List[Dict],
        right_data: List[Dict],
        join_conditions: Dict[str, str],
        enrich_fields: List[str],
    ) -> List[Dict]:
        """Perform enrich merge - add specific fields from right to left."""
        left_key = join_conditions.get("left_key")
        right_key = join_conditions.get("right_key")

        if not left_key or not right_key:
            return left_data.copy()

        # Create index for right data
        right_index = {}
        for right_record in right_data:
            key_value = right_record.get(right_key)
            if key_value is not None:
                right_index[key_value] = right_record

        # Perform enrichment
        result = []
        for left_record in left_data:
            enriched_record = left_record.copy()
            left_value = left_record.get(left_key)

            if left_value is not None and left_value in right_index:
                right_record = right_index[left_value]

                # Add all fields if no specific fields specified
                if not enrich_fields:
                    for key, value in right_record.items():
                        if key != right_key:  # Don't duplicate the join key
                            enriched_record[f"right_{key}"] = value
                else:
                    # Add only specified fields
                    for field in enrich_fields:
                        if field in right_record:
                            enriched_record[field] = right_record[field]

            result.append(enriched_record)

        return result


class AggregateNode(SmartNodeConnectionMixin, Node):
    """Enhanced aggregate node with natural language aggregation support.

    This node supports both traditional aggregation expressions and natural
    language specifications like "sum of amount by region" or "average price
    per category". It can automatically optimize aggregations to SQL when
    used in conjunction with the DataFlow optimization framework.

    Features:
    - Natural language aggregation expressions
    - Multiple aggregation functions in one operation
    - Group by with multiple fields
    - Having clauses for filtered aggregations
    - Automatic SQL optimization integration
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._aggregation_cache = {}

    def get_parameters(self) -> Dict[str, NodeParameter]:
        """Define parameters for AggregateNode."""
        return {
            "data": NodeParameter(
                name="data",
                type=list,
                required=True,
                description="Input data for aggregation operation",
            ),
            "aggregate_expression": NodeParameter(
                name="aggregate_expression",
                type=str,
                required=True,
                description="Aggregation expression (e.g., 'sum of amount', 'count of orders', 'average price by category')",
            ),
            "group_by": NodeParameter(
                name="group_by",
                type=list,
                required=False,
                default=[],
                description="Fields to group by for aggregation",
            ),
            "having": NodeParameter(
                name="having",
                type=dict,
                required=False,
                default={},
                description="Having clause conditions for filtered aggregations",
            ),
            "order_by": NodeParameter(
                name="order_by",
                type=list,
                required=False,
                default=[],
                description="Order by specifications for result sorting",
            ),
            "limit": NodeParameter(
                name="limit",
                type=int,
                required=False,
                description="Limit number of results returned",
            ),
            "natural_language": NodeParameter(
                name="natural_language",
                type=bool,
                required=False,
                default=True,
                description="Enable natural language processing of aggregation expressions",
            ),
            "connection_pool_id": NodeParameter(
                name="connection_pool_id",
                type=str,
                required=False,
                description="ID of DataFlowConnectionManager node for database operations",
            ),
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute aggregation operation with connection pool integration."""
        return self._execute_with_connection(self._perform_aggregation, **kwargs)

    def _perform_aggregation(self, **kwargs) -> Dict[str, Any]:
        """Perform the actual aggregation operation."""
        try:
            data = kwargs.get("data", [])
            aggregate_expression = kwargs.get("aggregate_expression", "")
            group_by = kwargs.get("group_by", [])
            having = kwargs.get("having", {})
            order_by = kwargs.get("order_by", [])
            limit = kwargs.get("limit")
            natural_language = kwargs.get("natural_language", True)

            if not data or not aggregate_expression:
                return {
                    "aggregated_data": [],
                    "summary": {
                        "total_groups": 0,
                        "aggregation_functions": [],
                        "group_by_fields": [],
                        "original_expression": aggregate_expression,
                    },
                }

            # Parse aggregation expression
            if natural_language:
                parsed_agg = self._parse_natural_language_aggregation(
                    aggregate_expression
                )
            else:
                parsed_agg = self._parse_structured_aggregation(aggregate_expression)

            # Extract group by from expression if not explicitly provided
            if not group_by and parsed_agg.get("group_by"):
                group_by = parsed_agg["group_by"]

            # Perform aggregation
            if group_by:
                result = self._grouped_aggregation(
                    data, parsed_agg, group_by, having, order_by, limit
                )
            else:
                result = self._simple_aggregation(data, parsed_agg)

            # Generate summary
            summary = self._generate_aggregation_summary(result, parsed_agg, group_by)

            return {
                "aggregated_data": result,
                "summary": summary,
                "aggregation_spec": parsed_agg,
                "optimization_metadata": {
                    "pattern": "aggregation",
                    "group_by_fields": group_by,
                    "aggregation_functions": parsed_agg.get("functions", []),
                    "can_optimize_to_sql": True,
                },
            }

        except Exception as e:
            logger.error(f"Aggregation failed: {e}")
            return {"error": str(e), "aggregated_data": [], "summary": {}}

    def _parse_natural_language_aggregation(self, expression: str) -> Dict[str, Any]:
        """Parse natural language aggregation expressions."""
        expr_lower = expression.lower().strip()

        # Initialize result structure
        result = {
            "functions": [],
            "group_by": [],
            "fields": [],
            "original_expression": expression,
        }

        # Handle multiple aggregations separated by commas
        parts = [part.strip() for part in expr_lower.split(",")]

        for part in parts:
            # Parse individual aggregation expressions
            agg_info = self._parse_single_aggregation(part)
            if agg_info:
                result["functions"].extend(agg_info.get("functions", []))
                result["fields"].extend(agg_info.get("fields", []))
                if agg_info.get("group_by"):
                    result["group_by"].extend(agg_info["group_by"])

        # Remove duplicates while preserving order
        result["functions"] = list(dict.fromkeys(result["functions"]))
        result["fields"] = list(dict.fromkeys(result["fields"]))
        result["group_by"] = list(dict.fromkeys(result["group_by"]))

        return result

    def _parse_single_aggregation(self, expr: str) -> Dict[str, Any]:
        """Parse a single aggregation expression."""
        result = {"functions": [], "fields": [], "group_by": []}

        # Common aggregation patterns
        patterns = [
            # "sum of amount by region"
            (
                r"(\w+)\s+of\s+(\w+)\s+by\s+(.+)",
                lambda m: {
                    "functions": [f"{m.group(1).upper()}({m.group(2)})"],
                    "fields": [m.group(2)],
                    "group_by": [field.strip() for field in m.group(3).split(",")],
                },
            ),
            # "sum of amount"
            (
                r"(\w+)\s+of\s+(\w+)",
                lambda m: {
                    "functions": [f"{m.group(1).upper()}({m.group(2)})"],
                    "fields": [m.group(2)],
                    "group_by": [],
                },
            ),
            # "count by region"
            (
                r"count\s+by\s+(.+)",
                lambda m: {
                    "functions": ["COUNT(*)"],
                    "fields": ["*"],
                    "group_by": [field.strip() for field in m.group(1).split(",")],
                },
            ),
            # "count"
            (
                r"^count$",
                lambda m: {"functions": ["COUNT(*)"], "fields": ["*"], "group_by": []},
            ),
            # "average price per category"
            (
                r"(\w+)\s+(\w+)\s+per\s+(\w+)",
                lambda m: {
                    "functions": [f"{m.group(1).upper()}({m.group(2)})"],
                    "fields": [m.group(2)],
                    "group_by": [m.group(3)],
                },
            ),
            # "total sales by month"
            (
                r"total\s+(\w+)\s+by\s+(.+)",
                lambda m: {
                    "functions": [f"SUM({m.group(1)})"],
                    "fields": [m.group(1)],
                    "group_by": [field.strip() for field in m.group(2).split(",")],
                },
            ),
            # "maximum price"
            (
                r"(maximum|minimum|max|min)\s+(\w+)",
                lambda m: {
                    "functions": [
                        f"{'MAX' if m.group(1) in ['maximum', 'max'] else 'MIN'}({m.group(2)})"
                    ],
                    "fields": [m.group(2)],
                    "group_by": [],
                },
            ),
        ]

        import re

        for pattern, extractor in patterns:
            match = re.search(pattern, expr)
            if match:
                return extractor(match)

        # Fallback: try to extract basic function and field
        simple_match = re.search(r"(\w+)\s*\((\w+)\)", expr)
        if simple_match:
            return {
                "functions": [
                    f"{simple_match.group(1).upper()}({simple_match.group(2)})"
                ],
                "fields": [simple_match.group(2)],
                "group_by": [],
            }

        return result

    def _parse_structured_aggregation(self, expression: str) -> Dict[str, Any]:
        """Parse structured aggregation expressions (SQL-like)."""
        # For structured expressions, assume they're already in SQL function format
        return {
            "functions": [expression.upper()],
            "fields": ["*"],
            "group_by": [],
            "original_expression": expression,
        }

    def _grouped_aggregation(
        self,
        data: List[Dict],
        agg_spec: Dict,
        group_by: List[str],
        having: Dict,
        order_by: List,
        limit: Optional[int],
    ) -> List[Dict]:
        """Perform grouped aggregation."""
        from collections import defaultdict

        # Group data by specified fields
        groups = defaultdict(list)

        for record in data:
            # Create group key from group_by fields
            group_key_parts = []
            for field in group_by:
                value = record.get(field, "NULL")
                group_key_parts.append(str(value))
            group_key = "|".join(group_key_parts)
            groups[group_key].append(record)

        # Calculate aggregations for each group
        results = []
        for group_key, group_records in groups.items():
            # Recreate group values
            group_values = group_key.split("|")
            group_dict = {}
            for i, field in enumerate(group_by):
                if i < len(group_values):
                    # Try to convert back to appropriate type
                    value = group_values[i]
                    if value == "NULL":
                        group_dict[field] = None
                    elif value.isdigit():
                        group_dict[field] = int(value)
                    elif self._is_float(value):
                        group_dict[field] = float(value)
                    else:
                        group_dict[field] = value
                else:
                    group_dict[field] = None

            # Calculate aggregations for this group
            agg_values = self._calculate_aggregations(
                group_records, agg_spec["functions"]
            )

            # Combine group fields and aggregation results
            result_record = {**group_dict, **agg_values}

            # Apply having clause
            if self._matches_having(result_record, having):
                results.append(result_record)

        # Apply ordering
        if order_by:
            results = self._apply_ordering(results, order_by)

        # Apply limit
        if limit:
            results = results[:limit]

        return results

    def _simple_aggregation(self, data: List[Dict], agg_spec: Dict) -> List[Dict]:
        """Perform simple aggregation without grouping."""
        agg_values = self._calculate_aggregations(data, agg_spec["functions"])
        return [agg_values] if agg_values else []

    def _calculate_aggregations(
        self, records: List[Dict], functions: List[str]
    ) -> Dict[str, Any]:
        """Calculate aggregation functions on records."""
        result = {}

        for func in functions:
            # Parse function format: FUNCTION(field) or FUNCTION(*)
            import re

            match = re.match(r"(\w+)\(([^)]+)\)", func)
            if not match:
                continue

            func_name = match.group(1).upper()
            field_name = match.group(2)

            if field_name == "*":
                # COUNT(*) or similar
                if func_name == "COUNT":
                    result["count"] = len(records)
            else:
                # Extract field values
                values = []
                for record in records:
                    value = record.get(field_name)
                    if value is not None and self._is_numeric(value):
                        values.append(float(value))

                # Calculate aggregation
                if values:
                    if func_name == "SUM":
                        result[f"sum_{field_name}"] = sum(values)
                    elif func_name == "AVG" or func_name == "AVERAGE":
                        result[f"avg_{field_name}"] = sum(values) / len(values)
                    elif func_name == "COUNT":
                        result[f"count_{field_name}"] = len(values)
                    elif func_name == "MAX":
                        result[f"max_{field_name}"] = max(values)
                    elif func_name == "MIN":
                        result[f"min_{field_name}"] = min(values)
                    elif func_name == "MEDIAN":
                        sorted_values = sorted(values)
                        n = len(sorted_values)
                        if n % 2 == 0:
                            result[f"median_{field_name}"] = (
                                sorted_values[n // 2 - 1] + sorted_values[n // 2]
                            ) / 2
                        else:
                            result[f"median_{field_name}"] = sorted_values[n // 2]
                else:
                    result[f"{func_name.lower()}_{field_name}"] = 0

        return result

    def _is_numeric(self, value) -> bool:
        """Check if value is numeric."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def _is_float(self, value: str) -> bool:
        """Check if string represents a float."""
        try:
            float(value)
            return "." in value
        except ValueError:
            return False

    def _matches_having(self, record: Dict, having: Dict) -> bool:
        """Check if record matches having clause conditions."""
        if not having:
            return True

        for field, condition in having.items():
            record_value = record.get(field)
            if record_value is None:
                return False

            if isinstance(condition, dict):
                # MongoDB-style operators
                for op, value in condition.items():
                    if op == "$gt" and not record_value > value:
                        return False
                    elif op == "$gte" and not record_value >= value:
                        return False
                    elif op == "$lt" and not record_value < value:
                        return False
                    elif op == "$lte" and not record_value <= value:
                        return False
                    elif op == "$eq" and not record_value == value:
                        return False
                    elif op == "$ne" and not record_value != value:
                        return False
            else:
                # Simple equality
                if record_value != condition:
                    return False

        return True

    def _apply_ordering(self, records: List[Dict], order_by: List) -> List[Dict]:
        """Apply ordering to results."""
        for order_spec in reversed(
            order_by
        ):  # Apply in reverse order for multiple sorts
            if isinstance(order_spec, dict):
                for field, direction in order_spec.items():
                    reverse = direction.lower() in ["desc", "descending", -1]
                    records.sort(key=lambda x: x.get(field, 0), reverse=reverse)
            elif isinstance(order_spec, str):
                # Simple field name (ascending)
                records.sort(key=lambda x: x.get(order_spec, 0))

        return records

    def _generate_aggregation_summary(
        self, results: List[Dict], agg_spec: Dict, group_by: List[str]
    ) -> Dict[str, Any]:
        """Generate summary information about the aggregation."""
        summary = {
            "total_groups": len(results),
            "aggregation_functions": agg_spec.get("functions", []),
            "group_by_fields": group_by,
            "original_expression": agg_spec.get("original_expression", ""),
        }

        if results:
            # Calculate summary statistics
            numeric_fields = []
            for result in results:
                for key, value in result.items():
                    if key not in group_by and self._is_numeric(value):
                        numeric_fields.append(key)

            numeric_fields = list(set(numeric_fields))

            if numeric_fields:
                summary["numeric_summaries"] = {}
                for field in numeric_fields:
                    values = [
                        r[field]
                        for r in results
                        if field in r and self._is_numeric(r[field])
                    ]
                    if values:
                        summary["numeric_summaries"][field] = {
                            "min": min(values),
                            "max": max(values),
                            "avg": sum(values) / len(values),
                        }

        return summary


class NaturalLanguageFilterNode(SmartNodeConnectionMixin, Node):
    """Natural language filter node for intuitive data filtering.

    Supports natural language filter expressions like:
    - "today", "yesterday", "last week", "this month"
    - "active users", "completed orders", "high value customers"
    - "price > 100", "status = active", "region in north,south"
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._filter_cache = {}

    def get_parameters(self) -> Dict[str, NodeParameter]:
        """Define parameters for NaturalLanguageFilterNode."""
        return {
            "data": NodeParameter(
                name="data",
                type=list,
                required=True,
                description="Input data to filter",
            ),
            "filter_expression": NodeParameter(
                name="filter_expression",
                type=str,
                required=True,
                description="Natural language filter expression",
            ),
            "connection_pool_id": NodeParameter(
                name="connection_pool_id",
                type=str,
                required=False,
                description="ID of DataFlowConnectionManager node for database operations",
            ),
        }

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute filter operation with connection pool integration."""
        return self._execute_with_connection(self._perform_filter, **kwargs)

    def _perform_filter(self, **kwargs) -> Dict[str, Any]:
        """Perform the actual filtering operation."""
        try:
            data = kwargs.get("data", [])
            filter_expression = kwargs.get("filter_expression", "")

            if not data or not filter_expression:
                return {
                    "filtered_data": data,
                    "filter_applied": filter_expression,
                    "records_filtered": 0,
                    "optimization_metadata": {
                        "pattern": "filter",
                        "filter_expression": filter_expression,
                        "can_optimize_to_sql": True,
                    },
                }

            # Parse and apply filter
            filter_func = self._parse_natural_language_filter(filter_expression)
            filtered_data = [record for record in data if filter_func(record)]

            return {
                "filtered_data": filtered_data,
                "filter_applied": filter_expression,
                "records_filtered": len(data) - len(filtered_data),
                "optimization_metadata": {
                    "pattern": "filter",
                    "filter_expression": filter_expression,
                    "can_optimize_to_sql": True,
                },
            }

        except Exception as e:
            logger.error(f"Filter operation failed: {e}")
            return {"error": str(e), "filtered_data": data}

    def _parse_natural_language_filter(self, expression: str):
        """Parse natural language filter expression into a filter function."""
        expr_lower = expression.lower().strip()

        # Date/time filters
        import datetime

        today = datetime.date.today()

        if expr_lower in ["today", "today's orders", "orders from today"]:
            return lambda record: self._is_today(
                record.get("created_at", record.get("date"))
            )
        elif expr_lower in ["yesterday", "yesterday's orders"]:
            return lambda record: self._is_yesterday(
                record.get("created_at", record.get("date"))
            )
        elif expr_lower in ["this week", "this week's orders"]:
            return lambda record: self._is_this_week(
                record.get("created_at", record.get("date"))
            )
        elif expr_lower in ["last week", "last week's orders"]:
            return lambda record: self._is_last_week(
                record.get("created_at", record.get("date"))
            )
        elif expr_lower in ["this month", "this month's orders"]:
            return lambda record: self._is_this_month(
                record.get("created_at", record.get("date"))
            )
        elif expr_lower in ["last month", "last month's orders"]:
            return lambda record: self._is_last_month(
                record.get("created_at", record.get("date"))
            )

        # Status filters
        elif expr_lower in ["active", "active users", "active customers"]:
            return (
                lambda record: record.get("active", record.get("status"))
                or record.get("status") == "active"
            )
        elif expr_lower in ["inactive", "inactive users"]:
            return (
                lambda record: not record.get("active", record.get("status"))
                or record.get("status") == "inactive"
            )
        elif expr_lower in ["completed", "completed orders"]:
            return lambda record: record.get("status") == "completed"
        elif expr_lower in ["pending", "pending orders"]:
            return lambda record: record.get("status") == "pending"

        # Value-based filters
        elif "high value" in expr_lower:
            return lambda record: self._is_high_value(record)
        elif "low value" in expr_lower:
            return lambda record: self._is_low_value(record)

        # Default: return all records
        return lambda record: True

    def _is_today(self, date_value) -> bool:
        """Check if date is today."""
        if not date_value:
            return False
        try:
            import datetime

            if isinstance(date_value, str):
                # Parse common date formats
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]:
                    try:
                        parsed_date = datetime.datetime.strptime(date_value, fmt).date()
                        return parsed_date == datetime.date.today()
                    except ValueError:
                        continue
            elif hasattr(date_value, "date"):
                return date_value.date() == datetime.date.today()
            elif hasattr(date_value, "year"):
                return date_value == datetime.date.today()
        except Exception:
            pass
        return False

    def _is_yesterday(self, date_value) -> bool:
        """Check if date is yesterday."""
        if not date_value:
            return False
        try:
            import datetime

            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            if isinstance(date_value, str):
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]:
                    try:
                        parsed_date = datetime.datetime.strptime(date_value, fmt).date()
                        return parsed_date == yesterday
                    except ValueError:
                        continue
            elif hasattr(date_value, "date"):
                return date_value.date() == yesterday
            elif hasattr(date_value, "year"):
                return date_value == yesterday
        except Exception:
            pass
        return False

    def _is_this_week(self, date_value) -> bool:
        """Check if date is in this week."""
        if not date_value:
            return False
        try:
            import datetime

            today = datetime.date.today()
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)

            if isinstance(date_value, str):
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]:
                    try:
                        parsed_date = datetime.datetime.strptime(date_value, fmt).date()
                        return start_of_week <= parsed_date <= end_of_week
                    except ValueError:
                        continue
            elif hasattr(date_value, "date"):
                return start_of_week <= date_value.date() <= end_of_week
            elif hasattr(date_value, "year"):
                return start_of_week <= date_value <= end_of_week
        except Exception:
            pass
        return False

    def _is_last_week(self, date_value) -> bool:
        """Check if date is in last week."""
        if not date_value:
            return False
        try:
            import datetime

            today = datetime.date.today()
            start_of_this_week = today - datetime.timedelta(days=today.weekday())
            start_of_last_week = start_of_this_week - datetime.timedelta(days=7)
            end_of_last_week = start_of_this_week - datetime.timedelta(days=1)

            if isinstance(date_value, str):
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]:
                    try:
                        parsed_date = datetime.datetime.strptime(date_value, fmt).date()
                        return start_of_last_week <= parsed_date <= end_of_last_week
                    except ValueError:
                        continue
            elif hasattr(date_value, "date"):
                return start_of_last_week <= date_value.date() <= end_of_last_week
            elif hasattr(date_value, "year"):
                return start_of_last_week <= date_value <= end_of_last_week
        except Exception:
            pass
        return False

    def _is_this_month(self, date_value) -> bool:
        """Check if date is in this month."""
        if not date_value:
            return False
        try:
            import datetime

            today = datetime.date.today()

            if isinstance(date_value, str):
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]:
                    try:
                        parsed_date = datetime.datetime.strptime(date_value, fmt).date()
                        return (
                            parsed_date.year == today.year
                            and parsed_date.month == today.month
                        )
                    except ValueError:
                        continue
            elif hasattr(date_value, "date"):
                dt = date_value.date()
                return dt.year == today.year and dt.month == today.month
            elif hasattr(date_value, "year"):
                return date_value.year == today.year and date_value.month == today.month
        except Exception:
            pass
        return False

    def _is_last_month(self, date_value) -> bool:
        """Check if date is in last month."""
        if not date_value:
            return False
        try:
            import datetime

            today = datetime.date.today()
            if today.month == 1:
                last_month_year = today.year - 1
                last_month = 12
            else:
                last_month_year = today.year
                last_month = today.month - 1

            if isinstance(date_value, str):
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d"]:
                    try:
                        parsed_date = datetime.datetime.strptime(date_value, fmt).date()
                        return (
                            parsed_date.year == last_month_year
                            and parsed_date.month == last_month
                        )
                    except ValueError:
                        continue
            elif hasattr(date_value, "date"):
                dt = date_value.date()
                return dt.year == last_month_year and dt.month == last_month
            elif hasattr(date_value, "year"):
                return (
                    date_value.year == last_month_year
                    and date_value.month == last_month
                )
        except Exception:
            pass
        return False

    def _is_high_value(self, record) -> bool:
        """Check if record represents high value."""
        # Look for amount, value, price, total fields
        value_fields = ["amount", "value", "price", "total", "revenue"]
        for field in value_fields:
            if field in record:
                value = record[field]
                if isinstance(value, (int, float)):
                    return value > 1000  # Configurable threshold
        return False

    def _is_low_value(self, record) -> bool:
        """Check if record represents low value."""
        value_fields = ["amount", "value", "price", "total", "revenue"]
        for field in value_fields:
            if field in record:
                value = record[field]
                if isinstance(value, (int, float)):
                    return value < 100  # Configurable threshold
        return False


# Register the nodes with Kailash's NodeRegistry
NodeRegistry.register(SmartMergeNode, alias="SmartMergeNode")
NodeRegistry.register(AggregateNode, alias="AggregateNode")
NodeRegistry.register(NaturalLanguageFilterNode, alias="NaturalLanguageFilterNode")
