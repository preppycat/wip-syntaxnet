import yaml
import os.path as path

# Load config file and paths
config_file = yaml.load(open(path.join(path.dirname(__file__), "../config.yml")))
config_syntaxnet = config_file['syntaxnet']
root_dir = config_syntaxnet['ROOT_DIR']
parser_eval_path = config_syntaxnet['PARSER_EVAL']
context_path = config_syntaxnet['CONTEXT']
model_path = config_syntaxnet['MODEL']

from syntaxnet_wrapper.wrapper import SyntaxNetWrapper
from syntaxnet_wrapper.wrapper_subprocess import SyntaxNetWrapperSubprocess
