"""
Condition evaluation and template rendering utilities for TAgent Community workflows.

Provides safe evaluation of Python expressions and Jinja2 template rendering
for dynamic workflow behavior.
"""

import ast
import operator
import logging
from typing import Dict, Any, Union
from jinja2 import Environment, BaseLoader, TemplateError, select_autoescape

logger = logging.getLogger(__name__)


class SafeEvaluator(ast.NodeVisitor):
    """
    Safe evaluator for Python expressions that restricts available operations.
    
    Only allows basic operations like comparisons, arithmetic, and attribute access
    to prevent code injection attacks.
    """
    
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.BitAnd: operator.and_,
        ast.FloorDiv: operator.floordiv,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Is: operator.is_,
        ast.IsNot: operator.is_not,
        ast.In: lambda x, y: x in y,
        ast.NotIn: lambda x, y: x not in y,
        ast.And: lambda x, y: x and y,
        ast.Or: lambda x, y: x or y,
        ast.Not: operator.not_,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    def __init__(self, context: Dict[str, Any]):
        self.context = context
    
    def evaluate(self, expression: str) -> Any:
        """Safely evaluate a Python expression."""
        try:
            tree = ast.parse(expression, mode='eval')
            return self.visit(tree.body)
        except Exception as e:
            raise ValueError(f"Invalid expression '{expression}': {e}")
    
    def visit_Expression(self, node):
        return self.visit(node.body)
    
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operator {type(node.op).__name__} not allowed")
        return op(left, right)
    
    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op = self.ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operator {type(node.op).__name__} not allowed")
        return op(operand)
    
    def visit_Compare(self, node):
        left = self.visit(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = self.visit(comparator)
            op_func = self.ALLOWED_OPERATORS.get(type(op))
            if op_func is None:
                raise ValueError(f"Operator {type(op).__name__} not allowed")
            if not op_func(left, right):
                return False
            left = right
        return True
    
    def visit_BoolOp(self, node):
        op = self.ALLOWED_OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError(f"Operator {type(node.op).__name__} not allowed")
        
        values = [self.visit(value) for value in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        elif isinstance(node.op, ast.Or):
            return any(values)
        else:
            raise ValueError(f"Boolean operator {type(node.op).__name__} not supported")
    
    def visit_Attribute(self, node):
        value = self.visit(node.value)
        if hasattr(value, node.attr):
            return getattr(value, node.attr)
        raise AttributeError(f"'{type(value).__name__}' object has no attribute '{node.attr}'")
    
    def visit_Subscript(self, node):
        value = self.visit(node.value)
        key = self.visit(node.slice)
        try:
            return value[key]
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(f"Subscript error: {e}")
    
    def visit_Index(self, node):
        return self.visit(node.value)
    
    def visit_Slice(self, node):
        lower = self.visit(node.lower) if node.lower else None
        upper = self.visit(node.upper) if node.upper else None
        step = self.visit(node.step) if node.step else None
        return slice(lower, upper, step)
    
    def visit_Name(self, node):
        if node.id in self.context:
            return self.context[node.id]
        # Allow some built-in constants
        if node.id in ('True', 'False', 'None'):
            return eval(node.id)
        raise NameError(f"Name '{node.id}' is not defined")
    
    def visit_Constant(self, node):
        return node.value
    
    def visit_Num(self, node):  # For Python < 3.8 compatibility
        return node.n
    
    def visit_Str(self, node):  # For Python < 3.8 compatibility
        return node.s
    
    def visit_List(self, node):
        return [self.visit(item) for item in node.elts]
    
    def visit_Tuple(self, node):
        return tuple(self.visit(item) for item in node.elts)
    
    def visit_Dict(self, node):
        keys = [self.visit(k) for k in node.keys]
        values = [self.visit(v) for v in node.values]
        return dict(zip(keys, values))
    
    def generic_visit(self, node):
        raise ValueError(f"Operation {type(node).__name__} not allowed")


class ConditionEvaluator:
    """Evaluates conditional expressions safely."""
    
    def evaluate(self, condition: str, context: Dict[str, Any]) -> bool:
        """
        Evaluate a condition expression against the given context.
        
        Args:
            condition: Python expression to evaluate
            context: Context dictionary for variable resolution
            
        Returns:
            Boolean result of the condition
            
        Raises:
            ValueError: If the expression is invalid or contains forbidden operations
        """
        evaluator = SafeEvaluator(context)
        result = evaluator.evaluate(condition.strip())
        
        # Ensure result is boolean
        return bool(result)


class TemplateRenderer:
    """Renders Jinja2 templates with context data."""
    
    def __init__(self):
        self.env = Environment(
            loader=BaseLoader(),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Add custom filters
        self.env.filters['jsonify'] = self._jsonify_filter
        self.env.filters['safe_get'] = self._safe_get_filter
    
    def render(self, template_str: str, context: Dict[str, Any]) -> str:
        """
        Render a Jinja2 template with the given context.
        
        Args:
            template_str: Template string to render
            context: Context dictionary for variable substitution
            
        Returns:
            Rendered template string
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            template = self.env.from_string(template_str)
            return template.render(**context)
        except TemplateError as e:
            raise TemplateError(f"Template rendering failed: {e}")
        except Exception as e:
            raise TemplateError(f"Unexpected error during template rendering: {e}")
    
    def _jsonify_filter(self, value: Any) -> str:
        """Custom filter to safely convert values to JSON strings."""
        import json
        try:
            return json.dumps(value, default=str, ensure_ascii=False)
        except Exception:
            return str(value)
    
    def _safe_get_filter(self, obj: Any, key: str, default: Any = None) -> Any:
        """Custom filter for safe dictionary/object access."""
        if isinstance(obj, dict):
            return obj.get(key, default)
        elif hasattr(obj, key):
            return getattr(obj, key, default)
        else:
            return default