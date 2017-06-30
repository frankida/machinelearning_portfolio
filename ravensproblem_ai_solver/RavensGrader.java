/**
 * DO NOT MODIFY THIS FILE.
 * 
 * Any modifications to this file will not be used when grading your project.
 * If you have any questions, please email the TAs.
 * 
 * This file grades the answers your agent submits.
 */

package ravensproject;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * The grader file. This will assign grades to the answers your agent
 * generates.
 */

public class RavensGrader {

    private static class Outcome{
        public int correct;
        public int incorrect;
        public int skipped;

        public Outcome(){
            this.correct = 0;
            this.incorrect = 0;
            this.skipped = 0;
        }

        public String add(int truth, int answer){
            if(truth == answer) {
                correct++;
                return "Correct";
            } else if(answer < 0) {
                skipped++;
                return "Skipped";
            } else {
                incorrect++;
                return "Incorrect";
            }
        }
    }

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

    public static void grade(){
        //Reading in answers
        HashMap<String, HashMap<String,Integer>> answers = new HashMap<String, HashMap<String,Integer>>();

        Scanner r = createScanner("AgentAnswers.csv");
        r.nextLine();                                                   // Skipping the header
        while(r.hasNext()) {                                            // Load each set in order.
            String line = r.nextLine();
            String[] row = line.split(",");
            if (!answers.containsKey(row[0]))
                answers.put(row[0], new HashMap<String, Integer>());    
            answers.get(row[0]).put(row[1], Integer.parseInt(row[2]));
        }

        // Writing out grades
        PrintWriter results = createPrintWriter("ProblemResults.csv");    // Results will be written to ProblemResults.txt.
        PrintWriter setResults = createPrintWriter("SetResults.csv");     // Note that each run of the program will overwrite the previous results.

        results.println("Problem,Agent's Answer,Correct?,Correct Answer");
        setResults.println("Set,Correct,Incorrect,Skipped");

        Scanner r0 = createScanner("Problems" + File.separator + "ProblemSetList.txt");        
        while(r0.hasNext()){
            String line0 = r0.nextLine();
            RavensGrader.Outcome outcome = new RavensGrader.Outcome();

            Scanner r1 = createScanner("Problems" + File.separator + 
                                        line0 + File.separator + 
                                       "ProblemList.txt");
            while(r1.hasNext()){
                String line1 = r1.nextLine();

                Scanner r2 = createScanner("Problems" + File.separator + 
                                             line0 + File.separator + 
                                             line1 + File.separator +
                                             "ProblemAnswer.txt");
                int truth = r2.nextInt();
                int ans = answers.get(line0).get(line1);
                results.println(line1 + "," + ans + "," + outcome.add(truth, ans) + "," +  truth);
            }

            setResults.println(line0 + "," + outcome.correct + "," + outcome.incorrect + "," + outcome.skipped);
        }

        results.close();
        setResults.close();
    }   

    /**
     * The main method of the project code.
     */
    public static void main(String[] args) {
        grade();
    }
}
