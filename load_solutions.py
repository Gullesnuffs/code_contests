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
import sys
import random

import riegeli

import contest_problem_pb2


def _all_problems(filenames):
  """Iterates through all ContestProblems in filenames."""
  for filename in filenames:
    reader = riegeli.RecordReader(io.FileIO(filename, mode='rb'),)
    for problem in reader.read_messages(contest_problem_pb2.ContestProblem):
      yield problem

def escape(s: str):
    return s.replace('\\', '\\backslash').replace('\n', '\\n')

def _print_names_and_sources(filenames):
  solution_pairs = []
  """Prints the names and sources of all ContestProblems in filenames."""
  for problem in _all_problems(filenames):
    correct_solutions = []
    incorrect_solutions = []
    for solution in problem.solutions:
      if solution.language == contest_problem_pb2.ContestProblem.Solution.Language.PYTHON3:
        correct_solutions.append(solution.solution)
    for solution in problem.incorrect_solutions:
      if solution.language == contest_problem_pb2.ContestProblem.Solution.Language.PYTHON3:
        incorrect_solutions.append(solution.solution)
    for i in range(min(len(correct_solutions), len(incorrect_solutions))):
      solution_pairs.append((correct_solutions[i], incorrect_solutions[i]))
  random.shuffle(solution_pairs)
  with open("solution_pairs.txt", "w") as f:
    for (correct, incorrect) in solution_pairs:
      f.write(f"{escape(correct)}\n{escape(incorrect)}\n")
      print(f"{escape(correct)}\n{escape(incorrect)}")



if __name__ == '__main__':
  _print_names_and_sources(sys.argv[1:])
