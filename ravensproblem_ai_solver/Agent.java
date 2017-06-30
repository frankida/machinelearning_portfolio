package ravensproject;

import ravensproject.Model.imageDB;
import ravensproject.Model.problemtypes;

import java.util.HashMap;

public class Agent {
    /**
     * The default constructor for your Agent. Make sure to execute any
     * processing necessary before your Agent starts solving problems here.
     * <p>
     * Do not add any variables to this signature; they will not be used by
     * main().
     */
    public Agent() {
    }

    /**
     * The primary method for solving incoming Raven's Progressive Matrices.
     * For each problem, your Agent's Solve() method will be called. At the
     * conclusion of Solve(), your Agent should return an int representing its
     * answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
     * are also the Names of the individual RavensFigures, obtained through
     * RavensFigure.getName(). Return a negative number to skip a problem.
     * <p>
     * Make sure to return your answer *as an integer* at the end of Solve().
     * Returning your answer as a string may cause your program to crash.
     *
     * @param problem the RavensProblem your agent should solve
     * @return your Agent's answer to this problem
     */
    public int Solve(RavensProblem problem) {
        figureScore scorer = new figureScore();  //initialize scorer that holds points for answer figures
        imageDB imageArrayDB = new imageDB();
        HashMap<String, int[][]> imageArrayHashmap = imageDB.loadImages(problem);  //all the images loaded once
        HashMap<String, int[][]> insideArrayHP = imageDB.converttoInside(imageArrayHashmap);  //inside images hashmap
        HashMap<String, int[][]> outsideArrayHP = imageDB.converttoOutside(imageArrayHashmap);  //outside images hashmap

        HashMap<String, Double> darkPixelhashmap = imageDB.load_darkpixel_Hashmap(problem);  //all the dark pixel ratios loaded once
        if (problem.getProblemType().equals("2x2")) {
            //top row execution - all shape are same
            if (isReflection("A", "B", "Horz", problem, imageArrayHashmap)) {
                System.out.println("** " + problem.getName() + " is a horizonal reflection problem");
                int[][] compare = imageArrayDB.horizontalFlipimage(imageArrayHashmap.get("C"));
                similarProcesswithimagearray(compare, scorer, problem, imageArrayHashmap);
                return scorer.topScore();
            } else if (isReflection("A", "C", "Vert", problem, imageArrayHashmap)) {
                System.out.println("** " + problem.getName() + " is a vertical reflection problem");
                int[][] compare = imageArrayDB.verticalFlipimage((imageArrayHashmap.get("B")));
                similarProcesswithimagearray(compare, scorer, problem, imageArrayHashmap);
                return scorer.topScore();
            } else if ((imageDB.imageSimilarity(imageArrayHashmap.get("A"), imageArrayHashmap.get("C")) > .70)) {
                System.out.println("** " + problem.getName() + " is similar then dark pixel");
                double compareRatio = (darkPixelhashmap.get("C") - darkPixelhashmap.get("A"));
                compareRatiotoAnswerDarkpixscorer(scorer, darkPixelhashmap.get("B") + compareRatio, darkPixelhashmap, problem);
                return scorer.topScore();
            } else if ((imageDB.imageSimilarity(imageArrayHashmap.get("A"), imageArrayHashmap.get("B")) > .70)) {
                System.out.println("** " + problem.getName() + " is similar then dark pixel for b11");
                double compareRatio = (darkPixelhashmap.get("A") - darkPixelhashmap.get("B"));
                compareRatiotoAnswerDarkpixscorer(scorer, darkPixelhashmap.get("C") - compareRatio, darkPixelhashmap, problem);
                return scorer.topScore();
            }
            return -1;

            //execute 3x3 code
        } else if (problem.getProblemType().equals("3x3")  /**&& problem.getName().equals("Basic Problem D-10") **/) {
            //Code for Problem Set C
            //top row execution - all shape are same
            if (problemtypes.isSame(darkPixelhashmap)) {
                System.out.println("** " + problem.getName() + " is same");
                compareRatiotoAnswerDarkpixscorer(scorer, darkPixelhashmap.get("H"), darkPixelhashmap, problem);
                similarProcesswithimagearray(imageArrayHashmap.get("H"), scorer, problem, imageArrayHashmap);
                if (!scorer.onetrueKing()) {
                    reflectionScorer("G", "Horz", problem, scorer, imageArrayHashmap); //checks for "Horz" or "Vert" reflection}
                    return scorer.topScore();
                }
                return scorer.topScore();
                //images dark pixels are getting bigger
            } else if (problemtypes.isBigger(darkPixelhashmap)) {
                System.out.println("** " + problem.getName() + " is a getting bigger problem");
                double compareRatio = (darkPixelhashmap.get("H") - darkPixelhashmap.get("G"));
                compareRatiotoAnswerDarkpixscorer(scorer, darkPixelhashmap.get("H") + compareRatio, darkPixelhashmap, problem);
                // adding D to F, G to answer comparison
                double compareRatio2 = (darkPixelhashmap.get("F") - darkPixelhashmap.get("D"));
                compareRatiotoAnswerDarkpixscorer(scorer, darkPixelhashmap.get("G") + compareRatio2, darkPixelhashmap, problem);
                if (!scorer.onetrueKing()) {
                    similarProcess("H", scorer, problem, imageArrayHashmap);
                    similarProcess("F", scorer, problem, imageArrayHashmap);
                }
                return scorer.topScore();
            }
            //images dark pixels are getting smaller
            else if (problemtypes.isSmaller(darkPixelhashmap)) {
                System.out.println("** " + problem.getName() + " is a getting smaller problem");
                double compareRatio = (darkPixelhashmap.get("G") - darkPixelhashmap.get("H"));
                compareRatiotoAnswerDarkpixscorer(scorer, darkPixelhashmap.get("H") - compareRatio, darkPixelhashmap, problem);
                return scorer.topScore();
// code for problem set D
            } else if (problemtypes.isAddition(darkPixelhashmap)) {
                System.out.println("** " + problem.getName() + " is image addition problem");
                double compareRatio = (darkPixelhashmap.get("G") + darkPixelhashmap.get("H"));
                compareRatiotoAnswerDarkpixscorer(scorer, compareRatio, darkPixelhashmap, problem);
                scorer.dropcopyAnswers(problem, imageArrayHashmap);
                return scorer.topScore();
            } else if (problemtypes.isSubtraction(darkPixelhashmap)) {
                System.out.println("** " + problem.getName() + " is image subtraction problem");
                double compareRatio = (darkPixelhashmap.get("G") - darkPixelhashmap.get("H"));
                compareRatiotoAnswerDarkpixscorer(scorer, compareRatio, darkPixelhashmap, problem);
                scorer.dropcopyAnswers(problem, imageArrayHashmap);
                return scorer.topScore();
            } else if (problemtypes.isXOR(imageArrayHashmap)) {  //code for XOR of images
                System.out.println("** " + problem.getName() + " is image XOR problem");
                int[][] xorarray = imageDB.xortwoimageArray(imageArrayHashmap.get("G"), imageArrayHashmap.get("H"));
                similarProcesswithimagearray(xorarray, scorer, problem, imageArrayHashmap);
                return scorer.topScore();
            } else if (problemtypes.isAND(imageArrayHashmap)) {  //code for AND of images
                System.out.println("** " + problem.getName() + " is image AND problem");
                int[][] andarray = imageDB.andtwoimageArray(imageArrayHashmap.get("G"), imageArrayHashmap.get("H"));
                similarProcesswithimagearray(andarray, scorer, problem, imageArrayHashmap);
                return scorer.topScore();
            } else if (problemtypes.isSameDiagonal(imageArrayHashmap, darkPixelhashmap)) {
                System.out.println("** " + problem.getName() + " is image Diagonal same problem");
                similarProcesswithimagearray(imageArrayHashmap.get("E"), scorer, problem, imageArrayHashmap);
                return scorer.topScore();
            } else if ((imageDB.imageSimilarity(insideArrayHP.get("A"), insideArrayHP.get("C")) > .90)
            /**&&(imageDB.imageSimilarity(insideArrayHP.get("A"), insideArrayHP.get("B")) > .90)**/) {
                System.out.println("** " + problem.getName() + " is image inside row problem");
                similarProcesswithimagearray(insideArrayHP.get("G"), scorer, problem, insideArrayHP);
                outsidefigureScorer(problem, scorer, outsideArrayHP);
                scorer.dropcopyAnswers(problem, imageArrayHashmap);
                return scorer.topScore();
            } else if ((imageDB.imageSimilarity(insideArrayHP.get("A"), insideArrayHP.get("G")) > .85)) {
                System.out.println("** " + problem.getName() + " is image inside column problem");
                similarProcesswithimagearray(insideArrayHP.get("C"), scorer, problem, insideArrayHP);
                outsidefigureScorer(problem, scorer, outsideArrayHP);
                return scorer.topScore();
            } else if ((imageDB.imageSimilarity(insideArrayHP.get("A"), insideArrayHP.get("E")) > .85)) {
                System.out.println("** " + problem.getName() + " is image inside diagonal problem");
                similarProcesswithimagearray(insideArrayHP.get("E"), scorer, problem, insideArrayHP);
                outsidefigureScorer(problem, scorer, outsideArrayHP);
                scorer.dropcopyAnswers(problem, imageArrayHashmap);
                return scorer.topScore();
            } else if ((imageDB.imageSimilarity(insideArrayHP.get("C"), insideArrayHP.get("G")) > .90)) {/// changed from .85
                System.out.println("** " + problem.getName() + " is image inside diagonal reverse problem");
                similarProcesswithimagearray(insideArrayHP.get("D"), scorer, problem, insideArrayHP);
                outsidefigureScorer(problem, scorer, outsideArrayHP);
                return scorer.topScore();
            } else {
                System.out.println("** " + problem.getName() + " Problem didn't fit a category**");
                return -1;
            }
        }
        return -1;
    }


    private void outsidefigureScorer(RavensProblem problem, figureScore scorer, HashMap<String, int[][]> outsideArrayHP) {
        if ((imageDB.imageSimilarity(outsideArrayHP.get("A"), outsideArrayHP.get("C")) > .85)) {
            System.out.println("** " + problem.getName() + " is image outside row problem");
            similarProcesswithimagearray(outsideArrayHP.get("G"), scorer, problem, outsideArrayHP);
        } else if ((imageDB.imageSimilarity(outsideArrayHP.get("A"), outsideArrayHP.get("G")) > .85)) {
            System.out.println("** " + problem.getName() + " is image outside column problem");
            similarProcesswithimagearray(outsideArrayHP.get("C"), scorer, problem, outsideArrayHP);
        } else if ((imageDB.imageSimilarity(outsideArrayHP.get("A"), outsideArrayHP.get("E")) > .85)) {
            System.out.println("** " + problem.getName() + " is image outside diagonal problem");
            similarProcesswithimagearray(outsideArrayHP.get("A"), scorer, problem, outsideArrayHP);
        } else if ((imageDB.imageSimilarity(outsideArrayHP.get("C"), outsideArrayHP.get("G")) > .85)) {
            System.out.println("** " + problem.getName() + " is image outside reverse diagonal problem");
            similarProcesswithimagearray(outsideArrayHP.get("B"), scorer, problem, outsideArrayHP);
        }
    }

    private void compareRatiotoAnswerDarkpixscorer(figureScore scorer, double compareRatio, HashMap<String, Double> darkPixelhashmap, RavensProblem problem) {
        // go through all the answer figures in 3x3
        if (problem.getProblemType().equals("3x3")) {
            for (int j = 1; j < 9; j++) {
                Double dpAnswer = darkPixelhashmap.get(Integer.toString(j));
                System.out.println("figure: " + j + " gets " + figureScore.ratiocomparetoPoints(dpAnswer, compareRatio) + " points");
                scorer.increaseScore(Integer.toString(j), figureScore.ratiocomparetoPoints(dpAnswer, compareRatio));
            }
        } else if (problem.getProblemType().equals("2x2")) {
            for (int i = 1; i < 7; i++) {
                Double dpAnswer = darkPixelhashmap.get(Integer.toString(i));
                System.out.println("figure: " + i + " gets " + figureScore.ratiocomparetoPoints(dpAnswer, compareRatio) + " points");
                scorer.increaseScore(Integer.toString(i), figureScore.ratiocomparetoPoints(dpAnswer, compareRatio));
            }
        }
    }

    private void similarProcess(String comparefigure, figureScore scorer, RavensProblem problem, HashMap<String, int[][]> imageArrayHashmap) {
        System.out.println("This problem is using the similarity process");
        HashMap<String, Double> similarRatiosmap = new HashMap<>();
        double topSimilar = 0;
        int Answer = -1;
        for (int i = 1; i < 9; i++) {
            double similarRatio = imageDB.imageSimilarity(imageArrayHashmap.get(comparefigure), imageArrayHashmap.get(Integer.toString(i)));
//            System.out.println("Figure: " + i + " Similarity ratio: " + similarRatio);
//            if (similarRatio > topSimilar) {
//                Answer = i;
//                topSimilar = similarRatio;
//            }
            similarRatiosmap.put(Integer.toString(i), similarRatio);
        }
        for (String s : similarRatiosmap.keySet()) {
            if (scorer.scoreBoard.get(s) != 0.0) {
                scorer.increaseScore(s, similarRatiosmap.get(s) * 10);  // had to tweak the number from 100 to 10...
                // similar is impact problem 2 and 3
            }
        }
    }

    private void similarProcesswithimagearray(int[][] comparearray, figureScore scorer, RavensProblem problem, HashMap<String, int[][]> imageArrayHashmap) {
        System.out.println("This problem is using the similarity with array process");
        HashMap<String, Double> similarRatiosmap = new HashMap<>();
        int points_earned = 100;
        double topSimilar = 0;
        int Answer = -1;
        int problemtypecounter;
        if (problem.getProblemType().equals("2x2")) {
            problemtypecounter = 7;
        } else {
            problemtypecounter = 9;
        }
        for (int i = 1; i < problemtypecounter; i++) {
            double similarRatio = imageDB.imageSimilarity(comparearray, imageArrayHashmap.get(Integer.toString(i)));
//            System.out.println("Figure: " + i + " Similarity ratio: " + similarRatio);
//            if (similarRatio > topSimilar) {
//                Answer = i;
//                topSimilar = similarRatio;
//            }
            similarRatiosmap.put(Integer.toString(i), similarRatio);
        }
//        System.out.println("test code");
        for (String s : similarRatiosmap.keySet()) {
            scorer.increaseScore(s, similarRatiosmap.get(s) * points_earned);  // had to tweak the number from 100 to 10...
            // similar is impact problemm 2 and 3
        }
    }

    private boolean isReflection(String fig1, String answerfigure, String horizonorVertical, RavensProblem problem, HashMap<String, int[][]> imageArrayHashmap) {
//        load images
//        System.out.println("test code for reflectino");
        int[][] fig1imageArray = imageArrayHashmap.get(fig1);
        int[][] fig2imageArray = imageArrayHashmap.get(answerfigure);
        int[][] horizontalFlipArray = imageDB.horizontalFlipimage(fig2imageArray);
        int[][] verticalFlipArray = imageDB.verticalFlipimage(fig2imageArray);

        //see if they are the same if same true, else not
//        System.out.println("for comparison between: " + fig1 + " : " + answerfigure + " Similarity Ratio is: " + imageDB.imageSimilarity(fig1imageArray, horizontalFlipArray));
        if (horizonorVertical.equals("Horz")) {
            if (imageDB.imageSimilarity(fig1imageArray, horizontalFlipArray) >= .85) {
                return true;
            }

        } else if (horizonorVertical.equals("Vert")) {
            if (imageDB.imageSimilarity(fig1imageArray, verticalFlipArray) >= .85) {
                return true;
            }
        }
        return false;
    }

    private void reflectionScorer(String testfigure, String horizontalorVertical, RavensProblem problem, figureScore scorer,
                                  HashMap<String, int[][]> imageArrayHashmap) {
        int Answernum = 0;
        if (problem.getProblemType().equals("3x3")) {
            Answernum = 8;
        } else if (problem.getProblemType().equals("2x2")) {
            Answernum = 6;
        }
        for (int i = 1; i < Answernum; i++) {
            if (isReflection(testfigure, Integer.toString(i), horizontalorVertical, problem, imageArrayHashmap)) {
                scorer.increaseScore(Integer.toString(i), 20.0);
            }
            ;
        }
    }

    private void scoringtestcode() {
        figureScore scorer = new figureScore();
        scorer.increaseScore("1", 100.1);
        scorer.increaseScore("1", 100.1);
        scorer.increaseScore("2", 500.1);
        scorer.increaseScore("3", 500.1);
        scorer.increaseScore("4", 301.1);
        System.out.println("the top score is: " + scorer.topScore());
        System.out.println("IS there one unique answer: " + scorer.onetrueKing());
//        System.out.println(scorer.alltopScores());
//        scorer.dropitlikeitsHot();
        System.out.println("all the last ones " + scorer.scoreBoard.keySet());
    }

    private void Testcodeinnerouter(HashMap<String, int[][]> imageArrayHashmap) {
        double test = imageDB.imageSimilarity(
                imageDB.converttoInsideonly(imageArrayHashmap.get("E")),
                imageDB.converttoInsideonly(imageArrayHashmap.get("1")));
        System.out.println("inside image similarity is " + test);
        double test2 = imageDB.imageSimilarity(
                imageDB.converttoOutsideonly(imageArrayHashmap.get("D")),
                imageDB.converttoOutsideonly(imageArrayHashmap.get("1")));
        System.out.println("outside image similarity is " + test2);
    }

}
