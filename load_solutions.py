# Copyright 2022 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A simple tool to iterate through the dataset, printing the name and source.

Example usage:

  print_names_and_sources /path/to/dataset/code_contests_train*
"""

import io
import os
import sys
import random

import riegeli
import json

import contest_problem_pb2


def _all_problems(filenames):
  """Iterates through all ContestProblems in filenames."""
  for filename in filenames:
    reader = riegeli.RecordReader(io.FileIO(filename, mode='rb'),)
    for problem in reader.read_messages(contest_problem_pb2.ContestProblem):
      yield problem

def escape(s: str):
    return s.replace('\\', '\\backslash').replace('\n', '\\n')

def get_language(solution):
  if solution.language == contest_problem_pb2.ContestProblem.Solution.Language.PYTHON3:
    return "Python3"
  if solution.language == contest_problem_pb2.ContestProblem.Solution.Language.CPP:
    return "Cpp"
  return None

def _print_names_and_sources(output_directory: str, filenames):
  output_filenames = set()
  for problem in _all_problems(filenames):
    correct_solutions = []
    incorrect_solutions = []
    for solution in problem.solutions:
      language = get_language(solution)
      if language is not None:
        correct_solutions.append({'solution': solution.solution, 'language': language})
    for solution in problem.incorrect_solutions:
      language = get_language(solution)
      if language is not None:
        incorrect_solutions.append({'solution': solution.solution, 'language': language})
    problem_json = json.dumps({
      'correct': correct_solutions,
      'incorrect': incorrect_solutions,
      'name': problem.name
    })
    filename = ""
    for c in problem.name:
      if c == ' ' or c == '_' or c == '-':
        filename += '_'
      elif c.isalnum():
        filename += c
    while filename in output_filenames:
      filename += " (2)"
    output_filenames.add(filename)
    with open(f"{output_directory}/{filename}.json", "w") as f:
      f.write(problem_json)


if __name__ == '__main__':
  output_directory = sys.argv[1]
  if not os.path.exists(output_directory):
    os.makedirs(output_directory)
  _print_names_and_sources(output_directory, sys.argv[2:])
