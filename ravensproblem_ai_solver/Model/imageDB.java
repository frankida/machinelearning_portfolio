package ravensproject.Model;

import ravensproject.RavensFigure;
import ravensproject.RavensProblem;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.HashMap;

public class imageDB {
    HashMap<String, int[][]> imageArrayHashmap = new HashMap<>();
    HashMap<String, Double> darkPixelhashmap = new HashMap<>();

    public static int[][] getImagearray(String filename) {
        BufferedImage img = null;
        try {
            img = ImageIO.read(new File(filename));
            int[][] imageArray = new int[img.getWidth()][img.getHeight()];
//            double blackPixel = 0;
            //    After loading a visual representation from a file into a BufferedImage, to iterate over all pixels in the image:
            for (int i = 0; i < img.getWidth(); i++) {
                for (int j = 0; j < img.getHeight(); j++) {
                    int thisPixel = img.getRGB(i, j);
                    if (thisPixel == -1) {
                        imageArray[i][j] = 0;
                    } else {
//                        blackPixel++;
                        imageArray[i][j] = 1;
                    }
                }
            }
//            System.out.println(blackPixel);
            return imageArray;
        } catch (Exception ex) {
            return null;
        }
    }

    public static HashMap<String, int[][]> loadImages(RavensProblem problem) {
        HashMap<String, int[][]> imageArrayHashmap = new HashMap<>();
        for (RavensFigure figure : problem.getFigures().values()) {
            imageArrayHashmap.put(figure.getName(), getImagearray(figure.getVisual()));
//                        System.out.println("Similarity code: " + figure.getVisual());
        }
        return imageArrayHashmap;
    }

    public static HashMap<String, int[][]> converttoInside(HashMap<String, int[][]> originalhashmap) {
        HashMap<String, int[][]> convertHP = new HashMap<>();
        for (String s : originalhashmap.keySet()) {
            convertHP.put(s, converttoInsideonly(originalhashmap.get(s)));
        }
        return convertHP;
    }

    public static HashMap<String, int[][]> converttoOutside(HashMap<String, int[][]> originalhashmap) {
        HashMap<String, int[][]> convertHP = new HashMap<>();
        for (String s : originalhashmap.keySet()) {
            convertHP.put(s, converttoOutsideonly(originalhashmap.get(s)));
        }
        return convertHP;
    }

    public static HashMap<String, Double> load_darkpixel_Hashmap(RavensProblem problem) {
        HashMap<String, Double> darkPixelhashmap = new HashMap<>();
//        System.out.println(problem.getName() + " " + problem.getProblemType());
        for (RavensFigure figure : problem.getFigures().values()) {
            darkPixelhashmap.put(figure.getName(), darkpixelimageProcess(figure.getVisual()));
        }
        return darkPixelhashmap;
    }

    private static double darkpixelimageProcess(String filename) {
        BufferedImage img = null;
        try {
            img = ImageIO.read(new File(filename));
            double blackPixel = 0;
            double totalPixel = 0;
            double ratio = 0;
            //    After loading a visual representation from a file into a BufferedImage, to iterate over all pixels in the image:
            for (int i = 0; i < img.getWidth(); i++) {
                for (int j = 0; j < img.getHeight(); j++) {
                    int thisPixel = img.getRGB(i, j);
                    if (thisPixel == -1) {
                        totalPixel++;
                    } else {
                        blackPixel++;
                        totalPixel++;
                    }
                }
            }
//            System.out.println("Black pixels: " + blackPixel);
//            System.out.println("Total pixels: " + totalPixel);
            ratio = blackPixel / totalPixel;
            //important debugging
//            System.out.println("File: " + filename + " Ratio: " + ratio);
            return ratio;
        } catch (Exception ex) {
            return 0;
        }
    }

    public static int[][] converttoInsideonly(int[][] originalarray) {
        int[][] insidearray = new int[originalarray.length][originalarray[0].length];
//        System.out.println("the size of array "+ insidearray.length + " and the other size "+ insidearray[0].length);
//        System.out.println("the 1/4 size of array "+ insidearray.length/4 + " and the other size 1/4 "+ insidearray[0].length*3/4);
        int innerboundary = 60;
        int outerboundary = 120;
        for (int j = 0; j < originalarray[0].length; j++) {
            for (int i = 0; i < originalarray.length; i++) {
                if (i > innerboundary && i < outerboundary &&
                        j > innerboundary && j < outerboundary) {
                    insidearray[i][j] = originalarray[i][j];
                } else {
                    insidearray[i][j] = 0;
                }
            }
        }

        return insidearray;
    }

    public static int[][] converttoOutsideonly(int[][] originalarray) {
        int[][] outsidearray = new int[originalarray.length][originalarray[0].length];
//        System.out.println("the size of array "+ outsidearray.length + " and the other size "+ outsidearray[0].length);
//        System.out.println("the 1/4 size of array "+ outsidearray.length/4 + " and the other size 1/4 "+ outsidearray[0].length*3/4);
        int innerboundary = 60;
        int outerboundary = 120;
        for (int j = 0; j < originalarray[0].length; j++) {
            for (int i = 0; i < originalarray.length; i++) {
                if ((i <= innerboundary || i >= outerboundary) &&
                        (j <= innerboundary || j >= outerboundary)) {
                    outsidearray[i][j] = originalarray[i][j];
                } else {
                    outsidearray[i][j] = 0;
                }
            }
        }

        return outsidearray;
    }

    public static int[][] verticalFlipimage(int[][] fig2imageArray) {
        int[][] fig2flipimageArray = new int[fig2imageArray.length][fig2imageArray[0].length];
        for (int i = 0; i < fig2imageArray.length; i++) {
            for (int j = 0; j < fig2imageArray[0].length; j++) {
                int reverser = fig2imageArray.length - j - 1;
//                System.out.println("normal j: " + j + " reverser " + reverser);
//  System.out.println(fig2imageArray[0].length);
                fig2flipimageArray[i][reverser] = fig2imageArray[i][j];
//                System.out.println("First Array: "+ i + " " + j);

            }
        }
        return fig2flipimageArray;
    }

    public static int[][] horizontalFlipimage(int[][] fig2imageArray) {
        int[][] fig2flipimageArray = new int[fig2imageArray.length][fig2imageArray[0].length];
        for (int j = 0; j < fig2imageArray[0].length; j++) {
            for (int i = 0; i < fig2imageArray.length; i++) {
                int reverser = fig2imageArray.length - i - 1;
//                System.out.println("normal j: " + j + " reverser " + reverser);
//  System.out.println(fig2imageArray[0].length);
                fig2flipimageArray[reverser][j] = fig2imageArray[i][j];
//                System.out.println("First Array: "+ i + " " + j);
            }
        }
        return fig2flipimageArray;
    }

    public static int[][] xortwoimageArray(int[][] fig1imageArray, int[][] fig2imageArray) {
        int[][] xorimagearray = new int[fig2imageArray.length][fig2imageArray[0].length];
        for (int j = 0; j < fig2imageArray[0].length; j++) {
            for (int i = 0; i < fig2imageArray.length; i++) {
                xorimagearray[i][j] = fig1imageArray[i][j] ^ fig2imageArray[i][j];
            }
        }
        return xorimagearray;
    }

    public static int[][] andtwoimageArray(int[][] fig1imageArray, int[][] fig2imageArray) {
        int[][] andimagearray = new int[fig2imageArray.length][fig2imageArray[0].length];
        for (int j = 0; j < fig2imageArray[0].length; j++) {
            for (int i = 0; i < fig2imageArray.length; i++) {
                andimagearray[i][j] = fig1imageArray[i][j] & fig2imageArray[i][j];
            }
        }
        return andimagearray;
    }

    public static double imageSimilarity(int[][] imagearray1, int[][] imagearray2) {
//        Critical code to calculate the similarity between images
        double samecounter = 0;
        double total = 0;
        for (int i = 0; i < imagearray1.length; i++) {
            for (int j = 0; j < imagearray1[i].length; j++) {
                if (imagearray1[i][j] == 1 && imagearray2[i][j] == 1) {
                    samecounter += 2;
                    total += 2;
                } else if (imagearray1[i][j] == 1 ^ imagearray2[i][j] == 1) {
                    total++;
                } else {
                }
            }
        }
        if (total == 0) {
            return 0.0;  //avoid NaN - something divided by 0

        }
//        System.out.println("Same pixels: " +samecounter + " Total " +total);
        return samecounter / total;
    }
}
