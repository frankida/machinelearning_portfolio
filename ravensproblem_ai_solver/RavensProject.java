/**
 * DO NOT MODIFY THIS FILE.
 * 
 * When you submit your project, an alternate version of this file will be used
 * to test your code against the sample Raven's problems in this zip file, as
 * well as other problems from the Raven's Test and former students.
 * 
 * Any modifications to this file will not be used when grading your project.
 * If you have any questions, please email the TAs.
 * 
 */

package ravensproject;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * The main driver file for the project. You may edit this file while debugging
 * and designing, but you should not depend on changes to this file for final
 * execution of your project. Your project will be graded using our own version
 * of this file. * 
 */

public class RavensProject {

    private static Scanner createScanner(String filename){
        Scanner r = null;

        try {
            r = new Scanner(new File(filename));
        } catch(Exception ex){
            System.out.println(ex);
        }

        return r;
    }

    private static PrintWriter createPrintWriter(String filename){
        PrintWriter p = null;

        try {
            p = new PrintWriter(new File(filename));
        } catch(Exception ex){
            System.out.println(ex);
        }

        return p;
    }

    /**
    * The project's main solve method. This will generate your agent's answers
    * to all the current problems.
    *
    * You do not need to use this method.
    */
    public static void solve(){
        PrintWriter answers = createPrintWriter("AgentAnswers.csv");    // Results will be written to ProblemResults.txt.
        answers.println("ProblemSet,RavensProblem,Agent's Answer");

        //Loading problems from files
        ArrayList<ProblemSet> sets = new ArrayList<ProblemSet>();       // The variable 'sets' stores multiple problem sets.
                                                                        // Each problem set comes from a different folder in /Problems/
                                                                        // Additional sets of problems will be used when grading projects.
                                                                        // You may also write your own problems.

        // Load each set in order.
        Scanner r = createScanner("Problems" + File.separator + "ProblemSetList.txt");        
        while(r.hasNext()) {                                            
            String line = r.nextLine();
            sets.add(new ProblemSet(line));
        }

        Agent agent = new Agent();

        for(ProblemSet set : sets) {
            for(RavensProblem problem : set.getProblems()) {            // Your agent will solve one problem at a time.
                int answer = agent.Solve(problem);                     // The problem will be passed to your agent as a RavensProblem object as a parameter to the Solve method
                answers.println(set.getName() + "," + problem.getName() + "," + answer);
            }
        }

        r.close();
        answers.close();
    }

    /**
     * The main method of the project code. This will have your agent generate
     * answers for all the problems, then generate grades for them.
     */
    public static void main(String[] args) {
        solve();
        RavensGrader.grade();
    }
}
