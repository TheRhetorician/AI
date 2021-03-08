package com.example.myapplication;

public class MessageFn {
    private boolean image,owned;
    private String textval;

    public MessageFn(String t,boolean o, boolean i)
    {
        owned = o;
        image = i;
        textval = t;
    }
    public String getTextval()
    {
        return textval;
    }
    public void setTextval(String t)
    {
        this.textval = t;
    }
    public boolean getImage()
    {
        return image;
    }
    public void setImage(boolean i)
    {
        this.image = i;
    }
    public boolean getOwned()
    {
        return owned;
    }
    public void setOwned(boolean o)
    {
        this.owned = o;
    }

}
