#
#
# Heavily inspired from https://github.com/IINemo/docker-syntaxnet_rus://github.com/IINemo/docker-syntaxnet_rus
# itself inspired from https://github.com/tensorflow/models/blob/master/syntaxnet/syntaxnet/parser_eval.py
# just modified to be able to call wrapper several time for the same process
#
# ==============================================================================

"""A program to annotate a conll file with a tensorflow neural net parser."""

import os, sys
import os.path as path
import time

################################################################################
# Make importable module from syntaxnet path
from syntaxnet_wrapper import root_dir, context_path

def CreatePythonPathEntries(python_imports, module_space):
    parts = python_imports.split(':');
    return [module_space] + ["%s/%s" % (module_space, path) for path in parts]

module_space = path.join(root_dir, 'bazel-bin/syntaxnet/parser_eval.runfiles/')
python_imports = 'protobuf/python'
python_path_entries = CreatePythonPathEntries(python_imports, module_space)

repo_dirs = [os.path.join(module_space, d) for d in os.listdir(module_space)]
repositories = [d for d in repo_dirs if os.path.isdir(d)]
python_path_entries += repositories


sys.path += python_path_entries
################################################################################
# Copy custoim context.pbtxt to replace the default one from syntaxnet repo
# The custom context.pbtxt use custom file instead of stdin and stdout
import shutil
shutil.copyfile(path.join(path.dirname(__file__), './context.pbtxt'), path.join(root_dir, context_path))

################################################################################

import tempfile 

import tensorflow as tf

from tensorflow.python.platform import gfile
from tensorflow.python.platform import tf_logging as logging

from google.protobuf import text_format

from syntaxnet import sentence_pb2
from syntaxnet.ops import gen_parser_ops
from syntaxnet import task_spec_pb2

from syntaxnet import graph_builder
from syntaxnet import structured_graph_builder

def RewriteContext(task_context, resource_dir):
  context = task_spec_pb2.TaskSpec()
  with gfile.FastGFile(task_context) as fin:
    text_format.Merge(fin.read(), context)
  for resource in context.input:
    for part in resource.part:
      if part.file_pattern != '-':
        part.file_pattern = os.path.join(resource_dir, part.file_pattern)
  with tempfile.NamedTemporaryFile(delete=False) as fout:
    fout.write(str(context))
    return fout.name

class SyntaxNetConfig:
    
    def __init__(self,
        task_context='', # Path to a task context with inputs and parameters for feature extractors.
        resource_dir='', # Optional base directory for task context resources.
        model_path='', # Path to model parameters.
        arg_prefix=None, # Prefix for context parameters.
        graph_builder_='greedy', # Which graph builder to use, either greedy or structured.
        input_='stdin', # Name of the context input to read data from.
        hidden_layer_sizes=[200, 200], # Comma separated list of hidden layer sizes.
        batch_size=32, # Number of sentences to process in parallel.
        beam_size=8, # Number of slots for beam parsing.
        max_steps=1000, # Max number of steps to take.
        slim_model=False, # Whether to expect only averaged variables.
        custom_file='/tmp/tmp.file', # File to communicate input to SyntaxNet
        variable_scope=None, # Scope with the defined parser variable, to set up the context
        max_tmp_size=262144000 # Maximum size of tmp input file
        ):

        self.task_context = task_context
        self.resource_dir = resource_dir
        self.model_path = model_path
        self.arg_prefix = arg_prefix
        self.graph_builder_ = graph_builder_
        self.input_ = input_
        self.hidden_layer_sizes = hidden_layer_sizes
        self.batch_size = batch_size
        self.beam_size = beam_size
        self.max_steps = max_steps
        self.slim_model = slim_model
        self.custom_file = custom_file
        self.variable_scope = variable_scope
        self.max_tmp_size = max_tmp_size

class SyntaxNetProcess:

    def __init__(self, processconfig):
        self._sess = tf.Session()
        self._pg = processconfig
        self.stdout_file_path = os.path.join(os.path.dirname(self._pg.custom_file), 'stdout.tmp') # File where syntaxnet output will be written

        """Builds and evaluates a network."""
        self.task_context = self._pg.task_context
        if self._pg.resource_dir:
            self.task_context = RewriteContext(self.task_context, self._pg.resource_dir)
        
	# Initiate custom tmp file
	with open(self._pg.custom_file, 'w') as f:
      	    pass
        self.fdescr_ = open(self._pg.custom_file, 'r')

	with tf.variable_scope(self._pg.variable_scope):
            feature_sizes, domain_sizes, embedding_dims, num_actions = self._sess.run(
                gen_parser_ops.feature_size(task_context=self.task_context, arg_prefix=self._pg.arg_prefix))


            if self._pg.graph_builder_ == 'greedy':
                self._parser = graph_builder.GreedyParser(num_actions,
                                            feature_sizes,
                                            domain_sizes,
                                            embedding_dims,
                                            self._pg.hidden_layer_sizes,
                                            gate_gradients=True,
                                            arg_prefix=self._pg.arg_prefix)
            else:
                self._parser = structured_graph_builder.StructuredGraphBuilder(num_actions,
                                                                    feature_sizes,
                                                                    domain_sizes,
                                                                    embedding_dims,
                                                                    self._pg.hidden_layer_sizes,
                                                                    gate_gradients=True,
                                                                    arg_prefix=self._pg.arg_prefix,
                                                                    beam_size=self._pg.beam_size,
                                                                    max_steps=self._pg.max_steps)
                self._parser.AddEvaluation(self.task_context, self._pg.batch_size, corpus_name=self._pg.input_, evaluation_max_steps=self._pg.max_steps)
                self._parser.AddSaver(self._pg.slim_model)
                self._sess.run(self._parser.inits.values())
                self._parser.saver.restore(self._sess, self._pg.model_path)
  
    def parse(self, raw_bytes):
        if os.stat(self._pg.custom_file).st_size > self._pg.max_tmp_size:
            # Cleaning input file at each new call of parse
            with open(self._pg.custom_file, 'w') as f:
                pass

            # Reset offset inside tensorflow input file class
            self._parse_impl()

        with open(self._pg.custom_file, 'a') as f:
            f.write(raw_bytes)
            f.flush()

        self._parse_impl()

        return self._read_all_stream()

    def _parse_impl(self):
        with tf.variable_scope(self._pg.variable_scope):
            tf_eval_epochs, tf_eval_metrics, tf_documents = self._sess.run([
                self._parser.evaluation['epochs'],
                self._parser.evaluation['eval_metrics'],
                self._parser.evaluation['documents'],
            ])

            sink_documents = tf.placeholder(tf.string)
            sink = gen_parser_ops.document_sink(sink_documents,
                                                task_context=self.task_context,
                                                corpus_name='stdout-conll')

            self._sess.run(sink, feed_dict={sink_documents: tf_documents})

            sys.stdout.write('\n')
            sys.stdout.flush()

    def _read_all_stream(self):
        with open(self.stdout_file_path, 'r') as f:
            result = f.read()

        # Truncate file and put descriptor to 0
        os.ftruncate(sys.stdout.fileno(), 0)
        os.lseek(sys.stdout.fileno(), 0, 0)
        sys.stdout.flush()

        return result[:-1]

def configure_stdout(stdout_file_path):
    strm = open(stdout_file_path, 'w') # bypassing linux 64 kb pipe limit
    os.dup2(strm.fileno(), sys.stdout.fileno())

    return strm

