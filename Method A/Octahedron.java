import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Octahedron {
    public static final int EDGES = 12;
    public static final int HALF_EDGES = EDGES * 2;
    private static final int SYMMETRIES[][] = new int[][] {
        { 2, 3, 4, 5, 6, 7, 0, 1, 10, 11, 12, 13, 14, 15, 8, 9, 18, 19, 20, 21, 22, 23, 16, 17 },
        { 14, 15, 7, 6, 13, 12, 23, 22, 1, 0, 4, 5, 21, 20, 16, 17, 9, 8, 3, 2, 10, 11, 19, 18 },
        { 5, 4, 11, 10, 21, 20, 12, 13, 2, 3, 19, 18, 22, 23, 7, 6, 1, 0, 8, 9, 17, 16, 15, 14 },
    };
    private static final List<int[]> ORIENTATIONS = new ArrayList<>(HALF_EDGES);
    static {
        int id[] = new int[HALF_EDGES];
        for (int i = 0; i < HALF_EDGES; i++) id[i] = i;
        Set<String> oris = new HashSet<>();
            for (int x = 0; x < 4; x++) {
                for (int y = 0; y < 4; y++) {
                    for (int z = 0; z < 4; z++) {
                        int ori[] = id.clone();
                        String str = Arrays.toString(ori);
                        if (!oris.contains(str)) { 
                            ORIENTATIONS.add(ori);
                            oris.add(str);
                        }
                        for (int j = 0; j < HALF_EDGES; j++) id[j] = ori[SYMMETRIES[0][j]];
                    }
                    int ori[] = id.clone();
                    for (int j = 0; j < HALF_EDGES; j++) id[j] = ori[SYMMETRIES[1][j]];
                }
                int ori[] = id.clone();
                for (int j = 0; j < HALF_EDGES; j++) id[j] = ori[SYMMETRIES[2][j]];
            }
    }

    private int labelling = 0;
    public Octahedron() { }
    public Octahedron(Octahedron o) { labelling = o.labelling; }
    public Octahedron(int o) { labelling = o; }
    public boolean labelled(int halfEdge) {

        return ((labelling >> halfEdge) & 1) == 1;

    }

    public boolean canLabel(int halfEdge) {
        return !(labelled(halfEdge) || labelled(halfEdge ^ 1));
    }

    public void label(int halfEdge) {
        labelling |= 1 << halfEdge;
    }
    private int orientate(int index) {

        int result = 0;
        int[] ori = ORIENTATIONS.get(index);
        for (int i = 0; i < HALF_EDGES; i++) {
            result |= ((labelling >> i) & 1) << ori[i];
        }
        return result;
    }
    private static void printResult(int labels, int results) {
        System.out.println(String.format("%6d:   %d", labels, results));
    }

    public static void main(String[] args) {
        System.out.println("Labels:   Results");
        Set<Integer> octs = new HashSet<>();
        octs.add(new Octahedron().labelling);
        printResult(0, 1);
        for (int labels = 1; labels <= 13; labels++) {
            Set<Integer> newOcts = new HashSet<>();
            for (int oct : octs) {
                for (int halfEdge = 0; halfEdge < HALF_EDGES; halfEdge++) {
                    Octahedron newOct = new Octahedron(oct);
                    if (newOct.canLabel(halfEdge)) {
                        newOct.label(halfEdge);                    
                        boolean add = !newOcts.contains(newOct.labelling);
                        for (int index = 1; add && index < ORIENTATIONS.size(); index++) {
                            int oLabel = newOct.orientate(index);
                            add = !newOcts.contains(oLabel);
                        }
                        if (add) newOcts.add(newOct.labelling);
                    } else {
                        halfEdge++;
                    }
                }
            }
            octs = newOcts;
            printResult(labels, octs.size());
        }
    }
}

