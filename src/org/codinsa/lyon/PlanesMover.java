package org.codinsa.lyon;

import model.Plane;

/**
 * Created by troll on 4/19/14.
 */
public class PlanesMover {
    private static PlanesMover instance;

    public static PlanesMover getInstance() {
        if (instance == null) {
            instance = new PlanesMover();
        }
        return instance;
    }

    public void move(Plane plane, Point p) {

    }
}
