import argparse
import markovify


COMMANDS = {}


def command(func):
    COMMANDS[func.__name__.replace('_', '-')] = func


@command
def build_model(args):
    with open(args.text) as text:
        if args.newline:
            factory = markovify.NewlineText
        else:
            factory = markovify.Text

        model = factory(text, retain_original=False)

    with open(args.output, 'w') as output:
        output.write(model.to_json())


@command
def run_model(args):
    with open(args.model) as fp:
        model = markovify.Text.from_json(fp.read())

    for _ in range(args.count):
        print(model.make_sentence())


def main():
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(dest='command', required=True)

    build_model_parser = subcommands.add_parser('build-model')
    build_model_parser.add_argument('text', help='The text file to build')
    build_model_parser.add_argument('output', help='The output file')
    build_model_parser.add_argument('--newline', '-n',
                                    help='Delimited by newlines instead of periods')

    run_model_parser = subcommands.add_parser('run-model')
    run_model_parser.add_argument('model', help='The model to use')
    run_model_parser.add_argument('--count', '-c', type=int,
                                  help='The # of sentences to generate', default=1)

    args = parser.parse_args()
    COMMANDS[args.command](args)
