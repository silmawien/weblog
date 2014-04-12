package com.example.customlayout;

import java.util.Arrays;
import java.util.Iterator;
import java.util.NoSuchElementException;

import android.content.Context;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;

/**
 * A simple list item view.
 */
public class ListItemLayout extends ViewGroup {

    public ListItemLayout(Context context) {
        this(context, null);
    }

    public ListItemLayout(Context context, AttributeSet attrs) {
        super(context, attrs);
    }
    
    /**
     * Called when children's XML is parsed.
     */
    @Override
    public MarginLayoutParams generateLayoutParams(AttributeSet attrs) {
        return new MarginLayoutParams(getContext(), attrs);
    }

    /**
     * Oops, someone called addView() but forgot to specify layout params.
     */
    @Override
    protected MarginLayoutParams generateDefaultLayoutParams() {
        return new MarginLayoutParams(MarginLayoutParams.WRAP_CONTENT, MarginLayoutParams.WRAP_CONTENT);
    }

    /**
     * These two methods are used to convert layout params of an incorrect type.
     */
    protected boolean checkLayoutParams(ViewGroup.LayoutParams p) {
        return p instanceof MarginLayoutParams;
    }

    @Override
    protected MarginLayoutParams generateLayoutParams(ViewGroup.LayoutParams p) {
        return new MarginLayoutParams(p);
    }

    private View imageView() {
        // convention, use first child as the image
        return getChildAt(0);
    }
    
    private Iterable<View> textViews = new Iterable<View> () {
        // the remaining views are assumed to be text lines 
        @Override
        public Iterator<View> iterator() {
            return new Iterator<View>() {
                private int current = 1;
                
                @Override
                public boolean hasNext() {
                    return current < getChildCount();
                }

                @Override
                public View next() {
                    if (current >= getChildCount())
                        throw new NoSuchElementException();
                    return getChildAt(current++);
                }
                
                @Override
                public void remove() {
                    throw new UnsupportedOperationException();
                }
            };
        }
    };
    
    private int widthWithMargins(View child) {
        MarginLayoutParams lp = (MarginLayoutParams)child.getLayoutParams();
        return child.getMeasuredWidth() + lp.leftMargin + lp.rightMargin;
    }

    private int heightWithMargins(View child) {
        MarginLayoutParams lp = (MarginLayoutParams)child.getLayoutParams();
        return child.getMeasuredHeight() + lp.topMargin + lp.bottomMargin;
    }

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        int widthUsed = 0;
        int heightUsed = 0;

        View image = imageView();
        // Image goes to the left: measure and reserve horizontal space for it
        if (image.getVisibility() != View.GONE) {
            measureChildWithMargins(image, widthMeasureSpec, widthUsed,
                    heightMeasureSpec, heightUsed);
            widthUsed += widthWithMargins(image);
        }
        
        // Use remaining space to stack the two text views vertically.
        int textWidth = 0;
        for (View child : textViews) {
            if (child.getVisibility() != View.GONE) { 
                measureChildWithMargins(child, widthMeasureSpec, widthUsed,
                        heightMeasureSpec, heightUsed);
                heightUsed += heightWithMargins(child);
                textWidth = Math.max(textWidth, widthWithMargins(child));
            }
        }
        widthUsed += textWidth;
        
        // handle the case where the image is taller than the texts combined
        if (image.getVisibility() != View.GONE) {
            heightUsed = Math.max(heightWithMargins(image), heightUsed);
        }
             
        widthUsed += getPaddingLeft() + getPaddingRight();
        heightUsed += getPaddingTop() + getPaddingBottom();
        
        setMeasuredDimension(
                resolveSize(widthUsed, widthMeasureSpec),
                resolveSize(heightUsed, heightMeasureSpec));
    }
    
    @Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
        int x = getPaddingLeft();
        int y = getPaddingTop();
        
        int innerHeight = getHeight() - getPaddingTop() - getPaddingBottom();

        // center image vertically
        View image = imageView();
        if (image.getVisibility() != View.GONE) {
            int dy = Math.max(0, (innerHeight - heightWithMargins(image)) / 2);
            placeChild(image, x, y + dy);
        
            x += widthWithMargins(image);
        }

        // center texts as a group
        int textHeight = 0;
        for (View child : textViews) {
            if (child.getVisibility() != View.GONE) {
                textHeight += heightWithMargins(child);
            }
        }
        
        y += Math.max(0, (innerHeight - textHeight) / 2);
        
        for (View child : textViews) {
            if (child.getVisibility() != View.GONE) {
                placeChild(child, x, y);
                y += heightWithMargins(child);
            }
        }
    }

    private void placeChild(View child, int left, int top) {
        MarginLayoutParams lp = (MarginLayoutParams)child.getLayoutParams();
        child.layout(
                left + lp.leftMargin,
                top + lp.topMargin,
                left + lp.leftMargin + child.getMeasuredWidth(),
                top + lp.topMargin + child.getMeasuredHeight());
    }
}
