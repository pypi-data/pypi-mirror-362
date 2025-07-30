import argparse

import secret_store


def get_secret(name: str, default: str, **kwargs) -> str:
    store = secret_store.connect(**kwargs)
    value = store.get(name, default)
    return f'{name}={value}'


def set_secret(name: str, value: str, **kwargs) -> str:
    store = secret_store.connect(**kwargs)
    store.set(name, value)
    return f'{name}={value}'


def parse():
    base_parser = argparse.ArgumentParser(add_help=False)

    local_store = base_parser.add_argument_group('Local Store')
    local_store.add_argument('--path', type=str,
                             help='Path to a file on disk where secrets will '
                                  'be/are stored.')

    aws_args = base_parser.add_argument_group('AWS Secrets Manager')
    aws_args.add_argument('--aws-access-key-id', type=str, default=None,
                          help='AWS access key ID')
    aws_args.add_argument('--aws-secret-access-key', type=str, default=None,
                          help='AWS secret access key.')
    aws_args.add_argument('--region', type=str, default=None,
                          help='The AWS region to connect to.')

    azure_args = base_parser.add_argument_group('Azure Key Vault')
    azure_args.add_argument('--key-vault-name', type=str,
                            help='The name of the Azure KeyVault.')

    parser = argparse.ArgumentParser(
        description="Get/Set secrets in multiple Secret Managers."
    )
    parser.add_argument('--store', type=str,
                        choices=[sub_cls.NAME
                                 for sub_cls
                                 in secret_store.SecretStore.__subclasses__()],
                        help='Explicit definition of store to use. '
                             'Otherwise store will be inferred from the '
                             'passed flags. Especially helpful if using '
                             'env vars or configs making flags '
                             'unnecessary.')
    subparser = parser.add_subparsers(title="actions")

    get_parser = subparser.add_parser(
        'get',
        description="Get secrets in multiple Secret Managers.",
        parents=[base_parser],
    )
    get_parser.set_defaults(func=get_secret)
    get_parser.add_argument('name', type=str,
                            help="The secret's name")
    get_parser.add_argument('--default', type=str,
                            default=secret_store.SecretStore.no_default,
                            help='If provided, a default value to return if '
                                 'a secret is not found or fails to be '
                                 'retrieved.')

    set_parser = subparser.add_parser(
        'set',
        description="Set secrets in multiple Secret Managers.",
        parents=[base_parser]
    )
    set_parser.set_defaults(func=set_secret)
    set_parser.add_argument('name', type=str,
                            help="The secret's name")
    set_parser.add_argument('value', type=str,
                            help="The secret's value")

    return parser.parse_args()


def main():
    args = parse()
    args_dict = {
        key: val
        for key, val in vars(args).items()
        if val is not None
    }

    func = args_dict.pop('func')
    resp = func(**args_dict)

    print(resp)


if __name__ == '__main__':
    main()
