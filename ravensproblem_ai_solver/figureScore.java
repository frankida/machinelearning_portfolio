package ravensproject;

import ravensproject.Model.imageDB;

import java.util.*;

public class figureScore {

    HashMap<String, Double> scoreBoard = new HashMap<>();

    public static Double ratiocomparetoPoints(double answer, double compare) {
        double comparison = answer / compare;
        /** if ((comparison > .99 && comparison < 1.01)) {
         return 100.0;
         } else **/if ((comparison > .95) && (comparison < (1.05))) {
            return 95.0;
        } else if ((comparison > .90) && (comparison < (1.10))) {
            return 90.0;
        } else if ((comparison > .85) && (comparison < (1.15))) {
            return 80.0;
        } else {
            if ((comparison > .80) && (comparison < (1.20))) {
                return 75.0;
            } else {
                return 0.0;
            }
        }
    }

    public void increaseScore(String name, Double score) {
        scoreBoard.merge(name, score, Double::sum);
    }

    public Boolean onetrueKing() {
        List<Double> scores = new ArrayList<Double>();
        for (Double s1 : scoreBoard.values()) {
            scores.add(s1);
        }
        scores.sort(Comparator.reverseOrder());
        Double test = 0.0;
        for (Double score : scores) {
            if (test == 0.0) {
                test = score;
            } else if (isSame(test, score, .05)) {  //previous .02
//            else if ((test <= score+10) || (test >= score-10)) {
                return false;
            } else {
                return true;
            }
        }
        return true;
    }

    public static boolean isSame(double ratioOne, double ratioDeuce, double acceptanceinterval) {
        // We can calibrate the acceptance interval between .05 to .10
        // Current optimal is .02 in order to make is true king works..
//        double acceptanceinterval = .02;
        boolean comparison = ratioOne / ratioDeuce > (1 - acceptanceinterval) && (ratioOne / ratioDeuce < (1 + acceptanceinterval));
        return comparison;
    }

    public Integer topScore() {
        Double compare = 0.0;
        String topscore = "-1";
        for (String s : scoreBoard.keySet()) {
            if (scoreBoard.get(s) > compare) {
                compare = scoreBoard.get(s);
                topscore = s;
            }
        }
        return Integer.parseInt(topscore);
    }

    public void dropScore(String answername) {
        scoreBoard.remove(answername);
    }

    public void dropcopyAnswers(RavensProblem problem, HashMap<String, int[][]> imageArrayHashmap) {
        HashMap<String, Double> similarRatiosmap = new HashMap<>();
        String[] figures3x3 = {"A", "B", "C", "D", "E", "F", "G", "H"};
        double topSimilar = 0;
        int Answer = -1;
        if (problem.getProblemType().equals("3x3")) {
            for (String s : figures3x3) {
                for (int i = 1; i < figures3x3.length + 1; i++) {
                    double similarRatio = imageDB.imageSimilarity(imageArrayHashmap.get(s), imageArrayHashmap.get(Integer.toString(i)));
//                    System.out.println("comparing " + s + " to " + i + " ratio is " + similarRatio);
                    similarRatiosmap.put(Integer.toString(i), similarRatio);
                    if (similarRatio >= .95) {  //if similarity is greater that 95% drop the answer from scoreboard
                        dropScore(Integer.toString(i));
//                        System.out.println("dropped " + i);
                    }
                }
            }
        }
    }
}
