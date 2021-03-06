"""Example of two water jugs problem for use with AIMA code"""

#! /usr/bin/python
"""
  Stubt for code to solve the jealous husbands problem for use with
  AIMA code.  AKSHAY PESHAVE, peshave1@UMBC.EDU
"""
from search import *

class JH(Problem):

    """
    Three missionaries and three cannibals are on the left bank of a river. A boat is
    available which will hold two people, and which can be navigated by any combination
    of missionaries and cannibals involving one or two people. If the missionaries on
    either bank of the river are outnumbered at any time by cannibals, the cannibals
    will indulge in their anthropophagic tendencies and do away with the missionaries
    who are outnumbered. Find a schedule of crossings that will permit all the missionaries
    and cannibals to cross the river from the left bank to the right bank safely.
    """

    '''
        the state is represented by an array of three-tuples
        ((W1, W2, W3), (H1, H2, H3), (BW1, BW2, BW3),(BH1, BH2, BH3))  =>W=wife, H=husband, B=boat
        The first two tuples represent the state of the left bank.
        The last two tuples represent the state of the boat.
        
        Each literal will assume the value 0 (absence from left bank/presence on right bank) or
        1 (presence on left bank/absence on rightbank)

        the initial state is when all husband-wife pairs are on the left bank and boat is empty.
                ((1,1,1),(1,1,1),(0,0,0),(0,0,0))

        the final state is when all wife-husband pairs are absent from the left bank and boat is empty.
                ((0,0,0),(0,0,0),(0,0,0),(0,0,0))
    '''

    def __init__(self, intial=((1,1,1),(1,1,1),(0,0,0),(0,0,0)), goal=((0,0,0),(0,0,0),(0,0,0),(0,0,0))):
        self.initial = intial
        self.goal = goal
        self.boat_location = 'L'
        self.step=0;

    def __repr__(self):
        """returns a string representing the object"""
        return "WJ(%s,%s)" % (self.initial, self.goal)

    def goal_test(self, state):
        """returns true if state is a goal state"""
        
        return (state[0][0]==0 and state[0][1]==0 and state[0][2]==0 and state[1][0]==0
                and state[1][1]==0 and state[1][2]==0 and state[2][0]==0 and state[2][1]==0 and state[2][2]==0
                and state[3][0]==0 and state[3][1]==0 and state[3][2]==0)
        

    def successor(self, ((W1, W2, W3), (H1, H2, H3), (BW1, BW2, BW3),(BH1, BH2, BH3))):
        """returns a list of successors to state"""
        successors = []
        
        self.step=self.step+1
        if self.boat_location=='L':
            '''
                boat has reached left bank and is departing towards right bank
            '''
            self.boat_location='R'
            
            if (H1+H2+H3)==3:
                if (W1+W2+W3)>1:
                    
                    #print "%s stepped into L1" % (self.step)
                    #print "(%s,%s,%s,%s,%s,%s)" % (LM,LH,RM,RH,BM,BH)

                    if W1==W2:
                        successors.append(('load the boat with wife 1 and wife 2 ->',((0, 0, W3), (H1, H2, H3), (1, 1 ,0), (0, 0, 0))))
                    elif W1==W3:
                        successors.append(('load the boat with wife 1 and wife 3 ->',((0, W2, 0), (H1, H2, H3), (1, 0 ,1), (0, 0, 0))))
                    else: #elif W2==W3:
                        successors.append(('load the boat with wife 2 and wife 3 ->',((W1, 0, 0), (H1, H2, H3), (0, 1 ,1), (0, 0, 0))))
                elif (W1+W2+W3)==1:
                    if W1==1:
                        successors.append(('load the boat with husband 2 and husband 3 ->',((W1, W2, W3), (H1, 0, 0), (0, 0 ,0), (0, 1, 1))))
                    elif W2==1:
                        successors.append(('load the boat with husband 1 and husband 3 ->',((W1, W2, W3), (0, H2, 0), (0, 0 ,0), (1, 0, 1))))
                    else:#elif W3==1:
                        successors.append(('load the boat with husband 1 and husband 2 ->',((W1, W2, W3), (0, 0, H3), (0, 0 ,0), (1, 1, 0))))
            elif (H1+H2+H3)==0:
                if W1==1 and W2==1:
                    successors.append(('load the boat with wife 1 and wife 2 ->',((0, 0, W3), (H1, H2, H3), (1, 1 ,0), (0, 0, 0))))
                elif W1==1 and W3==1:
                    successors.append(('load the boat with wife 1 and wife 3 ->',((0, W2, 0), (H1, H2, H3), (1, 0 ,1), (0, 0, 0))))
                else:#elif W2==1 and W3==1:
                    successors.append(('load the boat with wife 2 and wife 3 ->',((W1, 0, 0), (H1, H2, H3), (0, 1 ,1), (0, 0, 0))))
            elif ((W1+H1)==0):
                successors.append(('load the boat with husband 2 and husband 3 ->',((W1, W2, W3), (H1, 0, 0), (0, 0 ,0), (0, 1, 1))))
            elif ((W2+H2)==0):
               successors.append(('load the boat with husband 1 and husband 3 ->',((W1, W2, W3), (0, H2, 0), (0, 0 ,0), (1, 0, 1))))
            else:#elif ((W3+H3)==0):
                successors.append(('load the boat with husband 1 and husband 2 ->',((W1, W2, W3), (0, 0, H3), (0, 0 ,0), (1, 1, 0))))
        else:
            '''
                boat has reached right bank
            '''
            self.boat_location='L'

            if (H1+H2+H3)==0:
                if (W1+W2+W3)==0 :
                    #goal state
                    successors.append(('all done',((0,0,0),(0,0,0),(0,0,0),(0,0,0))))
                else: #if (W1+W2+W3)> 0 :
                    if W1==0:
                        successors.append(('<- load the boat with wife 1',((1, W2, W3), (H1, H2, H3), (1, 0 ,0), (0, 0,0))))
                    elif W2==0:
                        successors.append(('<- load the boat with wife 2',((W1,1, W3), (H1, H2, H3), (0, 1 ,0), (0,0,0))))
                    else:#elif W3==0:
                        successors.append(('<- load the boat with wife 3',((W1, W2, 1), (H1, H2, H3), (0, 0 ,1), (0,0,0))))
            elif (H1+H2+H3)==3:
                if W1==0:
                    successors.append(('<- load the boat with wife 1',((1, W2, W3), (H1, H2, H3), (1, 0 ,0), (0, 0,0))))
                elif W2==0:
                    successors.append(('<- load the boat with wife 2',((W1,1, W3), (H1, H2, H3), (0, 1 ,0), (0,0,0))))
                else:#elif W3==0:
                    successors.append(('<- load the boat with wife 3',((W1, W2, 1), (H1, H2, H3), (0, 0 ,1), (0,0,0))))
            
            else:#elif (W1+W2+W3)==1 and (H1+H2+H3)==1:
                if (W1==0 and H1==0):
                    successors.append(('<- load the boat with husband 1 and wife 1',((1, W2, W3), (1, H2, H3), (1, 0 ,0), (1,0,0))))
                elif (W2==0 and H2==0):
                    successors.append(('<- load the boat with husband 2 and wife 2',((W1, 1, W3), (H1, 1, H3), (0, 1 ,0), (0,1,0))))
                else:#elif (W3==0 and H3==0):
                    successors.append(('<- load the boat with husband 3 and wife 3',((W1, W2, 1), (H1, H2, 1), (0, 0 ,1), (0,0,1))))          
        
        return successors

def main():
    '''
    searchers = [breadth_first_tree_search, breadth_first_graph_search, depth_first_graph_search,
                 iterative_deepening_search, depth_limited_search]
    #searchers = [depth_first_graph_search]
    problems = [JH(((1,1,1),(1,1,1),(0,0,0),(0,0,0)),((0,0,0),(0,0,0),(0,0,0),(0,0,0)))]
    for p in problems:
        for s in searchers:
            print "Solution to %s found by %s" % (p, s.__name__)
            path = s(p).path()
            path.reverse()
            print path
            print
    print "SUMMARY: successors/goal tests/states generated/solution"
    compare_searchers(problems=problems,
                      header=['SEARCHER', 'GOAL:((0,0,0),(0,0,0),(0,0,0),(0,0,0))'],
                      searchers=[breadth_first_tree_search,
                                 breadth_first_graph_search, depth_first_graph_search,
                                 iterative_deepening_search, depth_limited_search])
                      #searchers = [depth_first_graph_search])
    '''

    searchers = [breadth_first_graph_search, depth_first_graph_search,\
                 iterative_deepening_search, depth_limited_search]

    for s in searchers:
        ip = InstrumentedProblem(JH())
        solution = s(ip)
        if solution:
            path = solution.path()
            path.reverse()
            print '\n%s finds a solution of length %s that' % (s.__name__, len(path))
            print '  Expanded %s states' % ip.succs
            print '  Called the goal test %s times' % ip.goal_tests
            print '  Added %s states to the graph' % ip.goal_tests
            print '  The actions on the solution path are: START',
            for node in path[1:]:
                print '=>', node.action,
            print '=> DONE \n '
        else:
            print '%s did not find a solution' % s.__name__


# if called from the command line, call main()
if __name__ == "__main__":
    main()
