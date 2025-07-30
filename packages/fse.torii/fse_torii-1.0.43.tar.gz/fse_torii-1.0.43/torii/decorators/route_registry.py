import functools
import json


class RouteRegistry:
    """
    A client-side imitation of a Web Framework view path registry.

    This class serves to create backwards compatibility and fallback capable code
    between established REST API calls and client-side data access objects (DAOs).
    """

    routes = {}

    def register(self, method, route):
        """
        Register a class method to a specific route.

        >>> @registry.register('GET', '{var}/path')
        >>> def my_class_method(self, var):
        >>>     print(var)

        :param method: The Http method (GET, POST, PUT, PATCH or DELETE).
        :param route: The unique route to associate with the class method. Supports multiple dynamic path variables.
        :returns: Calls the respective method and returns its result.
        """

        def decorator(func):

            @functools.wraps(func)
            def wrapped(instance, path, *args, **kwargs):
                variables = []
                route_parts = route.split('/')
                path_parts = path.split('/')

                # Grab the variables from the requested path
                for route_part, path_part in zip(route_parts, path_parts):
                    if route_part.startswith('{') and route_part.endswith('}'):
                        variables.append(path_part)

                kwargs = self._load_json(kwargs)

                return func(instance, *variables, *args, **kwargs)

            # Register the route to the registry
            if method not in self.routes: self.routes[method] = {}
            self.routes[method][route] = wrapped

            return wrapped

        return decorator

    def call_method(self, instance, http_method: str, path: str, *args, **kwargs):
        """
        Runs the wrapped function that corresponds to the given path.

        :param instance: Reference to the class instance
        :param http_method: The Http method (GET, POST, PUT, PATCH or DELETE)
        :param path: The requested path
        :param args: Any additional arguments to be passed to the function
        :param kwargs: Any additional keyword arguments to be passed to the function
        :returns: The wrapped function if path matches.
        :raises ValueError: If no match was found for given path.
        """
        if http_method not in self.routes:
            raise ValueError(f"No matching route found for ({http_method}, {path}).")

        path_parts = list(filter(None, path.split('/')))

        func = self.match_specific_route(self.routes[http_method], path_parts) \
               or self.match_any_route(self.routes[http_method], path_parts)

        if func: return func(instance, path, *args, **kwargs)

        raise ValueError(f"No matching route found for ({http_method}, {path}).")

    @staticmethod
    def _load_json(kwargs: dict):
        """
        Convert JSON compatible strings back to the original object.

        :param kwargs: Dictionary with all keyword arguments.
        :return: Dictionary with the correct objects loaded.
        """
        for key, item in kwargs.items():
            if isinstance(item, str):
                try:
                    kwargs[key] = json.loads(item)
                except ValueError:
                    pass
        return kwargs

    @staticmethod
    def match_specific_route(routes: dict, path_parts: list):
        """
        Match with specific route (i.e., {var}/path).

        :param routes: Dictionary with all the routes of a given Http method
        :param path_parts: The list of path parts to compare with the registry path parts
        :return: The wrapped function if paths match, otherwise None
        """
        for reg_path, func in routes.items():
            reg_path_parts = reg_path.split('/')
            if len(reg_path_parts) == len(path_parts):
                match = []
                for part, user_part in zip(reg_path_parts, path_parts):
                    if not part.startswith('{') and not part.endswith('}'):
                        match.append(True if part == user_part else False)
                if match and all(match):
                    return func
        return None

    @staticmethod
    def match_any_route(routes: dict, path_parts: list):
        """
        Get the first route that matches (i.e., {var1}/{var2}).

        :param routes: Dictionary with all the routes of a given Http method
        :param path_parts: The list of path parts to compare with the registry path parts
        :return: The wrapped function if paths match, otherwise None
        """
        for reg_path, func in routes.items():
            reg_path_parts = reg_path.split('/')
            if len(reg_path_parts) == len(path_parts):
                matches = True
                for part, user_part in zip(reg_path_parts, path_parts):
                    if not part.startswith('{') and not part.endswith('}') and part != user_part:
                        matches = False
                        break
                if matches:
                    return func
        return None
