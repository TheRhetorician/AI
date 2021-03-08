package com.example.myapplication;

import java.util.List;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import android.widget.Toast;

public class MessageAdapt extends ArrayAdapter<MessageFn> {
    private static final int MY_MESSAGE = 0, OTHER_MESSAGE = 1, MY_IMAGE = 2, OTHER_IMAGE = 3;
    public MessageAdapt(Context context, List<MessageFn> data) {
        super(context, R.layout.sender_msg, data);
    }
    @Override
    public int getViewTypeCount() {
        // my message, other message, my image, other image
        return 4;
    }
    @Override
    public int getItemViewType(int position) {
        MessageFn item = getItem(position);
        if (item.getOwned() && !item.getImage()) return MY_MESSAGE;
        else if (!item.getOwned() && !item.getImage()) return OTHER_MESSAGE;
        else if (item.getOwned() && item.getImage()) return MY_IMAGE;
        else return OTHER_IMAGE;
    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        int viewType = getItemViewType(position);
        if (viewType == MY_MESSAGE) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.sender_msg, parent, false);
            TextView textView = convertView.findViewById(R.id.text);
            textView.setText(getItem(position).getTextval());
        } else if (viewType == OTHER_MESSAGE) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.bot_msg, parent, false);
            TextView textView = convertView.findViewById(R.id.text);
            textView.setText(getItem(position).getTextval());
        } else if (viewType == MY_IMAGE) {
            //convertView = LayoutInflater.from(getContext()).inflate(R.layout.item_mine_image, parent, false);
        } else {
            // convertView = LayoutInflater.from(getContext()).inflate(R.layout.item_other_image, parent, false);
        }
        convertView.findViewById(R.id.chatMessageView).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getContext(), "onClick", Toast.LENGTH_LONG).show();
            }
        });
        return convertView;
    }
}
