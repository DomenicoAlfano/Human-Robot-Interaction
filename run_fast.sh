#!/bin/bash
../full_project/downward/./fast-downward.py ../full_project/downward/domain.pddl ../full_project/downward/problem.pddl --search "lazy_greedy([ff()], preferred=[ff()])" > out.txt
rm -r output.sas
rm -r out.txt