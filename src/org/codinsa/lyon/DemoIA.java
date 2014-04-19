package org.codinsa.lyon;

import ai.AbstractAI;

/**
 * Created by pvienne on 19/04/14.
 */
public class DemoIA extends AbstractAI
{

    public DemoIA(String ip, int port)
    {
        super(ip,port);
    }

    @Override
    public void think() {

        while (true) {
            game.updateSimFrame();


        }
    }

    public static void main(String[] args)
    {
        if (args.length != 2)
        {
            System.out.println("Usage : java AttackAI ip port");
            System.exit(1);
        }
        String ip = args[0];
        int port = Integer.parseInt(args[1]);

        AbstractAI ai = new DemoIA(ip,port);
        ai.think();
    }
}