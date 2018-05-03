import numpy as np

class Update:

    def __init__(self, problem_file):

        self.actions_code = dict({'go':0, 'tidy up':1, 'bar':2, 'come_back':3})

        self.object_code = dict({'1':1, '2':2})

        self.problem_name = problem_file

    def select_robot_position(self, a, o):

        robot_position = None

        if a == 0 or a == 3:

            if o == 1:

                robot_position = '   (at r x6 y11)'

            elif o == 2:

                robot_position = '   (at r x6 y4)'

        if a == 1:

            robot_position = '   (at r x16 y16)'

        if a == 2:

            robot_position = '   (at r x23 y9)'

            
        return robot_position + '\n'

    def select_goal(self, a, o):

        goal = None

        if a == 0:

            if o == 1:

                goal = '  (:goal (at r x6 y11))'

            elif o == 2:

                goal = '  (:goal (at r x6 y4))'

        if a == 1:

            goal ='  (:goal (and (in gs1 cl) (in gs2 cl) (clean tc) (in tc tb) (at r x16 y16)))'

        if a == 2:

            cust = 'gs' + str(o)

            goal = '  (:goal (clear ' + cust +'))'

        if a == 3:

            cust = 'gs' + str(o)

            sit = ' s' + str(o)

            goal = '  (:goal (in ' + cust + sit+'))'

        return goal +'\n'

    def select_init(self, a, o):

        if a == 1:

            init_0 = '   (at r x16 y16)'
            init_1 = '   (in gs1 cl) (not (clear gs1)) (clean gs1)'
            init_2 = '   (in gs2 cl) (not (clear gs2)) (clean gs2)'
            init_3 = '   (in tc tb)'
            
            return init_0 +'\n',init_1 +'\n', init_2 +'\n', init_3 +'\n'

        if a == 2:

            init = '   (in gs' + str(o) + ' cl) (not(clear gs' + str(o) + ')) (clean gs' + str(o) + ')'

            return init +'\n'

        if a == 3:

            init = '   (in gs' + str(o) + ' s'+str(o)+') (not(clear gs' + str(o) + ')) (not(clean gs' + str(o) + ')) (not(clean tc))'

            return init +'\n'

    def writer_init(self, query):
        if len(query) == 1:

            a_code = self.actions_code[query[0]]
            o_code = None
            
            init_0, init_1, init_2, init_3 = self.select_init(a_code,o_code)

            f = open(self.problem_name, 'r')
            lines = f.readlines()
            lines[21] = init_0
            lines[22] = init_1
            lines[23] = init_2
            lines[24] = init_3
            f.close()

        else:
            a_code = self.actions_code[query[0]]
            o_code = self.object_code[query[1]]
            init = self.select_init(a_code,o_code)

            f = open(self.problem_name, 'r')
            lines = f.readlines()
            lines[21 + o_code] = init
            f.close()

        f = open(self.problem_name, 'w')
        f.writelines(lines)
        f.close()

    def take_robot_position(self):

        f = open(self.problem_name, 'r')
        lines = f.readlines()
        r_p =lines[21].split()[2:]
        f.close()
        x = int(r_p[0].replace('x',''))
        y = int(r_p[1].replace('y','').replace(')',''))

        return x, y

    def writer_robot_position(self, query):
        if len(query) == 1:

            a_code = self.actions_code[query[0]]

            o_code = None

            robot_position = self.select_robot_position(a_code, o_code)

            f = open(self.problem_name, 'r')
            lines = f.readlines()
            lines[21] = robot_position
            f.close()


        else:

            a_code = self.actions_code[query[0]]

            o_code = self.object_code[query[1]]

            robot_position = self.select_robot_position(a_code, o_code)

            f = open(self.problem_name, 'r')
            lines = f.readlines()
            lines[21] = robot_position
            f.close()

        f = open(self.problem_name, 'w')
        f.writelines(lines)
        f.close()


    def writer_goal(self, query):
        if len(query) == 1:

            a_code = self.actions_code[query[0]]

            o_code = None

            goal = self.select_goal(a_code, o_code)
        
            f = open(self.problem_name, 'r')
            lines = f.readlines()
            lines[131] = goal
            f.close()

        else:

            a_code = self.actions_code[query[0]]

            o_code = self.object_code[query[1]]

            goal = self.select_goal(a_code, o_code)

            f = open(self.problem_name, 'r')
            lines = f.readlines()
            lines[131] = goal
            f.close()
        
        f = open(self.problem_name, 'w')
        f.writelines(lines)
        f.close()
