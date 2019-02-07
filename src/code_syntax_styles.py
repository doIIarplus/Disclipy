from html.parser import HTMLParser
from prompt_toolkit.styles import Style
from xml.sax.saxutils import escape

"""codehilite css
.codehilite .hll { background-color: #ffffcc }
// not converted
/.codehilite  { background: #f8f8f8; }
.codehilite .c { color: #408080; font-style: italic } /* Comment */
// uses background instead of border
/.codehilite .err { border: 1px solid #FF0000 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #BC7A00 } /* Comment.Preproc */
.codehilite .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.codehilite .c1 { color: #408080; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #408080; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #FF0000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #00A000 } /* Generic.Inserted */
.codehilite .go { color: #888888 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #0044DD } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #7D9029 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .no { color: #880000 } /* Name.Constant */
.codehilite .nd { color: #AA22FF } /* Name.Decorator */
.codehilite .ni { color: #999999; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #0000FF } /* Name.Function */
.codehilite .nl { color: #A0A000 } /* Name.Label */
.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mb { color: #666666 } /* Literal.Number.Bin */
.codehilite .mf { color: #666666 } /* Literal.Number.Float */
.codehilite .mh { color: #666666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666666 } /* Literal.Number.Oct */
.codehilite .sa { color: #BA2121 } /* Literal.String.Affix */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .dl { color: #BA2121 } /* Literal.String.Delimiter */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #BB6688 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #0000FF } /* Name.Function.Magic */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .vm { color: #19177C } /* Name.Variable.Magic */
.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */
"""

codehilite_style = Style.from_dict({
    "gr": '#FF0000',  # Generic.Error
    "cp": '#BC7A00',  # Comment.Preproc
    "c": '#408080 italic',  # Comment
    "ch": '#408080 italic',  # Comment.Hashbang
    "cm": '#408080 italic',  # Comment.Multiline
    "cpf": '#408080 italic',  # Comment.PreprocFile
    "c1": '#408080 italic',  # Comment.Single
    "cs": '#408080 italic',  # Comment.Special
    "gd": '#A00000',  # Generic.Deleted
    "gh": '#000080 bold',  # Generic.Heading
    "gp": '#000080 bold',  # Generic.Prompt
    "gi": '#00A000',  # Generic.Inserted
    "go": '#888888',  # Generic.Output
    "gu": '#800080 bold',  # Generic.Subheading
    "gt": '#0044DD',  # Generic.Traceback
    "kt": '#B00040',  # Keyword.Type
    "m": '#666666',  # Literal.Number
    "s": '#BA2121',  # Literal.String
    "na": '#7D9029',  # Name.Attribute
    "kp": '#008000',  # Keyword.Pseudo
    "nb": '#008000',  # Name.Builtin
    "sx": '#008000',  # Literal.String.Other
    "bp": '#008000',  # Name.Builtin.Pseudo
    "k": '#008000 bold',  # Keyword
    "kc": '#008000 bold',  # Keyword.Constant
    "kd": '#008000 bold',  # Keyword.Declaration
    "kn": '#008000 bold',  # Keyword.Namespace
    "kr": '#008000 bold',  # Keyword.Reserved
    "nt": '#008000 bold',  # Name.Tag
    "nc": '#0000FF bold',  # Name.Class
    "no": '#880000',  # Name.Constant
    "nd": '#AA22FF',  # Name.Decorator
    "ni": '#999999 bold',  # Name.Entity
    "ne": '#D2413A bold',  # Name.Exception
    "nf": '#0000FF',  # Name.Function
    "nl": '#A0A000',  # Name.Label
    "nn": '#0000FF bold',  # Name.Namespace
    "nv": '#19177C',  # Name.Variable
    "ow": '#AA22FF bold',  # Operator.Word
    "w": '#bbbbbb',  # Text.Whitespace
    "o": '#666666',  # Operator
    "mb": '#666666',  # Literal.Number.Bin
    "mf": '#666666',  # Literal.Number.Float
    "mh": '#666666',  # Literal.Number.Hex
    "mi": '#666666',  # Literal.Number.Integer
    "mo": '#666666',  # Literal.Number.Oct
    "il": '#666666',  # Literal.Number.Integer.Long
    "sa": '#BA2121',  # Literal.String.Affix
    "sb": '#BA2121',  # Literal.String.Backtick
    "sc": '#BA2121',  # Literal.String.Char
    "dl": '#BA2121',  # Literal.String.Delimiter
    "s2": '#BA2121',  # Literal.String.Double
    "sd": '#BA2121 italic',  # Literal.String.Doc
    "se": '#BB6622 bold',  # Literal.String.Escape
    "sh": '#BA2121',  # Literal.String.Heredoc
    "si": '#BB6688 bold',  # Literal.String.Interpol
    "sr": '#BB6688',  # Literal.String.Regex
    "s1": '#BA2121',  # Literal.String.Single
    "fm": '#0000FF',  # Name.Function.Magic
    "ss": '#19177C',  # Literal.String.Symbol
    "vc": '#19177C',  # Name.Variable.Class
    "vg": '#19177C',  # Name.Variable.Global
    "vi": '#19177C',  # Name.Variable.Instance
    "vm": '#19177C',  # Name.Variable.Magic
    "hll": 'bg:#ffffcc',
    "err": 'bg:#FF0000',  # Error
    "gs": 'bold',  # Generic.Strong
    "ge": 'italic'  # Generic.Emph
})


class HTML2PromptToolkitHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.prompt_toolkit_html = ''
        self.tags = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if 'class' in attributes:
            tag = attributes['class']

        self.tags.append(tag)
        self.prompt_toolkit_html += '<' + tag + '>'

    def handle_endtag(self, tag):
        self.prompt_toolkit_html += '</' + self.tags.pop() + '>'

    def handle_data(self, data):
        self.prompt_toolkit_html += escape(data)

    def __str__(self):
        return self.prompt_toolkit_html

    def __repr__(self):
        return self.prompt_toolkit_html


def HTML_2_prompt_toolkit_HTML(html):
    parser = HTML2PromptToolkitHTMLParser()
    parser.feed(html)
    return str(parser)


# run this module to check how the colors look
if __name__ == '__main__':
    from prompt_toolkit import print_formatted_text, HTML
    from markdown.extensions.codehilite import CodeHilite
    code_snippets = [
        CodeHilite('''#!/bin/bash

for OPT in "$@"
do
  case "$OPT" in
    '-f' )  canonicalize=1 ;;
    '-n' )  switchlf="-n" ;;
  esac
done

# readlink -f
function __readlink_f {
  target="$1"
  while test -n "$target"; do
    filepath="$target"
    cd `dirname "$filepath"`
    target=`readlink "$filepath"`
  done
  /bin/echo $switchlf `pwd -P`/`basename "$filepath"`
}

if [ ! "$canonicalize" ]; then
  readlink $switchlf "$@"
else
  for file in "$@"
  do
    case "$file" in
      -* )  ;;
      *  )  __readlink_f "$file" ;;
    esac
    done
fi

exit $?''', lang='bash').hilite(),
        CodeHilite('''extern size_t
pb_varint_scan(const uint8_t data[], size_t left) {
  assert(data && left);
  left = left > 10 ? 10 : left;

#ifdef __SSE2__

  /* Mapping: remaining bytes ==> bitmask */
  static const int mask_map[] = {
    0x0000, 0x0001, 0x0003, 0x0007,
    0x000F, 0x001F, 0x003F, 0x007F,
    0x00FF, 0x01FF, 0x03FF
  };

  /* Load buffer into 128-bit integer and create high-bit mask */
  __m128i temp = _mm_loadu_si128((const __m128i *)data);
  __m128i high = _mm_set1_epi8(0x80);

  /* Intersect and extract mask with high-bits set */
  int mask = _mm_movemask_epi8(_mm_and_si128(temp, high));
  mask = (mask & mask_map[left]) ^ mask_map[left];

  /* Count trailing zeroes */
  return mask ? __builtin_ctz(mask) + 1 : 0;

#else

  /* Linear scan */
  size_t size = 0;
  while (data[size++] & 0x80)
    if (!--left)
      return 0;
  return size;

#endif /* __SSE2__ */

}''', lang='c').hilite(),
        CodeHilite('''Extension::
Extension(const Descriptor *descriptor, const Descriptor *scope) :
    descriptor_(descriptor),
    scope_(scope) {

  /* Extract full name for signature */
  variables_["signature"] = descriptor_->full_name();

  /* Prepare message symbol */
  variables_["message"] = StringReplace(
    variables_["signature"], ".", "_", true);
  LowerString(&(variables_["message"]));

  /* Suffix scope to identifiers, if given */
  string suffix ("");
  if (scope_) {
    suffix = scope_->full_name();

    /* Check if the base and extension types are in the same package */
    if (!scope_->file()->package().compare(descriptor_->file()->package()))
      suffix = StripPrefixString(suffix,
        scope_->file()->package() + ".");

    /* Append to signature */
    variables_["signature"] += ".[" + suffix +"]";
    suffix = "_" + suffix;
  }

  /* Prepare extension symbol */
  variables_["extension"] = StringReplace(
    suffix, ".", "_", true);
  LowerString(&(variables_["extension"]));
}''', lang='c++').hilite(),
        CodeHilite('''(clojure-version)

(defn partition-when
  [f]
  (fn [rf]
    (let [a (java.util.ArrayList.)
          fval (volatile! false)]
      (fn
        ([] (rf))
        ([result]
           (let [result (if (.isEmpty a)
                          result
                          (let [v (vec (.toArray a))]
                            ;; Clear first
                            (.clear a)
                            (unreduced (rf result v))))]
             (rf result)))
        ([result input]
            (if-not (and (f input)  @fval)
               (do
                 (vreset! fval true)
                 (.add a input)
                 result)
               (let [v (vec (.toArray a))]
                 (.clear a)
                 (let [ret (rf result v)]
                   (when-not (reduced? ret)
                     (.add a input))
                   ret))))))))


(into [] (partition-when
          #(.startsWith % ">>"))
          ["1d" "33" ">> 1" ">> 2" "22" ">> 3"])''', lang='clojure').hilite(),
        CodeHilite('''Index: grunt.js
===================================================================
--- grunt.js    (revision 31200)
+++ grunt.js    (working copy)
@@ -12,6 +12,7 @@

 module.exports = function (grunt) {

+  console.log('hello world');
   // Project configuration.
   grunt.initConfig({
     lint: {
@@ -19,10 +20,6 @@
         'packages/services.web/{!(test)/**/,}*.js',
         'packages/error/**/*.js'
       ],
-      scripts: [
-        'grunt.js',
-        'db/**/*.js'
-      ],
       browser: [
         'packages/web/server.js',
         'packages/web/server/**/*.js',''', lang='diff').hilite(),
        CodeHilite('''FROM ubuntu

# Install vnc, xvfb in order to create a 'fake' display and firefox
RUN apt-get update && apt-get install -y x11vnc xvfb firefox
RUN mkdir ~/.vnc

# Setup a password
RUN x11vnc -storepasswd 1234 ~/.vnc/passwd

# Autostart firefox (might not be the best way, but it does the trick)
RUN bash -c 'echo "firefox" >> /.bashrc'

EXPOSE 5900
CMD ["x11vnc", "-forever", "-usepw", "-create"]''', lang='docker').hilite(),
        CodeHilite('''require Logger

def accept(port) do
  {:ok, socket} = :gen_tcp.listen(port,
                    [:binary, packet: :line, active: false, reuseaddr: true])
  Logger.info "Accepting connections on port #{port}"
  loop_acceptor(socket)
end

defp loop_acceptor(socket) do
  {:ok, client} = :gen_tcp.accept(socket)
  serve(client)
  loop_acceptor(socket)
end

defp serve(socket) do
  socket
  |> read_line()
  |> write_line(socket)

  serve(socket)
end

defp read_line(socket) do
  {:ok, data} = :gen_tcp.recv(socket, 0)
  data
end

defp write_line(line, socket) do
  :gen_tcp.send(socket, line)
end''', lang='elixir').hilite(),
        CodeHilite('''circular(Defs) ->
  [ { { Type, Base }, Fields } ||
    { { Type, Base }, Fields } <- Defs, Type == msg, circular(Base, Defs) ].

circular(Base, Defs) ->
  Fields = proplists:get_value({ msg, Base }, Defs),
  circular(Defs, Fields, [Base]).

circular(_Defs, [], _Path) ->
  false;
circular(Defs, [Field | Fields], Path) ->
  case Field#field.type of
    { msg, Type } ->
      case lists:member(Type, Path) of
        false ->
          Children = proplists:get_value({ msg, Type }, Defs),
          case circular(Defs, Children, [Type | Path]) of
            false -> circular(Defs, Fields, Path);
            true  -> true
          end;
        true ->
          Type == lists:last(Path) andalso
            (length(Path) == 1 orelse not is_tree(Path))
      end;
    _ ->
      circular(Defs, Fields, Path)
  end.''', lang='erlang').hilite(),
        CodeHilite('''package main

import "fmt"

func counter(id int, channel chan int, closer bool) {
  for i := 0; i < 10000000; i++ {
    fmt.Println("process", id," send", i)
    channel <- 1
  }
  if closer { close(channel ) }
}

func main() {
  channel := make(chan int)
  go counter(1, channel, false)
  go counter(2, channel, true)

  x := 0

  // receiving data from channel
  for i := range channel {
    fmt.Println("receiving")
    x += i
  }

  fmt.Println(x)
}''', lang='go').hilite(),
        CodeHilite('''<!doctype html>
<html class="no-js" lang="">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>HTML5 Boilerplate</title>
    <meta name="description" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <link rel="stylesheet" href="css/normalize.css">
    <link rel="stylesheet" href="css/main.css">
    <script src="js/vendor/modernizr-2.8.3.min.js"></script>
  </head>
  <body>
    <p>Hello world! This is HTML5 Boilerplate.</p>
  </body>
</html>''', lang='html').hilite(),
        CodeHilite('''import java.util.LinkedList;
import java.lang.reflect.Array;

public class UnsortedHashSet<E> {

  private static final double LOAD_FACTOR_LIMIT = 0.7;

  private int size;
  private LinkedList<E>[] con;

  public UnsortedHashSet() {
    con  = (LinkedList<E>[])(new LinkedList[10]);
  }

  public boolean add(E obj) {
    int oldSize = size;
    int index = Math.abs(obj.hashCode()) % con.length;
    if (con[index] == null)
      con[index] = new LinkedList<E>();
    if (!con[index].contains(obj)) {
      con[index].add(obj);
      size++;
    }
    if (1.0 * size / con.length > LOAD_FACTOR_LIMIT)
      resize();
    return oldSize != size;
  }

  private void resize() {
    UnsortedHashSet<E> temp = new UnsortedHashSet<E>();
    temp.con = (LinkedList<E>[])(new LinkedList[con.length * 2 + 1]);
    for (int i = 0; i < con.length; i++) {
      if (con[i] != null)
        for (E e : con[i])
          temp.add(e);
    }
    con = temp.con;
  }

  public int size() {
    return size;
  }
}''', lang='java').hilite(),
        CodeHilite('''var Math = require('lib/math');

var _extends = function (target) {
  for (var i = 1; i < arguments.length; i++) {
    var source = arguments[i];
    for (var key in source) {
      target[key] = source[key];
    }
  }

  return target;
};

var e = exports.e = 2.71828182846;
exports['default'] = function (x) {
  return Math.exp(x);
};

module.exports = _extends(exports['default'], exports);''', lang='javascript').hilite(),
        CodeHilite('''{
  "name": "mkdocs-material",
  "version": "0.2.4",
  "description": "A Material Design theme for MkDocs",
  "homepage": "http://squidfunk.github.io/mkdocs-material/",
  "authors": [
    "squidfunk <martin.donath@squidfunk.com>"
  ],
  "license": "MIT",
  "main": "Gulpfile.js",
  "scripts": {
    "start": "./node_modules/.bin/gulp watch --mkdocs",
    "build": "./node_modules/.bin/gulp build --production"
  }
  ...
}''', lang='json').hilite(),
        CodeHilite('''using MXNet

mlp = @mx.chain mx.Variable(:data)             =>
  mx.FullyConnected(name=:fc1, num_hidden=128) =>
  mx.Activation(name=:relu1, act_type=:relu)   =>
  mx.FullyConnected(name=:fc2, num_hidden=64)  =>
  mx.Activation(name=:relu2, act_type=:relu)   =>
  mx.FullyConnected(name=:fc3, num_hidden=10)  =>
  mx.SoftmaxOutput(name=:softmax)

# data provider
batch_size = 100
include(Pkg.dir("MXNet", "examples", "mnist", "mnist-data.jl"))
train_provider, eval_provider = get_mnist_providers(batch_size)

# setup model
model = mx.FeedForward(mlp, context=mx.cpu())

# optimization algorithm
optimizer = mx.SGD(lr=0.1, momentum=0.9)

# fit parameters
mx.fit(model, optimizer, train_provider, n_epoch=20, eval_data=eval_provider)''', lang='julia').hilite(),
        CodeHilite('''local ffi = require("ffi")

ffi.cdef[[
  void Sleep(int ms);
  int poll(struct pollfd *fds, unsigned long nfds, int timeout);
]]

local sleep
if ffi.os == "Windows" then
  function sleep(s)
    ffi.C.Sleep(s*1000)
  end
else
  function sleep(s)
    ffi.C.poll(nil, 0, s * 1000)
  end
end

for i = 1,160 do
  io.write("."); io.flush()
  sleep(0.01)
end
io.write("\n")''', lang='lua').hilite(),
        CodeHilite('''SELECT
  Employees.EmployeeID,
  Employees.Name,
  Employees.Salary,
  Manager.Name AS Manager
FROM
  Employees
LEFT JOIN
  Employees AS Manager
ON
  Employees.ManagerID = Manager.EmployeeID
WHERE
  Employees.EmployeeID = '087652';''', lang='mysql').hilite(),
        CodeHilite('''<?php

// src/AppBundle/Controller/LuckyController.php
namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Symfony\Component\HttpFoundation\Response;

class LuckyController {

  /**
   * @Route("/lucky/number")
   */
  public function numberAction() {
    $number = mt_rand(0, 100);

    return new Response(
      '<html><body>Lucky number: '.$number.'</body></html>'
    );
  }
}''', lang='php').hilite(),
        CodeHilite('''"""
  A very simple MNIST classifier.
  See extensive documentation at
  http://tensorflow.org/tutorials/mnist/beginners/index.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import data
from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('data_dir', '/tmp/data/', 'Directory for storing data')

mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

sess = tf.InteractiveSession()

# Create the model
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x, W) + b)''', lang='python').hilite(),
        CodeHilite('''require 'finity/event'
require 'finity/machine'
require 'finity/state'
require 'finity/transition'
require 'finity/version'

module Finity
  class InvalidCallback < StandardError; end
  class MissingCallback < StandardError; end
  class InvalidState    < StandardError; end

  # Class methods to be injected into the including class upon inclusion.
  module ClassMethods

    # Instantiate a new state machine for the including class by accepting a
    # block with state and event (and subsequent transition) definitions.
    def finity options = {}, &block
      @finity ||= Machine.new self, options, &block
    end

    # Return the names of all registered states.
    def states
      @finity.states.map { |name, _| name }
    end

    # Return the names of all registered events.
    def events
      @finity.events.map { |name, _| name }
    end
  end

  # Inject methods into the including class upon inclusion.
  def self.included base
    base.extend ClassMethods
  end
end''', lang='ruby').hilite(),
        CodeHilite('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mainTag SYSTEM "some.dtd" [ENTITY % entity]>
<?oxygen RNGSchema="some.rng" type="xml"?>
<xs:main-Tag xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <!-- This is a sample comment -->
  <childTag attribute="Quoted Value" another-attribute='Single quoted value'
      a-third-attribute='123'>
    <withTextContent>Some text content</withTextContent>
    <withEntityContent>Some text content with &lt;entities&gt; and
      mentioning uint8_t and int32_t</withEntityContent>
    <otherTag attribute='Single quoted Value'/>
  </childTag>
  <![CDATA[ some CData ]]>
</main-Tag>''', lang='xml').hilite()]
    code_snippets = [HTML_2_prompt_toolkit_HTML(c) for c in code_snippets]
    for c in code_snippets:
        print_formatted_text(HTML(c), style=codehilite_style)
    class_names = ''

    for cl in dict(codehilite_style.style_rules):
        class_names += '<%s>%s</%s> ' % ((cl,) * 3)

    print_formatted_text(HTML(class_names), style=codehilite_style)
