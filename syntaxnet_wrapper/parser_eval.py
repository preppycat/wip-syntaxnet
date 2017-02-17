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

from syntaxnet_wrapper import root_dir

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
import tempfile 

import tensorflow as tf

from tensorflow.python.platform import gfile
from tensorflow.python.platform import tf_logging as logging

from google.protobuf import text_format

print "HIHIHIHIH"
from syntaxnet import sentence_pb2
from syntaxnet.ops import gen_parser_ops
from syntaxnet import task_spec_pb2

print "HOHOHO"
from syntaxnet import graph_builder
from syntaxnet import structured_graph_builder

def RewriteContext(task_context):
  context = task_spec_pb2.TaskSpec()
  with gfile.FastGFile(task_context) as fin:
    text_format.Merge(fin.read(), context)
  for resource in context.input:
    for part in resource.part:
      if part.file_pattern != '-':
        part.file_pattern = os.path.join(FLAGS.resource_dir, part.file_pattern)
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
        max_temp_size=262144000 # Maximum size of temp input file
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
        self.max_temp_size = max_temp_size

class SyntaxNetProcess:

    def __init__(self, processconfig):
        self._sess = tf.Session()
        self._pg = processconfig
        self.stdout_file_path = os.path.join(os.path.dirname(self._pg.custom_file), 'stdout.tmp') # File where syntaxnet output will be written

        """Builds and evaluates a network."""
        self.task_context = self._pg.task_context
        if self._pg.resource_dir:
            task_context = RewriteContext(self.task_context)
        
        with tf.variable_scope(self.cfg_.variable_scope):
            feature_sizes, domain_sizes, embedding_dims, num_actions = sess.run(
                gen_parser_ops.feature_size(task_context=self.task_context, arg_prefix=self._pg.arg_prefix))

        if self._pg.graph_builder_ == 'greedy':
            parser = graph_builder.GreedyParser(num_actions,
                                        feature_sizes,
                                        domain_sizes,
                                        embedding_dims,
                                        self._pg.hidden_layer_sizes,
                                        gate_gradients=True,
                                        arg_prefix=self._pg.arg_prefix)
        else:
            parser = structured_graph_builder.StructuredGraphBuilder(num_actions,
                                                                feature_sizes,
                                                                domain_sizes,
                                                                embedding_dims,
                                                                self._pg.hidden_layer_sizes,
                                                                gate_gradients=True,
                                                                arg_prefix=self._pg.arg_prefix,
                                                                beam_size=self._pg.beam_size,
                                                                max_steps=self._pg.max_steps)
            parser.AddEvaluation(self.task_context, self._pg.batch_size, corpus_name=self._pg.input_, evaluation_max_steps=self._pg.max_steps)
            parser.AddSaver(self._pg.slim_model)
            sess.run(parser.inits.values())
            parser.saver.restore(sess, self._pg.model_path)

  
    def parse(self, raw_bytes):
        if os.stat(self.cfg_.custom_file_path).st_size > self.cfg_.max_tmp_size:
            # Cleaning input file at each new call of parse
            with open(self._pg.custom_file, 'w') as f:
                pass

        # Reset offset inside tensorflow input file class
        self._parse_impl()

        with open(self.cfg_.custom_file, 'a') as f:
            f.write(raw_bytes)
            f.flush()

        self._parse_impl()

        return self._read_all_stream()

    def _parse_impl(self):
        with tf.variable_scope(self.cfg_.variable_scope):
            tf_eval_epochs, tf_eval_metrics, tf_documents = sess.run([
                parser.evaluation['epochs'],
                parser.evaluation['eval_metrics'],
                parser.evaluation['documents'],
            ])

        sink_documents = tf.placeholder(tf.string)
        sink = gen_parser_ops.document_sink(sink_documents,
                                            task_context=self.task_context_,
                                            corpus_name='stdout-conll')

        self.sess_.run(sink, feed_dict={sink_documents: tf_documents})

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

