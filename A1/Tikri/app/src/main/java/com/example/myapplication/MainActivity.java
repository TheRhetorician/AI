package com.example.myapplication;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;

public class MainActivity extends AppCompatActivity {


    private ListView mListView;
    private FloatingActionButton mButtonSend;
    private EditText mEditTextMessage;
    private ImageView mImageView;
    private MessageAdapt mAdapter;
    boolean firstmsg = true;
    boolean chalo = false;
    String userid = "test";
    private static final int REQUEST_LOGIN = 0;
    public MainActivity()
    {
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        int num = 0;
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Intent intent = new Intent(this, LoginActivity.class);
        //startActivity(intent);
        startActivityForResult(intent, REQUEST_LOGIN);

    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_LOGIN) {
            if (resultCode == RESULT_OK) {

                // TODO: Implement successful signup logic here
                // By default we just finish the Activity and log them in automatically
                int num = 0;
                SharedPreferences saved_values = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
                userid = saved_values.getString("userid", "XXX");
                System.out.println(userid+" "+num);
                num++;
                mListView = (ListView) findViewById(R.id.listView);
                mButtonSend = (FloatingActionButton) findViewById(R.id.btn_send);
                mEditTextMessage = (EditText) findViewById(R.id.et_message);
                mImageView = (ImageView) findViewById(R.id.iv_image);
                mAdapter = new MessageAdapt(this, new ArrayList<MessageFn>());
                mListView.setAdapter(mAdapter);
                String URL = "http://10.0.2.2:8000/users/" + userid+"/details";
                final String[] nm = new String[1];
                final String[] us = new String[1];
                final String[] pass = new String[1];
                final String[] EMC = new String[1];
                final String[] pata = new String[1];
                RequestQueue requestQueue = Volley.newRequestQueue(this);
                JsonArrayRequest objectRequest = new JsonArrayRequest(
                        Request.Method.GET,
                        URL,
                        null,
                        new Response.Listener<JSONArray>() {
                            @RequiresApi(api = Build.VERSION_CODES.O)
                            @Override
                            public void onResponse(JSONArray response) {
                                System.out.println("Response received");
                                Log.e("rest Response",response.toString());
                                try {
                                    //SONArray Products = ItemDetail.getJSONObject(0).getJSONArray("Products");
                                    us[0] = response.getJSONObject(0).get("userid").toString();
                                    pass[0] = response.getJSONObject(0).get("password").toString();
                                    nm[0] = response.getJSONObject(0).get("name").toString();
                                    pata[0] = response.getJSONObject(0).get("address").toString();
                                    EMC[0] = response.getJSONObject(0).get("contact").toString();
                                    //sendMessage("Userid is "+us[0],userid);
                                    //sendMessage("Password is "+pass[0],userid);
                                    //sendMessage("Name is "+nm[0],userid);
                                    //sendMessage("Address is "+pata[0],userid);
                                    //sendMessage("Emergency Contact is "+EMC[0],userid);


                                    //displayPastMessages(response,mAdapter);
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                            }
                        },
                        new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                System.out.println("error");
                                Log.e("resttt",error.toString());
                            }
                        }
                );
                requestQueue.add(objectRequest);

                //POSTMAN_LEARN
                String URLp = "http://10.0.2.2:8000/learn";
                HashMap<String, String> params = new HashMap<String, String>();
                params.put("userid",userid);
                JsonObjectRequest objRequest = new JsonObjectRequest(URLp, new JSONObject(params),
                        new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject response) {
                                try {
                                    System.out.println(response.get("done"));
                                    VolleyLog.v("Response to post query:%n %s", response.toString(4));
                                    Log.e("rest Response",response.toString());
                                    //parsedata(response);

                                } catch (JSONException e) {
                                    Log.e("resttt",e.toString());
                                    e.printStackTrace();
                                }

                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        VolleyLog.e("Error: ", error.getMessage());
                    }
                });

                requestQueue.add(objRequest);
                System.out.println("LEARN HOGAYA POSTMAN KO");

                String toDisplay = "Hello "+userid + " I am fetching your messages.Let me use my speed booster for a busy person like you!";
                MessageFn displayGetMsg = new MessageFn(toDisplay, false, false);
                mAdapter.add(displayGetMsg);
                getMessages(mAdapter,userid);
                firstmsg = false;

                mEditTextMessage.setText("");
                mListView.setSelection(mAdapter.getCount() - 1);
//code for sending the message
                mButtonSend.setOnClickListener(new View.OnClickListener() {
                    @RequiresApi(api = Build.VERSION_CODES.O)
                    @Override
                    public void onClick(View v) {
                        String msg = mEditTextMessage.getText().toString();


                        if(msg.indexOf("Where do I live")>=0  || msg.indexOf("What's my address")>=0){
                            sendMessage(msg,userid);
                            mEditTextMessage.setText("");
                            mListView.setSelection(mAdapter.getCount() - 1);
                            Uri mapUri = Uri.parse("geo:0,0?q=" + Uri.encode(pata[0]));
                            Intent mapIntent = new Intent(Intent.ACTION_VIEW, mapUri);
                            mapIntent.setPackage("com.google.android.apps.maps");
                            startActivity(mapIntent);
                            //userid = msg;

                            //MessageFn userMsg = new MessageFn(userid, true, false);
                            //mAdapter.add(userMsg);



                        }
                        else if(msg.indexOf("Show me a video")>=0){
                            sendMessage(msg,userid);
                            mEditTextMessage.setText("");
                            mListView.setSelection(mAdapter.getCount() - 1);
                            String video_id = "SQ-SK_-LVRA";
                            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("vnd.youtube://" + video_id));
                            startActivity(intent);
                        }
                        else if(msg.indexOf("contact")>=0) {
                            sendMessage(msg,userid);
                            mEditTextMessage.setText("");
                            mListView.setSelection(mAdapter.getCount() - 1);
                            Intent intent = new Intent(Intent.ACTION_DIAL);
                            intent.setData(Uri.parse("tel: "+EMC[0]));
                            startActivity(intent);
                        }
                        else{
                            sendMessage(msg,userid);
                            mEditTextMessage.setText("");
                            mListView.setSelection(mAdapter.getCount() - 1);
                        }
                    }
                });
            }
        }
    }
    public void getMessages(final MessageAdapt mAdapter,String userid){
        System.out.println("AAYA");
        String URL = "http://10.0.2.2:8000/users/" + userid;
        JsonArrayRequest objectRequest = new JsonArrayRequest(
                Request.Method.GET,
                URL,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        System.out.println("Response received");
                        Log.e("rest Response",response.toString());
                        try {
                            displayPastMessages(response,mAdapter);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        System.out.println("error");
                        Log.e("resttt",error.toString());
                    }
                }
        );
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(objectRequest);
    }
    private void displayPastMessages(JSONArray response,MessageAdapt mAdapter) throws JSONException {
        if(response.length() == 0){
            MessageFn newUserMessage = new MessageFn("Looks like you are a new user!Welcome "+userid,false,false);
            mAdapter.add(newUserMessage);
            return;
        }

        for (int i = 0 ;i < response.length();i++){
            JSONObject tmp = (JSONObject) response.get(i);
            System.out.println(tmp.get("response"));
            MessageFn chatQuery = new MessageFn((String) tmp.get("query"), true, false);
            mAdapter.add(chatQuery);
            MessageFn chatResponse = new MessageFn((String) tmp.get("response"), false, false);
            mAdapter.add(chatResponse);
        }
        MessageFn chatQuery = new MessageFn("It was wonderful chatting with you last time.\n\nI hope we have a better conversation today!", false, false);
        mAdapter.add(chatQuery);

    }
    @RequiresApi(api = Build.VERSION_CODES.O)
    private void sendMessage(String message, String userid) {
        MessageFn chatMessage = new MessageFn(message, true, false);
        mAdapter.add(chatMessage);
        //respond message
        RequestQueue requestQueue = Volley.newRequestQueue(this);

        String URL = "http://10.0.2.2:8000/users/" + userid + "/query";
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        LocalDateTime now = LocalDateTime.now();
        System.out.println(dtf.format(now));
        HashMap<String, String> params = new HashMap<String, String>();
        params.put("query", message);
        params.put("userid",userid);
        params.put("time",dtf.format(now));
        JsonObjectRequest objectRequest = new JsonObjectRequest(URL, new JSONObject(params),
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            VolleyLog.v("Response to post query:%n %s", response.toString(4));
                            Log.e("rest Response",response.toString());
//                            System.out.println(response.get("response"));
                            parsedata(response);

                        } catch (JSONException e) {
                            Log.e("resttt",e.toString());
                            e.printStackTrace();
                        }

                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                VolleyLog.e("Error: ", error.getMessage());
            }
        });

        requestQueue.add(objectRequest);

    }
    public void parsedata(JSONObject response) throws JSONException {
        String botResponse = (String) response.get("response");
//        System.out.println("Testing post request response" + botResponse);
        mimicOtherMessage(botResponse);
    }

    private void mimicOtherMessage(String message) {
        MessageFn chatMessage = new MessageFn(message, false, false);
        mAdapter.add(chatMessage);
    }

    private void sendMessage() {
        MessageFn chatMessage = new MessageFn(null, true, true);
        mAdapter.add(chatMessage);

        mimicOtherMessage();
    }

    private void mimicOtherMessage() {
        MessageFn chatMessage = new MessageFn(null, false, true);
        mAdapter.add(chatMessage);
    }
}