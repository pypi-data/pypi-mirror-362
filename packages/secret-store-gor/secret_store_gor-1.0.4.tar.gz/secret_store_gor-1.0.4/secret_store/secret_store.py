import inspect
from typing import List, Callable, Set, Dict


def extract_parameters(func: Callable, required_only: bool = False) -> Set[str]:
    """Extract the names of a method or class's parameters.

    Args:
        func (Callable): The callable object to extract paramters from.
        required_only (bool, default=False): If True, will only return the
            required (no default value) parameters. Otherwise all parameters
            are returned.

    Returns:
        Set[str]: The set of paramters for the callable.
    """
    # Use the inspect module to get a function's parameters from its signature
    params = inspect.signature(func)._parameters

    param_names = set()

    # extract the name of the parameter as a string.
    for name, param in params.items():
        # If we only want required parameters, and the parameter has a default
        # (its default value is not _empty) skip it.
        if required_only and param.default != inspect._empty:
            continue
        param_names.add(name)

    return param_names


class SecretNotFoundError(Exception):
    """ Exception raised when the secret was unable to be retrieved.
    """
    pass


class SecretStore:
    """Factory for creating connections to secret stores.
    """

    # A value that is very unlikely to be requested as a default
    # value for a secret.
    no_default = '______NO_DEFAULT______'

    @classmethod
    def connect(cls, *ignore, **kwargs) -> "SecretStore":
        """Connect to a secret store.

        Note: For details upon each stores set of required parameters see the
              output of the function |SecretStore.stores|.

        Args:
            kwargs: Named arguments for the secret store being
                connected to. The names of these arguments are matched against
                those of the supported stores. The store with an exact match
                or required params with the params provided is instaniated.

        Raises:
            TypeError: If no store accepts the paramters contained in kwargs.

        Returns:
            SecretStore: An instance of the secret store.
        """
        if ignore:
            raise TypeError('Only keyword arguments are supported')

        store_name = kwargs.pop('store', None)
        given_params = set(kwargs.keys())

        store = None
        for sub_cls in cls.__subclasses__():
            # When given a store name, do not try and infer using args
            if store_name:
                if sub_cls.NAME == store_name:
                    store = sub_cls
                    break
                continue

            req_params = extract_parameters(sub_cls)
            if req_params == given_params:
                store = sub_cls
                break

        if store is None:
            raise TypeError("No secret store accepts the set of parameters "
                            f"'{given_params}'.")

        print(f'[Using Store: "{store.NAME}"]\n')

        return store(**kwargs)

    @classmethod
    def stores(cls) -> List[Dict[str, Set[str]]]:
        """Get a list of the supported secret stores and their required
        keyword arguments.

        Returns:
            list[dist[str: Set[str]]: A list of the names of supported secret
            store types.
        """
        return [
            {
                "name": sub_cls.__name__,
                "required_keyword_arguments": extract_parameters(sub_cls)
            }
            for sub_cls in cls.__subclasses__()
        ]


def connect(*ignore, **kwargs) -> "SecretStore":
    """Factory method for connecting to a secret store.

    Note: For details upon each stores set of required parameters see the
            output of the function |SecretStore.stores|.

    Args:
        kwargs: Named arguments for the secret store being
            connected to. The names of these arguments are matched against
            those of the supported stores. The store with an exact match
            or required params with the params provided is instaniated.

    Raises:
        TypeError: If no store accepts the paramters contained in kwargs.

    Returns:
        SecretStore: An instance of the secret store.
    """
    return SecretStore.connect(*ignore, **kwargs)
