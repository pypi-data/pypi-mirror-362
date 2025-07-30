import ast
import numpy as np
import copy
import ubelt as ub


class DynamicChannels:
    """
    A class to manage and compute dynamic channels based on expressions.

    Example:
        >>> from kwcoco_dataloader.tasks.fusion.datamodules.dynamic_channel_handler import DynamicChannels
        >>> import numpy as np
        >>> spec = [
        ...     {'name': 'r1', 'expr': '-g'},
        ...     {'name': 'r2', 'expr': 'exp(b / 255) ** 3 + 1'},
        ...     {'name': 'r3', 'expr': 'r'}
        ... ]
        >>> dyn = DynamicChannels(spec)
        >>> dyn.dynamic_names()
        ['r1', 'r2', 'r3']
        >>> input_lut = {
        ...     'r': np.ones((2, 2)) * 10,
        ...     'g': np.ones((2, 2)) * 20,
        ...     'b': np.ones((2, 2)) * 30,
        ... }
        >>> outputs = dyn.evaluate(input_lut, ['r1', 'r2'])
        >>> np.allclose(outputs['r1'], -20)
        True
        >>> np.allclose(outputs['r2'], (np.exp(30 / 255) ** 3 + 1))
        True
        >>> outputs = dyn.evaluate(input_lut)
        >>> sorted(outputs.keys())
        ['r1', 'r2', 'r3']
        >>> np.allclose(outputs['r3'], input_lut['r'])
        True
    """

    def __init__(self, dynamic_channel_spec):
        """
        Args:
            dynamic_channel_spec (List[Dict]): Each dict must have a 'name' and 'expr'.
        """
        self.raw_spec = copy.deepcopy(dynamic_channel_spec or [])
        # TODO: generalize beyond numpy, maybe use numexpr
        # https://numexpr.readthedocs.io/en/latest/user_guide.html#supported-functions
        # Note: numexpr does not have minimum and maximum
        # https://github.com/pydata/numexpr/issues/86
        self.allowed_funcnames = {
            'abs', 'ceil', 'floor', 'sign', 'isnan', 'isfinite',
            'log', 'log10', 'log2', 'log1p', 'expm1',
            'sqrt', 'exp',
            'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh',
            'arcsin', 'arccos', 'arctan',
            'arcsinh', 'arccosh', 'arctanh',

            'maximum', 'minimum', 'clip',

            # AI suggestions
            'round', 'rint', 'trunc', 'fix',
            'sum', 'prod', 'mean', 'std', 'var',
            'max', 'min', 'where',
            'logical_and', 'logical_or', 'logical_not',
            'equal', 'not_equal', 'greater', 'less',
            'greater_equal', 'less_equal',
            'nan_to_num', 'nanmax', 'nanmin', 'nansum', 'nanmean',
        }
        self._lut = {}
        self._channel_names = []

        self._parse_spec()

    def _parse_spec(self):
        for rule in self.raw_spec:
            rule = dict(rule)  # Shallow copy
            expr = rule['expr']
            name = rule['name']
            # TODO: can we check for unavailable names or be more robust in
            # general here?
            args = _get_free_varnames(expr)
            all_args = set(args)
            arg_vars = list(all_args - self.allowed_funcnames)
            funcnames = list(all_args & self.allowed_funcnames)
            ns = {n: getattr(np, n) for n in funcnames}
            rule.update({
                'args': arg_vars,
                'ns': ns,
            })
            self._lut[name] = rule
            self._channel_names.append(name)

    def dynamic_names(self):
        return self._channel_names

    def required_inputs(self, channel_names):
        """
        Given a list of dynamic channel names, returns the union of all input
        channels required to compute them.

        Example:
            >>> from kwcoco_dataloader.tasks.fusion.datamodules.dynamic_channel_handler import DynamicChannels
            >>> spec = [
            ...     {'name': 'r1', 'expr': 'r + g'},
            ...     {'name': 'r2', 'expr': 'exp(b / 255) ** 3 + 1'},
            ...     {'name': 'r3', 'expr': 'clip(r - b, 0, 1)'}
            ... ]
            >>> dyn = DynamicChannels(spec)
            >>> dyn.required_inputs(['r1'])
            ['g', 'r']
            >>> dyn.required_inputs(['r1', 'r2'])
            ['b', 'g', 'r']
            >>> dyn.required_inputs(['r1', 'r3'])
            ['b', 'g', 'r']
            >>> dyn.required_inputs(['r2', 'r3'])
            ['b', 'r']
            >>> dyn.required_inputs(dyn.dynamic_names())
            ['b', 'g', 'r']
        """
        return sorted(set(ub.flatten([self._lut[c]['args'] for c in channel_names])))

    def evaluate(self, input_lut, subset_names=None):
        """
        Evaluate only a subset of dynamic channels.

        Args:
            input_lut (Dict[str, np.ndarray])
            subset_names (List[str])

        Returns:
            Dict[str, np.ndarray]

        Example:
            >>> from kwcoco_dataloader.tasks.fusion.datamodules.dynamic_channel_handler import DynamicChannels
            >>> import numpy as np
            >>> spec = [
            ...     {'name': 'r1', 'expr': '-r'},
            ...     {'name': 'r2', 'expr': 'exp(r / 255) ** 3 + 1'},
            ...     {'name': 'r3', 'expr': 'minimum(maximum(r, 0.4), 0.5)'}
            ... ]
            >>> self = DynamicChannels(spec)
            >>> input_lut = {'r': np.random.rand(5, 5, 1)}
            >>> result = self.evaluate(input_lut)
            >>> assert np.all(result['r3'] >= 0.4)
            >>> assert np.all(result['r3'] <= 0.5)
        """
        if subset_names is None:
            subset_names = self._lut.keys()
        outputs = {}
        for name in subset_names:
            rule = self._lut[name]
            args = {k: input_lut[k] for k in rule['args']}
            args.update(rule['ns'])

            if 1:
                DEFAULT_ADDNODES = [
                    'Call', 'USub', 'UAdd', 'Not',
                    'Pow', 'Mult', 'Div', 'FloorDiv', 'Mod', 'Invert',
                    # optionally: 'BitAnd', 'BitOr', 'BitXor','LShift', 'RShift'
                ]
                from kwutil.util_eval import safeeval
                result = safeeval(
                    rule['expr'], context=args, addnodes=DEFAULT_ADDNODES,
                    funcs=list(rule['ns'].keys()))
            else:
                result = eval(rule['expr'], args)

            outputs[name] = result
        return outputs


def _get_free_varnames(expr):
    return [
        node.id for node in ast.walk(ast.parse(expr))
        if isinstance(node, ast.Name)
    ]
