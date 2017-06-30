package ravensproject.Model;

import ravensproject.figureScore;

import java.util.HashMap;

public class problemtypes {

    public static boolean isBigger(HashMap<String, Double> darkPixelhashmap) {
        return (darkPixelhashmap.get("A") < darkPixelhashmap.get("B")) &&
                (darkPixelhashmap.get("B") < darkPixelhashmap.get("C")) &&
                (darkPixelhashmap.get("D") < darkPixelhashmap.get("E")) &&
                (darkPixelhashmap.get("E") < darkPixelhashmap.get("F"));
    }

    public static boolean isSmaller(HashMap<String, Double> darkPixelhashmap) {  //this one isn't used
        return (darkPixelhashmap.get("A") > darkPixelhashmap.get("B")) &&
                (darkPixelhashmap.get("B") > darkPixelhashmap.get("C") &&
                        (darkPixelhashmap.get("D") > darkPixelhashmap.get("E")) &&
                        (darkPixelhashmap.get("E") > darkPixelhashmap.get("F")));
    }

    public static boolean isSame(HashMap<String, Double> darkPixelhashmap) {
        return (figureScore.isSame(darkPixelhashmap.get("A"), darkPixelhashmap.get("B"), .05) &&
                figureScore.isSame(darkPixelhashmap.get("B"), darkPixelhashmap.get("C"), .05));
    }

    public static boolean isAddition(HashMap<String, Double> darkPixelhashmap) {
        return figureScore.isSame(darkPixelhashmap.get("A") + darkPixelhashmap.get("B"), darkPixelhashmap.get("C"), .05);
    }

    public static boolean isSubtraction(HashMap<String, Double> darkPixelhashmap) {
        return figureScore.isSame(darkPixelhashmap.get("A") - darkPixelhashmap.get("B"), darkPixelhashmap.get("C"), .05);
    }

    public static boolean isXOR(HashMap<String, int[][]> imageArrayHashmap) {
        if (imageDB.imageSimilarity(imageDB.xortwoimageArray(imageArrayHashmap.get("A"), imageArrayHashmap.get("B")),
                imageArrayHashmap.get("C")) > .85) {
            return true;
        }
        return false;
    }

    public static boolean isAND(HashMap<String, int[][]> imageArrayHashmap) {
        if ((imageDB.imageSimilarity(imageDB.andtwoimageArray(imageArrayHashmap.get("A"), imageArrayHashmap.get("B")),
                imageArrayHashmap.get("C")) > .95) && (imageDB.imageSimilarity(imageDB.andtwoimageArray(imageArrayHashmap.get("D"), imageArrayHashmap.get("E")),
                imageArrayHashmap.get("F")) > .95)) {
            return true;
        }
        return false;
    }

    public static boolean isSameDiagonal(HashMap<String, int[][]> imageArrayHashmap, HashMap<String, Double> darkPixelhashmap) {
        return /**figureScore.isSame(darkPixelhashmap.get("A"), darkPixelhashmap.get("E"), .05) &&**/
                (imageDB.imageSimilarity(imageArrayHashmap.get("A"), imageArrayHashmap.get("E"))) >= .90; // changed from .85
    }
}
